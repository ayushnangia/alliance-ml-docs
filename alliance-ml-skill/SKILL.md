---
name: alliance-ml
description: "Guide for running ML/AI workloads on Alliance Canada (formerly Compute Canada) HPC clusters. Use this skill whenever the user mentions Alliance Canada, Compute Canada, Narval, Cedar, Graham, Trillium, Niagara, Fir, Nibi, Rorqual, Killarney, Slurm job submission on Canadian clusters, sbatch for ML training, GPU jobs on HPC, virtualenv on clusters, or anything related to running deep learning on shared computing infrastructure. Also use when the user asks about CUDA on clusters, distributed training with DeepSpeed/PyTorch DDP on Slurm, or managing datasets on parallel filesystems."
---

# Alliance Canada HPC for ML Researchers

This skill helps you write correct Slurm job scripts, set up Python environments, choose the right GPU cluster, manage data, and scale training on Alliance Canada (formerly Compute Canada) infrastructure.

Alliance clusters use **Slurm** for scheduling, **Lmod** for software modules, and **virtualenv** (never Conda) for Python environments. Pre-built Python wheels are available for most ML packages.

## Quick Reference

### Connect to a cluster

```bash
ssh username@trillium.alliancecan.ca
```

Cluster login nodes: `narval.alliancecan.ca`, `cedar.alliancecan.ca`, `trillium.alliancecan.ca`, `graham.alliancecan.ca`, `fir.alliancecan.ca`, `nibi.alliancecan.ca`, `rorqual.alliancecan.ca`

### Set up a Python environment

```bash
module load python/3.11
virtualenv --no-download ~/ENV
source ~/ENV/bin/activate
pip install --no-index --upgrade pip
pip install --no-index torch torchvision
```

The `--no-index` flag uses Alliance pre-built wheels (optimized for cluster hardware). Never use Conda/Anaconda on these clusters.

### Submit a basic GPU job

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-03:00
#SBATCH --output=%N-%j.out

module load python/3.11
source ~/ENV/bin/activate

python train.py
```

Submit with `sbatch train_job.sh`. Check status with `sq` (alias for your jobs only).

### GPU specifiers by cluster

| Cluster | GPU | Slurm specifier |
|---------|-----|-----------------|
| Trillium | H100 80GB | `h100` |
| Fir | H100 80GB | `h100` |
| Nibi | H100 80GB | `h100` |
| Rorqual | H100 80GB | `h100` |
| Killarney | H100 80GB / L40S 48GB | `h100` / `l40s` |
| Narval | A100 40GB | `a100` |
| tamIA | H100 80GB / H200 | `h100` / `h200` |
| Vulcan | L40S 48GB | `l40s` |

Use: `--gpus-per-node=h100:1` (or `a100:1`, `l40s:1`, etc.)

### Storage tiers

| Filesystem | Purpose | Quota | Backed up | Purged |
|------------|---------|-------|-----------|--------|
| `$HOME` | Code, scripts, small configs | 50 GB | Yes | No |
| `$SCRATCH` | Large temp files, checkpoints | 20 TB | No | 60 days |
| `$PROJECT` | Shared datasets, results | 1 TB (expandable) | Yes | No |
| `$SLURM_TMPDIR` | Fast local node storage (per job) | Varies | No | Job end |
| Nearline | Long-term archive | 2 TB | Yes | No |

For ML datasets: copy to `$SLURM_TMPDIR` at job start for best I/O performance.

### Check disk usage

```bash
diskusage_report
```

## When to read reference files

The sections below point to detailed reference files. Read the one that matches the user's task:

### Getting started (account, SSH, MFA)
Read `references/getting-started.md` when the user needs help with:
- Creating an account, first-time setup
- SSH connections, keys, MFA
- Basic Linux orientation on clusters

### Python environment setup
Read `references/python-env.md` when the user needs help with:
- Installing Python packages (pip, wheels)
- Virtualenv creation and activation
- Why not Conda, and what to do instead
- SciPy stack, available wheels
- Creating virtualenvs inside jobs ($SLURM_TMPDIR)

### GPU job submission
Read `references/gpu-jobs.md` when the user needs help with:
- Writing GPU job scripts (single/multi-GPU)
- Choosing GPU types and specifiers
- MIG (Multi-Instance GPU) partitions
- CPU/memory ratios per GPU
- Monitoring GPU jobs (nvidia-smi, nvtop)

### Storage and data management
Read `references/storage-data.md` when the user needs help with:
- Choosing where to store datasets
- Handling large collections of small files (tar, zip)
- Using $SLURM_TMPDIR for fast local I/O
- Transferring data (Globus, scp, rsync)
- Scratch purging policies

### Distributed training
Read `references/distributed-training.md` when the user needs help with:
- Multi-GPU training on a single node
- Multi-node distributed training
- PyTorch DDP (DistributedDataParallel)
- DeepSpeed (ZeRO stages, config)
- torchrun launcher with Slurm
- NCCL environment variables

### Cluster selection guide
Read `references/clusters.md` when the user needs help with:
- Which cluster to use for their workload
- Cluster specs (nodes, GPUs, memory, network)
- Trillium vs Narval vs Cedar vs others
- Whole-node scheduling (Trillium) vs per-core (others)

### Job management and monitoring
Read `references/job-management.md` when the user needs help with:
- Slurm directives (time, memory, account)
- Job arrays for hyperparameter sweeps
- Monitoring jobs (squeue, sacct, sstat)
- Checkpointing long training runs
- Experiment tracking (W&B, MLflow)

## Common pitfalls

1. **Using Conda**: Alliance clusters provide optimized wheels. Use `virtualenv` + `pip install --no-index`. Conda causes library conflicts and wastes quota.

2. **Not using `--no-index`**: Without it, pip downloads from PyPI instead of using pre-built cluster wheels, which can cause CUDA mismatches.

3. **Forgetting `--account`**: If you belong to multiple allocations, you must specify `--account=def-yourpi`.

4. **Storing datasets in `$HOME`**: Home is only 50 GB. Use `$PROJECT` for persistent datasets, `$SCRATCH` for temporary large files.

5. **Reading many small files from `$PROJECT`/`$SCRATCH`**: Parallel filesystems are slow with many small files. Archive them with `tar` and extract to `$SLURM_TMPDIR` at job start.

6. **Not checkpointing**: Jobs have wall-time limits. Save checkpoints regularly so you can resume. Split 3-day training into 3x 24h jobs.

7. **Requesting too much time**: Shorter jobs get scheduled faster. Request only what you need.

8. **H100 clusters need torch >= 2.5.1**: On Trillium/Fir/Nibi, older PyTorch versions won't work with H100 GPUs.
