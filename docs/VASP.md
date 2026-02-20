# VASP

Outdated

**This page or section contains obsolete information and some statements may not be valid.** The technical documentation is currently being updated by our support team.

Other languages:

- English
- [français](VASP_fr.md)

:   *The Vienna ab initio Simulation Package (VASP) is a computer program for atomic scale materials modelling, e.g. electronic structure calculations and quantum mechanical molecular dynamics, from first principles.*
:   Reference: [VASP website](https://www.vasp.at/)

## Licensing

VASP can only be used by research groups that have been licensed by the developers, VASP Software GmbH. Your PI (principal investigator, professor) must register at the [VASP website](https://www.vasp.at/) and obtain a license.

Once you have a license, if you wish to use the prebuilt VASP binaries on [Fir](Fir.md), [Nibi](Nibi.md), or [Trillium](Trillium.md), contact [Technical support](Technical_Support.md) requesting access to VASP with the following information:

- Include license holder (your PI) information:
  - Name
  - Email address
  - Department and institution (university)
- Include license information:
  - Version of the VASP license (**VASP version 4 or version 5**)
  - **License number**
  - Provide an updated list of who is allowed to use your VASP license. For example, forward to us the most recent email from the VASP license administrator that contains the list of licensed users.

If you are licensed for version 5 you may also use version 4, but a version 4 license does not permit you to use version 5. The same for version 6, if you are licensed for version 6 you may also use versions 5 and 4.

You may also choose to install VASP yourself, according to the terms of your license. See Building VASP yourself below.

### Why?

VASP Software GmbH will only grant licenses to groups that are hired by a single legal entity, which is incompatible with the way we operate. We have tried to negotiate an agreement with the licensor which would let us install the software everywhere on our infrastructure, but without success. Please read the terms of your own license, as you are likely subject to the same restriction. This limits the support we can offer to users who need help installing the software.

Simon Fraser University, the University of Waterloo, and the University of Toronto own Fir, Nibi, and Trillium, respectively, and have licenses with VASP. Some of their employees are therefore allowed to install specific versions of VASP on those clusters and provide limited support.

## Using prebuilt VASP

To load prebuilt VASP on [Fir](Fir.md) and [Nibi](Nibi.md), please do the following:

For **vasp/5.4.4**

```
module load StdEnv/2023  intel/2023.2.1 intelmpi/2021.9.0
module load vasp/5.4.4

```

For **vasp/6.4.2**

```
module load StdEnv/2023 intel/2023.2.1 intelmpi/2021.9.0
module load vasp/6.4.2

```

1. Run `module spider vasp` to see which versions are available.
2. Choose your version and run `module spider vasp/<version>` to see which dependencies you need to load for this particular version.
3. Load the dependencies and the VASP module, for example:

```
module load StdEnv/2023 intel/2023.2.1 intelmpi/2021.9.0
module load vasp/6.4.2

```

See [Using modules](Utiliser_des_modules.md) for more information.

To use VASP on [Trillium](Trillium.md), modules may be loaded as follows:

For **vasp/5.4.4**

```
module load StdEnv/2023 intel/2023.2.1 intelmpi/2021.9.0 
module load imkl/2023.2.0 
module use /opt/software/commercial/modules 
module load vasp/5.4.4

```

For **vasp/6.4.2**

```
module load StdEnv/2023 intel/2023.2.1 intelmpi/2021.9.0 hdf5/1.14.2
module use /opt/software/commercial/modules
module load vasp/6.4.2

```

For general usage of Trillium, please see the [Trillium Quickstart](Trillium_Quickstart.md) page.

### Pseudopotential files

All pseudopotentials have been downloaded from the official VASP website and untarred. They are all located in  `$EBROOTVASP/pseudopotentials/` on Cedar and Graham and can be accessed once the VASP module is loaded.

### Executable programs

**For VASP-4.6**, executable files are:

- `vasp` for standard NVT calculations with non gamma k points
- `vasp-gamma` for standard NVT calculations with only gamma points
- `makeparam` to estimate how much memory is required to run VASP for a particular cluster

**For VASP-5.4.1, 5.4.4 and 6.1.0 (without CUDA support)**, executable files are:

- `vasp_std` for standard NVT calculations with non gamma k points
- `vasp_gam` for standard NVT calculations with only gamma points
- `vasp_ncl` for NPT calculations with non gamma k points

**For VASP-5.4.4 and 6.1.0 (with CUDA support)**, executable files are:

- `vasp_gpu` for standard NVT calculations with gamma and non gamma k points
- `vasp_gpu_ncl` for NPT calculations with gamma and non gamma k points

Two extensions have also been incorporated:

- [Transition State Tools](http://theory.cm.utexas.edu/vtsttools/)
- [VASPsol](https://github.com/henniggroup/VASPsol)

If you need a version of VASP that does not appear here, you can either build it yourself (see below) or [write to us](Technical_Support.md) and ask that it be built and installed.

## Vasp-GPU

[![](/mediawiki/images/thumb/9/98/VASP_benchmark_ENG.png/400px-VASP_benchmark_ENG.png)](FileVASP_benchmark_ENGpng.md)

Fig.1 Simulation time as a function of the number of CPUs for GPU=0, 1, and 2

Vasp-GPU executable files run on both GPUs and CPUs of a node. Basically, calculation on a GPU is much more expensive than on a CPU, therefore we highly recommend to perform a benchmark using one or 2 GPUs to make sure they are getting a maximum performance from the GPU use. Fig.1 shows a benchmark of Si crystal which contains 256 Si-atoms in the simulation box. Blue, black and red lines show simulation time as a function of Number of CPU for GPU=0, 1, and 2 respectively. It shows the performance for GPU=1,2 and CPU=1 is more than 5 times better compared to GPU=0 and CPU=1. However, a comparison of calculations with GPU=1 and GPU=2 indicates that there is not much performance gain from GPU=1 to GPU=2. In fact, use for GPU=2 is around 50% in our monitoring system. Therefore we recommend users to first perform a benchmark like this for their own system to make sure they are not wasting any computer resources.

## Example of a VASP job script

The following is a job script to run VASP in parallel using the Slurm job scheduler:

**File :** vasp\_job.sh

```
#!/bin/bash
#SBATCH --account=<ACCOUNT>
#SBATCH --ntasks=4             # number of MPI processes
#SBATCH --mem-per-cpu=1024M    # memory
#SBATCH --time=0-00:05         # time (DD-HH:MM)
module load intel/2020.1.217  intelmpi/2019.7.217 vasp/<VERSION>
mpirun <VASP>

```

- The above job script requests four CPU cores and 4096MB memory (4x1024MB).
- <ACCOUNT> is a Slurm account name; see [Accounts and projects](Scheduler.md#Accounts_and_projects) to know what to enter there.
- <VERSION> is the number for the VASP version you want to use: 4.6, 5.4.1, 5.4.4 or 6.1.0.
- Use module spider vasp/<VERSION> to see how you can change this particular version.
- <VASP> is the name of the executable. Refer to section *Executable programs* above for the executables you can select for each version.

**File :** vasp\_gpu\_job.sh

```
#!/bin/bash
#SBATCH --account=<ACCOUNT>
#SBATCH --cpus-per-task=1      # number of CPU processes
#SBATCH --gres=gpu:p100:1      # Number of GPU type:p100 (valid type only for cedar)
#SBATCH --mem=3GB              # memory
#SBATCH --time=0-00:05         # time (DD-HH:MM)
module load intel/2020.1.217  cuda/11.0  openmpi/4.0.3 vasp/<VERSION>
mpirun <VASP>

```

- The above job script requests one CPU core and 1024MB memory.
- The above job script requests one GPU type p100 which is only available on Cedar. For other clusters, please see the [GPU types available](Using_GPUs_with_SLURM.md#Available_hardware).
- The above job uses `srun` to run VASP.

VASP uses four input files named as INCAR, KPOINTS, POSCAR, POTCAR. It is best to prepare VASP input files in a separate directory for each job. To submit the job from that directory, use:

```
sbatch vasp_job.sh

```

If you do not know how much memory you need for your job, prepare all your input files and then run `makeparam` in an [interactive job submission](Scheduler.md#Interactive_jobs). Then use the result as required memory for the next run. However, for a more accurate estimate for future jobs, check the maximum stack size used by [completed jobs](Scheduler.md#Completed_jobs) and use this as the memory requirement per processor for the next job.

If you want to use 32 or more cores, please read about [whole-node scheduling](Job_scheduling.md#Whole_nodes_versus_cores).

## Building VASP yourself

If you are licensed to use VASP and have access to VASP source code, you can install various versions of VASP in your /home directory on all our clusters using the following [EasyBuild](EasyBuild.md) commands.

`eb -f [RECIPE NAME] --sourcepath=[SOURCEPATH]`

where [SOURCEPATH] is the directory containing the VASP source code and [RECIPE NAME] is the name of the recipe. The first tab of table bellow shows the list of available recipes along with the corresponding required source files. In this table VTSTtools and vaspSOL are Transition State Tools and VASPsol extensions respectively. Second tabs of this table shows the list of the libraries that are included to vasp. You may download the source code from the [VASP website](https://www.vasp.at/). Running the command will take some time, perhaps more than an hour. Once it is done, you will be able to load and run VASP using `module` commands just as explained above in Using prebuilt VASP.

Alternatively to build a custom version of VASP, please see [Installing software in your home directory](Installing_software_in_your_home_directory.md) and
[Installing VASP 5](https://www.vasp.at/wiki/index.php/Installing_VASP.5.X.X) or [Installing VASP 6](https://www.vasp.at/wiki/index.php/Installing_VASP.6.X.X).

Recipe specification and implementationIncluded Libraries

| Recipe Name | Version | Environment | Source file | CPU/GPU | VTSTtools | vaspSOL |
| --- | --- | --- | --- | --- | --- | --- |
| VASP-5.4.4-iimpi-2020a.eb | 5.4.4 | StdEnv/2023 | vasp.5.4.4.pl2.tgz | CPU | yes | yes |
| VASP-6.1.2-iimpi-2020a.eb | 6.1.2 | StdEnv/2020 | vasp.6.1.2_patched.tgz | CPU | yes | yes |
| VASP-6.2.1-iimpi-2020a.eb | 6.2.1 | StdEnv/2020 | vasp.6.2.1.tgz | CPU | yes | yes |
| VASP-6.3.0-iimpi-2020a.eb | 6.3.0 | StdEnv/2020 | vasp.6.3.0.tgz | CPU | yes | yes |
| VASP-6.3.1-iimpi-2020a.eb | 6.3.1 | StdEnv/2020 | vasp.6.3.1.tgz | CPU | yes | yes |
| VASP-6.4.2-iimpi-2023a.eb | 6.4.2 | StdEnv/2023 | vasp.6.4.2.tar | CPU | yes | yes |
| VASP-6.4.3-iimpi-2023a.eb | 6.4.3 | StdEnv/2023 | vasp.6.4.3.tar | CPU | yes | yes |
| VASP-6.5.0-iimpi-2023a.eb | 6.5.0 | StdEnv/2023 | vasp.6.5.0.tgz | CPU | No | No |
| VASP-6.5.1-iimpi-2023a.eb | 6.5.1 | StdEnv/2023 | vasp.6.5.1.tgz | CPU | No | No |

| Recipe Name | Wannier Function | Beef | HDF5 | LibXC | ELPA | Libmbd | dft4 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VASP-5.4.4-iimpi-2020a.eb | Yes | Yes | No | No | No | No | No |
| VASP-6.1.2-iimpi-2020a.eb | Yes | Yes | No | No | No | No | No |
| VASP-6.2.1-iimpi-2020a.eb | Yes | Yes | No | No | No | No | No |
| VASP-6.3.0-iimpi-2020a.eb | Yes | Yes | Yes | Yes | No | No | No |
| VASP-6.3.1-iimpi-2020a.eb | Yes | Yes | Yes | Yes | No | No | No |
| VASP-6.4.2-iimpi-2023a.eb | Yes | Yes | Yes | Yes | No | No | No |
| VASP-6.4.3-iimpi-2023a.eb | Yes | Yes | Yes | Yes | No | No | Yes |
| VASP-6.5.0-iimpi-2023a.eb | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| VASP-6.5.1-iimpi-2023a.eb | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

# External links

- [Getting Started](https://www.vasp.at/tutorials/latest/part1/) guide from the developers' Web site.
- [py4vasp](https://www.vasp.at/py4vasp/latest/) is a Python interface to extract data from VASP calculations.