# Alliance Canada ML Documentation & Skill

A comprehensive collection of scraped, cleaned, and organized documentation from the [Digital Research Alliance of Canada](https://docs.alliancecan.ca/) (formerly Compute Canada), tailored for machine learning researchers working on Canadian HPC clusters.

## What's in this repo

```
.
├── docs/                    # Full technical documentation (409 pages)
│   ├── llms.txt             # LLM-friendly index of all docs
│   ├── llms-full.txt        # All docs inlined for LLM context
│   ├── INDEX.md             # Categorized human-readable index
│   └── *.md                 # Individual documentation pages
│
├── ml-docs/                 # ML researcher subset (156 pages)
│   ├── llms.txt             # LLM-friendly index (ML-focused)
│   ├── llms-full.txt        # All ML docs inlined for LLM context
│   ├── INDEX.md             # Categorized index for ML researchers
│   └── *.md                 # Individual documentation pages
│
├── alliance-ml-skill/       # Claude Code skill for Alliance HPC
│   ├── SKILL.md             # Main skill file (quick reference + routing)
│   └── references/          # Detailed reference guides
│       ├── getting-started.md
│       ├── python-env.md
│       ├── gpu-jobs.md
│       ├── storage-data.md
│       ├── distributed-training.md
│       ├── clusters.md
│       └── job-management.md
│
└── scrape_wiki.py           # Scraper used to fetch the docs
```

## docs/ — Full Documentation

All 409 English-language pages from the Alliance Canada technical wiki, converted to clean Markdown. Covers clusters, Slurm scheduling, storage, cloud computing, scientific software, bioinformatics, and more.

- **`llms.txt`** — Curated index following the [llms.txt spec](https://llmstxt.org/), with sections for clusters, getting started, jobs, storage, software, Python, AI/ML, programming, cloud, scientific software, and bioinformatics
- **`llms-full.txt`** — All 102 key docs inlined with XML tags, ready to drop into an LLM context window (~2 MB)
- **`INDEX.md`** — Full categorized index across 22 sections

## ml-docs/ — ML Researcher Subset

A hand-curated selection of 156 pages specifically relevant to ML researchers. Every file from the full docs was individually evaluated for inclusion. Organized into 16 sections covering everything from first SSH connection to multi-node DeepSpeed training.

### Sections

| Section | Pages | Covers |
|---------|-------|--------|
| Getting Started | 10 | Accounts, SSH, first job |
| SSH & Remote Access | 12 | SSH keys, tunnelling, MobaXterm |
| Cluster Specifications | 16 | Hardware specs for each cluster |
| Submitting & Managing Jobs | 12 | sbatch, squeue, job arrays |
| Storage & Data Management | 15 | $SCRATCH, $PROJECT, Globus, tar |
| Python Environment | 9 | virtualenv, pip wheels, Jupyter |
| Software Modules & Containers | 11 | Lmod, Apptainer, EasyBuild |
| GPU & CUDA Programming | 9 | CUDA, nvidia-smi, MIG, multi-GPU |
| AI & ML Frameworks | 24 | PyTorch, TensorFlow, HuggingFace, DeepSpeed, vLLM |
| ML Experiment Tracking | 7 | W&B, MLflow, TensorBoard |
| Distributed & Parallel Computing | 7 | MPI, NCCL, torchrun |
| Datasets & Data Formats | 7 | HDF5, NetCDF, large collections |
| Debugging & Profiling | 3 | Profiling, debugging tools |
| Cloud Computing | 6 | OpenStack VMs, vGPUs |
| Programming Tools | 5 | Git, R, Julia |
| Resource Allocation | 3 | RAC, allocations |

- **`llms.txt`** — ML-focused index with key facts (GPU specifiers, pip patterns, storage tiers)
- **`llms-full.txt`** — All 156 ML docs inlined (~3 MB)

## alliance-ml-skill/ — Claude Code Skill

A [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code) that gives Claude accurate, up-to-date knowledge about running ML workloads on Alliance Canada clusters. Divided into focused reference files so Claude loads only what's needed.

### Skill structure

| File | What it covers |
|------|---------------|
| **SKILL.md** | Quick reference cheat sheet — SSH, Python env, GPU job template, specifier table, storage tiers, common pitfalls. Routes to detailed references. |
| **references/getting-started.md** | Account creation, SSH, MFA, modules, first steps |
| **references/python-env.md** | virtualenv, `--no-index` wheels, SciPy stack, why not Conda |
| **references/gpu-jobs.md** | GPU specifiers by cluster, MIG, job scripts, interactive sessions |
| **references/storage-data.md** | Storage tiers, `$SLURM_TMPDIR`, dataset strategies, Globus |
| **references/distributed-training.md** | PyTorch DDP, multi-node, DeepSpeed ZeRO, torchrun, NCCL |
| **references/clusters.md** | Cluster comparison, Trillium details, selection guide |
| **references/job-management.md** | Slurm directives, job arrays, checkpointing, W&B/MLflow |

### Installing the skill

Copy or symlink into your Claude Code skills directory:

```bash
# Option 1: Symlink
ln -s /path/to/alliance-ml-skill ~/.claude/skills/alliance-ml

# Option 2: Copy
cp -r alliance-ml-skill ~/.claude/skills/alliance-ml
```

Then Claude will automatically use this skill when you ask about Alliance Canada clusters, GPU jobs, Slurm, or ML training on HPC.

## llms.txt files

This repo follows the [llms.txt specification](https://llmstxt.org/) for LLM-friendly documentation:

| File | Size | Contents |
|------|------|----------|
| `docs/llms.txt` | 12 KB | Curated index of all documentation |
| `docs/llms-full.txt` | ~2 MB | 102 key docs inlined with XML structure |
| `ml-docs/llms.txt` | 18 KB | ML-focused index with key facts |
| `ml-docs/llms-full.txt` | ~3 MB | All 156 ML docs inlined |

### Using with LLMs

Drop the relevant `llms.txt` (index only) or `llms-full.txt` (full content) into your LLM's context:

```python
# Quick reference — just the index
with open("ml-docs/llms.txt") as f:
    context = f.read()

# Full context — all docs inlined
with open("ml-docs/llms-full.txt") as f:
    context = f.read()
```

## Quick start for ML researchers

### 1. Connect

```bash
ssh youruser@narval.alliancecan.ca
```

### 2. Set up Python

```bash
module load python/3.11
virtualenv --no-download ~/mlenv
source ~/mlenv/bin/activate
pip install --no-index --upgrade pip
pip install --no-index torch torchvision
```

### 3. Submit a GPU job

```bash
#!/bin/bash
#SBATCH --account=def-yourpi
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-03:00

module load python/3.11
source ~/mlenv/bin/activate
python train.py
```

```bash
sbatch train_job.sh
```

### Key things to remember

- Use `virtualenv` + `pip install --no-index`, never Conda
- Copy datasets to `$SLURM_TMPDIR` for fast I/O
- Checkpoint regularly — split long training into 24h chunks
- Shorter jobs get scheduled faster

## Scraping

The documentation was scraped from the [Alliance Canada wiki](https://docs.alliancecan.ca/wiki/Technical_documentation) using `scrape_wiki.py`. The scraper:

- Fetches all English pages via the MediaWiki API
- Converts HTML to clean Markdown
- Filters out French pages, redirects, and junk
- Builds categorized indices

```bash
# Recreate the full docs (requires .venv with requests, beautifulsoup4, markdownify)
python scrape_wiki.py --all --output docs/
```

## License

The documentation content is sourced from the [Digital Research Alliance of Canada](https://docs.alliancecan.ca/) wiki. The scraper, skill, and organizational structure in this repo are provided as-is for educational and research purposes.
