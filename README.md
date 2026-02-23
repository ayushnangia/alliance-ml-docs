# Alliance Canada ML Documentation & Claude Code Plugin

Everything you need to run ML workloads on [Alliance Canada](https://docs.alliancecan.ca/) (formerly Compute Canada) HPC clusters — scraped docs, curated ML subset, and a Claude Code plugin that actually knows how these clusters work.

## Quick Start

### Option A: Agent Skills (works with Claude Code, Codex, Cursor, Copilot, etc.)

```bash
npx skills add ayushnangia/alliance-ml-docs
```

One command. Works with 37+ AI coding agents via the [open agent skills ecosystem](https://skills.sh).

### Option B: Claude Code plugin (marketplace)

```bash
# Add the marketplace
/plugin marketplace add ayushnangia/alliance-ml-docs

# Install the plugin
/plugin install alliance-ml@alliance-ml-docs
```

### Option C: Install from a local clone

```bash
git clone https://github.com/ayushnangia/alliance-ml-docs.git
cd alliance-ml-docs
claude plugin add ./alliance-ml-plugin
```

### Option D: On a cluster login node (symlink)

```bash
git clone https://github.com/ayushnangia/alliance-ml-docs.git ~/alliance-ml-docs
mkdir -p ~/.claude/skills
ln -s ~/alliance-ml-docs/skills/alliance-ml ~/.claude/skills/alliance-ml
```

### Try it

Ask Claude things like:
- "Write me a multi-GPU training job for Narval"
- "How do I use vLLM for inference on 2 nodes?"
- "Set up HuggingFace with offline mode for Trillium"
- "Why is my W&B job crashing on Narval?"

## What's in this repo

```
.
├── skills/                    # Agent Skills (npx skills add)
│   └── alliance-ml/
│       ├── SKILL.md           # Quick reference + routing logic
│       └── references/        # 12 detailed reference guides
│
├── alliance-ml-plugin/       # Claude Code plugin wrapper
│   ├── plugin.json
│   └── skills/alliance-ml → ../../skills/alliance-ml
│
├── .claude-plugin/
│   └── marketplace.json      # Marketplace config (enables remote install)
│
├── ml-docs/                   # 156 ML-relevant docs (curated subset)
│   ├── llms.txt               # LLM-friendly index
│   └── llms-full.txt          # All docs inlined (~3 MB)
│
├── docs/                      # Full 409-page doc set
│   ├── llms.txt
│   └── llms-full.txt
│
└── scrape_wiki.py             # Scraper to refresh docs
```

## Plugin Reference Files

The plugin has 12 reference files that Claude loads on-demand based on what you're asking about:

| Reference | What it covers |
|-----------|---------------|
| **getting-started.md** | Account, SSH, MFA, Lmod modules, StdEnv/2023 |
| **python-env.md** | virtualenv, `--no-index` wheels, why not Conda |
| **gpu-jobs.md** | GPU specifiers by cluster, MIG, job scripts |
| **storage-data.md** | Storage tiers, `$SLURM_TMPDIR`, Globus transfers |
| **clusters.md** | Cluster comparison and selection guide |
| **distributed-training.md** | PyTorch DDP, DeepSpeed ZeRO, torchrun, NCCL |
| **job-management.md** | Slurm directives, job arrays, checkpointing, W&B per-cluster availability, JupyterHub |
| **huggingface.md** | Transformers, Datasets, Accelerate, FSDP, offline mode, HF_TOKEN for gated models |
| **data-formats.md** | Apache Arrow module, PyArrow, Parquet |
| **containers.md** | Apptainer: GPU containers, bind mounts, SIF from Docker, Conda in containers |
| **vllm.md** | vLLM install, tensor parallelism, multi-node Ray inference |
| **best-practices.md** | Job design, I/O optimization, checkpointing, memory, anti-patterns |

## Key Things to Remember

```bash
# Python: always use virtualenv + Alliance wheels
module load python/3.11
virtualenv --no-download ~/mlenv
source ~/mlenv/bin/activate
pip install --no-index torch torchvision

# HuggingFace: set token for gated models, download on login node
export HF_TOKEN="hf_your_token_here"
export HF_HOME=$SCRATCH/.cache/huggingface
huggingface-cli download meta-llama/Llama-3.1-8B

# Jobs: always enforce offline mode
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_DATASETS_OFFLINE=1

# Arrow: required for HF datasets/evaluate
module load gcc arrow
```

- Use `virtualenv` + `pip install --no-index`, **never Conda**
- Copy datasets to `$SLURM_TMPDIR` at job start for fast I/O
- Download models/datasets on **login nodes** only
- Use `local_files_only=True` in all `from_pretrained()` calls in jobs
- Checkpoint regularly — split long training into 24h chunks
- Shorter jobs get scheduled faster
- Store large models in `$SCRATCH` (20 TB), not `$HOME` (50 GB)

## ml-docs/ — For Non-Plugin Use

If you're not using Claude Code, you can still use the curated docs directly:

```python
# Drop into any LLM's context
with open("ml-docs/llms-full.txt") as f:
    context = f.read()  # ~3 MB, all 156 ML docs inlined
```

The 156 pages cover: getting started, SSH, cluster specs, Slurm jobs, storage, Python environments, Lmod/Apptainer, GPU/CUDA, PyTorch/TensorFlow/HuggingFace/DeepSpeed/vLLM, W&B/MLflow, MPI/NCCL, data formats, debugging, cloud, and resource allocation.

## Scraping

```bash
# Recreate docs from the Alliance wiki
pip install requests beautifulsoup4 markdownify
python scrape_wiki.py --all --output docs/
```

## Disclaimer & Attribution

The documentation in `docs/` and `ml-docs/` is sourced from the [Digital Research Alliance of Canada](https://docs.alliancecan.ca/) public wiki. All credit for the original documentation goes to the Alliance and its contributors.

**This is not an official Alliance Canada product.** For authoritative documentation, refer to [docs.alliancecan.ca](https://docs.alliancecan.ca/).

The scraper, plugin, README, llms.txt curation, and organizational structure are original work. If you are a representative of the Alliance and have concerns, please open an issue.
