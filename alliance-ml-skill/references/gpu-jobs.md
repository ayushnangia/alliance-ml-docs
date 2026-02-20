# GPU Job Submission on Alliance Clusters

## Requesting GPUs

Use `--gpus-per-node` to request GPUs:

```bash
#SBATCH --gpus-per-node=a100:1     # 1x A100 on Narval
#SBATCH --gpus-per-node=h100:1     # 1x H100 on Trillium/Fir/Nibi
#SBATCH --gpus-per-node=h100:4     # 4x H100 (full GPU node on Trillium)
#SBATCH --gpus-per-node=l40s:1     # 1x L40S on Killarney/Vulcan
```

Always specify the GPU model. Without it, your job may be rejected or sent to an arbitrary GPU.

## Available GPUs by cluster

| Cluster | GPU | VRAM | Specifier | GPUs/node |
|---------|-----|------|-----------|-----------|
| Trillium | H100 SXM | 80 GB | `h100` | 4 |
| Fir | H100 | 80 GB | `h100` | varies |
| Nibi | H100 | 80 GB | `h100` | varies |
| Rorqual | H100 | 80 GB | `h100` | varies |
| Killarney | H100 / L40S | 80 GB / 48 GB | `h100` / `l40s` | varies |
| Narval | A100 | 40 GB | `a100` | 4 |
| tamIA | H100 / H200 | 80 GB | `h100` / `h200` | varies |
| Vulcan | L40S | 48 GB | `l40s` | varies |

### MIG (Multi-Instance GPU)

Some clusters offer MIG partitions of H100/A100 GPUs for smaller workloads:

**Narval A100 MIG instances:**
- `a100_1g.5gb` - 1/7 of an A100 (5 GB)
- `a100_2g.10gb` - 2/7 of an A100 (10 GB)
- `a100_3g.20gb` - 3/7 of an A100 (20 GB)

**Fir/Nibi/Rorqual H100 MIG instances:**
- `nvidia_h100_80gb_hbm3_1g.10gb` - 1/7 of an H100 (10 GB)
- `nvidia_h100_80gb_hbm3_2g.20gb` - 2/7 of an H100 (20 GB)
- `nvidia_h100_80gb_hbm3_3g.40gb` - 3/7 of an H100 (40 GB)

MIG is great for inference, small model fine-tuning, or development/debugging. Shorter queue wait times since you're sharing a GPU.

### Discover available GPU specifiers

```bash
sinfo -o "%G" | grep gpu | sed 's/gpu://g' | sed 's/),/\n/g' | cut -d: -f1 | sort | uniq
```

## CPU and memory per GPU

Each GPU should be paired with appropriate CPU cores and memory. Recommended ratios vary by cluster. General guidelines:

- **Narval**: ~6 CPUs, ~32 GB memory per A100
- **Trillium**: Whole-node scheduling (you get all 96 cores and 749 GB with 4 GPUs)
- **Cedar/Graham**: ~6 CPUs, ~32 GB per GPU (varies by node type)

For exact ratios, check the "bundle characteristics" in your cluster's documentation.

```bash
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
```

## Example job scripts

### Single GPU training

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-12:00
#SBATCH --output=%N-%j.out

module load python/3.11
source ~/ENV/bin/activate

# Copy dataset to fast local storage
cp $PROJECT/datasets/my_data.tar $SLURM_TMPDIR/
cd $SLURM_TMPDIR && tar xf my_data.tar

python train.py --data-dir $SLURM_TMPDIR/my_data --epochs 50
```

### Multi-GPU single node (4x H100 on Trillium)

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=h100:4
#SBATCH --cpus-per-task=96
#SBATCH --mem=0                 # Request all memory on the node
#SBATCH --nodes=1
#SBATCH --time=0-24:00
#SBATCH --output=%N-%j.out

module load python/3.11
source ~/ENV/bin/activate

export NCCL_ASYNC_ERROR_HANDLING=1

torchrun --nproc_per_node=4 \
    train_ddp.py --epochs 100
```

### Interactive GPU session (for debugging)

```bash
salloc --account=def-someuser --gpus-per-node=a100:1 \
    --cpus-per-task=6 --mem=32000M --time=1:00:00
```

Once allocated, you get a shell on a compute node where you can run Python interactively.

## Monitoring GPU usage

### Inside a running job

```bash
nvidia-smi                    # GPU utilization snapshot
watch -n 1 nvidia-smi         # Live monitoring
nvtop                         # Interactive GPU monitor (if available)
```

### From a login node

```bash
sq                            # List your jobs
squeue -u $USER               # Same, more verbose
sacct -j JOBID --format=JobID,Elapsed,MaxRSS,MaxVMSize,TotalCPU
```

### Check GPU utilization of a running job

```bash
srun --jobid=JOBID --pty nvidia-smi
```

## Tips

1. **Start small**: Test with a MIG instance or short time limit before requesting full GPUs for long runs.
2. **Use `--time` wisely**: Shorter jobs get scheduled faster. If your training takes 3 days, split into 3x 24h jobs with checkpointing.
3. **Match resources**: Don't request 4 GPUs if your code only uses 1. Wasted resources hurt your priority.
4. **Email notifications**: Add `#SBATCH --mail-user=you@email.com` and `#SBATCH --mail-type=ALL` to get notified when jobs start/end/fail.
