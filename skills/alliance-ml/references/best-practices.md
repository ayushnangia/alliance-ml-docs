# ML Best Practices on Alliance Clusters

## Test before you train

**Always run a short test job before submitting a long training run.** A 5-10 minute GPU test can save hours of wasted allocation by catching issues early: wrong modules, broken data paths, CUDA mismatches, or missing dependencies.

### Test job policies by cluster

| Cluster | Min job time | Test job minimum | Fast-start option | Notes |
|---------|-------------|-----------------|-------------------|-------|
| **Narval** | 1 hour | **5 minutes** | — | No internet on compute nodes |
| **Fir** | 1 hour | **5 minutes** | — | Has internet on compute nodes |
| **Rorqual** | 1 hour | **5 minutes** | — | No internet on compute nodes |
| **Graham** | 1 hour | **5 minutes** | — | |
| **Trillium** | — | — | `debugjob` (fast-start) | Up to 2h for 1 GPU; no internet, read-only home/project |
| **tamIA** | 1 hour | **5 minutes** | — | Must request full GPU nodes (4×H100 or 8×H200) |
| **Killarney** | — | Not documented | — | PAICE cluster; test with short `--time` |
| **Vulcan** | — | Not documented | — | PAICE cluster; test with short `--time` |
| **Nibi** | — | Not documented | — | Test with short `--time` |

### Quick test job examples

**Standard clusters (Narval, Fir, Rorqual, Graham):**
```bash
#!/bin/bash
#SBATCH --account=def-yourpi
#SBATCH --gpus-per-node=h100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0:10:00
#SBATCH --output=test-%j.out

module load python/3.11 gcc arrow
source ~/ENV/bin/activate

python train.py --max_steps=10 --data_dir $SLURM_TMPDIR/data
```

Or submit inline without a script:
```bash
sbatch --time=0:10:00 --gpus-per-node=h100:1 --cpus-per-task=6 \
  --mem=32000M --account=def-yourpi --wrap="
    module load python/3.11 gcc arrow && \
    source ~/ENV/bin/activate && \
    python train.py --max_steps=10
  "
```

**Trillium (`debugjob` — fast-start, dedicated debug nodes):**
```bash
# CPU debug session (up to 60 min, 1 full node)
debugjob

# 1 GPU debug session (up to 120 min)
debugjob -g 1

# 2 nodes, 8 GPUs (up to 15 min)
debugjob 2 -g 8
```

`debugjob` limitations on Trillium:
- No internet access
- Read-only access to `$HOME` and `$PROJECT` (can write to `$SCRATCH` and `$SLURM_TMPDIR`)
- No job submissions from within a debugjob
- Use `--export=ALL` to inherit your loaded modules

**tamIA (PAICE — whole GPU nodes only):**
```bash
#!/bin/bash
#SBATCH --account=aip-yourpi
#SBATCH --gpus=h100:4
#SBATCH --time=0:10:00
#SBATCH --output=test-%j.out

module load python/3.11 gcc arrow
source ~/ENV/bin/activate

python train.py --max_steps=10
```
Note: tamIA requires using all GPUs on allocated nodes (4 for H100, 8 for H200). Even test jobs burn a full node.

**Killarney / Vulcan (PAICE):**
```bash
#!/bin/bash
#SBATCH --account=aip-yourpi
#SBATCH --gpus-per-node=l40s:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=0:15:00
#SBATCH --output=test-%j.out

module load python/3.11 gcc arrow
source ~/ENV/bin/activate

python train.py --max_steps=10
```

### Pre-flight checklist

Run these checks in your test job (add to the top of your training script or run interactively):

```bash
# 1. Can you see GPUs?
nvidia-smi

# 2. Does PyTorch see them?
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, GPUs: {torch.cuda.device_count()}')"

# 3. Can you load your data?
python -c "
from datasets import load_dataset
ds = load_dataset('my_dataset', split='train[:10]')
print(f'Loaded {len(ds)} samples')
"

# 4. Does a forward pass work?
python -c "
import torch
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained('./my_model', local_files_only=True)
model.cuda()
x = torch.randint(0, 1000, (1, 32)).cuda()
with torch.no_grad():
    out = model(x)
print(f'Forward pass OK, output shape: {out.logits.shape}')
"

# 5. Are SLURM variables set?
echo "TMPDIR: $SLURM_TMPDIR"
echo "JOB ID: $SLURM_JOB_ID"
echo "GPUs:   $SLURM_GPUS_ON_NODE"
```

### What to verify in your test

| Check | Why | Fix |
|-------|-----|-----|
| `nvidia-smi` shows GPUs | GPU not allocated or wrong specifier | Check `--gpus-per-node` flag |
| `torch.cuda.is_available()` | CUDA/PyTorch mismatch | H100 needs torch >= 2.5.1 |
| Data loads without error | Wrong path or missing `module load gcc arrow` | Use `$SLURM_TMPDIR`, load arrow module |
| Forward pass completes | OOM or model too large | Reduce batch size or use gradient checkpointing |
| Checkpoint saves | Disk quota or permission issue | Save to `$SCRATCH`, check with `diskusage_report` |

## Job design

### Split long training into chunks

Alliance clusters enforce wall-time limits (typically 24h or 72h max). Design training to checkpoint and resume:

```bash
#!/bin/bash
#SBATCH --account=def-yourpi
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-24:00
#SBATCH --output=%N-%j.out

module load python/3.11
source ~/ENV/bin/activate

# Resume from latest checkpoint if it exists
CKPT_DIR=~/scratch/checkpoints/my_experiment
python train.py \
  --checkpoint_dir $CKPT_DIR \
  --resume_from_latest
```

### Request only what you need

Shorter jobs get scheduled faster. Over-requesting wastes both your allocation and queue time.

| Resource | How to right-size |
|----------|------------------|
| Time | Run a short test first, then extrapolate. Add 10-20% buffer. |
| GPUs | Start with 1 GPU. Only scale up if you've confirmed multi-GPU speedup. |
| Memory | Check actual usage with `sstat -j $JOBID --format=MaxRSS`. Request 10-20% more. |
| CPUs | 4-6 per GPU for data loading is usually enough. More rarely helps. |

### Use job arrays for hyperparameter sweeps

Don't submit 100 separate jobs manually. Use Slurm job arrays:

```bash
#!/bin/bash
#SBATCH --array=0-9
#SBATCH --account=def-yourpi
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-03:00

LR_VALUES=(1e-5 2e-5 5e-5 1e-4 2e-4 5e-4 1e-3 2e-3 5e-3 1e-2)
LR=${LR_VALUES[$SLURM_ARRAY_TASK_ID]}

module load python/3.11
source ~/ENV/bin/activate
python train.py --lr $LR --run_name "lr_sweep_${LR}"
```

## Data I/O

### The small files problem

The parallel filesystem (`$HOME`, `$SCRATCH`, `$PROJECT`) is optimized for large sequential reads, not millions of small files. Common ML datasets (ImageNet, COCO) with millions of small images will be extremely slow if read directly from the parallel filesystem.

**Solutions**:

1. **Archive with tar** (best for image datasets):
```bash
# Once, on login node:
tar cf $SCRATCH/imagenet.tar imagenet/

# In every job script:
cp $SCRATCH/imagenet.tar $SLURM_TMPDIR/
cd $SLURM_TMPDIR && tar xf imagenet.tar
```

2. **Use Parquet/HDF5** (best for tabular/text data):
```python
# Convert once on login node
import pyarrow.csv as pv
import pyarrow.parquet as pq
table = pv.read_csv("data.csv")
pq.write_table(table, "data.parquet")
```

3. **Use WebDataset** (best for large-scale training):
```python
# Stores images + labels in tar shards
import webdataset as wds
dataset = wds.WebDataset("$SLURM_TMPDIR/shards-{0000..0099}.tar")
```

### Always use `$SLURM_TMPDIR`

`$SLURM_TMPDIR` is fast local NVMe storage on the compute node. It's the fastest storage available during a job.

```bash
# Copy data at job start
cp $SCRATCH/dataset.tar $SLURM_TMPDIR/
cd $SLURM_TMPDIR && tar xf dataset.tar

# Point your training to local storage
python train.py --data_dir $SLURM_TMPDIR/dataset
```

**Do not** read training data directly from `$SCRATCH` or `$PROJECT` during training.

### DataLoader workers

Set `num_workers` in your DataLoader to match your CPU request:

```python
train_loader = DataLoader(
    dataset,
    batch_size=64,
    num_workers=4,          # Match --cpus-per-task
    pin_memory=True,        # Faster CPU→GPU transfer
    persistent_workers=True # Avoid re-spawning workers each epoch
)
```

## Checkpointing

### Save checkpoints regularly

Save at least every 30 minutes of training. Save to `$SCRATCH` (fast, 20 TB):

```python
import torch
import os

def save_checkpoint(model, optimizer, epoch, step, loss, path):
    os.makedirs(path, exist_ok=True)
    torch.save({
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "epoch": epoch,
        "step": step,
        "loss": loss,
    }, os.path.join(path, f"checkpoint_epoch{epoch}_step{step}.pt"))

def load_latest_checkpoint(model, optimizer, path):
    checkpoints = sorted(
        [f for f in os.listdir(path) if f.startswith("checkpoint_")],
        key=lambda x: os.path.getmtime(os.path.join(path, x))
    )
    if not checkpoints:
        return 0, 0
    ckpt = torch.load(os.path.join(path, checkpoints[-1]))
    model.load_state_dict(ckpt["model_state_dict"])
    optimizer.load_state_dict(ckpt["optimizer_state_dict"])
    return ckpt["epoch"], ckpt["step"]
```

### Checkpoint cleanup

Don't keep every checkpoint — `$SCRATCH` is purged after 60 days. Keep only the last N:

```python
def cleanup_checkpoints(path, keep=3):
    checkpoints = sorted(
        [f for f in os.listdir(path) if f.startswith("checkpoint_")],
        key=lambda x: os.path.getmtime(os.path.join(path, x))
    )
    for old in checkpoints[:-keep]:
        os.remove(os.path.join(path, old))
```

### Resubmit-friendly job scripts

Chain jobs that resume from checkpoints:

```bash
#!/bin/bash
#SBATCH --account=def-yourpi
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-24:00
#SBATCH --output=%N-%j.out

module load python/3.11
source ~/ENV/bin/activate

CKPT_DIR=~/scratch/my_experiment/checkpoints

python train.py \
  --checkpoint_dir $CKPT_DIR \
  --resume_from_latest \
  --max_steps 50000

# Auto-resubmit if training isn't done
if [ ! -f "$CKPT_DIR/DONE" ]; then
  sbatch $0
fi
```

## Memory management

### GPU memory

1. **Use gradient checkpointing** to trade compute for memory:
```python
model.gradient_checkpointing_enable()
```

2. **Use mixed precision** (fp16/bf16) — halves memory for activations:
```python
from torch.cuda.amp import autocast, GradScaler
scaler = GradScaler()
with autocast():
    output = model(input)
    loss = criterion(output, target)
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

3. **Gradient accumulation** — simulate larger batches without more memory:
```python
accumulation_steps = 4
for i, batch in enumerate(dataloader):
    loss = model(batch) / accumulation_steps
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### CPU memory

- Don't load entire datasets into RAM. Use memory-mapped formats (Parquet, HDF5, Arrow).
- Set `--mem` appropriately. Check actual usage after a test run with `sstat`.

## Experiment organization

### Directory structure

```
$PROJECT/$USER/
├── models/              # Downloaded pretrained models (persistent)
├── datasets/            # Processed datasets (Parquet, tar)
├── envs/                # Or ~/ENV for virtualenvs
│
$SCRATCH/
├── experiments/
│   ├── exp001_baseline/
│   │   ├── checkpoints/
│   │   ├── logs/
│   │   └── config.yaml
│   ├── exp002_larger_lr/
│   └── ...
```

### Reproducibility checklist

1. **Pin all package versions**: `pip freeze > requirements.txt`
2. **Save your config**: Log hyperparameters alongside checkpoints
3. **Set random seeds**:
```python
import torch
import numpy as np
import random

def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
```
4. **Save the exact commit**: `git rev-parse HEAD > experiment_dir/git_hash.txt`

### Experiment tracking

Use W&B or MLflow for tracking (available on most clusters except Graham):

```python
import wandb

# Set offline mode if cluster blocks outbound connections
# os.environ["WANDB_MODE"] = "offline"

wandb.init(project="my-project", config={"lr": 1e-4, "batch_size": 32})
wandb.log({"loss": loss.item(), "epoch": epoch})
```

For W&B, sync offline runs later:
```bash
wandb sync ~/scratch/wandb/offline-run-*
```

## Common anti-patterns

| Anti-pattern | Why it's bad | Do this instead |
|-------------|-------------|----------------|
| `conda install` | Library conflicts, wastes quota, not supported | `virtualenv` + `pip install --no-index` |
| Reading from `$SCRATCH` during training | Parallel FS can't handle random I/O well | Copy to `$SLURM_TMPDIR` first |
| `--time=7-00:00` | Won't schedule, max is usually 24-72h | Split into 24h chunks with checkpointing |
| No checkpointing | Lose all progress if job is preempted or times out | Save every 30 min |
| `--mem=0` on per-core clusters | Requests all memory, blocks other users | Request only what you need |
| Millions of small files on `$PROJECT` | Kills filesystem metadata performance | Archive with `tar` or use Parquet |
| Training on login nodes | Login nodes are shared, you'll get killed | Always use `sbatch` or `salloc` |
| `pip install torch` (without `--no-index`) | Downloads from PyPI, CUDA mismatch likely | `pip install --no-index torch` |
| Not setting `TOKENIZERS_PARALLELISM=false` | Deadlocks with multiprocessing DataLoader | Set the env var in job scripts |

## GPU-specific tips

### H100 clusters (Trillium, Fir, Nibi, Rorqual)

- Require PyTorch >= 2.5.1. Check with: `python -c "import torch; print(torch.__version__)"`
- Use bf16 instead of fp16 (H100 has native bf16 support, 2x throughput)
- NVLink enables fast multi-GPU communication within a node

### A100 clusters (Narval)

- A100-40GB per GPU. For models > 30 GB, use FSDP or DeepSpeed ZeRO
- MIG instances available for smaller tasks (5GB, 10GB, 20GB fractions)

### Monitoring GPU usage

```bash
# In an interactive job or via srun:
nvidia-smi                    # Snapshot of GPU usage
watch -n 1 nvidia-smi         # Live monitoring
nvtop                         # Interactive GPU monitor (if available)

# From outside the job:
sstat -j $JOBID --format=MaxRSS,MaxVMSize,AveCPU
```
