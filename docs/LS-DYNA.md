# LS-DYNA

Other languages:

- English
- [français](LS-DYNA_fr.md)

# Introduction

[LS-DYNA](http://www.lstc.com) is available on all our clusters. It is used for many [applications](http://www.lstc.com/applications) to solve problems in multiphysics, solid mechanics, heat transfer and fluid dynamics. Analyses are performed as separate phenomena or coupled physics simulations such as thermal stress or fluid structure interaction. LSTC was recently purchased by Ansys, so the LS-DYNA software may eventually be exclusively provided as part of the Ansys module. For now, we recommend using the LS-DYNA software traditionally provided by LSTC as documented in this wiki page.

# Licensing

The Alliance is a hosting provider for LS-DYNA. This means that we have LS-DYNA software installed on our clusters. The Alliance does NOT however provide a generic license accessible to everyone or provide license hosting services. Instead, many institutions, faculties, and departments already have licenses that can be used on our clusters. So that such licenses can be reached from a cluster's compute nodes, some cluster-specific network changes will generally need to be done. In cases where a license has already been used on a particular cluster, these changes may already be done. Users unable to locate or arrange for a license on campus may contact [CMC Microsystems](https://www.cmc.ca/support/). Licenses purchased from CMC do not require the overhead of hosting a local license server since they are hosted on a remote server system that CMC manages with the added benefit of being usable anywhere. If you have your own server and need a quote for a locally managed license, consider contacting [Simutech](https://simutechgroup.com) or contact Ansys directly. SHARCNET does not provide any free LS-DYNA licenses or license hosting services at this time.

### Initial setup and testing

If your (existing or new) license server has never been used on the cluster where you plan to run jobs, firewall changes will first need to be done on both the cluster side and server side. This will typically require involvement from both our technical team and the technical people managing your license software. To arrange this, send an email containing the service port and IP address of your floating license server to [technical support](Technical_Support.md). To check if your license file is working run the following commands

```
module load ls-dyna
ls-dyna_s or ls-dyna_d

```

You don't need to specify any input file or arguments to run this test. The output header should contain a (non-empty) value for `Licensed to:` with the exception of CMC license servers. Press ^C to quit the program and return to the command line.

## Configuring your license

In 2019 Ansys, purchased the Livermore Software Technology Corporation (LSTC), developer of LS-DYNA. LS-DYNA licenses issued by Ansys since that time use **Ansys license servers**. Licenses issued by LSTC may still use an **LSTC license server**. You can also obtain an LS-DYNA license through [CMC Microsystems](https://www.cmc.ca/). This section explains how to configure your account or job script for each of these cases.

### LSTC license

If you have a license issued to run on a LSTC license server, there are two options to specify it:

Option 1) Specify your license server by creating a small file named ls-dyna.lic with the following contents:

**File :** ls-dyna.lic

```
#LICENSE_TYPE: network
#LICENSE_SERVER:<port>@<server>

```

where <port> is an integer number and <server> is the hostname of your LSTC license server. Put this file in directory $HOME/.licenses/ on each cluster where you plan to submit jobs. The values in the file are picked up by LS-DYNA when it runs. This occurs because our module system sets the LSTC\_FILE variable to `LSTC_FILE=/home/$USER.licenses/ls-dyna.lic` whenever you load a `ls-dyna` or `ls-dyna-mpi` module. This approach is recommended for users with a license hosted on a LSTC license server since (compared to the next option) the identical settings will automatically be used by all jobs you submit on the cluster (without the need to specify them in each individual slurm script or setting them in your environment).

Option 2) Specify your license server by setting the following two environment variables in your slurm scripts:

```
export LSTC_LICENSE=network
export LSTC_LICENSE_SERVER=<port>@<server>

```

where <port> is an integer number and <server> is the hostname or IP address of your LSTC license server. These variables will take priority over any values specified in your `~/.licenses/ls-dyna.lic` file which must exist (even if it's empty) for any `ls-dyna` or `ls-dyna-mpi` module to successfully load. To ensure it exists, run `touch ~/.licenses/ls-dyna.lic` once on the command line on each cluster where you will submit jobs. For further details, see the official [documentation](https://lsdyna.ansys.com/download-install-overview/).

### Ansys license

If your LS-DYNA license is hosted on an Ansys license server, set the following two environment variables in your slurm scripts:

```
export LSTC_LICENSE=ansys
export ANSYSLMD_LICENSE_FILE=<port>@<server>

```

where <port> is an integer number and <server> is the hostname or IP address of your Ansys license server. These variables cannot be defined in your `~/.licenses/ls-dyna.lic` file. The file however must exist (even if it's empty) for any `ls-dyna` module to load. To ensure this, run `touch ~/.licenses/ls-dyna.lic` once from the command line (or each time in your slurm scripts). Note that only module versions >= 12.2.1 will work with Ansys license servers.

#### SHARCNET

The SHARCNET Ansys license supports running SMP and MPP LS-DYNA jobs. It can be used for free by anyone (on a core and job limited basis) on Nibi cluster by adding the following lines to your slurm script:

```
export LSTC_LICENSE=ansys
export ANSYSLMD_LICENSE_FILE=1055@license1.computecanada.ca

```

### CMC license

If your LS-DYNA license was purchased from CMC, set the following two environment variables according to the cluster you are using:

```
export LSTC_LICENSE=ansys
Fir:      export ANSYSLMD_LICENSE_FILE=6624@172.26.0.101
Nibi:     export ANSYSLMD_LICENSE_FILE=6624@10.25.1.56
Narval:   export ANSYSLMD_LICENSE_FILE=6624@10.100.64.10
Rorqual:  export ANSYSLMD_LICENSE_FILE=6624@10.100.64.10
Trillium: export ANSYSLMD_LICENSE_FILE=6624@scinet-cmc

```

where the IP address corresponds to the respective CADpass servers. No firewall changes are required to use a CMC license on any cluster since these have already been done. Since the remote CMC server that hosts LS=DYNA licenses is Ansys-based, these variables cannot be defined in your `~/.licenses/ls-dyna.lic` file. The file however must exist (even if it's empty) for any `ls-dyna` module to load. To ensure this is the case, run `touch ~/.licenses/ls-dyna.lic` once from the command line (or each time in your slurm scripts). Note that only module versions >= 13.1.1 will work with Ansys license servers.

# Cluster job submission

LS-DYNA provides binaries for running jobs on a single compute node (SMP - Shared Memory Parallel using OpenMP) or across multiple compute nodes (MPP - Message Passing Parallel using MPI). This section provides slurm scripts for each job type.

## Single node jobs

Modules for running jobs on a single compute node can be listed with: `module spider ls-dyna`. Jobs may be submitted to the queue with: `sbatch script-smp.sh`. The following slurm script shows how to run LS-DYNA with 8 cores on a single compute node. Regarding the AUTO option of the LSTC\_MEMORY [environment variable](https://www.dynasupport.com/howtos/general/environment-variables), this setting allows memory to be dynamically extended beyond the specified `memory=1500M` word setting where it is suitable for explicit analysis such as metal forming simulations but not crash analysis. Given there are 4 Bytes/word for the single precision solver and 8 Bytes/word for the double precision solver, the 1500M setting in the slurm script example below equates to either 1) a maximum amount of (1500Mw\*8Bytes/w) = 12GB memory before LS-DYNA self-terminates when solving an implicit problem or 2) a starting amount of 12GB memory prior to extending it (up 25% if necessary) when solving an explicit problem assuming `LSTC_MEMORY=AUTO` is uncommented. Note that 12GB represents 75% of the total mem=16GB reserved for the job and is considered ideal for implicit jobs on a single node. To summarize, for both implicit and explicit analysis, once an estimate for the total solver memory is determined in GB, the total memory setting for slurm can be determined by multiplying by 25% while the memory parameter value in mega words can be calculated as (0.75\*memGB/8Bytes/w)\*1000M and (0.75\*memGB/4Bytes/w)\*1000M for double and single precision solutions respectively.

**File :** script-smp.sh

```
#!/bin/bash
#SBATCH --account=def-account   # Specify
#SBATCH --time=0-03:00          # D-HH:MM
#SBATCH --cpus-per-task=8       # Specify number of cores
#SBATCH --mem=16G               # Specify total memory
#SBATCH --nodes=1               # Do not change

#module load StdEnv/2020        # Versions 12.0, 13.0, 13.1.1
#export RSNT_ARCH=avx2
#module load intel/2020.1.217
#module load ls-dyna/13.1.1

module load StdEnv/2023         # Version 12.2.1
module load intel/2023.2.1
module load ls-dyna/12.2.1

#export LSTC_LICENSE=ansys      # Specify an ANSYS License Server
#export ANSYSLMD_LICENSE_FILE=<port>@<server>

#export LSTC_MEMORY=AUTO        # Optional for explicit only

ls-dyna_d ncpu=$SLURM_CPUS_ON_NODE i=airbag.deploy.k memory=1500M

```

where

- ls-dyna\_s = single precision smp solver
- ls-dyna\_d = double precision smp solver

## Multiple node jobs

There are several modules installed for running jobs on multiple nodes using the MPP (Message Passing Parallel) version of LS-DYNA. The method is based on mpi and can scale to very many cores (8 or more). The modules may be listed by running `module spider ls-dyna-mpi`. Sample slurm scripts below demonstrate how to use these modules for submitting jobs to a specified number of whole nodes \*OR\* a specified total number of cores using `sbatch script-mpp-bynode.sh` or `sbatch script-mpp-bycore.sh` respectively. The MPP version requires a sufficiently large enough amount of memory (memory1) for the first core (processor 0) on the master node to decompose and simulate the model. This amount may be satisfied by specifying a value of mem-per-cpu to slurm slightly larger than the memory (memory2) required per core for simulation and then placing enough cores on the master node such that their differential sum (mem-per-cpu less memory2) is greater than or equal to memory1. Similar to the single node model, for best results, keep the sum of all expected memory per node within 75% of the reserved ram on a node. Thus in the first script below, assuming a 128GB full node memory compute node, memory1 maybe 6000M (48GB) maximum and memory2 200M (48GB/31cores).

### Specify node count

Jobs can be submitted to a specified number of **whole** compute nodes with the following script.

**File :** script-mpp-bynode.sh

```
#!/bin/bash
#SBATCH --account=def-account    # Specify
#SBATCH --time=0-03:00           # D-HH:MM
#SBATCH --ntasks-per-node=192    # Specify all cores per node (narval/nibi/fir/trillium 192)
#SBATCH --nodes=1                # Specify number compute nodes (1 or more)
#SBATCH --mem=0                  # Use all memory per compute node (do not change)
##SBATCH --constraint=cascade    # Uncomment to specify a cluster specific node type

#module load StdEnv/2020         # Versions 12.0, 13.0, 13.1.1
#export RSNT_ARCH=avx2
#module load intel/2020.1.217
#module load openmpi/4.0.3
#module load ls-dyna-mpi/13.1.1 

module load StdEnv/2023          # Version 12.2.1
module load intel/2023.2.1
module load ls-dyna-mpi/12.2.1

#export LSTC_LICENSE=ansys       # Specify an ANSYS License Server
#export ANSYSLMD_LICENSE_FILE=<port>@<server>

#export LSTC_MEMORY=AUTO         # Optional for explicit only

if [ "$EBVERSIONNIXPKGS" == 16.09 ]; then
 slurm_hl2hl.py --format MPIHOSTLIST > /tmp/mpihostlist-$SLURM_JOB_ID
 mpirun -np $NCORES -hostfile /tmp/mpihostlist-$SLURM_JOB_ID ls-dyna_d i=airbag.deploy.k memory=200M
else
 srun ls-dyna_d i=airbag.deploy.k memory=200M
fi

```

where

- ls-dyna\_s = single precision mpp solver
- ls-dyna\_d = double precision mpp solver

### Specify core count

Jobs can be submitted to an arbitrary number of compute nodes by specifying the number of cores. This approach allows the scheduler to determine the optimal number of compute nodes to minimize job wait time in the queue. Memory limits are applied per core, therefore a sufficiently large value of mem-per-cpu must be specified so the master processor can successfully decompose and handle its computations as explained in more detail in the opening paragraph of this section.

**File :** script-mpp-bycore.sh

```
#!/bin/bash
#SBATCH --account=def-account     # Specify
#SBATCH --time=0-03:00            # D-HH:MM
#SBATCH --ntasks=64               # Specify any total number of cores
#SBATCH --mem-per-cpu=2G          # Specify memory per core
##SBATCH --constraint=cascade     # Uncomment to specify a cluster specific node type

#module load StdEnv/2020          # Versions 12.0, 13.0, 13.1.1
#export RSNT_ARCH=avx2            # Uncomment on beluga, nibi, rorqual
#export load intel/2020.1.217
#module load openmpi/4.0.3
#module load ls-dyna-mpi/13.1.1

module load StdEnv/2023           # Version 12.2.1 (more versions added on request)
module load intel/2023.2.1
module load ls-dyna-mpi/12.2.1

#export LSTC_LICENSE=ansys        # Specify an ANSYS License Server
#export ANSYSLMD_LICENSE_FILE=<port>@<server>

#export LSTC_MEMORY=AUTO          # Optional for explicit only

if [ "$EBVERSIONNIXPKGS" == 16.09 ]; then
 slurm_hl2hl.py --format MPIHOSTLIST > /tmp/mpihostlist-$SLURM_JOB_ID
 mpirun -np $SLURM_NTASKS -hostfile /tmp/mpihostlist-$SLURM_JOB_ID ls-dyna_d i=airbag.deploy.k memory=200M
else
 srun ls-dyna_d i=airbag.deploy.k memory=200M
fi

```

where

- ls-dyna\_s = single precision mpp solver
- ls-dyna\_d = double precision mpp solver

## Performance testing

Depending on the simulation LS-DYNA may not be able to efficiently use very many cores in parallel. Scaling test jobs should therefore always be run before submitting long jobs. Doing this will help determine the maximum number of cores that can be used before performance degradation begins to occur. To extract test job statistics such as Job Wall-clock time, CPU Efficiency and Memory Efficiency either the seff jobnumber command or a cluster job portal such as [this](https://portal.nibi.sharcnet.ca) can be used. In the past scaling test jobs for the standard airbag problem have shown significantly different performance characteristics in the past depending which cluster they were being run on. These tests however were rather small using only 6 cores on a single node with the ls-dyna/12.2.1 module and 6 cores evenly distributed across two nodes with the ls-dyna-mpi/12.2.1 module. Scaling tests should instead be run using the actual research simulation and cluster where the full production runs will be done to get reliable results.

# Graphical use

LSTC provides [LS-PrePost](https://www.lstc.com/products/ls-prepost) for pre- and post-processing of LS-DYNA [models](https://www.dynaexamples.com/). This program is made available by a separate module and does not require a license. To run abaqus graphically in a remote gui desktop do one of the following where the OnDemand desktop approach is recommended :

## OnDemand

1. Connect to an OnDemand system using one of the following URLs in your laptop browser :

```
NIBI: https://ondemand.sharcnet.ca
FIR: https://jupyterhub.fir.alliancecan.ca
RORQUAL: https://jupyterhub.rorqual.alliancecan.ca
TRILLIUM: https://ondemand.scinet.utoronto.ca

```

2. Open a new terminal window in your desktop and run :

```
module load StdEnv/2020
module load ls-prepost/4.9
lsprepost OR lspp49

```

## VncViewer

1. Connect with a VncViewer client to a login or compute node by following [TigerVNC](VNC.md)  
2. Open a new terminal window in your desktop and run:

```
module load StdEnv/2020
module load ls-prepost/4.9
lsprepost OR lspp49

```