# Ansys

Other languages:

- English
- [français](Ansys_fr.md)

[Ansys](http://www.ansys.com/) is a software suite for engineering simulation and 3-D design. It includes packages such as [Ansys Fluent](http://www.ansys.com/Products/Fluids/ANSYS-Fluent) and [Ansys CFX](http://www.ansys.com/products/fluids/ansys-cfx).

# Licensing

We are a hosting provider for Ansys. This means that we have the software installed on our clusters, but we do not provide a generic license accessible to everyone. However, many institutions, faculties, and departments already have licenses that can be used on our clusters. Once the legal aspects are worked out for licensing, there will be remaining technical aspects. The license server on your end will need to be reachable by our compute nodes. This will require our technical team to get in touch with the technical people managing your license software. In some cases, this has already been done. You should then be able to load the Ansys module, and it should find its license automatically. If this is not the case, please contact our [technical support](Technical_Support.md) so that they can arrange this for you.

## Configuring your license file

Our module for Ansys is designed to look for license information in a few places. One of those places is your /home folder. You can specify your license server by creating a file named `$HOME/.licenses/ansys.lic` consisting of two lines as shown. Customize the file by replacing FLEXPORT and LICSERVER with the appropriate values for your server.

| setenv("ANSYSLMD_LICENSE_FILE", " FLEXPORT@LICSERVER ") |
| --- |

The following table provides established values for the CMC and SHARCNET license servers. To use a different server, locate the corresponding values as explained in Local license servers.

| License | System/Cluster | LICSERVER | FLEXPORT | NOTES |
| --- | --- | --- | --- | --- |
| CMC | fir | 172.26.0.101 | 6624 | Discontinue use (to be shutdown) |
| CMC | narval/rorqual | 10.100.64.10 | 6624 | Discontinue use (to be shutdown) |
| CMC | nibi | 10.25.1.56 | 6624 | Discontinue use (to be shutdown) |
| CMC | trillium | scinet-cmc | 6624 | Discontinue use (to be shutdown) |
| SHARCNET | nibi/fir/narval/rorqual | license1.computecanada.ca | 1055 |  |
| SHARCNET | trillium | localhost | 1055 |  |

Researchers who purchase a new CMC license subscription must [submit](https://www.cmc.ca/support/) your Alliance account username otherwise license checkouts will fail. The number of cores that can be used with a CMC license is described in the *Other Tricks and Tips* sections of the [Ansys Electronics Desktop and Ansys Mechanical/Fluids quick start guides](https://www.cmc.ca/?s=Other+Tricks+and+Tips&lang=en/).

### Local license servers

Before a local institutional Ansys license server can be used on the Alliance, firewall changes will need to be done on both the server and cluster side. For many Ansys servers this work has already been done and they can be used by following the steps in the "Ready To Use" section below. For Ansys servers that have never used on the Alliance, two additional steps must be done as shown in the "Setup Required" section also below.

#### Ready to use

To use a local institutional ANSYS License server whose network/firewall connections have already been setup for use on an Alliance cluster, contact your local Ansys license server administrator and get the following two pieces of information:

```
1) the configured Ansys flex port (FLEXPORT) number commonly 1055
2) the fully qualified hostname (LICSERVER) of the license server

```

Then simply configure your `~/.licenses/ansys.lic` file by plugging the values for FLEXPORT and LICSERVER into the `FILE: ansys.lic` template above.

#### Setup required

To use a local Ansys license server that has never been setup for use with an Alliance cluster, then you will ALSO need to get the following from your local Ansys license server administrator:

```
 3) the statically configured vendor port (VENDPORT) of the license server
 4) confirmation <servername> will resolve to the same IP address as LICSERVER on the cluster

```

where the <servername> can be found in the first line of the license file with format "SERVER <servername> <host id> <lmgrd port>". Send items 1->3 by email to [technical support](Technical_Support.md) and mention which Alliance cluster you want to run Ansys jobs on. An Alliance system administrator will then open the outbound cluster firewall so license checkout requests can reach your license server from the cluster compute nodes. A range of IP addresses will then be sent back to you. Give these to your local network administrator. Request the firewall into your local license server be opened so that Ansys license connection (checkout requests) can reach your servers FLEXPORT and VENDPORT ports across the IP range.

## Checking license

To test if your `ansys.lic` is configured and working properly copy/paste the following sequence of commands on the cluster you are submitting jobs to. The only required change would be to specify YOURUSERID. If the software on a remote license server has not been updated then a failure can occur if the latest module version of ansys is loaded to test with. Therefore to be certain the license checkouts will work when jobs are run in the queue, the same ansys module version that you load in your slurm scripts should be specified below.

```
[login-node:~] cd /tmp
[login-node:~] salloc --time=1:0:0 --mem=1000M --account=def-YOURUSERID
[login-node:~] module load StdEnv/2023; module load ansys/2023R2
[login-node:~] $EBROOTANSYS/v$(echo ${EBVERSIONANSYS:2:2}${EBVERSIONANSYS:5:1})/licensingclient/linx64/lmutil lmstat -c $ANSYSLMD_LICENSE_FILE | grep "ansyslmd: UP" 1> /dev/null && echo Success || echo Fail

```

If `Success` is output license checkouts should work when jobs are submitted to the queue.  
If `Fail` is output then jobs will likely fail requiring a problem ticket to be submitted to resolve.

# Version compatibility

Ansys simulations are typically forward compatible but NOT backwards compatible. This means that simulations created using an older version of Ansys can be expected to load and run fine with any newer version. For example, a simulation created and saved with ansys/2022R2 should load and run smoothly with ansys/2023R2 but NOT the other way around. While it may be possible to start a simulation running with an older version random error messages or crashing will likely occur. Regarding Fluent simulations, if you cannot recall which version of ansys was used to create your cas file try grepping it as follows to look for clues :

```
$ grep -ia fluent combustor.cas
  (0 "fluent15.0.7  build-id: 596")

```
```
$ grep -ia fluent cavity.cas.h5
  ANSYS_FLUENT 24.1 Build 1018

```

## Platform support

Ansys provides detailed platform support information describing software/hardware compatibility for the [Current Release](https://www.ansys.com/it-solutions/platform-support) and [Previous Releases](https://www.ansys.com/it-solutions/platform-support/previous-releases). The *Platform Support by Application / Product* pdf is of special interest since it shows which packages are supported under Windows but not under Linux and thus not on the Alliance such as Spaceclaim.

## What's new

Ansys posts [Product Release and Updates](https://www.ansys.com/products/release-highlights) for the latest releases. Similar information for previous releases can generally be pulled up for various application topics by visiting the Ansys [blog](https://www.ansys.com/blog) page and using the FILTERS search bar. For example, searching on `What’s New Fluent 2024 gpu` pulls up a document with title `[What’s New for Ansys Fluent in 2024 R1?](https://www.ansys.com/blog/fluent-2024-r1)` containing a wealth of the latest gpu support information. Specifying a version number in the [Press Release](https://www.ansys.com/news-center/press-releases) search bar is also a good way to find new release information. Recently a module for the latest ANSYS release was installed `ansys/2025R1.02` however to use it requires a suitably updated license server such as CMCs. The upgrade of the SHARCNET license server is underway however until it is complete (and this message updated accordingly) it will only support jobs run with `ansys/2024R2.04` or older. To request a new version be installed or a problem with an exiting module please [submit a ticket](Technical_Support.md).

## Service packs

Starting with Ansys 2024 a separate Ansys module will appear on the clusters with a decimal and two digits appearing after the release number whenever a service pack is been installed over the initial release. For example, the initial 2024 release with no service pack applied may be loaded with `module load ansys/2024R1` while a module with Service Pack 3 applied may be loaded with `module load ansys/2024R1.03` instead. If a service pack is already available by the time a new release is to be installed, then most likely only a module for that service pack number will be installed unless a request to install the initial release is also received.

Most users will likely want to load the latest module version equipped with the latest installed service pack which can be achieved by simply doing `module load ansys`. While it's not expected service packs will impact numerical results, the changes they make are extensive and so, if computations have already been done with the initial release or an earlier service pack then some groups may prefer to continue using it. Having separate modules for each service pack makes this possible. Starting with Ansys 2024R1 a detailed description of what each service pack does can be found by searching this [link](https://storage.ansys.com/staticfiles/cp/Readme/release2024R1/info_combined.pdf) for *Service Pack Details*. Future versions will presumably be similarly searchable by manually modifying the version number contained in the link.

# Cluster batch job submission

The Ansys software suite comes with multiple implementations of MPI to support parallel computation. Unfortunately, none of them support our [Slurm scheduler](Scheduler.md). For this reason, we need special instructions for each Ansys package on how to start a parallel job. In the sections below, we give examples of submission scripts for some of the packages. While the slurm scripts should work with on all clusters, Niagara users may need to make some additional changes covered [here](https://docs.scinet.utoronto.ca/index.php).

## Fluent

Typically, you would use the following procedure to run Fluent on one of our clusters:

1. Prepare your Fluent job using Fluent from the Ansys Workbench on your desktop machine up to the point where you would run the calculation.
2. Export the "case" file with *File > Export > Case…* or find the folder where Fluent saves your project's files. The case file will often have a name like `FFF-1.cas.gz`.
3. If you already have data from a previous calculation, which you want to continue, export a "data" file as well (*File > Export > Data…*) or find it in the same project folder (`FFF-1.dat.gz`).
4. [Transfer](Data_transfer.md) the case file (and if needed the data file) to a directory on the [/project](Project_Layout.md) or [/scratch](Filesystem.md#Storage_types) filesystem on the cluster. When exporting, you can save the file(s) under a more instructive name than `FFF-1.*` or rename them when they are uploaded.
5. Now you need to create a "journal" file. Its purpose is to load the case file (and optionally the data file), run the solver and finally write the results. See examples below and remember to adjust the filenames and desired number of iterations.
6. If jobs frequently fail to start due to license shortages and manual resubmission of failed jobs is not convenient, consider modifying your script to requeue your job (up to 4 times) as shown under the *by node + requeue* tab further below. Be aware that doing this will also requeue simulations that fail due to non-license related issues (such as divergence), resulting in lost compute time. Therefore it is strongly recommended to monitor and inspect each Slurm output file to confirm each requeue attempt is license related. When it is determined that a job is requeued due to a simulation issue, immediately manually kill the job progression with `scancel jobid` and correct the problem.
7. After [running the job](Scheduler.md), you can download the data file and import it back into Fluent with *File > Import > Data…*.

### Slurm scripts

#### General purpose

Most Fluent jobs should use the following *by node* script to minimize solution latency and maximize performance over as few nodes as possible. Very large jobs, however, might wait less in the queue if they use a *by core* script. However, the startup time of a job using many nodes can be significantly longer, thus offsetting some of the benefits. In addition, be aware that running large jobs over an unspecified number of potentially very many nodes will make them far more vulnerable to crashing if any of the compute nodes fail during the simulation. The scripts will ensure Fluent uses shared memory for communication when run on a single node or distributed memory (utilizing MPI and the appropriate HPC interconnect) when run over multiple nodes. The two narval tabs may be be useful to provide a more robust alternative if fluent crashes during the initial auto mesh partitioning phase when using the standard intel based scripts with the parallel solver. The other option would be to manually perform the mesh partitioning in the fluent gui then try to run the job again on the cluster with the intel scripts. Doing so will allow you to inspect the partition statistics and specify the partitioning method to obtain an optimal result. The number of mesh partitions should be an integral multiple of the number of cores; for optimal efficiency, ensure at least 10000 cells per core.

Multinode (by node)Multinode (by core)Multinode (by node, narval)Multinode (by core, narval)Multinode (by node, trillium)

**File :** script-flu-bynode-intel.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account name
#SBATCH --time=00-03:00       # Specify time limit dd-hh:mm
#SBATCH --nodes=1             # Specify number of compute nodes (narval 1 node max)
#SBATCH --ntasks-per-node=32  # Specify upto maximum number of cores per compute node
#SBATCH --mem=0               # Specify memory per compute node (0 allocates all memory)
#SBATCH --cpus-per-task=1     # Do not change

module load StdEnv/2023       # Do not change
module load ansys/2023R2      # or newer versions

MYJOURNALFILE=sample.jou      # Specify your journal file name
MYVERSION=3d                  # Specify 2d, 2ddp, 3d or 3ddp

# ------- do not change any lines below --------

if [[ "$CC_CLUSTER" == narval ]]; then
 module load intel/2023 intelmpi
 export INTELMPI_ROOT=$I_MPI_ROOT
 unset I_MPI_ROOT
fi

if [[ ("${EBVERSIONANSYS//R*}" -ge 2025 && "${CC_CLUSTER}" == nibi) || "${CC_CLUSTER}" == narval ]]; then
 export I_MPI_HYDRA_BOOTSTRAP=ssh
 unset I_MPI_HYDRA_BOOTSTRAP_EXEC_EXTRA_ARGS
fi

slurm_hl2hl.py --format ANSYS-FLUENT > /tmp/machinefile-$SLURM_JOB_ID
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
 fluent -g $MYVERSION -t $NCORES -mpi=intel -pshmem -i $MYJOURNALFILE
else
 if [[ "${CC_CLUSTER}" == nibi ]]; then
   fluent -g $MYVERSION -t $NCORES -mpi=intel -peth -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
 else
   fluent -g $MYVERSION -t $NCORES -mpi=intel -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
 fi
fi

```

**File :** script-flu-bycore-intel.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account
#SBATCH --time=00-03:00       # Specify time limit dd-hh:mm
##SBATCH --nodes=1            # Uncomment to specify (narval 1 node max)
#SBATCH --ntasks=16           # Specify total number of cores across all nodes
#SBATCH --mem-per-cpu=4G      # Specify memory per core
#SBATCH --cpus-per-task=1     # Do not change

module load StdEnv/2023       # Do not change
module load ansys/2023R2      # or newer versions

MYJOURNALFILE=sample.jou      # Specify your journal file name
MYVERSION=3d                  # Specify 2d, 2ddp, 3d or 3ddp

# ------- do not change any lines below --------

if [[ "$CC_CLUSTER" == narval ]]; then
 module load intel/2023 intelmpi
 export INTELMPI_ROOT=$I_MPI_ROOT
 unset I_MPI_ROOT
fi

if [[ ("${EBVERSIONANSYS//R*}" -ge 2025 && "${CC_CLUSTER}" == nibi) || "${CC_CLUSTER}" == narval ]]; then
 export I_MPI_HYDRA_BOOTSTRAP=ssh
 unset I_MPI_HYDRA_BOOTSTRAP_EXEC_EXTRA_ARGS
fi

slurm_hl2hl.py --format ANSYS-FLUENT > /tmp/machinefile-$SLURM_JOB_ID
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
 fluent -g $MYVERSION -t $NCORES -mpi=intel -pshmem -i $MYJOURNALFILE
else
 if [[ "${CC_CLUSTER}" == nibi ]]; then
   fluent -g $MYVERSION -t $NCORES -mpi=intel -peth -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
 else
   fluent -g $MYVERSION -t $NCORES -mpi=intel -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
 fi
fi

```

**File :** script-flu-bynode-openmpi.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account name
#SBATCH --time=00-03:00       # Specify time limit dd-hh:mm
#SBATCH --nodes=1             # Specify number of compute nodes (1 or more)
#SBATCH --ntasks-per-node=64  # Specify number of cores per node (narval 64 or less)
#SBATCH --mem=0               # Do not change (allocate all memory per compute node)
#SBATCH --cpus-per-task=1     # Do not change

module load StdEnv/2023       # Do not change
module load ansys/2023R2      # or newer versions

MYJOURNALFILE=sample.jou      # Specify your journal file name
MYVERSION=3d                  # Specify 2d, 2ddp, 3d or 3ddp

# ------- do not change any lines below --------

export OPENMPI_ROOT=$EBROOTOPENMPI
slurm_hl2hl.py --format ANSYS-FLUENT > /tmp/mf-$SLURM_JOB_ID
for i in `cat /tmp/mf-$SLURM_JOB_ID | uniq`; do echo "${i}:$(cat /tmp/mf-$SLURM_JOB_ID | grep $i | wc -l)" >> /tmp/machinefile-$SLURM_JOB_ID; done
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
 fluent -g $MYVERSION -t $NCORES -mpi=openmpi -pshmem -i $MYJOURNALFILE
else
 export FI_PROVIDER=verbs
 fluent -g $MYVERSION -t $NCORES -mpi=openmpi -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
fi

```

**File :** script-flu-bycore-openmpi.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account name
#SBATCH --time=00-03:00       # Specify time limit dd-hh:mm
##SBATCH --nodes=1            # Uncomment to specify number of compute nodes (1 or more)
#SBATCH --ntasks=16           # Specify total number of cores across all nodes
#SBATCH --mem-per-cpu=4G      # Specify memory per core
#SBATCH --cpus-per-task=1     # Do not change

module load StdEnv/2023       # Do not change     
module load ansys/2023R2      # or newer versions

MYJOURNALFILE=sample.jou      # Specify your journal file name
MYVERSION=3d                  # Specify 2d, 2ddp, 3d or 3ddp

# ------- do not change any lines below --------

export OPENMPI_ROOT=$EBROOTOPENMPI
slurm_hl2hl.py --format ANSYS-FLUENT > /tmp/mf-$SLURM_JOB_ID
for i in `cat /tmp/mf-$SLURM_JOB_ID | uniq`; do echo "${i}:$(cat /tmp/mf-$SLURM_JOB_ID | grep $i | wc -l)" >> /tmp/machinefile-$SLURM_JOB_ID; done
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
 fluent -g $MYVERSION -t $NCORES -mpi=openmpi -pshmem -i $MYJOURNALFILE
else
 export FI_PROVIDER=verbs
 fluent -g $MYVERSION -t $NCORES -mpi=openmpi -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
fi

```

**File :** script-flu-bynode-intel-tri.sh

```
#!/bin/bash

#SBATCH --account=def-group      # Specify account name
#SBATCH --time=00-03:00          # Specify time limit dd-hh:mm
#SBATCH --nodes=1                # Specify number of compute nodes (1 or more)
#SBATCH --ntasks-per-node=16     # Specify number cores per node (max 192 on trillium)
##SBATCH --mem=0                 # Do not uncomment (be default trillium uses all memory per node)
#SBATCH --cpus-per-task=1        # Do not change (required parameter)

module load StdEnv/2023          # Do not change
module load ansys/2023R2         # or newer versions

MYJOURNALFILE=sample.jou         # Specify your journal file name
MYVERSION=3d                     # Specify 2d, 2ddp, 3d or 3ddp

# These settings are used instead of your ~/.licenses/ansys.lic
LICSERVER=license1.computecanada.ca   # Specify license server hostname
FLEXPORT=1055                         # Specify server flex port
VENDPORT=1793                         # Specify server vendor port

# ------- do not change any lines below --------

ssh tri-gw -fNL $FLEXPORT:$LICSERVER:$FLEXPORT
ssh tri-gw -fNL $VENDPORT:$LICSERVER:$VENDPORT
export ANSYSLMD_LICENSE_FILE=$FLEXPORT@localhost
export ANSYSLI_SERVERS=$INTEPORT@localhost

slurm_hl2hl.py --format ANSYS-FLUENT > $SLURM_SUBMIT_DIR/machinefile-$SLURM_JOB_ID
NCORES=$SLURM_NTASKS

if [ ! -L "$HOME/.ansys" ]; then
  echo "ERROR: A link to a writable .ansys directory does not exist."
  echo 'Remove ~/.ansys if one exists and then run: ln -s $SCRATCH/.ansys ~/.ansys'
  echo "Then try submitting your job again. Aborting the current job now!"
elif [ ! -L "$HOME/.fluentconf" ]; then
  echo "ERROR: A link to a writable .fluentconf directory does not exist."
  echo 'Remove ~/.fluentconf if one exists and run: ln -s $SCRATCH/.fluentconf ~/.fluentconf'
  echo "Then try submitting your job again. Aborting the current job now!"
elif [ ! -L "$HOME/.flrecent" ]; then
  echo "ERROR: A link to a writable .flrecent file does not exist."
  echo 'Remove ~/.flrecent if one exists and then run: ln -s $SCRATCH/.flrecent ~/.flrecent'
  echo "Then try submitting your job again. Aborting the current job now!"
else
  mkdir -pv $SCRATCH/.ansys
  mkdir -pv $SCRATCH/.fluentconf
  touch $SCRATCH/.flrecent
  if [ "$SLURM_NNODES" == 1 ]; then
   fluent -g $MYVERSION -t $NCORES -mpi=intel -pshmem -i $MYJOURNALFILE
  else
   fluent -g $MYVERSION -t $NCORES -mpi=intel -pib -cnf=$SLURM_SUBMIT_DIR/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
  fi
fi

```

#### License requeue

The scripts in this section should only be used with Fluent jobs that are known to complete normally without generating any errors in the output however typically require multiple requeue attempts to checkout licenses. They are not recommended for Fluent jobs that may 1) run for a long time before crashing 2) run to completion but contain unresolved journal file warnings, since in both cases the simulations will be repeated from the beginning until the maximum number of requeue attempts specified by the `array` value is reached. For these types of jobs, the general purpose scripts above should be used instead.

Multinode (by node + requeue)Multinode (by core + requeue)

**File :** script-flu-bynode+requeue.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account
#SBATCH --time=00-03:00       # Specify time limit dd-hh:mm
#SBATCH --nodes=1             # Specify number of compute nodes (narval 1 node max)
#SBATCH --ntasks-per-node=32  # Specify upto maximum number of cores per compute node
#SBATCH --mem=0               # Specify memory per compute node (0 allocates all memory)
#SBATCH --cpus-per-task=1     # Do not change
#SBATCH --array=1-5%1         # Specify number of requeue attempts (2 or more, 5 is shown)

module load StdEnv/2023       # Do not change
module load ansys/2023R2      # Specify version (or newer)

MYJOURNALFILE=sample.jou      # Specify your journal file name
MYVERSION=3d                  # Specify 2d, 2ddp, 3d or 3ddp

# ------- do not change any lines below --------

if [[ "$CC_CLUSTER" == narval ]]; then
 module load intel/2023 intelmpi
 export INTELMPI_ROOT=$I_MPI_ROOT
 unset I_MPI_ROOT
fi

if [[ ("${EBVERSIONANSYS//R*}" -ge 2025 && "${CC_CLUSTER}" == nibi) || "${CC_CLUSTER}" == narval ]]; then
 export I_MPI_HYDRA_BOOTSTRAP=ssh
 unset I_MPI_HYDRA_BOOTSTRAP_EXEC_EXTRA_ARGS
fi

slurm_hl2hl.py --format ANSYS-FLUENT > /tmp/machinefile-$SLURM_JOB_ID
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
 fluent -g $MYVERSION -t $NCORES -mpi=intel -pshmem -i $MYJOURNALFILE
else
 if [[ "${CC_CLUSTER}" == nibi ]]; then
   fluent -g $MYVERSION -t $NCORES -mpi=intel -peth -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
 else
   fluent -g $MYVERSION -t $NCORES -mpi=intel -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
 fi
fi
if [ $? -eq 0 ]; then
    echo "Job completed successfully! Exiting now."
    scancel $SLURM_ARRAY_JOB_ID
else
    echo "Job attempt $SLURM_ARRAY_TASK_ID of $SLURM_ARRAY_TASK_COUNT failed due to license or simulation issue!"
    if [ $SLURM_ARRAY_TASK_ID -lt $SLURM_ARRAY_TASK_COUNT ]; then
       echo "Resubmitting job now …"
    else
       echo "All job attempts failed exiting now."
    fi
fi

```

**File :** script-flu-bycore+requeue.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account
#SBATCH --time=00-03:00       # Specify time limit dd-hh:mm
##SBATCH --nodes=1            # Uncomment to specify (narval 1 node max) 
#SBATCH --ntasks=16           # Specify total number of cores
#SBATCH --mem-per-cpu=4G      # Specify memory per core
#SBATCH --cpus-per-task=1     # Do not change
#SBATCH --array=1-5%1         # Specify number of requeue attempts (2 or more, 5 is shown)

module load StdEnv/2023       # Do not change
module load ansys/2023R2      # Specify version (or newer)

MYJOURNALFILE=sample.jou      # Specify your journal file name
MYVERSION=3d                  # Specify 2d, 2ddp, 3d or 3ddp

# ------- do not change any lines below --------

if [[ "$CC_CLUSTER" == narval ]]; then
 module load intel/2023 intelmpi
 export INTELMPI_ROOT=$I_MPI_ROOT
 unset I_MPI_ROOT
fi

if [[ ("${EBVERSIONANSYS//R*}" -ge 2025 && "${CC_CLUSTER}" == nibi) || "${CC_CLUSTER}" == narval ]]; then
 export I_MPI_HYDRA_BOOTSTRAP=ssh
 unset I_MPI_HYDRA_BOOTSTRAP_EXEC_EXTRA_ARGS
fi

slurm_hl2hl.py --format ANSYS-FLUENT > /tmp/machinefile-$SLURM_JOB_ID
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
 fluent -g $MYVERSION -t $NCORES -mpi=intel -pshmem -i $MYJOURNALFILE
else
 if [[ "${CC_CLUSTER}" == nibi ]]; then
   fluent -g $MYVERSION -t $NCORES -mpi=intel -peth -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
 else
   fluent -g $MYVERSION -t $NCORES -mpi=intel -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOURNALFILE
 fi
fi
if [ $? -eq 0 ]; then
    echo "Job completed successfully! Exiting now."
    scancel $SLURM_ARRAY_JOB_ID
else
    echo "Job attempt $SLURM_ARRAY_TASK_ID of $SLURM_ARRAY_TASK_COUNT failed due to license or simulation issue!"
    if [ $SLURM_ARRAY_TASK_ID -lt $SLURM_ARRAY_TASK_COUNT ]; then
       echo "Resubmitting job now …"
    else
       echo "All job attempts failed exiting now."
    fi
fi

```

#### Solution restart

The following two scripts are provided to automate restarting very large jobs that require more than the typical seven-day maximum runtime window available on most clusters. Jobs are restarted from the most recent saved time step files. A fundamental requirement is the first time step can be completed within the requested job array time limit (specified at the top of your Slurm script) when starting a simulation from an initialized solution field. It is assumed that a standard fixed time step size is being used. To begin, a working set of sample.cas, sample.dat and sample.jou files must be present. Next edit your sample.jou file to contain `/solve/dual-time-iterate 1` and `/file/auto-save/data-frequency 1`. Then create a restart journal file by doing `cp sample.jou sample-restart.jou` and edit the sample-restart.jou file to contain `/file/read-cas-data sample-restart` instead of `/file/read-cas-data sample` and comment out the initialization line with a semicolon for instance `;/solve/initialize/initialize-flow`. If your 2nd and subsequent time steps are known to run twice as fast (as the initial time step), edit sample-restart.jou to specify `/solve/dual-time-iterate 2`. By doing this, the solution will only be restarted after two 2 time steps are completed following the initial time step. An output file for each time step will still be saved in the output subdirectory. The value 2 is arbitrary but should be chosen such that the time for 2 steps fits within the job array time limit. Doing this will minimize the number of solution restarts which are computationally expensive. If your first time step performed by sample.jou starts from a converged (previous) solution, choose 1 instead of 2 since likely all time steps will require a similar amount of wall time to complete. Assuming 2 is chosen, the total time of simulation to be completed will be 1\*Dt+2\*Nrestart\*Dt where Nrestart is the number of solution restarts specified in the script. The total number of time steps (and hence the number of output files generated) will therefore be 1+2\*Nrestart. The value for the time resource request should be chosen so the initial time step and subsequent time steps will complete comfortably within the Slurm time window specifiable up to a maximum of "#SBATCH --time=07-00:00" days.

Multinode (by node + restart)Multinode (by core + restart)

**File :** script-flu-bynode+restart.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account
#SBATCH --time=07-00:00       # Specify time limit dd-hh:mm
#SBATCH --nodes=1             # Specify number of compute nodes (narval 1 node max)
#SBATCH --ntasks-per-node=32  # Specify upto maximum number of cores per compute node
#SBATCH --mem=0               # Specify memory per compute node (0 allocates all memory)
#SBATCH --cpus-per-task=1     # Do not change
#SBATCH --array=1-5%1         # Specify number of solution restarts (2 or more, 5 is shown)

module load StdEnv/2023       # Do not change
module load ansys/2023R2      # Specify version (or newer)

MYVERSION=3d                        # Specify 2d, 2ddp, 3d or 3ddp
MYJOUFILE=sample.jou                # Specify your journal filename
MYJOUFILERES=sample-restart.jou     # Specify journal restart filename
MYCASFILERES=sample-restart.cas.h5  # Specify cas restart filename
MYDATFILERES=sample-restart.dat.h5  # Specify dat restart filename

# ------- do not change any lines below --------

if [[ "$CC_CLUSTER" == narval ]]; then
 module load intel/2023 intelmpi
 export INTELMPI_ROOT=$I_MPI_ROOT
 unset I_MPI_ROOT
fi

if [[ ("${EBVERSIONANSYS//R*}" -ge 2025 && "${CC_CLUSTER}" == nibi) || "${CC_CLUSTER}" == narval ]]; then
 export I_MPI_HYDRA_BOOTSTRAP=ssh
 unset I_MPI_HYDRA_BOOTSTRAP_EXEC_EXTRA_ARGS
fi

slurm_hl2hl.py --format ANSYS-FLUENT > /tmp/machinefile-$SLURM_JOB_ID
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
  if [ "$SLURM_ARRAY_TASK_ID" == 1 ]; then
    fluent -g 2ddp -t $NCORES -mpi=intel -pshmem -i $MYJOUFILE
  else
    fluent -g 2ddp -t $NCORES -mpi=intel -pshmem -i $MYJOUFILERES
  fi
else 
  if [ "$SLURM_ARRAY_TASK_ID" == 1 ]; then
   if [[ "${CC_CLUSTER}" == nibi ]]; then
     fluent -g $MYVERSION -t $NCORES -mpi=intel -peth -cnf=/tmp/machinefile-$SLURM_JOB_ID -ssh -i $MYJOUFILE
   else
     fluent -g $MYVERSION -t $NCORES -mpi=intel -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -ssh -i $MYJOUFILE
   fi
  else
   if [[ "${CC_CLUSTER}" == nibi ]]; then
     fluent -g $MYVERSION -t $NCORES -mpi=intel -peth -cnf=/tmp/machinefile-$SLURM_JOB_ID -ssh -i $MYJOUFILERES
   else
     fluent -g $MYVERSION -t $NCORES -mpi=intel -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -ssh -i $MYJOUFILERES
   fi
  fi
fi
if [ $? -eq 0 ]; then
    echo
    echo "SLURM_ARRAY_TASK_ID  = $SLURM_ARRAY_TASK_ID"
    echo "SLURM_ARRAY_TASK_COUNT = $SLURM_ARRAY_TASK_COUNT"
    echo
    if [ $SLURM_ARRAY_TASK_ID -lt $SLURM_ARRAY_TASK_COUNT ]; then
      echo "Restarting job with the most recent output dat file …"
      ln -sfv output/$(ls -ltr output | grep .cas | tail -n1 | awk '{print $9}') $MYCASFILERES
      ln -sfv output/$(ls -ltr output | grep .dat | tail -n1 | awk '{print $9}') $MYDATFILERES
      ls -lh cavity* output/*
    else
      echo "Job completed successfully! Exiting now."
      scancel $SLURM_ARRAY_JOB_ID
     fi
else
     echo "Simulation failed. Exiting …"
fi

```

**File :** script-flu-bycore+restart.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account
#SBATCH --time=00-03:00       # Specify time limit dd-hh:mm
##SBATCH --nodes=1            # Uncomment to specify (narval 1 node max)
#SBATCH --ntasks=16           # Specify total number of cores
#SBATCH --mem-per-cpu=4G      # Specify memory per core
#SBATCH --cpus-per-task=1     # Do not change
#SBATCH --array=1-5%1         # Specify number of restart aka time steps (2 or more, 5 is shown)

module load StdEnv/2023       # Do not change
module load ansys/2023R2      # Specify version (or newer)

MYVERSION=3d                        # Specify 2d, 2ddp, 3d or 3ddp
MYJOUFILE=sample.jou                # Specify your journal filename
MYJOUFILERES=sample-restart.jou     # Specify journal restart filename
MYCASFILERES=sample-restart.cas.h5  # Specify cas restart filename
MYDATFILERES=sample-restart.dat.h5  # Specify dat restart filename

# ------- do not change any lines below --------

if [[ "$CC_CLUSTER" == narval ]]; then
 module load intel/2023 intelmpi
 export INTELMPI_ROOT=$I_MPI_ROOT
 unset I_MPI_ROOT
fi

if [[ ("${EBVERSIONANSYS//R*}" -ge 2025 && "${CC_CLUSTER}" == nibi) || "${CC_CLUSTER}" == narval ]]; then
 export I_MPI_HYDRA_BOOTSTRAP=ssh
 unset I_MPI_HYDRA_BOOTSTRAP_EXEC_EXTRA_ARGS
fi

slurm_hl2hl.py --format ANSYS-FLUENT > /tmp/machinefile-$SLURM_JOB_ID
NCORES=$SLURM_NTASKS

if [ "$SLURM_NNODES" == 1 ]; then
  if [ "$SLURM_ARRAY_TASK_ID" == 1 ]; then
    fluent -g $MYVERSION -t $NCORES -mpi=intel -pshmem -I $MYFILEJOU
  else
    fluent -g $MYVERSION -t $NCORES -mpi=intel -pshmem -I $MYFILEJOURES
  fi
else 
  if [ "$SLURM_ARRAY_TASK_ID" == 1 ]; then
    if [[ "${CC_CLUSTER}" == nibi ]]; then
      fluent -g $MYVERSION -t $NCORES -mpi=intel -peth -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOUFILE
    else
      fluent -g $MYVERSION -t $NCORES -mpi=intel -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOUFILE
    fi
  else
    if [[ "${CC_CLUSTER}" == nibi ]]; then
      fluent -g $MYVERSION -t $NCORES -mpi=intel -peth -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOUFILERES
    else
      fluent -g $MYVERSION -t $NCORES -mpi=intel -pib -cnf=/tmp/machinefile-$SLURM_JOB_ID -i $MYJOUFILERES
    fi
  fi
fi
if [ $? -eq 0 ]; then
    echo
    echo "SLURM_ARRAY_TASK_ID  = $SLURM_ARRAY_TASK_ID"
    echo "SLURM_ARRAY_TASK_COUNT = $SLURM_ARRAY_TASK_COUNT"
    echo
    if [ $SLURM_ARRAY_TASK_ID -lt $SLURM_ARRAY_TASK_COUNT ]; then
      echo "Restarting job with the most recent output dat file"
      ln -sfv output/$(ls -ltr output | grep .cas | tail -n1 | awk '{print $9}') $MYCASFILERES
      ln -sfv output/$(ls -ltr output | grep .dat | tail -n1 | awk '{print $9}') $MYDATFILERES
      ls -lh cavity* output/*
    else
      echo "Job completed successfully! Exiting now."
      scancel $SLURM_ARRAY_JOB_ID
     fi
else
     echo "Simulation failed. Exiting now."
fi

```

### Journal files

Fluent journal files can include basically any command from Fluent's Text-User-Interface (TUI); commands can be used to change simulation parameters like temperature, pressure and flow speed. With this you can run a series of simulations under different conditions with a single case file, by only changing the parameters in the journal file. Refer to the Fluent User's Guide for more information and a list of all commands that can be used. The following journal files are set up with `/file/cff-files no` to use the legacy .cas/.dat file format (the default in module versions 2019R3 or older). Set this instead to `/file/cff-files yes` to use the more efficient .cas.h5/.dat.h5 file format (the default in module versions 2020R1 or newer).

Journal file (steady, case)Journal file (steady, case + data)Journal file (transient)

**File :** sample1.jou

```
; SAMPLE FLUENT JOURNAL FILE - STEADY SIMULATION
; ----------------------------------------------
; lines beginning with a semicolon are comments

; Overwrite files by default
/file/confirm-overwrite no

; Preferentially read/write files in legacy format
/file/cff-files no

; Read input case and data files
/file/read-case-data FFF-in

; Run the solver for this many iterations
/solve/iterate 1000

; Overwrite output files by default
/file/confirm-overwrite n

; Write final output data file
/file/write-case-data FFF-out

; Write simulation report to file (optional)
/report/summary y "My_Simulation_Report.txt"

; Cleanly shutdown fluent
/exit

```

**File :** sample2.jou

```
; SAMPLE FLUENT JOURNAL FILE - STEADY SIMULATION
; ----------------------------------------------
; lines beginning with a semicolon are comments

; Overwrite files by default
/file/confirm-overwrite no

; Preferentially read/write files in legacy format
/file/cff-files no

; Read input files
/file/read-case-data FFF-in

; Write a data file every 100 iterations
/file/auto-save/data-frequency 100

; Retain data files from 5 most recent iterations
/file/auto-save/retain-most-recent-files y

; Write data files to output sub-directory (appends iteration)
/file/auto-save/root-name output/FFF-out

; Run the solver for this many iterations
/solve/iterate 1000

; Write final output case and data files
/file/write-case-data FFF-out

; Write simulation report to file (optional)
/report/summary y "My_Simulation_Report.txt"

; Cleanly shutdown fluent
/exit

```

**File :** sample3.jou

```
; SAMPLE FLUENT JOURNAL FILE - TRANSIENT SIMULATION
; -------------------------------------------------
; lines beginning with a semicolon are comments

; Overwrite files by default
/file/confirm-overwrite no

; Preferentially read/write files in legacy format
/file/cff-files no

; Read the input case file
/file/read-case FFF-transient-inp

; For continuation (restart) read in both case and data input files
;/file/read-case-data FFF-transient-inp

; Write a data (and maybe case) file every 100 time steps
/file/auto-save/data-frequency 100
/file/auto-save/case-frequency if-case-is-modified

; Retain only the most recent 5 data (and maybe case) files
/file/auto-save/retain-most-recent-files y

; Write to output sub-directory (appends flowtime and timestep)
/file/auto-save/root-name output/FFF-transient-out-%10.6f

; ##### Settings for Transient simulation :  #####

; Set the physical time step size
/solve/set/time-step 0.0001

; Set the number of iterations for which convergence monitors are reported
/solve/set/reporting-interval 1

; ##### End of settings for Transient simulation #####

; Initialize using the hybrid initialization method
/solve/initialize/hyb-initialization

; Set max number of iters per time step and number of time steps
;/solve/set/max-iterations-per-time-step 75
;/solve/dual-time-iterate 1000 ,
/solve/dual-time-iterate 1000 75

; Write final case and data output files
/file/write-case-data FFF-transient-out

; Write simulation report to file (optional)
/report/summary y Report_Transient_Simulation.txt

; Cleanly shutdown fluent
/exit

```

### UDFs

The first step is to transfer your User-Defined Function or UDF (namely the sampleudf.c source file and any additional dependency files) to the cluster. When uploading from a windows machine, be sure the text mode setting of your transfer client is used otherwise fluent won't be able to read the file properly on the cluster since it runs linux. The UDF should be placed in the directory where your journal, cas and dat files reside. Next add one of the following commands into your journal file before the commands that read in your simulation cas/dat files. Regardless of whether you use the Interpreted or Compiled UDF approach, before uploading your cas file onto the Alliance please check that neither the Interpreted UDFs Dialog Box or the UDF Library Manager Dialog Box are configured to use any UDF; this will ensure that only the journal file commands are in control when jobs are submitted.

#### Interpreted

To tell fluent to interpret your UDF at runtime, add the following command line into your journal file before the cas/dat files are read or initialized. The filename sampleudf.c should be replaced with the name of your source file. The command remains the same regardless if the simulation is being run in serial or parallel. To ensure the UDF can be found in the same directory as the journal file, open your cas file in the fluent gui, remove any managed definitions and resave it. Doing this will ensure only the following command/method is in control when fluent runs. To use an interpreted UDF with parallel jobs, it will need to be parallelized as described in the section below.

```
define/user-defined/interpreted-functions "sampleudf.c" "cpp" 10000 no

```

#### Compiled

To use this approach, your UDF must be compiled on an Alliance cluster at least once. Doing so will create a libudf subdirectory structure containing the required `libudf.so` shared library. The libudf directory cannot simply be copied from a remote system (such as your laptop) to the Alliance since the library dependencies of the shared library will not be satisfied, resulting in fluent crashing on startup. That said, once you have compiled your UDF on an Alliance cluster, you can transfer the newly created libudf to any other Alliance cluster, providing your account loads the same StdEnv environment module version. Once copied, the UDF can be used by uncommenting the second (load) libudf line below in your journal file when submitting jobs to the cluster. Both (compile and load) libudf lines should not be left uncommented in your journal file when submitting jobs on the cluster, otherwise your UDF will automatically (re)compiled for each and every job. Not only is this highly inefficient, but it will also lead to racetime-like build conflicts if multiple jobs are run from the same directory. Besides configuring your journal file to build your UDF, the fluent gui (run on any cluster compute node or gra-vdi) may also be used. To do this, you would navigate to the Compiled UDFs Dialog Box, add the UDF source file and click Build. When using a compiled UDF with parallel jobs, your source file should be parallelized as discussed in the section below.

```
define/user-defined/compiled-functions compile libudf yes sampleudf.c "" ""

```

and/or

```
define/user-defined/compiled-functions load libudf

```

#### Parallel

Before a UDF can be used with a fluent parallel job (single node SMP and multinode MPI) it will need to be parallelized. By doing this we control how/which processes (host and/or compute) run specific parts of the UDF code when fluent is run in parallel on the cluster. The instrumenting procedure involves adding compiler directives, predicates and reduction macros into your working serial UDF. Failure to do so will result in fluent running slow at best or immediately crashing at worst. The end result will be a single UDF that runs efficiently when fluent is used in both serial and parallel mode. The subject is described in detail under *Part I: Chapter 7: Parallel Considerations* of the Ansys 2024 *Fluent Customization Manual* which can be accessed here.

#### DPM

UDFs can be used to customize Discrete Phase Models (DPM) as described in *Part III: Solution Mode | Chapter 24: Modeling Discrete Phase | 24.2 Steps for Using the Discrete Phase Models| 24.2.6 User-Defined Functions* of the *2024R2 Fluent Users Guide* and section *Part I: Creating and Using User Defined Functions | Chapter 2: DEFINE Macros | 2.5 Discrete Phase Model (DPM) DEFINE Macros* of the *2024R2 Fluent Customization Manual*. Before a DMP based UDF can be worked into a simulation, the injection of a set of particles must be defined by specifying "Point Properties" with variables such as source position, initial trajectory, mass flow rate, time duration, temperature and so forth depending on the injection type. This can be done in the gui by clicking the Physics panel, Discrete Phase to open the *Discrete Phase Model* box and then clicking the *Injections* button. Doing so will open an *Injections* dialog box where one or more injections can be created by clicking the *Create* button. The "Set Injection Properties" dialog which appears will contain an "Injection Type" pulldown with first four types available are "single, group, surface, flat-fan-atomizer". If you select any of these then you can then the "Point Properties" tab can be selected to input the corresponding Value fields. Another way to specify the "Point Properties" would be to read an injection text file. To do this select "file" from the Injection Type pulldown, specify the Injection Name to be created and then click the *File* button (located beside the *OK* button at the bottom of the "Set Injection Properties" dialog). Here either an Injection Sample File (with .dpm extension) or a manually created injection text file can be selected. To Select the File in the Select File dialog box that change the File of type pull down to All Files (\*), then highlight the file which could have any arbitrary name but commonly does have a .inj extension, click the OK button. Assuming there are no problems with the file, no Console error or warning message will appear in fluent. As you will be returned to the "Injections" dialog box, you should see the same Injection name that you specified in the "Set Injection Properties" dialog and be able to List its Particles and Properties in the console. Next open the Discrete Phase Model Dialog Box and select Interaction with Continuous Phase which will enable updating DPM source terms every flow iteration. This setting can be saved in your cas file or added via the journal file as shown. Once the injection is confirmed working in the gui the steps can be automated by adding commands to the journal file after solution initialization, for example:

```
/define/models/dpm/interaction/coupled-calculations yes
/define/models/dpm/injections/delete-injection injection-0:1
/define/models/dpm/injections/create injection-0:1 no yes file no zinjection01.inj no no no no
/define/models/dpm/injections/list-particles injection-0:1
/define/models/dpm/injections/list-injection-properties injection-0:1

```

where a basic manually created injection steady file format might look like:

```
 $ cat  zinjection01.inj
 (z=4 12)
 ( x          y        z    u         v    w    diameter  t         mass-flow  mass  frequency  time name )
 (( 2.90e-02  5.00e-03 0.0 -1.00e-03  0.0  0.0  1.00e-04  2.93e+02  1.00e-06   0.0   0.0        0.0 ) injection-0:1 )

```

noting that injection files for DPM simulations are generally setup for either steady or unsteady particle tracking where the format of the former is described in subsection *Part III: Solution Mode | Chapter 24: Modeling Discrete Phase | 24.3. Setting Initial Conditions for the Discrete Phase | 24.3.13 Point Properties for File Injections | 24.3.13.1 Steady File Format* of the *2024R2 Fluent Customization Manual*.

## CFX

### Slurm scripts

A summary of command-line options can be printed by running **cfx5solve -help** where the same module version thats loaded in your slurm script should be first manually loaded. By default cfx5solve will run in single precision (-single). To run cfx5solve in double precision add the `-double` option noting that doing so will also double memory requirements. By default cfx5solve can support meshes with up to 80 million elements (structured) or 200 million elements (unstructured). For larger meshes with up to 2 billion elements, add the `-large` option. Various combinations of these options can be specified for the Partitioner, Interpolator or Solver. Consult the ANSYS CFX-Solver Manager User's Guide for further details.

Single nodeMultinode

**File :** script-cfx-local.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account name
#SBATCH --time=00-03:00       # Specify time limit dd-hh:mm
#SBATCH --nodes=1             # Do not change
#SBATCH --ntasks-per-node=4   # Specify number of cores
#SBATCH --mem=16G             # Specify total memory
#SBATCH --cpus-per-task=1     # Do not change

#module load StdEnv/2020      # Uncomment to use (deprecated)     
#module load 2021R2           # Specify 2021R2 only

module load StdEnv/2023
module load ansys/2023R2      # Or newer module versions

# append additional cfx5solve command line options as required
if [[ "$CC_CLUSTER" = narval || "$CC_CLUSTER" == fir ]]; then
  cfx5solve -def YOURFILE.def -start-method "Open MPI Local Parallel" -part $SLURM_CPUS_ON_NODE
else
  cfx5solve -def YOURFILE.def -start-method "Intel MPI Local Parallel" -part $SLURM_CPUS_ON_NODE
fi

```

**File :** script-cfx-multiple.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify account name
#SBATCH --time=00-03:00       # Specify time limit dd-hh:mm
#SBATCH --nodes=2             # Specify multiple compute nodes (2 or more)
#SBATCH --ntasks-per-node=192 # Use all cores per compute node (do not change)
#SBATCH --mem=0               # Use all memory on each compute node (do not change)
#SBATCH --cpus-per-task=1     # Do not change

#module load StdEnv/2020      # Uncomment to use (deprecated)     
#module load 2021R2           # Specify 2021R2 only

module load StdEnv/2023
module load ansys/2023R2      # Or newer module versions

NNODES=$(slurm_hl2hl.py --format ANSYS-CFX)

# append additional cfx5solve command line options as required
if [[ "$CC_CLUSTER" = narval || "$CC_CLUSTER" == fir ]]; then
  cfx5solve -def YOURFILE.def -start-method "Open MPI Distributed Parallel" -par-dist $NNODES
else
  export I_MPI_HYDRA_BOOTSTRAP=ssh
  unset I_MPI_HYDRA_BOOTSTRAP_EXEC_EXTRA_ARGS
  cfx5solve -def YOURFILE.def -start-method "Intel MPI Distributed Parallel" -par-dist $NNODES
fi

```

## Workbench

Before submitting a project file to the queue on a cluster (for the first time) follow these steps to initialize it.

1. Connect to the cluster with [TigerVNC](VNC.md#Compute_nodes).
2. Switch to the directory where the project file is located (YOURPROJECT.wbpj) and start Workbench with the same Ansys module you used to create your project.
3. In Workbench, open the project with *File -> Open*.
4. In the main window, right-click on *Setup* and select *Clear All Generated Data*.
5. In the top menu bar pulldown, select *File -> Exit* to exit Workbench.
6. In the Ansys Workbench popup, when asked *The current project has been modified. Do you want to save it?*, click on the *No* button.
7. Quit Workbench and submit your job using one of the Slurm scripts shown below.

To avoid writing the solution when a running job successfully completes remove `;Save(Overwrite=True)` from within the last line of your script. Doing this will make it easier to run multiple test jobs (for scaling purposes when changing ntasks), since the initialized solution will not be overwritten each time. Alternatively, keep a copy of the initialized YOURPROJECT.wbpj file and YOURPROJECT\_files subdirectory and restore them after the solution is written.

### Slurm scripts

A project file can be submitted to the queue by customizing one of the following scripts and then running the `sbatch script-wbpj-202X.sh` command:

Single node (StdEnv/2023)Single node (StdEnv/2020)

**File :** script-wbpj-2023.sh

```
#!/bin/bash

#SBATCH --account=def-account
#SBATCH --time=00-03:00                # Time (DD-HH:MM)
#SBATCH --mem=16G                      # Specify total memory
#SBATCH --ntasks=4                     # Specify number of cores
#SBATCH --nodes=1                      # Do not change (multi-node not supported)
##SBATCH --exclusive                   # Uncomment ONLY for scaling testing
##SBATCH --constraint=broadwell        # Uncomment to specify an available node type

module load StdEnv/2023 ansys/2023R2   # OR newer Ansys module versions (untested)

if [ "$SLURM_NNODES" == 1 ]; then
  MEMPAR=0                             # Set to 0 for SMP (shared memory parallel)
else
  MEMPAR=1                             # Set to 1 for DMP (distributed memory parallel)
fi

rm -fv *_files/.lock
MWFILE=~/.mw/Application\ Data/Ansys/`basename $(find $EBROOTANSYS/v* -maxdepth 0 -type d)`/SolveHandlers.xml
sed -re "s/(.AnsysSolution>+)[a-zA-Z0-9]*(<\/Distribute.)/\1$MEMPAR\2/" -i "$MWFILE"
sed -re "s/(.Processors>+)[a-zA-Z0-9]*(<\/MaxNumber.)/\1$SLURM_NTASKS\2/" -i "$MWFILE"
sed -i "s!UserConfigured=\"0\"!UserConfigured=\"1\"!g" "$MWFILE"

export KMP_AFFINITY=disabled
export I_MPI_HYDRA_BOOTSTRAP=ssh

runwb2 -B -E "Update()" -F YOURPROJECT.wbpj
#runwb2 -B -E "Update();Save(Overwrite=True)" -F YOURPROJECT.wbpj

```

**File :** script-wbpj-2020.sh

```
#!/bin/bash

#SBATCH --account=def-account
#SBATCH --time=00-03:00                # Time (DD-HH:MM)
#SBATCH --mem=16G                      # Specify total memory
#SBATCH --ntasks=4                     # Specify number of cores
#SBATCH --nodes=1                      # Do not change (multi-node not supported)
##SBATCH --exclusive                   # Uncomment ONLY for scaling testing
##SBATCH --constraint=broadwell        # Uncomment to specify an available node type

module load StdEnv/2020 ansys/2022R2   # OR older Ansys module versions

if [ "$SLURM_NNODES" == 1 ]; then
  MEMPAR=0                             # Set to 0 for SMP (shared memory parallel)
else
  MEMPAR=1                             # Set to 1 for DMP (distributed memory parallel)
fi

rm -fv *_files/.lock
MWFILE=~/.mw/Application\ Data/Ansys/`basename $(find $EBROOTANSYS/v* -maxdepth 0 -type d)`/SolveHandlers.xml
sed -re "s/(.AnsysSolution>+)[a-zA-Z0-9]*(<\/Distribute.)/\1$MEMPAR\2/" -i "$MWFILE"
sed -re "s/(.Processors>+)[a-zA-Z0-9]*(<\/MaxNumber.)/\1$SLURM_NTASKS\2/" -i "$MWFILE"
sed -i "s!UserConfigured=\"0\"!UserConfigured=\"1\"!g" "$MWFILE"

export KMP_AFFINITY=disabled
export I_MPI_HYDRA_BOOTSTRAP=ssh

runwb2 -B -E "Update()" -F YOURPROJECT.wbpj
#runwb2 -B -E "Update();Save(Overwrite=True)" -F YOURPROJECT.wbpj

```

## Mechanical

The input file can be generated from within your interactive Workbench Mechanical session by clicking *Solution -> Tools -> Write Input Files* then specify `File name:` YOURAPDLFILE.inp and `Save as type:` APDL Input Files (\*.inp). APDL jobs can then be submitted to the queue by running the `sbatch script-name.sh` command.

### Slurm scripts

In the following slurm scripts, lines beginning with `##SBATCH` are commented.

Shared Memory Parallel (cpu)Distributed Memory Parallel (cpu)Shared Memory Parallel (gpu)Distributed Memory Parallel (gpu)

**File :** script-smp-2023-cpu.sh

```
#!/bin/bash
#SBATCH --account=def-account   # Specify your account
#SBATCH --time=00-03:00         # Specify time (DD-HH:MM)
#SBATCH --mem=32G               # Specify memory for all cores
#SBATCH --nodes=1               # Do not change
#SBATCH --tasks=8               # Specify number of cores
#SBATCH --cpus-per-task=1       # Do not change

module load StdEnv/2023
#module load ansys/2023R2
module load ansys/2024R1.03

mkdir outdir-$SLURM_JOBID
[[ "$CC_CLUSTER" = cedar ]] && export LD_LIBRARY_PATH=$EBROOTGCC/../lib/gcc

mapdl -smp -b nolist -np $SLURM_NTASKS -dir outdir-$SLURM_JOBID -i YOURAPDLFILE.inp

```

**File :** script-dmp-2023-cpu.sh

```
#!/bin/bash
#SBATCH --account=def-account   # Specify your account
#SBATCH --time=00-03:00         # Specify time (DD-HH:MM)
#SBATCH --mem-per-cpu=4G        # Specify memory per core
##SBATCH --nodes=2              # Specify number of nodes (optional)
#SBATCH --ntasks=8              # Specify number of cores
##SBATCH --ntasks-per-node=4    # Specify cores per node (optional)
#SBATCH --cpus-per-task=1       # Do not change

module load StdEnv/2023
#module load ansys/2023R2
module load ansys/2024R1.03

mkdir outdir-$SLURM_JOBID
if [[ "$CC_CLUSTER" = cedar ]]; then
 ln -s $EBROOTGCC/../lib/gcc/libstdc++.so.6.0.29 $PWD/outdir-$SLURM_JOBID/libstdc++.so.6.0.29
 export LD_LIBRARY_PATH=$PWD/outdir-$SLURM_JOBID
fi

if [[ "$CC_CLUSTER" = beluga  ]]; then
  export KMP_AFFINITY=none
  mapdl -dis -mpi intelmpi -b nolist -np $SLURM_NTASKS -dir outdir-$SLURM_JOBID -i YOURAPDLFILE.inp
else
  mapdl -dis -mpi openmpi -b nolist -np $SLURM_NTASKS -dir outdir-$SLURM_JOBID -i YOURAPDLFILE.inp
fi

```

**File :** script-smp-2023-gpu.sh

```
#!/bin/bash
#SBATCH --account=def-account    # Specify your account
#SBATCH --time=00-03:00          # Specify time (DD-HH:MM)
#SBATCH --mem=32G                # Specify memory for all cores
#SBATCH --ntasks=8               # Specify number of cores
#SBATCH --nodes=1                # Do not change
#SBATCH --cpus-per-task=1        # Do not change
#SBATCH --gpus-per-node=1        # Specify [gputype:]quantity
##SBATCH --gpus-per-node=h100:1  # Temporarily required on mini-graham
##SBATCH --partition=debug       # Temporarily required on mini-graham

module load StdEnv/2023
#module load ansys/2023R2
module load ansys/2024R1.03

mkdir outdir-$SLURM_JOBID
[[ "$CC_CLUSTER" = cedar ]] && export LD_LIBRARY_PATH=$EBROOTGCC/../lib/gcc

export ANSGPU_PRINTDEVICES=1
mapdl -smp -acc nvidia -na $SLURM_GPUS_ON_NODE -b nolist -np $SLURM_NTASKS -dir outdir-$SLURM_JOBID  -i YOURAPDLFILE.inp

```

**File :** script-dmp-2023-gpu.sh

```
#!/bin/bash
#SBATCH --account=def-account    # Specify your account
#SBATCH --time=00-03:00          # Specify time (DD-HH:MM)
#SBATCH --mem-per-cpu=4G         # Specify memory per core
#SBATCH --nodes=1                # Specify number of nodes
#SBATCH --ntasks-per-node=8      # Specify cores per node
#SBATCH --cpus-per-task=1        # Do not change
#SBATCH --gpus-per-node=1        # Specify [gputype:]quantity
##SBATCH --gpus-per-node=h100:1  # Temporarily required on mini-graham
##SBATCH --partition=debug       # Temporarily required on mini-graham

module load StdEnv/2023
#module load ansys/2023R2
module load ansys/2024R1.03

mkdir outdir-$SLURM_JOBID
if [[ "$CC_CLUSTER" = cedar ]]; then
 ln -s $EBROOTGCC/../lib/gcc/libstdc++.so.6.0.29 $PWD/outdir-$SLURM_JOBID/libstdc++.so.6.0.29
 export LD_LIBRARY_PATH=$PWD/outdir-$SLURM_JOBID
fi

export ANSGPU_PRINTDEVICES=1
if [[ "$CC_CLUSTER" = beluga  ]]; then 
  export KMP_AFFINITY=none
  mapdl -dis -acc nvidia -na $SLURM_GPUS_ON_NODE -mpi intelmpi -b nolist -np $SLURM_NTASKS -dir outdir-$SLURM_JOBID -i YOURAPDLFILE.inp
else
  mapdl -dis -acc nvidia -na $SLURM_GPUS_ON_NODE -mpi openmpi -b nolist -np $SLURM_NTASKS -dir outdir-$SLURM_JOBID -i YOURAPDLFILE.inp
fi

```

Ansys allocates 1024 MB total memory and 1024 MB database memory by default for APDL jobs. These values can be manually specified (or changed) by adding arguments `-m 1024` and/or `-db 1024` to the mapdl command line in the above scripts. When using a remote institutional license server with multiple Ansys licenses, it may be necessary to add `-p aa_r` or `-ppf anshpc`, depending on which Ansys module you are using. As always, perform detailed scaling tests before running production jobs to ensure that the optimal number of cores and minimum amount memory is specified in your scripts. The *single node* (SMP Shared Memory Parallel) scripts will typically perform better than the *multinode* (DIS Distributed Memory Parallel) scripts and therefore should be used whenever possible. To help avoid compatibility issues the Ansys module loaded in your script should ideally match the version used to generate the input file:

```
 [gra-login2:~/testcase] cat YOURAPDLFILE.inp | grep version
! ANSYS input file written by Workbench version 2019 R3

```

## Rocky

Besides being able to run simulations in gui mode (as discussed in the Graphical usage section below) [Ansys Rocky](https://www.ansys.com/products/fluids/ansys-rocky) can also run simulations in non-gui mode. Both modes support running Rocky with cpus only or with cpus and [gpus](https://www.ansys.com/blog/mastering-multi-gpu-ansys-rocky-software-enhancing-its-performance). Use of the ansysrocky/2024R2.0 module locally installed only on nibi and loadable by doing `module load ansysrocky/2024R2.0 StdEnv/2023 ansys/2024R2.04` should be discontinued as it is no longer supported and will be removed. Instead use Rocky included within the `ansys/2025R1` module (and future versions that will be installed) available on all clusters.

### Slurm scripts

To get a full listing of command line options run `Rocky -h` on the command line after loading any rocky module. Note that it is currently necessary to set your path to Rocky (as is shown in the scripts below) for the Rocky command to be found. The path will be included in future module version installs and ansys/2025R1 when updated at such time this message will be removed. If Rocky is being run with gpus to solving coupled problems, the number of cpus you should request from slurm (on the same node) should be increased to a maximum until the scalability limit of the coupled application is reached. If however Rocky is being run with gpus to solve standalone uncoupled problems, then only a minimal number of cpus should be requested that will allow be sufficient for Rocky to still run optimally. For instance only 2cpus or possibly 3cpus may be required. When Rocky is run with >= 4 cpus then *rocky\_hpc* licenses will be required which the SHARCNET license does provide. The scripts below have not been tested since the clusters were updated across the Alliance in fall 2025 therefore some adjustments maybe required.

CPU onlyGPU based

**File :** script-rocky-cpu.sh

```
#!/bin/bash

#SBATCH --account=account      # Specify your account (def or rrg)
#SBATCH --time=00-02:00        # Specify time (DD-HH:MM)
#SBATCH --mem=24G              # Specify total memory for cores
#SBATCH --cpus-per-task=6      # Specify number of cores to use
#SBATCH --nodes=1              # Request one node (do not change)

module load StdEnv/2023 ansys/2025R1       # or newer versions
export PATH=$EBROOTANSYS/v251/rocky:$PATH

Rocky --simulate “mysim.rocky” --resume=1 --ncpus=$SLURM_CPUS_PER_TASK --use-gpu=0

```

**File :** script-rocky-gpu.sh

```
#!/bin/bash

#SBATCH --account=account      # Specify your account (def or reg)
#SBATCH --time=00-01:00        # Specify time (DD-HH:MM)
#SBATCH --mem=24G              # Specify total memory for cores
#SBATCH --cpus-per-task=6      # Specify number of cores to use
#SBATCH --gres=gpu:v100:2      # Specify gpu type : gpu quantity
#SBATCH --nodes=1              # Request one node (do not change)

module load StdEnv/2023 ansys/2025R1       # or newer versions
export PATH=$EBROOTANSYS/v251/rocky:$PATH

Rocky --simulate “mysim.rocky” --resume=1 --ncpus=$SLURM_CPUS_PER_TASK --use-gpu=1 --gpu-num=$SLURM_GPUS_ON_NODE

```

## Electronics

Slurm scripts for using AnsysEDT is provided in a separate wiki page [here](https://docs.alliancecan.ca/wiki/AnsysEDT).

# Graphical use

To run Ansys programs in graphical mode click on one of the following OnDemand or Jupyterhub links. A job submission web page to configure the resources for an interactive session should appear in your browser :

```
NIBI: https://ondemand.sharcnet.ca
FIR: https://jupyterhub.fir.alliancecan.ca
RORQUAL: https://jupyterhub.rorqual.alliancecan.ca
NARVAL:  https://jupyterhub.narval.alliancecan.ca/
TRILLIUM: https://ondemand.scinet.utoronto.ca

```

Submit your resource request and then wait. If you started a Juypter Lab launcher interface then you can simply load an ansys software module from the left side menu and then click one of the ansys icons to start cfx, fluent mapdl or workbench. Otherwise if you started a Compute/Basic Desktop from the Nibi OnDemand system then you will need to open a terminal window, manually load an ansys module and then type the program name to start it command line. For this later case, if the application requires accelerated graphics to run properly (for instance for fluent to support 3d rendering) then either a whole GPU resource (H100 or T4 at the time of this writing) should be requested. Since the various ansys applications launched in graphical mode behave differently when different ansys module versions are loaded, recommendations for adding command line argument and exporting environment variables for virtualgl or mesa environments are suggested below depending on whether a GPU has been requested or not and whether a On Demand or Juypter Lab desktop is being used.

### Fluids

This section shows howto start Ansys Fluid applications from the command line of an On Demand Desktop or the convenience Icon's of a Juypter Lab Desktop.

#### Fluent

To start fluent the following steps should be done including setting the indicated Environment Variables depending on which type of Compute Node the desktop is being started on (with or without a gpu).

:   :   :   `module load StdEnv/2023 ansys/2025R1`
        :   `fluent`

In the following steps, when the Fluent Launcher popup selector panel appears, click the Environment Tab and copy/paste the following environment variable settings. Do NOT include the text between the round brackets, these are comments. Also do NOT put the word export in front of the variable names.

**Compute Node (no GPU requested) or Basic Desktop**

:   :   :   :   `I_MPI_HYDRA_BOOTSTRAP=ssh` (required on nibi)
            :   `HOOPS_PICTURE=opengl2-mesa` (version 2025R1 or newer)
            :   `HOOPS_PICTURE=null` (version 2024R2 or older)
        :   Click the `Start` button

**Compute Node (with GPU requested)**

:   :   :   When starting an OnDemand Desktop on nibi that requests a GPU you must currently choose a full `h100 (80GB)` GPU so the required VirtualGL environment variables are automatically setup in the Deskop environment required to enable OpenGL graphics calls to be accelerated with OpenGL.

            :   `I_MPI_HYDRA_BOOTSTRAP=ssh` (required on nibi)
            :   `HOOPS_PICTURE=opengl2` (version 2025R1 or newer)
            :   `HOOPS_PICTURE=opengl` (version 2024R2 or older)
        :   Click the `Start` button

```
If I_MPI_HYDRA_BOOTSTRAP=ssh is not set properly on nibi when fluent is started from within OOD Compute Desktop sessions and  intelmpi is used then fluent will crash on startup producing the following error output.  Should this occur completely exit fluent, shutdown workbench and start over again.
[mpiexec@g4.nibi.sharcnet] Error: Unable to run bstrap_proxy on g4.nibi.sharcnet (pid 2251587, exit code 256)
[mpiexec@g4.nibi.sharcnet] poll_for_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:157): check exit codes error
[mpiexec@g4.nibi.sharcnet] HYD_dmx_poll_wait_for_proxy_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:206): poll for  event error
[mpiexec@g4.nibi.sharcnet] HYD_bstrap_setup (../../../../../src/pm/i_hydra/libhydra/bstrap/src/intel/i_hydra_bstrap.c:1063): error waiting for event
[mpiexec@g4.nibi.sharcnet] Error setting up the bootstrap proxies

```

#### CFX

When starting CFX from an On Demand Desktop the following arguments maybe specified on the terminal window command line depending on whether a GPU was requested when the Desktop was started.

:   :   :   `module load StdEnv/2023 ansys/2025R1` (or older)
        :   `cfx5 -graphics mesa` (no GPU requested)
        :   `cfx5 -graphics ogl` (with GPU requested)

### Mapdl

The following steps for starting the Mechanical APDL gui from the command line of a terminal window should work regardless if you have started your On Demand Desktop on a Compute node with or without a gpu.

:   :   :   `module load StdEnv/2023 ansys/2022R2` (or newer versions)
        :   `mapdl -g`, or,
        :   `launcher` then click `RUN` button

### Workbench

This sections shows howto start workbench (and optionally fluent) on either an On Demand Desktop or Jupyter Lab Desktop.

#### On Demand Desktop

**Compute Node (no GPU requested) or Basic Desktop**

:   :   :   `module load StdEnv/2023 ansys/2025R1`
        :   `runwb2 -oglmesa`

:   :   :   To start fluent from within workbench click `Fluid Flow (Fluent)` in the left hand Analysis Menu, then click `Setup` in the center canvas `Fluid Flow (Fluent)` popup. Once the `Fluent Launcher` selector panel popup appears, click the Environment Tab and copy/paste the following environment variable settings:

            :   `I_MPI_HYDRA_BOOTSTRAP=ssh` (required on nibi)
            :   `HOOPS_PICTURE=opengl2-mesa` (version 2025R1 or newer)
            :   `HOOPS_PICTURE=null` (version 2024R2 or older)
        :   Click the `Start` button

**Compute Node (with GPU requested)**

For this option to work on nibi, as mentioned in the first paragraph of this section, a full h100(80GB) GPU must be selected from the GPU pulldown when starting the OnDemand desktop session. This particular GPU selection is required since it the only one (currently) on nibi that will ensure the VirtualGL environment variables required to enable accelerated OpenGL graphics calls are setup in the Deskop environment. Once your desktop appears, open a terminal window and start workbench as follows :

:   :   :   `module load StdEnv/2023 ansys/2025R1`
        :   `runwb2`

To optionally start fluent from within workbench click `Fluid Flow (Fluent)` in the left hand Analysis Menu, then click `Setup` in the center canvas `Fluid Flow (Fluent)` popup. Once the `Fluent Launcher` selector panel popup appears, click the Environment Tab and copy/paste the following environment variable settings.

:   :   :   `I_MPI_HYDRA_BOOTSTRAP=ssh` (required on nibi only)
        :   `HOOPS_PICTURE=opengl2` (version 2025R1 or newer)
        :   `HOOPS_PICTURE=null` (version 2024R2 or older)
    :   Click the `Start` button

```
If I_MPI_HYDRA_BOOTSTRAP=ssh is not set properly on nibi when fluent is started from within OOD Compute Desktop sessions and  intelmpi is used then fluent will crash on startup produce the following error output.  If this occurs completely exit fluent, shutdown workbench then start again.
[mpiexec@g4.nibi.sharcnet] Error: Unable to run bstrap_proxy on g4.nibi.sharcnet (pid 2251587, exit code 256)
[mpiexec@g4.nibi.sharcnet] poll_for_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:157): check exit codes error
[mpiexec@g4.nibi.sharcnet] HYD_dmx_poll_wait_for_proxy_event (../../../../../src/pm/i_hydra/libhydra/demux/hydra_demux_poll.c:206): poll for  event error
[mpiexec@g4.nibi.sharcnet] HYD_bstrap_setup (../../../../../src/pm/i_hydra/libhydra/bstrap/src/intel/i_hydra_bstrap.c:1063): error waiting for event
[mpiexec@g4.nibi.sharcnet] Error setting up the bootstrap proxies

```

#### Jupyter Lab Desktop

**Compute Node (no GPU requested)**

:   :   :   Click to load ansys/2025R1 (or newer version) in the Desktop left hand side menu
        :   Click the "Workbench (VNC)" icon located in the Jupyter Lab desktop center window
        :   Since the default icon is configured for a gpu node, we must customize it so
        :   workbench can be restart in mesa mode. To proceed, Exit the Workbench desktop,
        :   open a terminal window, and run the following commands on the command line:
        :   cd ~/Desktop; cp -p $(realpath workbench.desktop) workbench-mesa.desktop
        :   then edit workbench-mesa.desktop and change runwb2 -> runwb2 -oglmesa
        :   Save the file then click your newly customized icon to start workbench.
        :   Note the workbench icon that you created will persist for future sessions
        :   until manually deleted with: rm -f ~/Desktop/workbench-mesa.desktop

**Compute Node (with GPU requested)**

:   :   :   Click to load ansys/2025R1 (or newer version) in the Desktop left hand side menu
        :   Click the Workbench (VNC) icon located in the Jupyter Lab desktop center window

### Ensight

:   :   :   `module load StdEnv/2023 ansys/2022R2; A=222; B=5.12.6`
        :   `export LD_LIBRARY_PATH=$EBROOTANSYS/v$A/CEI/apex$A/machines/linux_2.6_64/qt-$B/lib`
        :   `ensight -X`

### Rocky

:   :   :   `module load StdEnv/2023 ansys/2025R1` (or newer versions)
        :   `export PATH=$EBROOTANSYS/v251/rocky:$PATH` (path to be included in future module versions)
        :   `Rocky` The ansys module handles reading your ~/licenses/ansys.lic
        :   `RockySolver` Run rocky solver directly from command line (add -h for help, untested)
        :   `RockySchedular` Start rocky schedular gui to submit/run jobs on present node (untested)
        :   o The SHARCNET license includes Rocky and is therefore free for all researchers to use
        :   o Rocky supports GPU-accelerated computing however this capability not been tested or documented yet

## Electronics

Information describing howto run AnsysEDT in graphical mode maybe found here [here](https://docs.alliancecan.ca/wiki/AnsysEDT).

# Site-specific usage

## SHARCNET license

The SHARCNET Ansys license is free for academic use by **any** Alliance researcher on **any** Alliance system. The installed software does not have any solver or geometry limits. The SHARCNET license may be used for ***Publishable Academic Research*** but not for any private/commercial purposes as this is strictly prohibited by the license terms. The SHARCNET Ansys license is based on the Multiphysics Campus Solution and includes products such as: HF, EM, Electronics HPC, Mechanical, CFD as described [here](https://www.ansys.com/academic/educator-tools/academic-product-portfolio). ROCKY and LS-DYNA are also now included by the SHARCNET license. Lumerical acquired by ANSYS in 2020 however is not covered presently although the software is installed with recent ansys modules so can be used with other suitably licensed Ansys servers. SpaceClaim is not installed Alliance systems (since they are all linux based) however it is technically covered by the SHARCNET license. A pool of 1986 anshpc licenses is included with the SHARCNET license to support running large scale parallel simulations with most Ansys products. To ensure they are used efficiently scaling tests should be run before launching long jobs. Parallel jobs that do not achieve at least 50% CPU utilization will probably be flagged by the system, resulting in a followup by an Alliance team member.

The SHARCNET Ansys license is made available on a first come first serve basis. It currently permits each researcher to run a maximum of simultaneous 8 jobs using upto 512 hpc cores. Therefore any of the following maximum even sized combinations can be run simultaneously 1x512, 2x256, 4x128 or 8x64 across all clusters. Since the license is oversubscribed there is however the potential for a shortage of anshpc licenses to develop. Should a job fail on startup due to a shortage of licenses it will need to be manually be resubmitted. If over time there are many instances of license shortages reported then either the total job limit per researcher will be decreased (to 6 or 4) and/or the total hpc core limit per researcher will be decreased (to 384 cores or 256) if necessary. If you need more than 512 hpc cores for your research then consider using the local ANSYS License server at your institution if one is available and contributing towards expanding it if necessary.

Some researchers may prefer to purchase a license subscription from [CMC](https://www.cmc.ca/subscriptions/) to gain access to their remote license servers to run ansys anywhere besides just on Alliance systems such as in your lab or at home on your laptop. Doing so will have several benefits 1) a local institutional license server is not needed 2) a physical license does not need to be obtained and reconfigured each year 3) the license can be used [almost anywhere](https://www.cmc.ca/ansys-campus-solutions-cmc-00200-04847/) including at home, institutions, or any alliance cluster across Canada and 4) installation instructions are provided for Windows machines to enable running spaceclaim (not currently possible on the Alliance clusters since all systems are linux based). Note however that according to the CMC [Ansys Quick Start Guides](https://www.cmc.ca/qsg-ansys-cadpass-r20/) there may be a 64 core limit per user!

#### License file

As of February 2026 the old license3.sharcnet.ca license server has been permanently shutdown. To use the SHARCNET Ansys license on any Alliance cluster, simply configure your `ansys.lic` file as follows instead:

```
[username@cluster:~] cat ~/.licenses/ansys.lic
setenv("ANSYSLMD_LICENSE_FILE", "1055@license1.computecanada.ca")

```

#### License query

To show the number of licenses in use by your username and the total in use by all users, run:

```
ssh nibi.alliancecan.ca
module load ansys
$EBROOTANSYS/v$(echo ${EBVERSIONANSYS:2:2}${EBVERSIONANSYS:5:1})/licensingclient/linx64/lmutil lmstat -c $ANSYSLMD_LICENSE_FILE -a | grep "Users of\|$USER"

```

If you discover any licenses unexpectedly in use by your username (due to ansys not exiting cleanly), connect to the node where it's running, open a terminal window and run the following command to terminate the rogue processes `pkill -9 -e -u $USER -f "ansys"` after which your licenses should be freed.

# Additive Manufacturing

To get started configure your `~/.licenses/ansys.lic` file to point to a license server that has a valid Ansys Mechanical License. This must be done on all systems where you plan to run the software.

## Enable Additive

This section describes how to make the Ansys Additive Manufacturing ACT extension available for use in your project. The steps must be performed on each cluster for each ansys module version where the extension will be used. Any extensions needed by your project will also need to be installed on the cluster as described below. If you get warnings about missing un-needed extensions (such as ANSYSMotion) then uninstall them from your project.

### Download Extension

- download AdditiveWizard.wbex from [https://catalog.ansys.com/](https://catalog.ansys.com/)
- upload AdditiveWizard.wbex to the cluster where it will be used

### Start Workbench

- follow the Workbench section in [Graphical use above](ANSYS.md#Graphical_use).
- File -> Open your project file (ending in .wbpj) into Workbench gui

### Open Extension Manager

- click ACT Start Page and the ACT Home page tab will open
- click Manage Extensions and the Extension Manager will open

### Install Extension

- click the box with the large + sign under the search bar
- navigate to select and install your AdditiveWizard.wbex file

### Load Extension

- click to highlight the AdditiveWizard box (loads the AdditiveWizard extension for current session only)
- click lower right corner arrow in the AdditiveWizard box and select *Load extension* (loads the extension for current AND future sessions)

### Unload Extension

- click to un-highlight the AdditiveWizard box (unloads extension for the current session only)
- click lower right corner arrow in the AdditiveWizard box and select *Do not load as default* (extension will not load for future sessions)

## Run Additive

### Gra-vdi

A user can run a single Ansys Additive Manufacturing job on gra-vdi with up to 16 cores as follows:

- Start Workbench on Gra-vdi as described above in **Enable Additive**.
- click File -> Open and select *test.wbpj* then click Open
- click View -> reset workspace if you get a grey screen
- start Mechanical, Clear Generated Data, tick Distributed, specify Cores
- click File -> Save Project -> Solve

Check utilization:

- open another terminal and run: `top -u $USER` \*\*OR\*\* `ps u -u $USER | grep ansys`
- kill rogue processes from previous runs: `pkill -9 -e -u $USER -f "ansys|mwrpcss|mwfwrapper|ENGINE"`

Please note that rogue processes can persistently tie up licenses between gra-vdi login sessions or cause other unusual errors when trying to start gui programs on gra-vdi. Although rare, rogue processes can occur if an ansys gui session (fluent, workbench, etc) is not cleanly terminated by the user before vncviewer is terminated either manually or unexpectedly - for instance due to a transient network outage or hung filesystem. If the latter is to blame then the processes may not by killable until normal disk access is restored.

### Cluster

Project preparation:

Before submitting a newly uploaded Additive project to a cluster queue (with `sbatch scriptname`) certain preparations must be done. To begin, open your simulation with Workbench gui (as described in the `Enable Additive` section above) in the same directory that your job will be submitted from and then save it again. Be sure to use the same ansys module version that will be used for the job. Next create a Slurm script (as explained in the *Cluster Batch Job Submission - WORKBENCH* section above). To perform parametric studies, change `Update()` to `UpdateAllDesignPoints()` in the Slurm script. Determine the optimal number of cores and memory by submitting several short test jobs. To avoid needing to manually clear the solution **and** recreate all the design points in Workbench between each test run, either 1) change `Save(Overwrite=True)` to `Save(Overwrite=False)` or 2) save a copy of the original YOURPROJECT.wbpj file and corresponding YOURPROJECT\_files directory. Optionally create and then manually run a replay file on the cluster in the respective test case directory between each run, noting that a single replay file can be used in different directories by opening it in a text editor and changing the internal FilePath setting.

```
module load ansys/2019R3
rm -f test_files/.lock
runwb2 -R myreplay.wbjn

```

Resource utilization:

Once your additive job has been running for a few minutes, a snapshot of its resource utilization on the compute node(s) can be obtained with the following srun command. Sample output corresponding to an eight core submission script is shown next. It can be seen that two nodes were selected by the scheduler:

```
[gra-login1:~] srun --jobid=myjobid top -bn1 -u $USER | grep R | grep -v top
  PID USER   PR  NI    VIRT    RES    SHR S  %CPU %MEM    TIME+  COMMAND
22843 demo   20   0 2272124 256048  72796 R  88.0  0.2  1:06.24  ansys.e
22849 demo   20   0 2272118 256024  72822 R  99.0  0.2  1:06.37  ansys.e
22838 demo   20   0 2272362 255086  76644 R  96.0  0.2  1:06.37  ansys.e
  PID USER   PR  NI    VIRT    RES    SHR S  %CPU %MEM    TIME+  COMMAND
 4310 demo   20   0 2740212 271096 101892 R 101.0  0.2  1:06.26  ansys.e
 4311 demo   20   0 2740416 284552  98084 R  98.0  0.2  1:06.55  ansys.e
 4304 demo   20   0 2729516 268824 100388 R 100.0  0.2  1:06.12  ansys.e
 4305 demo   20   0 2729436 263204 100932 R 100.0  0.2  1:06.88  ansys.e
 4306 demo   20   0 2734720 431532  95180 R 100.0  0.3  1:06.57  ansys.e

```

Scaling tests:

After a job completes, its "Job Wall-clock time" can be obtained from `seff myjobid`. Using this value, scaling tests can be performed by submitting short test jobs with an increasing number of cores. If the Wall-clock time decreases by ~50% when the number of cores is doubled, additional cores may be considered.

# Help resources

The official full documentation for recent versions Ansys 202[4|5]R[1|2] is available [here](https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/main_page.html?lang=en). Documentation for older versions such as Ansys 2023R[1|2] however requires [login](https://ansyshelp.ansys.com/). Developer documentation can be found in the Ansys Developer [Portal](https://developer.ansys.com). Additional learning resources include the Ansys HowTo [videos](https://www.youtube.com/@AnsysHowTo/videos), the Ansys Educator [Educator Hub](https://innovationspace.ansys.com/educator-hub/) and the Ansys Webinar [series](https://www.ansys.com/events/ansys-academic-webinar-series).

**XoverSSH Legacy Note**: Some programs can be run remotely on a cluster compute node by forwarding X over SSH to your local desktop. Unlike VNC, this approach is untested and unsupported since it relies on a properly setup X display server for your particular operating system OR the selection, installation and configuration of a suitable X client emulator package such as MobaXterm. Most users will find interactive response times unacceptably slow for basic menu tasks let alone performing more complex tasks such as those involving graphics rendering. Startup times for GUI programs can also be very slow depending on your Internet connection. For example, in one test it took 40 minutes to fully start the gui up over SSH while starting it with vncviewer required only 34 seconds. Despite the potential slowness, using this method to connect may still be of interest if your only goal is to open a simulation and perform some basic menu operations or run some calculations and response delays can be tolerated. The basic steps are given here as a starting point: 1) ssh -Y username@alliancecan.ca 2) salloc --x11 --time=1:00:00 --mem=16G --cpus-per-task=4 [--gpus-per-node=1] --account=def-mygroup; 3) once connected onto a compute node try running `xclock`. If the clock appears on your desktop, proceed to load the desired Ansys module and try running the program.