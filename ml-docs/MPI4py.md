# MPI4py

Other languages:

- English
- [français](MPI4py_fr.md)

[MPI for Python](https://mpi4py.readthedocs.io/en/stable/) provides Python bindings for the Message Passing Interface (MPI) standard, allowing Python applications to exploit multiple processors on workstations, clusters and supercomputers.

# Available versions

`mpi4py` is available as a module, and not from the [wheelhouse](Wheels.md) as typical Python packages are.
You can find available version with

```
[name@server ~]$ module spider mpi4py

```

and look for more information on a specific version with

```
[name@server ~]$ module spider mpi4py/X.Y.Z

```

where `X.Y.Z` is the exact desired version, for instance `4.0.0`.

# Famous first words: Hello World

1. Run a short [interactive job](Scheduler.md#Interactive_jobs).

```
[name@server ~]$ salloc --account=<your account> --ntasks=5

```

2. Load the module.

```
[name@server ~]$ module load mpi4py/4.0.0 python/3.12

```

3. Run a Hello World test.

```
[name@server ~]$ srun python -m mpi4py.bench helloworld
Hello, World! I am process 0 of 5 on node1.
Hello, World! I am process 1 of 5 on node1.
Hello, World! I am process 2 of 5 on node3.
Hello, World! I am process 3 of 5 on node3.
Hello, World! I am process 4 of 5 on node3.

```

In the case above, two nodes (`node1` and `node3`) were allocated, and the jobs were distributed across the available resources.

# mpi4py as a package dependency

Often `mpi4py` is a dependency of another package. In order to fulfill this dependency :

1. Deactivate any Python virtual environment.

```
[name@server ~]$ test $VIRTUAL_ENV && deactivate

```

**Note:** If you had a virtual environment activated, it is important to deactivate it first, then load the module, before reactivating your virtual environment.

2. Load the module.

```
[name@server ~]$ module load mpi4py/4.0.0 python/3.12

```

3. Check that it is visible by `pip`

```
[name@server ~]$ pip list | grep mpi4py
mpi4py            4.0.0

```

and is accessible for your currently loaded python module.

```
[name@server ~]$ python -c 'import mpi4py'

```

If no errors are raised, then everything is OK!

4. [Create a virtual environment and install your packages](Python.md#Creating_and_using_a_virtual_environment).

# Running jobs

You can run mpi jobs distributed across multiple nodes or cores.
For efficient MPI scheduling, please see:

- [MPI job](Scheduler.md#MPI_job)
- [Advanced MPI scheduling](Advanced_MPI_scheduling.md)

## CPU

1. Write your python code, for instance, broadcasting a numpy array.

**File :** "mpi4py-np-bc.py"

```
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = np.arange(100, dtype='i')
else:
    data = np.empty(100, dtype='i')

comm.Bcast(data, root=0)

for i in range(100):
    assert data[i] == i

```

The example above is based on the [mpi4py tutorial](https://mpi4py.readthedocs.io/en/stable/tutorial.html#running-python-scripts-with-mpi).

2. Write your submission script.

DistributedWhole nodes

**File :** submit-mpi4py-distributed.sh

```
#!/bin/bash

#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=08:00:00           # adjust this to match the walltime of your job
#SBATCH --ntasks=4                # adjust this to match the number of tasks/processes to run
#SBATCH --mem-per-cpu=4G          # adjust this according to the memory you need per process

# Run on cores across the system : https://docs.alliancecan.ca/wiki/Advanced_MPI_scheduling#Few_cores,_any_number_of_nodes

# Load modules dependencies.
module load StdEnv/2023 gcc mpi4py/4.0.0 python/3.12

# create the virtual environment on each allocated node: 
srun --ntasks $SLURM_NNODES --tasks-per-node=1 bash << EOF
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate

pip install --no-index --upgrade pip
pip install --no-index numpy==2.1.1
EOF

# activate only on main node
source $SLURM_TMPDIR/env/bin/activate;

# srun exports the current env, which contains $VIRTUAL_ENV and $PATH variables
srun python mpi4py-np-bc.py;

```

**File :** submit-mpi4py-whole-nodes.sh

```
#!/bin/bash

#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=01:00:00           # adjust this to match the walltime of your job
#SBATCH --nodes=2                 # adjust this to match the number of whole node
#SBATCH --ntasks-per-node=40      # adjust this to match the number of tasks/processes to run per node
#SBATCH --mem-per-cpu=1G          # adjust this according to the memory you need per process

# Run on N whole nodes : https://docs.alliancecan.ca/wiki/Advanced_MPI_scheduling#Whole_nodes

# Load modules dependencies.
module load StdEnv/2023 gcc openmpi mpi4py/4.0.0 python/3.12

# create the virtual environment on each allocated node: 
srun --ntasks $SLURM_NNODES --tasks-per-node=1 bash << EOF
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate

pip install --no-index --upgrade pip
pip install --no-index numpy==2.1.1
EOF

# activate only on main node
source $SLURM_TMPDIR/env/bin/activate;

# srun exports the current env, which contains $VIRTUAL_ENV and $PATH variables
srun python mpi4py-np-bc.py;

```

3. Test your script.

Before submitting your job, it is important to test that your submission script will start without errors. You can do a quick test in an [interactive job](Scheduler.md#Interactive_jobs).

4. Submit your job to the scheduler.

```
[name@server ~]$ sbatch submit-mpi4py-distributed.sh

```

## GPU

1. From a login node, download the demo example.

```
[name@server ~]$ wget https://raw.githubusercontent.com/mpi4py/mpi4py/refs/heads/master/demo/cuda-aware-mpi/use_cupy.py

```

The example above and others, can be found in the [demo folder](https://github.com/mpi4py/mpi4py/tree/master/demo).

2. Write your submission script.

**File :** submit-mpi4py-gpu.sh

```
#!/bin/bash

#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=08:00:00           # adjust this to match the walltime of your job
#SBATCH --ntasks=2                # adjust this to match the number of tasks/processes to run
#SBATCH --mem-per-cpu=2G          # adjust this according to the memory you need per process
#SBATCH --gpus=1

# Load modules dependencies.
module load StdEnv/2023 gcc cuda/12 mpi4py/4.0.0 python/3.11

# create the virtual environment on each allocated node:
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate

pip install --no-index --upgrade pip
pip install --no-index cupy numba

srun python use_cupy.py;

```

3. Test your script.

Before submitting your job, it is important to test that your submission script will start without errors.
You can do a quick test in an [interactive job](Scheduler.md#Interactive_jobs).

4. Submit your job

```
[name@server ~]$ sbatch submit-mpi4py-gpu.sh

```

# Troubleshooting

## ModuleNotFoundError: No module named 'mpi4py'

If `mpi4py` is not accessible, you may get the following error when importing it:
`ModuleNotFoundError: No module named 'mpi4py'`

Possible solutions:

- check which Python versions are compatible with your loaded mpi4py module using `module spider mpi4py/X.Y.Z`. Once a compatible Python module is loaded, check that `python -c 'import mpi4py'` works.
- load the module before activating your virtual environment: please see the mpi4py as a package dependency section above.

See also [ModuleNotFoundError: No module named 'X'](Python.md#ModuleNotFoundError:_No_module_named_'X').