# VLLM

[vLLM](https://github.com/vllm-project/vllm) is a community-driven project that provides high-throughput and memory-efficient inference and serving for large language models (LLMs). It supports various decoding algorithms, quantizations, parallelism, and models from Hugging Face and other sources.

# Installation

## Latest available wheels

To see the latest version of vLLM that we have built:

```
[name@server ~]$ avail_wheels "vllm"

```

For more information, see [Available wheels](Python.md#Available_wheels).

## Installing our wheel

The preferred option is to install it using the Python [wheel](https://pythonwheels.com/) as follows:

:   1. Load dependencies, load a Python and OpenCV [modules](Utiliser_des_modules.md#Sub-command_load),

```
[name@server ~]$ module load opencv/4.11 python/3.12

```

:   2. Create and start a temporary [virtual environment](Python.md#Creating_and_using_a_virtual_environment).

```
[name@server ~]$ virtualenv --no-download ~/vllm_env
[name@server ~]$ source ~/vllm_env/bin/activate

```

:   3. Install vLLM in the virtual environment and its Python dependencies.

```
(vllm_env) [name@server ~] pip install --no-index --upgrade pip
(vllm_env) [name@server ~] pip install --no-index vllm==X.Y.Z

```

where `X.Y.Z` is the exact desired version, for instance `0.8.4`.
You can omit to specify the version in order to install the latest one available from the wheelhouse.

:   4. Freeze the environment and requirements set.

```
(vllm_env) [name@server ~] pip freeze > ~/vllm-requirements.txt

```

:   5. Deactivate the environment.

```
(vllm_env) [name@server ~] deactivate

```

:   6. Clean up and remove the virtual environment.

```
[name@server ~]$ rm -r ~/vllm_env

```

# Job submission

## Before submitting a job: Downloading models

Models loaded for inference on vLLM will typically come from the [Hugging Face Hub](https://huggingface.co/docs/hub/models-the-hub).

The following is an example of how to use the command line tool from the Hugging face to download a model. Note that models must be downloaded on a login node to avoid idle compute while waiting for resources to download. Also note that models will be cached at by default at $HOME/.cache/huggingface/hub. For more information on how to change the default cache location, as well as other means of downloading models, please see our article on the [Hugging Face ecosystem](Huggingface.md).

```
module load python/3.12
virtualenv --no-download temp_env && source temp_env/bin/activate
pip install --no-index huggingface_hub
huggingface-cli download facebook/opt-125m
rm -r temp_env

```

## Single Node

The following is an example of how to submit a job that performs inference on a model split across 2 GPUs. If your model **fits entirely inside one GPU**, change the python script below to call LLM(<model name>) without extra arguments.

This example **assumes you have pre-downloaded** the model facebook/opt-125m as described on the previous section.

**File :** vllm-example.sh

```
#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --gpus-per-task=2
#SBATCH --cpus-per-task=2  
#SBATCH --mem=32000M       
#SBATCH --time=0-00:05
#SBATCH --output=%N-%j.out

module load python/3.12 gcc opencv/4.11
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate

pip install -r vllm-requiremnts.txt --no-index

python vllm-example.py

```

**File :** vllm-example.py

```
from vllm import LLM

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]

# Set "tensor_parallel_size" to the number of GPUs in your job.

llm = LLM(model="facebook/opt-125m",tensor_parallel_size=2)

outputs = llm.generate(prompts)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

```

## Multiple Nodes

The following example revisits the single node example above, but splits the model across 4 GPUs over 2 separate nodes, i.e., 2 GPUs per node.

Currently, vLLM relies on [Ray](Ray.md) to manage splitting models over multiple nodes. The code example below contains the necessary steps to start a [multi-node Ray cluster](Ray.md#Multiple_Nodes) and run vLLM on top of it:

**File :** vllm-multinode-example.sh

```
#!/bin/bash
#SBATCH --nodes 2
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=2
#SBATCH --cpus-per-task=6  
#SBATCH --mem=32000M       
#SBATCH --time=0-00:10
#SBATCH --output=%N-%j.out

## Create a virtualenv and install Ray on all nodes ##

module load gcc python/3.12 arrow/19 opencv/4.11

srun -N $SLURM_NNODES -n $SLURM_NNODES config_env.sh

export HEAD_NODE=$(hostname --ip-address) # store head node's address
export RAY_PORT=34567 # choose a port to start Ray on the head node 

## Set Huggingface libraries to OFFLINE mode ##

export HF_HUB_OFFLINE=1 
export TRANSFORMERS_OFFLINE=1

source $SLURM_TMPDIR/ENV/bin/activate

## Start Ray cluster Head Node ##
ray start --head --node-ip-address=$HEAD_NODE --port=$RAY_PORT --num-cpus=$SLURM_CPUS_PER_TASK --num-gpus=2 --block &
sleep 10

## Launch worker nodes on all the other nodes allocated by the job ##
srun launch_ray.sh &
ray_cluster_pid=$!
sleep 10

VLLM_HOST_IP=`hostname --ip-address` python vllm_example.py

## Shut down Ray worker nodes after the Python script exits ##
kill $ray_cluster_pid

```

Where the script `config_env.sh` is:

**File :** config\_env.sh

```
#!/bin/bash

module load python/3.12 gcc opencv/4.11 arrow/19

virtualenv --no-download $SLURM_TMPDIR/ENV

source $SLURM_TMPDIR/ENV/bin/activate

pip install --upgrade pip --no-index

pip install ray -r vllm-requirements.txt --no-index

deactivate

```

The script `launch_ray.sh` is:

**File :** launch\_ray.sh

```
#!/bin/bash

if [[ "$SLURM_PROCID" -eq "0" ]]; then
        echo "Ray head node already started..."
        sleep 10

else
        export VLLM_HOST_IP=`hostname --ip-address`
        ray start --address "${HEAD_NODE}:${RAY_PORT}" --num-cpus="${SLURM_CPUS_PER_TASK}" --num-gpus=2 --block
        sleep 5
        echo "ray worker started!"
fi

```

And finally, the script vllm\_example.py is:

**File :** vllm\_example.py

```
from vllm import LLM

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]

# Set "tensor_parallel_size" to the TOTAL number of GPUs on all nodes.

llm = LLM(model="facebook/opt-125m",tensor_parallel_size=4)

outputs = llm.generate(prompts)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

```