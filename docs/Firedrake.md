# Firedrake

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

[Firedrake](https://www.firedrakeproject.org/) is an automated system for the solution of partial differential equations using the finite element method (FEM).

Please note that every release of Firedrake requires a specific version of PETSc and several other modules or Python wheels.

# Installation

Please note that all modules must be loaded before creating and/or activating the Python virtualenv.

## Firedrake 2025.4.2

```
[name@server ~]$ module load StdEnv/2023  gcc/12.3  openmpi/4.1.5  python/3.13  mpi4py/4.0.3  symengine/0.14.0  libspatialindex/1.9.3  petsc/3.23.4
[name@server ~]$ virtualenv venv-firedrake
[name@server ~]$ source venv-firedrake/bin/activate
[name@server ~]$ pip install -U pip
[name@server ~]$ pip install --no-index  pytools==2025.2.2  immutabledict
[name@server ~]$ pip install --no-index  firedrake[check]==2025.4.2

```

The above has been tested with both `python/3.13` as well as `python/3.12`.

# Running jobs

## Firedrake 2025.4.2

**File :** job\_firedrake\_multigrid.sh

```
#!/bin/bash
#SBATCH --time=0-00:15:00  # d-hh:mm:ss
#SBATCH --ntasks=2
#SBATCH --mem-per-cpu=4000M
export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}

# Load modules
module load StdEnv/2023 gcc/12.3 openmpi/4.1.5 
module load python/3.13 mpi4py/4.0.3 
module load symengine/0.14.0 libspatialindex/1.9.3 petsc/3.23.4

# activate virtualenv
source venv-firedrake/bin/activate

# run MPI job
# example from: https://firedrakeproject.org/demos/geometric_multigrid.py
srun  python  geometric_multigrid.py

```

The above has been tested with both `python/3.13` as well as `python/3.12`.

# Optional dependencies

Firedrake has a number of [optional dependencies](https://www.firedrakeproject.org/install.html#optional-dependencies) that can be installed into the virtualenv:

- **SLEPc** and slepc4py are part of the petsc module and always available.
- **netgen**: we provide [precompiled wheels](Python.md#Available_wheels) for `ngsPETSc` and `netgen_mesher`.
- **PyTorch**: since we provide precompiled [precompiled wheels](Python.md#Available_wheels) for `torch`.
- **Jax**: since we provide precompiled [precompiled wheels](Python.md#Available_wheels) for `jax`.
- **VTK**: currently we don't have a module for VTK that supports recent enough versions of Python for Firedrake (Python 3.12 and newer).  
  As a temporary workaround VTK can be installed into the virtualenv with: `pip install --no-index --find-links ~stuekero/wheels/vtk vtk==9.4.2` until we install a new VTK module.