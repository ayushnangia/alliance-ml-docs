# vLLM Inference on Alliance Clusters

## Overview

[vLLM](https://github.com/vllm-project/vllm) provides high-throughput, memory-efficient inference and serving for large language models. It supports various decoding algorithms, quantization methods, and parallelism strategies.

Use vLLM when you need to:
- Run inference on large language models (LLMs)
- Serve models with high throughput
- Split large models across multiple GPUs (tensor parallelism)
- Run multi-node inference for models too large for a single node

## Installation

```bash
# Load required modules
module load opencv/4.11 python/3.12

# Check available versions
avail_wheels vllm

# Create environment and install
virtualenv --no-download ~/vllm_env
source ~/vllm_env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index vllm

# Save requirements for reproducibility
pip freeze > ~/vllm-requirements.txt

# Deactivate and clean up install environment
deactivate
rm -r ~/vllm_env
```

**Note:** The `opencv` module is a required dependency. Use `pip install --no-index vllm==X.Y.Z` to pin a specific version (e.g., `0.8.4`).

## Downloading models

**Download models on the login node only** — compute nodes may not have internet access.

```bash
module load python/3.12
virtualenv --no-download /tmp/dl_env && source /tmp/dl_env/bin/activate
pip install --no-index huggingface_hub

# Download a model (cached in $HOME/.cache/huggingface/hub by default)
huggingface-cli download facebook/opt-125m

rm -r /tmp/dl_env
```

For large models, redirect the cache to `$PROJECT` to avoid filling `$HOME`:

```bash
export HF_HOME=$PROJECT/.cache/huggingface
huggingface-cli download meta-llama/Llama-3-8B
```

See `references/huggingface.md` for more details on caching and offline mode.

## Single-node inference

### Job script

**File:** vllm-example.sh

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --ntasks=1
#SBATCH --gpus-per-task=2
#SBATCH --cpus-per-task=2
#SBATCH --mem=32000M
#SBATCH --time=0-00:30
#SBATCH --output=%N-%j.out

module load python/3.12 gcc opencv/4.11
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate

pip install --no-index -r ~/vllm-requirements.txt

python vllm-example.py
```

### Python script

**File:** vllm-example.py

```python
from vllm import LLM

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]

# Set tensor_parallel_size to the number of GPUs in your job
llm = LLM(model="facebook/opt-125m", tensor_parallel_size=2)

outputs = llm.generate(prompts)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

**Tip:** If your model fits in a single GPU, omit `tensor_parallel_size` (defaults to 1).

## Multi-node inference with Ray

For models that don't fit on a single node, vLLM uses [Ray](https://www.ray.io/) to manage multi-node tensor parallelism.

### Job script

**File:** vllm-multinode.sh

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=2
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-00:30
#SBATCH --output=%N-%j.out

## Install environment on all nodes
module load gcc python/3.12 arrow/19 opencv/4.11
srun -N $SLURM_NNODES -n $SLURM_NNODES config_env.sh

export HEAD_NODE=$(hostname --ip-address)
export RAY_PORT=34567

## Set HuggingFace to offline mode (compute nodes may lack internet)
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

source $SLURM_TMPDIR/ENV/bin/activate

## Start Ray head node
ray start --head --node-ip-address=$HEAD_NODE --port=$RAY_PORT \
    --num-cpus=$SLURM_CPUS_PER_TASK --num-gpus=2 --block &
sleep 10

## Start Ray workers on other nodes
srun launch_ray.sh &
ray_cluster_pid=$!
sleep 10

## Run inference
VLLM_HOST_IP=$(hostname --ip-address) python vllm_example.py

## Clean up Ray cluster
kill $ray_cluster_pid
```

### Environment setup

**File:** config_env.sh

```bash
#!/bin/bash
module load python/3.12 gcc opencv/4.11 arrow/19
virtualenv --no-download $SLURM_TMPDIR/ENV
source $SLURM_TMPDIR/ENV/bin/activate
pip install --upgrade pip --no-index
pip install --no-index ray -r ~/vllm-requirements.txt
deactivate
```

### Ray worker launcher

**File:** launch_ray.sh

```bash
#!/bin/bash
if [[ "$SLURM_PROCID" -eq "0" ]]; then
    echo "Ray head node already started..."
    sleep 10
else
    export VLLM_HOST_IP=$(hostname --ip-address)
    ray start --address "${HEAD_NODE}:${RAY_PORT}" \
        --num-cpus="${SLURM_CPUS_PER_TASK}" --num-gpus=2 --block
    sleep 5
    echo "Ray worker started!"
fi
```

### Python script

**File:** vllm_example.py

```python
from vllm import LLM

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]

# tensor_parallel_size = TOTAL GPUs across ALL nodes
llm = LLM(model="facebook/opt-125m", tensor_parallel_size=4)

outputs = llm.generate(prompts)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
```

## Tips

- **Single GPU:** Omit `tensor_parallel_size` entirely — it defaults to 1.
- **Offline mode:** Always set `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` in job scripts. Download models on the login node beforehand.
- **Model storage:** Store downloaded models in `$PROJECT` (persistent) rather than `$HOME` (limited to 50 GB). Set `HF_HOME=$PROJECT/.cache/huggingface`.
- **Multi-node:** `tensor_parallel_size` must equal the **total** number of GPUs across all nodes.
- **Ray dependency:** Multi-node inference requires installing `ray` alongside vLLM: `pip install --no-index ray`.
- **Arrow module:** Multi-node examples need the `arrow` module: `module load arrow/19`.
