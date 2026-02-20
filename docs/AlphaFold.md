# AlphaFold3

Other languages:

- English
- [français](AlphaFold3_fr.md)

This page discusses how to use AlphaFold v3.0.

Source code and documentation for AlphaFold3 can be found at their [GitHub page](https://github.com/google-deepmind/alphafold3).
Any publication that discloses findings arising from use of this source code or the model parameters should [cite](https://github.com/google-deepmind/alphafold3#citing-this-work) the [AlphaFold3 paper](https://doi.org/10.1038/s41586-024-07487-w).

## Available versions

AlphaFold3 is available on our clusters as prebuilt Python packages (wheels). You can list available versions with `avail_wheels`.

```
[name@server ~]$ avail_wheels alphafold3

```

AlphaFold2 is still available. Documentation is [here](AlphaFold2.md).

## Creating a requirements file for AlphaFold3

1. Load AlphaFold3 dependencies.

```
[name@server ~]$ module load StdEnv/2023 hmmer/3.4 rdkit/2024.03.5 python/3.12

```

2. Download run script.

3.0.13.0.0

```
[name@server ~]$ wget https://raw.githubusercontent.com/google-deepmind/alphafold3/refs/tags/v3.0.1/run_alphafold.py

```

```
[name@server ~]$ wget https://raw.githubusercontent.com/google-deepmind/alphafold3/23e3d46d4ca126e8731e8c0cbb5673e9a848ceb5/run_alphafold.py

```

3. Create and activate a Python virtual environment.

```
[name@server ~]$ virtualenv --no-download ~/alphafold3_env
[name@server ~]$ source ~/alphafold3_env/bin/activate

```

4. Install a specific version of AlphaFold3 and its Python dependencies.

```
(alphafold3_env) [name@server ~] pip install --no-index --upgrade pip
(alphafold3_env) [name@server ~] pip install --no-index alphafold3==X.Y.Z

```

where `X.Y.Z` is the exact desired version, for instance `3.0.0`.
You can omit to specify the version in order to install the latest one available from the wheelhouse.

5. Build data.

```
(alphafold3_env) [name@server ~] build_data

```

This will create data files inside your virtual environment.

6. Validate it.

```
(alphafold3_env) [name@server ~] python run_alphafold.py --help

```

7. Freeze the environment and requirements set.

```
(alphafold3_env) [name@server ~] pip freeze > ~/alphafold3-requirements.txt

```

8. Deactivate the environment.

```
(alphafold3_env) [name@server ~] deactivate

```

9. Clean up and remove the virtual environment.

```
[name@server ~]$ rm -r ~/alphafold3_env

```

The virtual environment will be created in your job instead.

## Model

You can obtain the model by requesting it from Google. They aim to respond to requests within 2-3 business days.
Please see [Obtaining Model Parameters](https://github.com/google-deepmind/alphafold3?tab=readme-ov-file).

## Databases

Note that AlphaFold3 requires a set of databases.

**Important:** The databases must live in the `$SCRATCH` directory.

1. Download the fetch script

```
[name@server ~]$ wget https://raw.githubusercontent.com/google-deepmind/alphafold3/refs/heads/main/fetch_databases.sh

```

2. Download the databases

```
[name@server ~]$ mkdir -p $SCRATCH/alphafold/dbs
[name@server ~]$ bash fetch_databases.sh $SCRATCH/alphafold/dbs

```

## Running AlphaFold3 in stages

Alphafold3 must be run in [stages](https://github.com/google-deepmind/alphafold3/blob/main/docs/performance.md#running-the-pipeline-in-stages), that is:

1. Splitting the CPU-only data pipeline from model inference (which requires a GPU), to optimise cost and resource usage.
2. Caching the results of MSA/template search, then reusing the augmented JSON for multiple different inferences across seeds or across variations of other features (e.g. a ligand).

For reference on Alphafold3:

- see [inputs](https://github.com/google-deepmind/alphafold3/blob/main/docs/input.md)
- see [outputs](https://github.com/google-deepmind/alphafold3/blob/main/docs/output.md)
- see [performance](https://github.com/google-deepmind/alphafold3/blob/main/docs/performance.md)

### 1. Data pipeline (CPU)

Edit the following submission script according to your needs.

**File :** alphafold3-data.sh

```
#!/bin/bash

#SBATCH --job-name=alphafold3-data
#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=08:00:00           # adjust this to match the walltime of your job
#SBATCH --cpus-per-task=8         # a MAXIMUM of 8 core, AlphaFold has no benefit to use more
#SBATCH --mem=64G                 # adjust this according to the memory you need

# Load modules dependencies.
module load StdEnv/2023 hmmer/3.4 rdkit/2024.03.5 python/3.12

DOWNLOAD_DIR=$SCRATCH/alphafold/dbs    # set the appropriate path to your downloaded data
INPUT_DIR=$SCRATCH/alphafold/input     # set the appropriate path to your input data
OUTPUT_DIR=$SLURM_TMPDIR/alphafold/output   # set the appropriate path to your output data

# Generate your virtual environment in $SLURM_TMPDIR.
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate

# Install AlphaFold and its dependencies.
pip install --no-index --upgrade pip
pip install --no-index --requirement ~/alphafold3-requirements.txt

# build data in $VIRTUAL_ENV
build_data

# https://github.com/google-deepmind/alphafold3/blob/main/docs/performance.md#compilation-time-workaround-with-xla-flags
export XLA_FLAGS="--xla_gpu_enable_triton_gemm=false"

# Edit with the proper arguments and run your commands.
# run_alphafold.py --help
python run_alphafold.py \
    --db_dir=$DOWNLOAD_DIR \
    --input_dir=$INPUT_DIR \
    --output_dir=$OUTPUT_DIR \
    --jax_compilation_cache_dir=$HOME/.cache \
    --nhmmer_n_cpu=$SLURM_CPUS_PER_TASK \
    --jackhmmer_n_cpu=$SLURM_CPUS_PER_TASK \
    --norun_inference  # Run data stage

# copy back
mkdir $SCRATCH/alphafold/output
cp -vr $OUTPUT_DIR $SCRATCH/alphafold/output

```

### 2. Model inference

Edit the following submission script according to your needs.

Compatibility

Alphafold3 **only** support compute capability 8.0 or greater, that is **A100s or greater**.

**File :** alphafold3-inference.sh

```
#!/bin/bash

#SBATCH --job-name=alphafold3-inference
#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=08:00:00           # adjust this to match the walltime of your job
#SBATCH --cpus-per-task=1         # AlphaFold has no benefit to use more for the inference stage
#SBATCH --gpus=a100:1             # Alphafold3 inference only runs on ONE A100 or greater.
#SBATCH --mem=20G                 # adjust this according to the memory you need

# Load modules dependencies.
module load StdEnv/2023 hmmer/3.4 rdkit/2024.03.5 python/3.12 cuda/12.2 cudnn/9.2

DOWNLOAD_DIR=$SCRATCH/alphafold/dbs    # set the appropriate path to your downloaded data
INPUT_DIR=$SCRATCH/alphafold/input     # set the appropriate path to your input data, following the data stage.
OUTPUT_DIR=$SCRATCH/alphafold/output   # set the appropriate path to your output data

# Generate your virtual environment in $SLURM_TMPDIR.
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate

# Install AlphaFold and its dependencies.
pip install --no-index --upgrade pip
pip install --no-index --requirement ~/alphafold3-requirements.txt

# build data in $VIRTUAL_ENV
build_data

# https://github.com/google-deepmind/alphafold3/blob/main/docs/performance.md#compilation-time-workaround-with-xla-flags
export XLA_FLAGS="--xla_gpu_enable_triton_gemm=false"

# https://github.com/google-deepmind/alphafold3/blob/main/docs/performance.md#gpu-memory
export XLA_PYTHON_CLIENT_PREALLOCATE=true
export XLA_CLIENT_MEM_FRACTION=0.95

# Edit with the proper arguments and run your commands.
# run_alphafold.py --help
python run_alphafold.py \
    --db_dir=$DOWNLOAD_DIR \
    --input_dir=$INPUT_DIR \
    --output_dir=$OUTPUT_DIR \
    --jax_compilation_cache_dir=$HOME/.cache \
    --norun_data_pipeline  # Run inference stage

```

### 3. Job submission

Then, submit the jobs to the scheduler.

#### Independent jobs

```
[name@server ~]$ sbatch alphafold3-data.sh

```

Wait until it complete, then submit the second stage:

```
[name@server ~]$ sbatch alphafold3-inference.sh

```

#### Dependent jobs

```
[name@server ~]$ jid1=$(sbatch alphafold3-data.sh)
[name@server ~]$ jid2=$(sbatch --dependency=afterok:$jid1 alphafold3-inference.sh)
[name@server ~]$ sq

```

If the first stage fails, you will have to manually cancel the second stage:

```
[name@server ~]$ scancel -u $USER -n alphafold3-inference

```

## Troubleshooting

### Out of memory (GPU)

If you would like to run AlphaFold3 on inputs larger than 5,120 tokens, or on a GPU with less memory (an A100 with 40 GB of memory, for instance), you can enable [unified memory](https://github.com/google-deepmind/alphafold3/blob/main/docs/performance.md#unified-memory)

In your submission script for the inference stage, add these environment variables:

```
export XLA_PYTHON_CLIENT_PREALLOCATE=false
export TF_FORCE_UNIFIED_MEMORY=true
export XLA_CLIENT_MEM_FRACTION=2.0  # 2 x 40GB = 80 GB

```

and adjust the amount of memory allocated to your job accordingly, for instance: `#SBATCH --mem=80G`