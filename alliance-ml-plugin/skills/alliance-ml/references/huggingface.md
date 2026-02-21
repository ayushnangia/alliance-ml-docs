# HuggingFace on Alliance Clusters

## Overview

The HuggingFace ecosystem (Transformers, Datasets, Evaluate, Accelerate) works on Alliance clusters with some important differences from local development:

1. **Install from Alliance wheels** (`pip install --no-index`), not PyPI
2. **Download models/datasets on login nodes** (compute nodes have no internet)
3. **Use offline mode** in job scripts to prevent download attempts
4. **Cache to `$SCRATCH`**, not `$HOME` (50 GB quota fills fast with LLMs)
5. **Set `HF_TOKEN`** for gated models (Llama, Gemma, etc.)

## HuggingFace token (for gated models)

Many popular models (Llama, Gemma, Mistral, etc.) are **gated** — you need to:

1. Create a token at https://huggingface.co/settings/tokens
2. Accept the model's license on its HuggingFace page (e.g., https://huggingface.co/meta-llama/Llama-3.1-8B)
3. Set the token as an environment variable on the cluster

```bash
# Add to your ~/.bashrc so it persists across sessions
export HF_TOKEN="hf_your_token_here"
```

Then all HF tools (CLI, Python API) will authenticate automatically:

```bash
# CLI — uses $HF_TOKEN automatically
huggingface-cli download meta-llama/Llama-3.1-8B

# Python — also uses $HF_TOKEN automatically
from transformers import AutoModel
model = AutoModel.from_pretrained("meta-llama/Llama-3.1-8B")
```

**In job scripts**, the token is **not needed** if you already downloaded the model and use `local_files_only=True`. But if you want belt-and-suspenders, include it:

```bash
# In your .sbatch file
export HF_TOKEN="hf_your_token_here"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
```

**Security:** Never hardcode tokens in scripts you commit to git. Use `~/.bashrc` or a `.env` file excluded from version control.

## Installing HuggingFace packages

```bash
module load python/3.11
virtualenv --no-download ~/ENV
source ~/ENV/bin/activate
pip install --no-index --upgrade pip

# Core packages
pip install --no-index transformers
pip install --no-index accelerate

# Datasets and Evaluate require the Arrow module
module load gcc arrow
pip install --no-index datasets
pip install --no-index evaluate
```

**Important**: You must `module load gcc arrow` every time you want to use `datasets` or `evaluate`, even after they're installed. Arrow provides the `pyarrow` dependency as a system module.

## Downloading models

Models must be downloaded **on a login node** before submitting jobs. Choose one method:

### Method 1: git-lfs (recommended for large models)

```bash
module load git-lfs/3.4.0
cd $SCRATCH   # or $PROJECT/$USER for persistent storage

# --depth 1 avoids downloading full git history
# --jobs 1 prevents overloading the login node
git clone --depth 1 --jobs 1 https://huggingface.co/meta-llama/Llama-3.1-8B
```

### Method 2: HuggingFace CLI

```bash
source ~/ENV/bin/activate
HF_HUB_DISABLE_XET=1 hf download --max-workers=1 HuggingFaceH4/zephyr-7b-beta
```

**Note**: Set `HF_HUB_DISABLE_XET=1` — the `hf_xet` download accelerator currently fails on Alliance systems.

### Method 3: Python

```python
from transformers import AutoModel, AutoTokenizer
model = AutoModel.from_pretrained("bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
```

Default cache: `$HOME/.cache/huggingface/hub`. Change it with `TRANSFORMERS_CACHE`.

### Where to store models

| Model size | Store in | Why |
|-----------|----------|-----|
| < 5 GB | `$HOME` | Backed up, persistent |
| 5–50 GB | `$SCRATCH` (default) or `$PROJECT` | `$SCRATCH` has 20 TB; use `$PROJECT` if you need persistence beyond 60 days |
| > 50 GB | `$SCRATCH` | Only place with enough space; re-download if purged |

**Default to `$SCRATCH`** — it has far more space (20 TB vs 1 TB for `$PROJECT`). Use `$PROJECT` only when you need the model to persist beyond the 60-day purge window or share with your group.

```bash
# Set HF_HOME to $SCRATCH (recommended)
export HF_HOME=$SCRATCH/.cache/huggingface

# Download a large model
huggingface-cli download meta-llama/Llama-3.1-8B
```

## Downloading datasets

```bash
# On a login node:
module load python/3.11 gcc arrow
source ~/ENV/bin/activate

# Set cache to $SCRATCH (more space) or $PROJECT (persistent)
export HF_DATASETS_CACHE=$SCRATCH/hf_datasets

python -c "
from datasets import load_dataset
dataset = load_dataset('HuggingFaceH4/ultrachat_200k', split='train_gen')
"
```

### Check available configs and splits first

Many HuggingFace datasets have multiple **configs** (subsets) and **splits** — loading with the wrong combination will crash. Always check before downloading:

```python
from datasets import get_dataset_config_names, get_dataset_split_names

# What configs (subsets) exist?
configs = get_dataset_config_names("AI-MO/aimo-validation-aime")
print(configs)  # e.g., ['AIME2025-I', 'AIME2025-II']

# What splits does each config have?
for config in configs:
    splits = get_dataset_split_names("AI-MO/aimo-validation-aime", config)
    print(f"{config}: {splits}")  # e.g., 'AIME2025-I': ['test']

# Then load the right config + split
dataset = load_dataset("AI-MO/aimo-validation-aime", "AIME2025-I", split="test")
```

**Common mistake:** Using `split="train"` when the dataset only has `split="test"`, or loading the whole dataset without specifying a config when multiple configs exist.

## Environment variables for jobs

Set these in your job scripts to enforce offline mode and control caching:

```bash
# Prevent any download attempts (compute nodes have no internet)
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_EVALUATE_OFFLINE=1
export HF_HUB_OFFLINE=1

# Point to where you downloaded models/datasets
export TRANSFORMERS_CACHE=/path/to/model/directory
export HF_DATASETS_CACHE=$SLURM_TMPDIR/datasets  # after copying
export HF_HOME=$SCRATCH/.cache/huggingface  # $SCRATCH has more space; use $PROJECT if you need persistence

# Disable tokenizer parallelism warnings with DataLoader workers
export TOKENIZERS_PARALLELISM=false
```

## Loading models offline in jobs

Always use `local_files_only=True` in job scripts:

```python
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained(
    "/path/to/model",
    local_files_only=True
)
tokenizer = AutoTokenizer.from_pretrained(
    "/path/to/model",
    local_files_only=True
)
```

For pipelines:

```python
from transformers import pipeline, AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("/path/to/model", local_files_only=True)
tokenizer = AutoTokenizer.from_pretrained("/path/to/model", local_files_only=True)
pipe = pipeline("text-classification", model=model, tokenizer=tokenizer)
```

## Accelerate for multi-GPU training

Accelerate simplifies distributed training by handling process launching and device placement.

### Installation

```bash
pip install --no-index accelerate
```

### Single-node multi-GPU job

```bash
#!/bin/bash
#SBATCH --account=def-yourpi
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=a100:4
#SBATCH --cpus-per-task=24
#SBATCH --mem=128G
#SBATCH --time=0-12:00
#SBATCH --output=%N-%j.out

module load python/3.11 gcc arrow
source ~/ENV/bin/activate

export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false

accelerate launch \
  --num_processes=4 \
  --mixed_precision=fp16 \
  train.py
```

### Multi-node job with Accelerate

```bash
#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=a100:4
#SBATCH --cpus-per-task=24
#SBATCH --mem=128G
#SBATCH --time=0-12:00
#SBATCH --output=%N-%j.out

module load python/3.11 gcc arrow
source ~/ENV/bin/activate

export HEAD_NODE=$(hostname)
export HEAD_NODE_PORT=29500
export NCCL_ASYNC_ERROR_HANDLING=1
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

srun bash -c '
source ~/ENV/bin/activate
accelerate launch \
  --multi_gpu \
  --num_machines=$SLURM_NNODES \
  --machine_rank=$SLURM_NODEID \
  --num_processes=8 \
  --main_process_ip=$HEAD_NODE \
  --main_process_port=$HEAD_NODE_PORT \
  train.py
'
```

## Fine-tuning LLMs with FSDP

For models too large for a single GPU, use Fully Sharded Data Parallel (FSDP) via Accelerate:

### FSDP config file

```yaml
# fsdp.yaml
compute_environment: LOCAL_MACHINE
distributed_type: FSDP
fsdp_config:
  fsdp_auto_wrap_policy: TRANSFORMER_BASED_WRAP
  fsdp_backward_prefetch: BACKWARD_PRE
  fsdp_cpu_ram_efficient_loading: true
  fsdp_forward_prefetch: true
  fsdp_offload_params: false
  fsdp_sharding_strategy: FULL_SHARD
  fsdp_state_dict_type: SHARDED_STATE_DICT
  fsdp_sync_module_states: true
  fsdp_use_orig_params: true
num_processes: 4
```

### LLM fine-tuning job script

```bash
#!/bin/bash
#SBATCH --account=def-yourpi
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=48
#SBATCH --mem=0
#SBATCH --time=0-06:00
#SBATCH --output=%N-%j.out

module load python/3.11 gcc arrow
source ~/ENV/bin/activate

# Copy dataset to fast local storage
cp -r $SCRATCH/my_dataset $SLURM_TMPDIR/

export HF_DATASETS_CACHE=$SLURM_TMPDIR/my_dataset
export TRANSFORMERS_CACHE=$SCRATCH/my_model
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TORCH_NCCL_ASYNC_ERROR_HANDLING=1

accelerate launch \
  --config_file=fsdp.yaml \
  --mixed_precision=fp16 \
  --num_processes=4 \
  train_llm.py
```

### Training script pattern

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from datasets import load_dataset
from trl import SFTTrainer
from accelerate import Accelerator

accelerator = Accelerator()

model = AutoModelForCausalLM.from_pretrained(
    "./my_model", local_files_only=True
)
tokenizer = AutoTokenizer.from_pretrained(
    "./my_model", local_files_only=True
)
tokenizer.pad_token = tokenizer.eos_token

dataset = load_dataset("my_dataset_name", split="train")

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    tokenizer=tokenizer,
    args=TrainingArguments(
        output_dir="./output",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        gradient_checkpointing=True,
        max_steps=1000,
        save_steps=100,
        logging_steps=10,
        learning_rate=2e-5,
        optim="adamw_torch",
        fp16=True,
    ),
)

trainer.train()
accelerator.wait_for_everyone()
```

## Common pitfalls

1. **Downloading in a job**: Compute nodes have no internet. Always download on login nodes.
2. **Missing `local_files_only=True`**: Without it, HuggingFace will try to reach the internet and timeout.
3. **Forgetting `module load gcc arrow`**: Required every time you use `datasets` or `evaluate`, even after installation.
4. **Filling `$HOME` with model cache**: Large models fill the 50 GB quota fast. Set `HF_HOME` to `$SCRATCH` (more space) or `$PROJECT` (persistent).
5. **Not copying datasets to `$SLURM_TMPDIR`**: Reading many small files from the parallel filesystem is slow. Copy to local storage first.
6. **Using `hf_xet`**: The XET download accelerator currently fails on Alliance systems. Set `HF_HUB_DISABLE_XET=1`.
7. **Not setting `TOKENIZERS_PARALLELISM=false`**: Causes deadlocks when using DataLoader with multiple workers.
