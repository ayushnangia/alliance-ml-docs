# Job Management, Monitoring, and Checkpointing

## Submitting jobs

```bash
sbatch job_script.sh           # Submit a job
sbatch --time=3:00:00 job.sh   # Override time limit
```

### Essential Slurm directives

```bash
#SBATCH --account=def-someuser       # Required if multiple accounts
#SBATCH --time=0-12:00               # Required: wall time (D-HH:MM)
#SBATCH --gpus-per-node=a100:1       # GPU request
#SBATCH --cpus-per-task=6            # CPU cores
#SBATCH --mem=32000M                 # Memory per node
#SBATCH --nodes=1                    # Number of nodes
#SBATCH --output=%N-%j.out           # Output file (%N=node, %j=jobid)
#SBATCH --error=%N-%j.err            # Separate error file
#SBATCH --mail-user=you@email.com    # Email notifications
#SBATCH --mail-type=BEGIN,END,FAIL   # When to email
#SBATCH --job-name=my_training       # Job name
```

### Time formats

- `30` = 30 minutes
- `3:00:00` = 3 hours
- `0-12:00` = 12 hours
- `3-0:00:00` = 3 days

Shorter time limits get scheduled faster.

## Monitoring jobs

### Check your jobs

```bash
sq                             # Your jobs only (short format)
squeue -u $USER                # Same, standard command
squeue -u $USER -t RUNNING     # Only running jobs
squeue -u $USER -t PENDING     # Only pending jobs
```

Status codes: `R` = Running, `PD` = Pending, `CG` = Completing

### Job details

```bash
scontrol show job JOBID        # Full job details
sacct -j JOBID                 # Accounting info after completion
sacct -j JOBID --format=JobID,Elapsed,MaxRSS,MaxVMSize,TotalCPU,AllocGRES
```

### Check why a job is pending

```bash
squeue -j JOBID -o "%R"       # Shows reason
```

Common reasons:
- `Priority` - waiting for higher priority jobs to finish
- `Resources` - waiting for requested resources to become available
- `AssocGrpCpuLimit` - group CPU limit reached

### Cancel a job

```bash
scancel JOBID                  # Cancel one job
scancel -u $USER               # Cancel all your jobs
scancel -u $USER -t PENDING    # Cancel only pending jobs
```

## Job arrays (hyperparameter sweeps)

Job arrays submit many similar jobs with one command:

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-06:00
#SBATCH --array=0-9            # 10 jobs, indices 0-9
#SBATCH --output=%A_%a.out     # %A=array job ID, %a=task index

module load python/3.11
source ~/ENV/bin/activate

LEARNING_RATES=(1e-3 5e-4 1e-4 5e-5 1e-5 1e-3 5e-4 1e-4 5e-5 1e-5)
LR=${LEARNING_RATES[$SLURM_ARRAY_TASK_ID]}

python train.py --lr $LR --run-id $SLURM_ARRAY_TASK_ID
```

Useful array options:
- `--array=0-99` - 100 tasks
- `--array=0-99%10` - 100 tasks, max 10 running at once
- `--array=1,3,5,7` - specific indices

## Checkpointing long training runs

### Why checkpoint?

- Jobs have wall-time limits (max 24h-72h depending on cluster)
- Node failures can kill your job
- Shorter jobs get scheduled faster
- Split a 3-day training into 3x 24h jobs

### PyTorch checkpointing

```python
import torch

# Save checkpoint
def save_checkpoint(model, optimizer, epoch, loss, path):
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss,
    }, path)

# Load checkpoint
def load_checkpoint(model, optimizer, path):
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    return checkpoint['epoch'], checkpoint['loss']

# In training loop
for epoch in range(start_epoch, num_epochs):
    # ... train ...
    if epoch % save_every == 0:
        save_checkpoint(model, optimizer, epoch, loss,
                       f'checkpoints/ckpt_{epoch}.pt')
```

### Auto-resume job script

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-24:00

module load python/3.11
source ~/ENV/bin/activate

# Find latest checkpoint
CKPT_DIR=$SCRATCH/checkpoints/my_experiment
LATEST=$(ls -t $CKPT_DIR/ckpt_*.pt 2>/dev/null | head -1)

if [ -n "$LATEST" ]; then
    echo "Resuming from $LATEST"
    python train.py --resume $LATEST
else
    echo "Starting fresh"
    python train.py
fi
```

### Where to save checkpoints

- **`$SCRATCH`**: Good default. Accessible from all nodes. Remember 60-day purge.
- **`$PROJECT`**: For important checkpoints you want to keep.
- **Not `$SLURM_TMPDIR`**: Local to one node, deleted when job ends.

## Experiment tracking

### Weights & Biases (wandb)

```bash
pip install --no-index wandb
```

```python
import wandb
wandb.init(project="my-project", config=args,
           settings=wandb.Settings(start_method="fork"))
# In training loop:
wandb.log({"loss": loss, "accuracy": acc, "epoch": epoch})
```

#### Per-cluster W&B availability

Full W&B usage requires internet access **and** access to Google Cloud Storage. Not all clusters support both:

| Cluster | W&B Availability | Notes |
|---------|-----------------|-------|
| Fir | Full access | No httpproxy needed |
| Nibi | Full access | No httpproxy needed |
| Vulcan | Full access | No httpproxy needed |
| Killarney | Full access | No httpproxy needed |
| Trillium | No access | Internet disabled on compute nodes |
| Narval | Limited | MILA and eligible groups only (via httpproxy) |
| Rorqual | Limited | MILA and eligible groups only (via httpproxy) |
| TamIA | Limited | MILA and eligible groups only (via httpproxy) |

**Google Cloud Storage API issue (Narval, Rorqual, TamIA):** Even with internet access, W&B automatically uploads environment info to Google Cloud Storage. This is **blocked** on these clusters and will cause your job to **crash or freeze** until wall time is reached. `wandb.save()` also requires GCS access and will fail. Use offline mode instead.

**MILA users:** Members of MILA Québec AI Institute can use W&B on clusters with internet access via `module load httpproxy` and a valid Mila-org W&B account.

#### Offline workflow (recommended for restricted clusters)

```bash
# In your job script, before training:
wandb offline

# Or set via environment variable:
export WANDB_MODE=offline
```

After your job finishes, sync from the login node:

```bash
wandb sync ./wandb/offline-run*
```

Complete offline job example:

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=32000M
#SBATCH --time=0-03:00

module load python/3.11
source ~/ENV/bin/activate

wandb offline
python train.py
```

**Alternative:** [Comet.ml](https://www.comet.ml/) works on Narval, Rorqual, and TamIA where W&B has issues. Install with `pip install --no-index comet_ml`.

### MLflow

```bash
pip install --no-index mlflow
```

```python
import mlflow
mlflow.start_run()
mlflow.log_params({"lr": lr, "batch_size": bs})
mlflow.log_metric("loss", loss, step=epoch)
mlflow.end_run()
```

## JupyterHub

JupyterHub is available on select clusters for short interactive work:

| Cluster | JupyterHub |
|---------|-----------|
| Fir | Yes |
| Narval | Yes |
| Rorqual | Yes |

Connect at the cluster's JupyterHub URL using your Alliance username and password.

### Important limitations

- **Compute nodes have no internet access.** You cannot `pip install`, `git clone`, or download data from within Jupyter notebooks on compute nodes.
- **Use for short interactive tasks only** — testing, debugging, quick visualization (a few minutes). For real training, submit batch jobs with `sbatch`.
- **One interactive job priority at a time.** If you already have an `salloc` or other interactive job running, your Jupyter session may queue for up to 5 minutes before timing out.

### Converting notebooks to scripts

For real training runs, convert notebooks to Python scripts:

```bash
jupyter nbconvert --to script my_notebook.ipynb
# Produces my_notebook.py — clean up and submit with sbatch
```

## GNU Parallel (many serial tasks)

For running many small tasks (preprocessing, inference on many files):

```bash
#!/bin/bash
#SBATCH --cpus-per-task=32
#SBATCH --mem=64000M
#SBATCH --time=0-06:00

module load python/3.11 gnu-parallel
source ~/ENV/bin/activate

# Process 1000 files using 32 parallel workers
ls $SCRATCH/inputs/*.json | parallel -j $SLURM_CPUS_PER_TASK \
    python process.py --input {} --output $SCRATCH/outputs/{/.}.out
```
