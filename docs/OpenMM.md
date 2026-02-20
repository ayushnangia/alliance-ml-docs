# OpenMM

Other languages:

- English
- [français](OpenMM_fr.md)

# Introduction

OpenMM[1] is a toolkit for molecular simulation. It can be used either as a standalone application for running simulations or as a library you call from your own code. It provides a combination of extreme flexibility (through custom forces and integrators), openness, and high performance (especially on recent GPUs) that make it unique among MD simulation packages.

# Running a simulation with AMBER topology and restart files

## Preparing the Python virtual environment

This example is for the openmm/7.7.0 module.

1. Create and activate the Python virtual environment.

```
[name@server ~] module load python
[name@server ~] virtualenv $HOME/env-parmed
[name@server ~] source $HOME/env-parmed/bin/activate

```

2. Install ParmEd and netCDF4 Python modules.

```
(env-parmed)[name@server ~] pip install --no-index parmed==3.4.3 netCDF4

```

## Job submission

Below is a job script for a simulation using one GPU.

**File :** submit\_openmm.cuda.sh

```
#!/bin/bash
#SBATCH --cpus-per-task=1 
#SBATCH --gpus=1
#SBATCH --mem-per-cpu=4000M
#SBATCH --time=0-01:00:00
# Usage: sbatch $0

module purge
module load StdEnv/2020 gcc/9.3.0 cuda/11.4 openmpi/4.0.3 
module load python/3.8.10 openmm/7.7.0 netcdf/4.7.4 hdf5/1.10.6 mpi4py/3.0.3
source $HOME/env-parmed/bin/activate

python openmm_input.py

```

Here `openmm_input.py` is a Python script loading Amber files, creating the OpenMM simulation system, setting up the integration, and running dynamics. An example is available [here](https://mdbench.ace-net.ca/mdbench/idbenchmark/?q=129).

# Performance and benchmarking

A team at [ACENET](https://www.ace-net.ca/) has created a [Molecular Dynamics Performance Guide](https://mdbench.ace-net.ca/mdbench/) for Alliance clusters.
It can help you determine optimal conditions for AMBER, GROMACS, NAMD, and OpenMM jobs. The present section focuses on OpenMM performance.

OpenMM on the CUDA platform requires only one CPU per GPU because it does not use CPUs for calculations. While OpenMM can use several GPUs in one node, the most efficient way to run simulations is to use a single GPU. As you can see from [Narval benchmarks](https://mdbench.ace-net.ca/mdbench/bform/?software_contains=OPENMM.cuda&software_id=&module_contains=&module_version=&site_contains=Narval&gpu_model=&cpu_model=&arch=&dataset=6n4o) and [Cedar benchmarks](https://mdbench.ace-net.ca/mdbench/bform/?software_contains=OPENMM.cuda&software_id=&module_contains=&module_version=&site_contains=Cedar&gpu_model=V100-SXM2&cpu_model=&arch=&dataset=6n4o), on nodes with NvLink (where GPUs are connected directly), OpenMM runs slightly faster on multiple GPUs. Without NvLink there is a very little speedup of simulations on P100 GPUs ([Cedar benchmarks](https://mdbench.ace-net.ca/mdbench/bform/?software_contains=OPENMM.cuda&software_id=&module_contains=&module_version=&site_contains=Cedar&gpu_model=P100-PCIE&cpu_model=&arch=&dataset=6n4o)).

1. ↑ OpenMM home page: [https://openmm.org/](https://openmm.org/)