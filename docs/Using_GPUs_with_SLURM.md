# Using GPUs with Slurm

Other languages:

- English
- [français](Using_GPUs_with_Slurm_fr.md)

# Introduction

To request one or more GPUs for a [Slurm](Scheduler.md) job, use this form:

```
 --gpus-per-node=<model_specifier>:<number>

```

For example:

```
 --gpus-per-node=a100:1

```

This requests a single A100 GPU (unless you also use `--nodes` to specify more than a single node).
See the following section, *Available GPUs,* for valid model specifiers.

The following form can also be used:

```
 --gres=gpu:<model_specifier>:<number>

```

This form may not be supported in the future. We recommend that you replace it in your scripts with `--gpus-per-node`.

Slurm supports a variety of other directives that you can use to request GPU resources: `--gpus`, `--gpus-per-socket`, `--gpus-per-task`, `--mem-per-gpu`, and `--ntasks-per-gpu`. Please see the Slurm documentation for [sbatch](https://slurm.schedmd.com/sbatch.html) for more about these. Our staff do not test all of these; if you try one but don't get the result you expect, [contact technical support](Technical_Support.md).

For general advice on job scheduling, see [Running jobs](Scheduler.md).

# Available GPUs

The following table summarizes the available GPU models and their corresponding specifiers:

| Cluster | GPU model | Model specifiers for Slurm | Notes |
| --- | --- | --- | --- |
| Fir | H100-80gb | h100 |  |
| nvidia_h100_80gb_hbm3_1g.10gb | MIG |
| nvidia_h100_80gb_hbm3_2g.20gb | MIG |
| nvidia_h100_80gb_hbm3_3g.40gb | MIG |
| Narval | A100-40gb | a100 |  |
| a100_1g.5gb | MIG |
| a100_2g.10gb | MIG |
| a100_3g.20gb | MIG |
| a100_4g.20gb | MIG |
| Nibi | H100-80gb | h100 |  |
| nvidia_h100_80gb_hbm3_1g.10gb | MIG |
| nvidia_h100_80gb_hbm3_2g.20gb | MIG |
| nvidia_h100_80gb_hbm3_3g.40gb | MIG |
| MI300A-128gb | (none; see Nibi ) |  |
| Rorqual | H100-80gb | h100 |  |
| nvidia_h100_80gb_hbm3_1g.10gb | MIG; synonyms h100_1g.10gb, h100_1.10, h100_10gb |
| nvidia_h100_80gb_hbm3_2g.20gb | MIG; synonyms h100_2g.20gb, h100_2.20, h100_20gb |
| nvidia_h100_80gb_hbm3_3g.40gb | MIG; synonyms h100_3g.40gb, h100_3.40, h100_40gb |
| Trillium | H100-80gb | h100 |  |
| Killarney | H100-80gb | h100 |  |
| L40S-48gb | l40s |  |
| tamIA | H100-80gb | h100 |  |
| H200 | h200 |  |
| Vulcan | L40S-48gb | l40s |  |

GPU model specifiers (including MIG specifiers) available on any given cluster can be obtained from Slurm with the following command.
This may be useful if the table above has not been updated with the latest changes.

```
[name@server ~]$ sinfo -o "%G"|grep gpu|sed 's/gpu://g'|sed 's/),/\n/g'|cut -d: -f1|sort|uniq

```

There are short synonyms available for some of the MIG specifiers at certain sites; this command will not provide those synonyms.
Also, the presence of a GPU model does not guarantee that you will be able to use one of the corresponding specifiers in your jobs; there may be
further restrictions on what model specifiers are available based on (for example) which research group you belong.
For further information see the site-specific page by clicking on the cluster name in the above table, or [contact support](Technical_Support.md).

If you do not supply a model specifier your job may be rejected or it may be sent to an arbitrary GPU instance.
There are very few programs which can use an arbitrary GPU efficiently,
so we strongly recommend that you always provide a specific GPU model specifier in your job scripts.

There are GPUs available at Arbutus, but like other cloud resources they cannot be scheduled via Slurm.
See [Cloud resources](Cloud_resources.md) for more details.

## Multi-Instance GPUs (MIGs)

MIG is a technology that partitions a GPU into multiple instances.
Your jobs might be able to use a MIG instance instead of a whole GPU.
Please see [Multi-Instance\_GPU](Multi-Instance_GPU.md) for more about this.

# Requesting CPU cores and system memory

Along with each GPU instance, your job should have a number of CPU cores (default is `1`) and some amount of system memory. The recommended maximum numbers of CPU cores and gigabytes of system memory per GPU instance are listed in the [table of bundle characteristics](Allocations_and_compute_scheduling.md#Ratios_in_bundles).

# Examples

## Single-core job

If you need only a single CPU core and one GPU:

**File :** gpu\_serial\_job.sh

```
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:1
#SBATCH --mem=4000M               # memory per node
#SBATCH --time=0-03:00
./program                         # you can use 'nvidia-smi' for a test

```

## Multi-threaded job

For a GPU job which needs multiple CPUs in a single node:

**File :** gpu\_threaded\_job.sh

```
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:1 
#SBATCH --cpus-per-task=6         # CPU cores or threads
#SBATCH --mem=4000M               # memory per node
#SBATCH --time=0-03:00
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
./program

```

For each GPU requested, we recommend

- on Fir, no more than 12 CPU cores;
- on Narval, no more than 12 CPU cores
- on Nibi, no more than 14 CPU cores,
- on Rorqual, no more than 16 CPU cores

## MPI job

**File :** gpu\_mpi\_job.sh

```
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus=a100:8             # total number of GPUs
#SBATCH --ntasks-per-gpu=1        # total of 8 MPI processes
#SBATCH --cpus-per-task=6         # CPU cores per MPI process
#SBATCH --mem-per-cpu=5G          # host memory per CPU core
#SBATCH --time=0-03:00            # time (DD-HH:MM)
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
srun --cpus-per-task=$SLURM_CPUS_PER_TASK ./program

```

## Whole nodes

If your application can efficiently use an entire node and its associated GPUs, you will probably experience shorter wait times if you ask Slurm for a whole node. Use one of the following job scripts as a template.

### Packing single-GPU jobs within one SLURM job

If you need to run four single-GPU programs or two 2-GPU programs for longer than 24 hours, [GNU Parallel](GNU_Parallel.md) is recommended. A simple example is:

```
cat params.input | parallel -j4 'CUDA_VISIBLE_DEVICES=$(({%} - 1)) python {} &> {#}.out'

```

In this example, the GPU ID is calculated by subtracting 1 from the slot ID {%} and {#} is the job ID, starting from 1.

A `params.input` file should include input parameters in each line, like this:

```
code1.py
code2.py
code3.py
code4.py
...

```

With this method, you can run multiple tasks in one submission. The `-j4` parameter means that GNU Parallel can run a maximum of four concurrent tasks, launching another as soon as one ends. CUDA\_VISIBLE\_DEVICES is used to ensure that two tasks do not try to use the same GPU at the same time.

## Profiling GPU tasks

On [Narval](Narval.md) and [Rorqual](Rorqual.md), profiling is possible but requires disabling the
[NVIDIA Data Center GPU Manager (DCGM)](https://developer.nvidia.com/dcgm). This must be done during job submission by setting the `DISABLE_DCGM` environment variable:

```
[name@server ~]$ DISABLE_DCGM=1 salloc --account=def-someuser --gpus-per-node=a100:1 --mem=4000M --time=03:00

```

Then, in your interactive job, wait until DCGM is disabled on the node:

```
[name@server ~]$ while [ ! -z "$(dcgmi -v | grep 'Hostengine build info:')" ]; do  sleep 5; done

```

Finally, launch your profiler. For more details on profilers, see [Debugging and profiling](Debugging_and_profiling.md).

On Fir and Nibi, GPU profiling like the above technique is not available yet.

# See also

[CUDA](CUDA.md)  
[Multi-Instance GPU](Multi-Instance_GPU.md)  
[Running jobs](Scheduler.md)