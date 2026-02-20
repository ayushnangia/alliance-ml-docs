#!/usr/bin/env python3
"""
Scrape the Alliance Canada technical documentation wiki into Markdown files.

Usage:
    source .venv/bin/activate
    python scrape_wiki.py --all              # scrape ALL English wiki pages
    python scrape_wiki.py --depth 3          # crawl from Technical_documentation
    python scrape_wiki.py --all --delay 0.2  # faster (be polite though)
"""

import argparse
import json
import re
import time
import urllib.parse
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BASE_URL = "https://docs.alliancecan.ca"
API_URL = f"{BASE_URL}/mediawiki/api.php"
START_PAGE = "Technical_documentation"
OUTPUT_DIR = Path("docs")

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "AllianceCanWikiScraper/1.0 (educational)"})

# French-only page prefixes/patterns to skip
FRENCH_SKIP = re.compile(
    r"^(Utiliser |Configurer |Installer |Connexion |Conseils |"
    r"Créer |Démarrer |Dépannage |Gestion |Guide |Migration |"
    r"Mise à jour |Politique |Premiers |Renouvellement |"
    r"Rôles |Sécurité |Serveurs |Stockage |"
    r"Systèmes |Transfert |Tutoriel )",
    re.IGNORECASE,
)

# Category keywords for the structured index
CATEGORIES = {
    "Clusters & Systems": [
        "Fir", "Nibi", "Narval", "Rorqual", "Trillium", "Killarney", "TamIA",
        "Vulcan", "Béluga", "Beluga", "Cedar", "Graham", "Niagara", "Arbutus",
        "Mist", "Siku", "Helios", "National systems", "Infrastructure renewal",
        "System status", "HPC4Health",
    ],
    "Getting Started & Accounts": [
        "Getting started", "Apply for", "CCDB", "Account", "Multifactor",
        "SSH", "PuTTY", "MobaXTerm", "Linux introduction", "What is a scheduler",
    ],
    "Storage & Data Management": [
        "Storage", "Transferring", "Scratch", "Globus", "Nextcloud", "nearline",
        "Lustre", "Archiving", "Diskusage", "Sharing data", "Project layout",
        "SLURM_TMPDIR", "node-local", "migration", "Filesystem", "object storage",
        "CephFS", "Dar", "tar", "backup", "Quota",
    ],
    "Job Scheduling (Slurm)": [
        "Running jobs", "Job array", "Job scheduling", "Monitoring jobs",
        "GLOST", "GNU Parallel", "META-Farm", "META:", "scheduler", "Slurm",
        "Advanced MPI", "Managing Slurm", "GPUs with Slurm", "Allocations",
    ],
    "Software & Modules": [
        "Available software", "modules", "Standard software", "CVMFS",
        "Installing software", "EasyBuild", "Conda", "Apptainer",
    ],
    "Programming & Development": [
        "Programming guide", "Python", "R", "Julia", "Java", "Perl", "C++",
        "C", "Fortran", "Chapel", "Rust", "Make", "CMake", "Autotools",
        "Build tools", "Git", "Version control", "MPI", "OpenMP", "Pthreads",
        "CUDA", "OpenACC", "BLAS", "Debugging", "profiling", "GDB", "Valgrind",
    ],
    "AI & Machine Learning": [
        "AI and Machine Learning", "PyTorch", "TensorFlow", "Keras", "XGBoost",
        "SpaCy", "Weights", "wandb", "Comet", "Large Scale Machine",
        "Machine Learning", "Huggingface", "Deepspeed", "VLLM", "LLM",
        "MLflow", "Optuna", "RAPIDS", "Ray", "Tensorboard", "AlphaFold",
        "Dask", "Faiss",
    ],
    "Cloud Computing": [
        "Cloud", "VM", "OpenStack", "Terraform", "vGPU", "ipv6",
        "web server", "data server", "object storage", "Working with volumes",
        "Virtual machine", "Automating VM", "Backing up", "security responsibility",
    ],
    "Scientific Software": [
        "GROMACS", "NAMD", "LAMMPS", "AMBER", "OpenMM", "VASP", "Gaussian",
        "ORCA", "Quantum ESPRESSO", "CP2K", "ABINIT", "ADF", "AMS", "CPMD",
        "Dalton", "GAMESS", "GPAW", "MRCC", "OpenMolcas", "DL POLY",
        "Abaqus", "Ansys", "OpenFOAM", "WRF", "StarCCM", "COMSOL",
        "LS-DYNA", "Delft3D", "MATLAB", "Symbolic algebra",
    ],
    "Bioinformatics": [
        "Bioinformatics", "BLAST", "FastTree", "GBrowse", "Samtools", "GATK",
        "FreeSurfer", "Cellranger", "BUSCO", "Galaxy", "QIIME", "SAIGE",
        "MrBayes", "Parabricks", "MetaPhlAn", "AlphaFold", "MAFFT",
    ],
    "Visualization": [
        "Visualization", "ParaView", "VTK", "VisIt", "VMD", "Yt", "VNC",
        "GUI Desktop", "Open OnDemand",
    ],
    "Jupyter & Notebooks": [
        "Jupyter", "JupyterHub", "JupyterLab", "JupyterNotebook",
    ],
    "Quantum Computing": [
        "quantique", "Quantum", "MonarQ", "PennyLane", "Snowflurry", "Qiskit",
    ],
    "Security & Networking": [
        "SSH", "Securing", "Cybersecurity", "tunnelling", "host keys",
        "Automation in the context",
    ],
}


# ---------------------------------------------------------------------------
# Custom Markdown converter
# ---------------------------------------------------------------------------
class WikiConverter(MarkdownConverter):
    def convert_a(self, el, text, parent_tags):
        href = el.get("href", "")
        if not href or not text.strip():
            return text
        if href.startswith("/wiki/") or href.startswith("/mediawiki/index.php"):
            page = href.split("/wiki/")[-1] if "/wiki/" in href else ""
            if page:
                page = urllib.parse.unquote(page)
                page_base = page.split("#")[0]
                anchor = "#" + page.split("#")[1] if "#" in page else ""
                slug = slugify(page_base)
                return f"[{text.strip()}]({slug}.md{anchor})"
            return text
        if href.startswith(("http://", "https://", "ftp://")):
            return f"[{text.strip()}]({href})"
        return text

    def convert_pre(self, el, text, parent_tags):
        lang = ""
        code_el = el.find("code")
        if code_el and code_el.get("class"):
            for cls in code_el["class"]:
                if cls.startswith("language-"):
                    lang = cls.replace("language-", "")
                    break
        content = el.get_text()
        return f"\n```{lang}\n{content}\n```\n"

    def convert_table(self, el, text, parent_tags):
        rows = el.find_all("tr")
        if not rows:
            return text
        md_rows = []
        for i, row in enumerate(rows):
            cells = row.find_all(["th", "td"])
            cell_texts = []
            for c in cells:
                cell_text = c.get_text(separator=" ", strip=True)
                cell_text = re.sub(r"\n+", " ", cell_text)
                cell_texts.append(cell_text)
            md_rows.append("| " + " | ".join(cell_texts) + " |")
            if i == 0:
                md_rows.append("| " + " | ".join(["---"] * len(cell_texts)) + " |")
        return "\n" + "\n".join(md_rows) + "\n\n"


def html_to_md(html: str) -> str:
    return WikiConverter(
        heading_style="atx",
        bullets="-",
        strong_em_symbol="*",
        strip=["script", "style"],
    ).convert(html)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def slugify(page_title: str) -> str:
    s = page_title.replace("/en", "").replace("/", "_")
    s = urllib.parse.unquote(s)
    s = re.sub(r"[^\w\s\-]", "", s)
    s = re.sub(r"[\s]+", "_", s.strip())
    return s


def is_french_page(title: str) -> bool:
    if title.endswith("/fr"):
        return True
    if FRENCH_SKIP.match(title):
        return True
    # Heuristic: titles with accented chars that don't have /en suffix
    # and aren't cluster names
    french_chars = set("àâéèêëïîôùûüÿçœæ")
    has_french = any(c in french_chars for c in title.lower())
    if has_french and not title.endswith("/en") and title not in ("Béluga", "Béluga/en"):
        return True
    return False


def fetch_all_pages() -> list[str]:
    """Get ALL page titles from the wiki using allpages API."""
    all_titles = []
    params = {
        "action": "query",
        "list": "allpages",
        "aplimit": "500",
        "apnamespace": "0",
        "format": "json",
    }
    while True:
        r = SESSION.get(API_URL, params=params, timeout=30)
        data = r.json()
        pages = data.get("query", {}).get("allpages", [])
        all_titles.extend(p["title"] for p in pages)
        cont = data.get("continue")
        if cont:
            params["apcontinue"] = cont["apcontinue"]
        else:
            break
    return all_titles


def fetch_page_html(title: str) -> dict | None:
    params = {
        "action": "parse",
        "page": title,
        "format": "json",
        "prop": "text|links|categories|displaytitle",
        "disabletoc": "false",
    }
    try:
        r = SESSION.get(API_URL, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            return None
        return data["parse"]
    except Exception as e:
        print(f"  [ERROR] Failed to fetch '{title}': {e}")
        return None


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for sel in [".mw-editsection", "#mw-content-text .mw-jump-link",
                ".navbox", ".metadata", ".catlinks", ".mw-indicators",
                "#toc", ".toc"]:
        for el in soup.select(sel):
            el.decompose()
    for p in soup.find_all("p"):
        if not p.get_text(strip=True):
            p.decompose()
    return str(soup)


def save_page(title: str, parse_data: dict, output_dir: Path):
    display_title = parse_data.get("displaytitle", title)
    raw_html = parse_data.get("text", {}).get("*", "")
    if not raw_html:
        return None

    cleaned = clean_html(raw_html)
    md = html_to_md(cleaned)
    md = re.sub(r"\n{4,}", "\n\n\n", md)

    if not md.lstrip().startswith("# "):
        clean_title = BeautifulSoup(display_title, "html.parser").get_text()
        md = f"# {clean_title}\n\n{md}"

    slug = slugify(title)
    filepath = output_dir / f"{slug}.md"
    filepath.write_text(md, encoding="utf-8")
    return filepath


# ---------------------------------------------------------------------------
# Categorized index builder
# ---------------------------------------------------------------------------
def categorize_page(title: str) -> str:
    """Return the best-matching category for a page title."""
    title_lower = title.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw.lower() in title_lower:
                return cat
    return "Other"


def build_categorized_index(saved_files: list[tuple[str, Path]]):
    """Build INDEX.md organized by category."""
    # Group by category
    categorized: dict[str, list[tuple[str, str]]] = {}
    for title, fpath in saved_files:
        cat = categorize_page(title)
        categorized.setdefault(cat, []).append((title, fpath.name))

    lines = [
        "# Alliance Canada Technical Documentation",
        "",
        f"**{len(saved_files)} pages** scraped from [docs.alliancecan.ca]"
        f"(https://docs.alliancecan.ca/wiki/Technical_documentation)",
        "",
        "---",
        "",
    ]

    # TOC
    lines.append("## Table of Contents\n")
    cat_order = list(CATEGORIES.keys()) + ["Other"]
    for cat in cat_order:
        if cat in categorized:
            anchor = cat.lower().replace(" ", "-").replace("&", "").replace("(", "").replace(")", "")
            anchor = re.sub(r"-+", "-", anchor).strip("-")
            lines.append(f"- [{cat}](#{anchor}) ({len(categorized[cat])} pages)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Each category
    for cat in cat_order:
        if cat not in categorized:
            continue
        lines.append(f"## {cat}\n")
        for title, fname in sorted(categorized[cat], key=lambda x: x[0].lower()):
            lines.append(f"- [{title}]({fname})")
        lines.append("")

    index_path = OUTPUT_DIR / "INDEX.md"
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  -> Categorized index: {index_path}")


# ---------------------------------------------------------------------------
# Scrape modes
# ---------------------------------------------------------------------------
def scrape_all(delay: float):
    """Scrape every English page from the wiki."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Fetching complete page list from wiki API...")
    all_titles = fetch_all_pages()
    print(f"Found {len(all_titles)} total pages in wiki.\n")

    # Filter to English-only
    en_titles = []
    seen_slugs: set[str] = set()
    for t in all_titles:
        if is_french_page(t):
            continue
        slug = slugify(t)
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)
        en_titles.append(t)

    print(f"After filtering French/duplicates: {len(en_titles)} English pages to scrape.\n")

    saved_files: list[tuple[str, Path]] = []
    errors = []

    for i, title in enumerate(en_titles, 1):
        pct = (i / len(en_titles)) * 100
        print(f"[{i}/{len(en_titles)} {pct:.0f}%] {title}")

        parse_data = fetch_page_html(title)
        if not parse_data:
            print(f"  [SKIP] Could not parse")
            errors.append(title)
            continue

        filepath = save_page(title, parse_data, OUTPUT_DIR)
        if filepath:
            saved_files.append((title, filepath))
            print(f"  -> {filepath}")
        else:
            errors.append(title)

        time.sleep(delay)

    build_categorized_index(saved_files)

    print(f"\n{'='*60}")
    print(f"Done! Scraped {len(saved_files)} pages into {OUTPUT_DIR}/")
    if errors:
        print(f"Failed/skipped: {len(errors)} pages")
        for e in errors[:20]:
            print(f"  - {e}")
    print(f"{'='*60}")


def crawl(start: str, max_depth: int, delay: float):
    """Crawl from a start page following links to max_depth."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    visited: set[str] = set()
    queue: list[tuple[str, int]] = [(start, 0)]
    saved_files: list[tuple[str, Path]] = []

    while queue:
        title, depth = queue.pop(0)
        if title in visited:
            continue
        visited.add(title)

        if is_french_page(title):
            continue

        print(f"[depth={depth}] Fetching: {title}")
        parse_data = fetch_page_html(title)
        if not parse_data:
            print(f"  [SKIP] Could not parse '{title}'")
            continue

        filepath = save_page(title, parse_data, OUTPUT_DIR)
        if filepath:
            saved_files.append((title, filepath))
            print(f"  -> Saved: {filepath}")

        if depth < max_depth:
            links = [
                link["*"]
                for link in parse_data.get("links", [])
                if link.get("ns") == 0 and "exists" in link
            ]
            for link_title in links:
                if link_title not in visited:
                    queue.append((link_title, depth + 1))

        time.sleep(delay)

    build_categorized_index(saved_files)
    print(f"\nDone! Scraped {len(saved_files)} pages into {OUTPUT_DIR}/")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape Alliance Canada wiki to Markdown"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Scrape ALL English pages (recommended for complete docs)",
    )
    parser.add_argument(
        "--depth", type=int, default=2,
        help="Max link-follow depth (ignored with --all)",
    )
    parser.add_argument(
        "--delay", type=float, default=0.3,
        help="Delay between requests in seconds (default: 0.3)",
    )
    parser.add_argument(
        "--start", type=str, default=START_PAGE,
        help=f"Starting page for crawl mode (default: {START_PAGE})",
    )
    args = parser.parse_args()

    print(f"Output: {OUTPUT_DIR.resolve()}\n")

    if args.all:
        print("Mode: ALL PAGES")
        scrape_all(args.delay)
    else:
        print(f"Mode: CRAWL from '{args.start}' depth={args.depth}")
        crawl(args.start, args.depth, args.delay)
