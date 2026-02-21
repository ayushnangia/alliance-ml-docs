# Distributed Training on Alliance Clusters

## Overview

Distributed training on Alliance clusters uses Slurm for scheduling and `torchrun` for launching processes. The key patterns:

- **Single-node multi-GPU**: Use `torchrun --nproc_per_node=N`
- **Multi-node multi-GPU**: Use `torchrun` with `--nnodes` and `--rdzv_endpoint`
- **DeepSpeed**: Use `torchrun` launcher (not DeepSpeed's own launcher)

## PyTorch DDP (Single Node, Multi-GPU)

### Job script

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:4
#SBATCH --cpus-per-task=24
#SBATCH --mem=128000M
#SBATCH --time=0-12:00
#SBATCH --output=%N-%j.out

module load python/3.11
source ~/ENV/bin/activate

export NCCL_ASYNC_ERROR_HANDLING=1

torchrun --nproc_per_node=4 train_ddp.py
```

### Minimal DDP training script

```python
import os
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def main():
    dist.init_process_group("nccl")
    rank = dist.get_rank()
    device = rank % torch.cuda.device_count()

    model = MyModel().to(device)
    model = DDP(model, device_ids=[device])

    # ... training loop ...

    dist.destroy_process_group()

if __name__ == "__main__":
    main()
```

`torchrun` automatically sets `MASTER_ADDR`, `MASTER_PORT`, `WORLD_SIZE`, and `RANK` environment variables.

## PyTorch DDP (Multi-Node)

### Job script

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --nodes=2
#SBATCH --gpus-per-node=a100:4
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=128000M
#SBATCH --time=0-24:00
#SBATCH --output=%N-%j.out

module load python/3.11
source ~/ENV/bin/activate

export NCCL_ASYNC_ERROR_HANDLING=1
export HEAD_NODE=$(hostname)

srun torchrun \
    --nnodes=$SLURM_NNODES \
    --nproc_per_node=4 \
    --rdzv_backend=c10d \
    --rdzv_endpoint="$HEAD_NODE" \
    train_ddp.py
```

Key points:
- `srun` launches the command on every allocated node
- `--ntasks-per-node=1` means one `torchrun` per node, which spawns 4 GPU processes
- `torchrun` handles rank assignment across nodes
- `NCCL_ASYNC_ERROR_HANDLING=1` is important for proper error handling in distributed runs

## DeepSpeed

DeepSpeed provides memory-efficient distributed training with ZeRO optimizer stages.

### Installation

```bash
pip install --no-index torch deepspeed
```

### Multi-node DeepSpeed job

**Job script** (`deepspeed-job.sh`):

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=2
#SBATCH --cpus-per-task=4
#SBATCH --mem=16000M
#SBATCH --time=0-00:30
#SBATCH --output=%N-%j.out

# Set up env on all nodes
srun -N $SLURM_NNODES -n $SLURM_NNODES config_env.sh

export HEAD_NODE=$(hostname)
module load cuda/11.4

srun launch_training.sh
```

**Environment setup** (`config_env.sh`):

```bash
#!/bin/bash
module load python/3.11
virtualenv --no-download $SLURM_TMPDIR/ENV
source $SLURM_TMPDIR/ENV/bin/activate
pip install --upgrade pip --no-index
pip install --no-index torch torchvision deepspeed
```

**Launch script** (`launch_training.sh`):

```bash
#!/bin/bash
source $SLURM_TMPDIR/ENV/bin/activate
export NCCL_ASYNC_ERROR_HANDLING=1

torchrun \
    --nnodes=$SLURM_NNODES \
    --nproc_per_node=2 \
    --rdzv_backend=c10d \
    --rdzv_endpoint="$HEAD_NODE" \
    train.py --deepspeed_config="./ds_config.json"
```

Use `torchrun` to launch, not DeepSpeed's own launcher (`deepspeed` CLI). The Alliance recommends `torchrun` for better Slurm integration.

### DeepSpeed config example (ZeRO Stage 2)

```json
{
    "train_batch_size": 64,
    "gradient_accumulation_steps": 4,
    "optimizer": {
        "type": "Adam",
        "params": {
            "lr": 1e-4,
            "betas": [0.9, 0.999],
            "eps": 1e-8,
            "weight_decay": 3e-7
        }
    },
    "fp16": {
        "enabled": true,
        "loss_scale": 0,
        "initial_scale_power": 16
    },
    "zero_optimization": {
        "stage": 2,
        "offload_optimizer": {
            "device": "cpu"
        },
        "contiguous_gradients": true,
        "overlap_comm": true
    }
}
```

### ZeRO stages quick guide

| Stage | What's partitioned | Memory savings | Speed impact |
|-------|-------------------|----------------|-------------|
| 0 | Nothing (pure DDP) | None | Fastest |
| 1 | Optimizer states | ~4x | Minimal |
| 2 | + Gradients | ~8x | Small |
| 3 | + Parameters | ~N x (N = GPUs) | Moderate |

Stage 2 is a good default. Stage 3 for models that don't fit in GPU memory.

## NCCL environment variables

Important variables for multi-node training:

```bash
export NCCL_ASYNC_ERROR_HANDLING=1    # Required for proper error handling
export NCCL_DEBUG=INFO                 # Verbose NCCL logging (for debugging)
export NCCL_IB_DISABLE=0              # Enable InfiniBand (default, don't disable)
```

## Checkpointing for long distributed runs

Save checkpoints periodically so you can resume after job ends:

```python
# Save (only on rank 0)
if dist.get_rank() == 0:
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.module.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss,
    }, f'{checkpoint_dir}/checkpoint_{epoch}.pt')

# Load (all ranks)
checkpoint = torch.load(checkpoint_path, map_location=f'cuda:{local_rank}')
model.module.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
```

Save checkpoints to `$SCRATCH` (accessible from all nodes), not `$SLURM_TMPDIR` (local to one node).

## Hugging Face Accelerate

An alternative to manual DDP setup:

```bash
pip install --no-index accelerate
```

```python
from accelerate import Accelerator

accelerator = Accelerator()
model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)

for batch in dataloader:
    outputs = model(batch)
    loss = compute_loss(outputs)
    accelerator.backward(loss)
    optimizer.step()
    optimizer.zero_grad()
```

Launch with the same `torchrun` command. Accelerate auto-detects the distributed setup.

## Troubleshooting

### NCCL timeout errors
- Check `NCCL_ASYNC_ERROR_HANDLING=1` is set
- Verify all nodes can communicate (InfiniBand should work by default)
- Try `NCCL_DEBUG=INFO` for detailed logs

### Out of memory
- Reduce batch size per GPU
- Use gradient accumulation
- Enable DeepSpeed ZeRO Stage 2 or 3
- Use mixed precision (`fp16` or `bf16`)

### Jobs stuck in PENDING
- Request fewer nodes/GPUs
- Request shorter time limits
- Check cluster load with `squeue` or `partition_summary`
