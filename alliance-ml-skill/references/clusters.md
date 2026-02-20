# Alliance Cluster Selection Guide

## Quick recommendation

| Your workload | Best cluster | Why |
|---------------|-------------|-----|
| Large-scale GPU training (H100) | **Trillium** | 63 GPU nodes, 4x H100 each, NVLink, 800 Gb/s InfiniBand |
| A100 GPU work | **Narval** | 4x A100-40GB per node, well-established |
| Smaller GPU tasks / inference | **Fir**, **Nibi**, **Rorqual** | H100 with MIG support for fractional GPU |
| L40S for inference/viz | **Killarney**, **Vulcan** | L40S-48GB GPUs |
| Large CPU-parallel jobs | **Trillium** (CPU) | 1224 CPU nodes, 192 cores each, whole-node scheduling |
| Classic HPC (MPI, OpenMP) | **Narval**, **Cedar**, **Graham** | General-purpose, per-core scheduling |

## Cluster details

### Trillium (University of Toronto / SciNet)
- **Login**: `trillium.alliancecan.ca`, `trillium-gpu.alliancecan.ca`
- **CPU nodes**: 1224 nodes, 192 cores (2x AMD EPYC 9655), 749 GB RAM
- **GPU nodes**: 63 nodes, 96 cores (1x AMD EPYC 9654), 4x H100 SXM 80GB, NVLink
- **Network**: NDR InfiniBand (400 Gb/s CPU, 800 Gb/s GPU), fully non-blocking
- **Storage**: 29 PB NVMe SSD (VAST Data), 714 GB/s read, 275 GB/s write
- **Archive**: 114 PB HPSS tape
- **Scheduling**: **Whole-node only**. You get entire nodes. No partial-node jobs.
- **Best for**: Large-scale multi-node training, LLM training, anything needing fast interconnect

### Narval (ETS Montreal / Calcul Quebec)
- **Login**: `narval.alliancecan.ca`
- **GPU nodes**: A100-40GB, 4 per node
- **MIG**: A100 MIG instances (5GB, 10GB, 20GB fractions)
- **Scheduling**: Per-core (standard Slurm)
- **Best for**: General GPU workloads, single-GPU fine-tuning, multi-GPU training

### Fir (SFU)
- **Login**: `fir.alliancecan.ca`
- **GPU**: H100-80GB with MIG support
- **Best for**: H100 workloads, MIG for smaller tasks

### Nibi
- **Login**: `nibi.alliancecan.ca`
- **GPU**: H100-80GB with MIG, also AMD MI300A-128GB
- **Best for**: H100 workloads, AMD GPU experimentation

### Rorqual
- **Login**: `rorqual.alliancecan.ca`
- **GPU**: H100-80GB with MIG (has short synonym specifiers like `h100_1g.10gb`)
- **Best for**: H100 workloads with flexible MIG sizing

### Killarney
- **Login**: `killarney.alliancecan.ca`
- **GPU**: H100-80GB and L40S-48GB
- **Best for**: Mixed GPU workloads

### Cedar (SFU)
- **Login**: `cedar.alliancecan.ca`
- **GPU**: Mixed (V100, P100, T4 on older nodes)
- **Best for**: Legacy workloads, general HPC

### Graham (University of Waterloo)
- **Login**: `graham.alliancecan.ca`
- **GPU**: Mixed older GPUs
- **Note**: W&B and Comet.ml not currently available on Graham
- **Best for**: General HPC, CPU workloads

### Vulcan
- **Login**: `vulcan.alliancecan.ca`
- **GPU**: L40S-48GB
- **Best for**: Inference, visualization, L40S workloads

### tamIA
- **GPU**: H100-80GB and H200
- **Specifiers**: `h100`, `h200`
- **Best for**: H200 access, large-scale training

### Niagara (University of Toronto / SciNet) — legacy
- **Login**: `niagara.alliancecan.ca`
- **Note**: Being replaced by Trillium. CPU-only, 80k cores, whole-node scheduling.
- **Best for**: Legacy large-scale CPU parallel jobs. Transitioning users should move to Trillium.

## Trillium-specific notes

Trillium uses **whole-node scheduling**, which is different from other clusters:

1. **No partial nodes**: Even a 1-core job gets an entire 192-core node
2. **No `--mem` needed**: You get all memory (749 GB) automatically
3. **GPU nodes**: Request with `--gpus-per-node=h100:N` (1-4)
4. **Create virtualenv on login node**: On Trillium, create your virtualenv in `$HOME` on a login node, then `source` it in job scripts (recommended over creating in `$SLURM_TMPDIR`)

### Trillium GPU job template

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=h100:4
#SBATCH --nodes=1
#SBATCH --time=0-24:00
#SBATCH --output=%N-%j.out

module load python/3.11
source ~/ENV/bin/activate

# No --cpus-per-task or --mem needed (whole node)
torchrun --nproc_per_node=4 train.py
```

## How to choose

1. **Need H100s?** → Trillium (most H100 nodes), or Fir/Nibi/Rorqual/Killarney
2. **Need A100s?** → Narval
3. **Small task, want fast scheduling?** → Use MIG instances on Narval/Fir/Nibi
4. **Need multi-node?** → Trillium (fastest interconnect, 800 Gb/s)
5. **Budget-conscious?** → MIG instances use fractions of a GPU
6. **Training LLMs?** → Trillium (H100 NVLink + fast interconnect + 29 PB storage)
