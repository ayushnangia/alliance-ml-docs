# OpenFOAM

Other languages:

- English
- [français](OpenFOAM_fr.md)

The [OpenFOAM](https://www.openfoam.com/) (Open Field Operation and Manipulation) CFD Toolbox is a free, open source software package for computational fluid dynamics. OpenFOAM has an extensive range of features to solve anything from complex fluid flows involving chemical reactions, turbulence and heat transfer, to solid dynamics and electromagnetics.

### Module files

To load the recent version, run

```
[name@server ~]$ module load openfoam

```

The OpenFOAM development community consists of:

- The OpenFOAM Foundation Ltd., with web sites [openfoam.org](https://openfoam.org/) and [cfd.direct](https://cfd.direct/)
- OpenCFD Ltd., with web site [openfoam.com](https://www.openfoam.com/)

Up to version 2.3.1, released in December 2014, the release histories appear to be the same. On our clusters, module names after 2.3.1 which begin with "v" are derived from the .com branch (for example, openfoam/v1706); those beginning with a digit are derived from the .org branch (for example, openfoam/4.1).

See [Using modules](Utiliser_des_modules.md) for more on module commands.

### Documentation

[OpenFOAM.com documentation](https://www.openfoam.com/documentation/) and [CFD Direct user guide](https://cfd.direct/openfoam/user-guide/).

### Usage

OpenFOAM requires substantial preparation of your environment. In order to run OpenFOAM commands (such as `paraFoam`, `blockMesh`, etc), you must load a [module file](Utiliser_des_modules.md).

Here is an example of a serial submission script for OpenFOAM 5.0:

**File :** submit.sh

```
#!/bin/bash
#SBATCH --time=00:01:00
#SBATCH --account=def-someuser

module purge
module load openfoam/12

blockMesh
icoFoam

```

Here is an example of a parallel submission script:

**File :** submit.sh

```
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --ntasks=4               # number of MPI processes
#SBATCH --mem-per-cpu=1024M      # memory; default unit is megabytes
#SBATCH --time=0-00:10           # time (DD-HH:MM)

module purge
module load openfoam/12

blockMesh
setFields
decomposePar
srun interFoam -parallel

```

Mesh preparation (`blockMesh`) may be fast enough to be done at the command line (see [Running jobs](Scheduler.md)). The solver (`icoFoam` and others) is usually the most expensive step and should always be submitted as a Slurm job except in very small test cases or tutorials.

### petscFoam solver

OpenFOAM can be compiled with the external petscFoam solver.
Our OpenFOAM modules don't include this solver but it can easily be compiled on any of our clusters.

The versions of OpenFOAM and PETSc need to be compatible. Compatible combinations are e.g.:

- `openfoam/v2412` and `petsc/3.21.6`
- `openfoam/v2312` and `petsc/3.20.0`

#### Determine compatible versions of OpenFOAM and PETSc

To check which minor release of PETSc is compatible with a particular version of OpenFOAM,
load the desired module of OpenFOAM and run the following `grep` command:

```
[name@server ~]$  module load openfoam/v2412 && grep "^petsc_version"  $EBROOTOPENFOAM/OpenFOAM*/etc/config.sh/petsc
petsc_version=petsc-3.21.2

```

This tells us that when `openfoam/v2412` was released, it was tested with PETSc 3.21.2.

We have a module for `petsc/3.21.6`, which is from the same 3.21 release branch and should
only contain bugfixes compared to 3.21.2.

#### Compile petscFoam solver

Next we need to download and extract the `external-solver-main.tar.gz` package.

```
[name@server ~]$ module load StdEnv/2023 gcc/12.3 openmpi/4.1.5 openfoam/v2412 petsc/3.21.6
[name@server ~]$ wget https://develop.openfoam.com/modules/external-solver/-/archive/main/external-solver-main.tar.gz
[name@server ~]$ tar xvfz external-solver-main.tar.gz
[name@server ~]$ cd tar xvfz external-solver-main

```

Running `./Allmake` will compile the petscFoam solver:

```
[name@server ~]$  ./Allwmake
========================================
2025-08-14 15:00:00 -0400
Starting compile of external-solver (petsc) with OpenFOAM-v2412
[...]
========================================
  Finished compile of external-solver (petsc) with OpenFOAM-v2412
  Gcc system compiler
  linux64GccDPInt32Opt, with EASYBUILDMPI eb-mpi

```

#### Confirm that petscFoam solver is functional

A few quick tests will confirm that petscFoam solver is working:

Check whether OpenFOAM can load petscFoam:

```
[name@server ~]$  foamHasLibrary -verbose petscFoam
Can load "petscFoam"

```

Check whether the dynamic library is located in `$FOAM_USER_LIBBIN`:

```
[name@server ~]$  ls $FOAM_USER_LIBBIN
libpetscFoam.so

```

Check whether `libpetscFoam.so` can find its dependencies:

```
[name@server ~]$  ldd $FOAM_USER_LIBBIN/libpetscFoam.so | grep petsc
libpetsc.so.3.21 => /cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/gcc12/openmpi4/petsc/3.21.6/lib/libpetsc.so.3.21 (0x00007f96fa800000)
 libstrumpack.so.7.2 => /cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/gcc12/openmpi4/petsc/3.21.6/lib/libstrumpack.so.7.2 (0x00007f96f8200000)
 libml.so.13 => /cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/gcc12/openmpi4/petsc/3.21.6/lib/libml.so.13 (0x00007f96fa281000)

```

### Performance

OpenFOAM can emit a lot of debugging information in very frequent small writes (e.g. hundreds per second). This may lead to poor performance on our shared filesystems. If you are in stable production and don't need the debug output, you can reduce or disable it with:

```
[name@server ~]$ mkdir -p $HOME/.OpenFOAM/$WM_PROJECT_VERSION
[name@server ~]$ cp $WM_PROJECT_DIR/etc/controlDict $HOME/.OpenFOAM/$WM_PROJECT_VERSION/

```

There are a variety of other parameters which can be used to reduce the amount of output that OpenFOAM writes to disk as well as the frequency; these run-time parameters are documented for [version 6](https://cfd.direct/openfoam/user-guide/v6-controldict/) and [version 7](https://cfd.direct/openfoam/user-guide/v7-controldict/).

For example, the `debugSwitches` dictionary in `$HOME/.OpenFOAM/$WM_PROJECT_VERSION/controlDict` can be altered to change the flags from values greater than zero to zero. Another solution would be to make use of the local scratch ($SLURM\_TMPDIR), a disk attached directly to the compute node, discussed [here](Handling_large_collections_of_files.md#Local_disk).

#### Node-local scratch

If your workflow involves the creation of many small files, you may benefit from making `$SLURM_TMPDIR` your working directory. See [Using node-local storage](Using_SLURM_TMPDIR.md) for more on this.