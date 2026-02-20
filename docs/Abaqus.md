# Abaqus

Other languages:

- English
- [français](Abaqus_fr.md)

[Abaqus FEA](https://www.3ds.com/products-services/simulia/products/abaqus/) is a software suite for finite element analysis and computer-aided engineering.

# Licensing

## Using your license file

Abaqus software modules are available on our clusters; however, you must provide your own license. To configure your account on a cluster, log in and create a file named `$HOME/.licenses/abaqus.lic` containing the following line. Next, replace `port@server` with the flexlm port number and server IP address (or fully qualified hostname) of your Abaqus license server. If you want to use legacy version 6.14.1 then replace ABAQUSLM\_LICENSE\_FILE with LM\_LICENSE\_FILE.

**File :** abaqus.lic

```
prepend_path("ABAQUSLM_LICENSE_FILE","port@server")

```

If your license has not been set up for use on an Alliance cluster, some additional configuration changes by the Alliance system administrator and your local system administrator will need to be done. Such changes are necessary to ensure the flexlm and vendor TCP ports of your Abaqus server are reachable from all cluster compute nodes when jobs are run via the queue. For us to help you get this done, write to [technical support](Technical_Support.md). Please be sure to include the following three items:

- flexlm port number
- static vendor port number
- IP address of your Abaqus license server

You will then be sent a list of cluster IP addresses so that your administrator can open the local server firewall to allow connections from the cluster on both ports. Please note that a special license agreement must generally be negotiated and signed by SIMULIA and your institution before a local license may be used remotely on Alliance hardware.

## FLEXnet/DSLS Servers

Similar to previously installed modules the abaqus/2026 module is configured by default to work with Simulia `FLEXnet` license server such as the free SHARCNET license server. To use a local `DSLS` based institutional license server two small text files `abaqus_v6.env` and `DSLicSrv.txt` should be created in your simulation submit directory as follows. These will be read automatically when abaqus starts running to reconfigure itself accordingly.

```
[l2 (login node):~/mysimdir] cat abaqus_v6.env
license_server_type=DSLS
dsls_license_config="DSLicSrv.txt" 

```
```
[l2 (login node):~/mysimdir] DSLicSrv.txt
YOUR-SERVER-HOSTNAME:PORT-NUMBER

```

# Version compatibility

## Module Changes

A new module for abaqus/2026 is now installed into the default StdEnv/2023 environment. This new version resolves the \*\*\* buffer overflow detected \*\*\* error with abaqus/2021 on all recent clusters. Note that each slurm script on this wiki page has been updated to work with both abaqus/2026 and abaqus/2021 where possible therefore all personal slurm scripts should likewise be updated by researchers. The abaqus/2026 module contains the initial *Abaqus 2026 Golden* release. Another module named abaqus/2026.2606 containing *Abaqus 2026 FP.CFA.2606* level updates will be installed next.

# Cluster job submission

Below are prototype Slurm scripts for submitting thread and mpi-based parallel simulations to single or multiple compute nodes. Most users will find it sufficient to use one of the **project directory scripts** provided in the *Single node computing* sections. The optional `memory=` argument found in the last line of the scripts is intended for larger memory or problematic jobs where 3072MB offset value may require tuning. A listing of all Abaqus command line arguments can be obtained by loading an Abaqus module and running: `abaqus -help | less`.

Single node jobs that run less than one day should find the *project directory script* located in the first tab sufficient. However, single node jobs that run for more than a day should use one of the restart scripts. Jobs that create large restart files will benefit by writing to the local disk through the use of the SLURM\_TMPDIR environment variable utilized in the **temporary directory scripts** provided in the two rightmost tabs of the single node standard and explicit analysis sections. The restart scripts shown here will continue jobs that have been terminated early for some reason. Such job failures can occur if a job reaches its maximum requested runtime before completing and is killed by the queue or if the compute node the job was running on crashed due to an unexpected hardware failure. Other restart types are possible by further tailoring of the input file (not shown here) to continue a job with additional steps or change the analysis (see the documentation for version specific details).

Jobs that require large memory or larger compute resources (beyond that which a single compute node can provide) should use the mpi scripts in the **multiple node sections** below to distribute computing over arbitrary node ranges determined automatically by the scheduler. Short scaling test jobs should be run to determine wall-clock times (and memory requirements) as a function of the number of cores (2, 4, 8, etc.) to determine the optimal number before running any long jobs.

## Standard analysis

Abaqus solvers support thread-based and mpi-based parallelization. Scripts for each type are provided below for running Standard Analysis type jobs on Single or Multiple nodes respectively. Scripts to perform multiple node job restarts are not currently provided.

### Single node computing

project directory scriptproject directory restart scripttemporary directory scripttemporary directory restart script

**File :** "scriptsp1.txt"

```
#!/bin/bash
#SBATCH --account=def-group     # Specify account
#SBATCH --time=00-06:00         # Specify days-hrs:mins
#SBATCH --cpus-per-task=4       # Specify number of cores
#SBATCH --mem=8G                # Specify total memory > 5G
#SBATCH --nodes=1               # Do not change !
##SBATCH --constraint=granite   # Uncomment to specify a node type
##SBATCH --gpus-per-node=h100:1 # Uncomment to specify [type:]number

module load abaqus/2026         # Latest version
#module load StdEnv/2020        # Legacy version
#module load abaqus/2021        # Discontinue use

unset SLURM_GTIDS
export MPI_IC_ORDER='tcp'
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"

rm -f testsp1* testsp2*

if [[ $EBVERSIONABAQUS -eq 2021 ]]; then
   /cvmfs/soft.computecanada.ca/gentoo/2023/x86-64-v3/usr/bin/unshare \
   --fork --pid --mount-proc --user --map-user $USER \
   abaqus job=testsp1 input=mystd-sim.inp \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB" \
   #gpus=$SLURM_GPUS_ON_NODE  # uncomment this line to use gpu
elif [[ $EBVERSIONABAQUS -ge 2026 ]]; then
   abaqus job=testsp1 input=mystd-sim.inp \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB" \
   #gpus=$SLURM_GPUS_ON_NODE  # uncomment this line to use gpu
fi

```

To write restart data every N=12 time increments specify in the input file:

```
*RESTART, WRITE, OVERLAY, FREQUENCY=12

```

To write restart data for a total of 12 time increments specify instead:

```
*RESTART, WRITE, OVERLAY, NUMBER INTERVAL=12, TIME MARKS=NO

```

To check for completed restart information do:

```
egrep -i "step|start" testsp*.com testsp*.msg testsp*.sta

```

Some simulations may benefit by adding the following to the Abaqus command at the bottom of the script:

```
order_parallel=OFF

```

**File :** "scriptsp2.txt"

```
#!/bin/bash
#SBATCH --account=def-group     # Specify account
#SBATCH --time=00-06:00         # Specify days-hrs:mins
#SBATCH --cpus-per-task=4       # Specify number of cores
#SBATCH --mem=8G                # Specify total memory > 5G
#SBATCH --nodes=1               # Do not change !
##SBATCH --constraint=granite   # Uncomment to specify a node type
##SBATCH --gpus-per-node=h100:1 # Uncomment to specify [type:]number

module load abaqus/2026         # Latest version
#module load StdEnv/2020        # Legacy version
#module load abaqus/2021        # Discontinue use

unset SLURM_GTIDS
export MPI_IC_ORDER='tcp'
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"

rm -f testsp2* testsp1.lck

if [[ $EBVERSIONABAQUS -eq 2021 ]]; then
   /cvmfs/soft.computecanada.ca/gentoo/2023/x86-64-v3/usr/bin/unshare \
   --fork --pid --mount-proc --user --map-user $USER \
   abaqus job=testsp2 oldjob=testsp1 input=mystd-sim-restart.inp \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB" \
   #gpus=$SLURM_GPUS_ON_NODE  # uncomment this line to use gpu
elif [[ $EBVERSIONABAQUS -ge 2026 ]]; then
   abaqus job=testsp2 oldjob=testsp1 input=mystd-sim-restart.inp \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB" \
   #gpus=$SLURM_GPUS_ON_NODE  # uncomment this line to use gpu
fi

```

The restart input file should contain:

```
*HEADING
*RESTART, READ

```

**File :** "scriptst1.txt"

```
#!/bin/bash
#SBATCH --account=def-group     # Specify account
#SBATCH --time=00-06:00         # Specify days-hrs:mins
#SBATCH --cpus-per-task=4       # Specify number of cores
#SBATCH --mem=8G                # Specify total memory > 5G
#SBATCH --nodes=1               # Do not change !
##SBATCH --constraint=granite   # Uncomment to specify a node type
##SBATCH --gpus-per-node=h100:1 # Uncomment to specify [type:]number

module load abaqus/2026         # Latest version
#module load StdEnv/2020        # Legacy version
#module load abaqus/2021        # Discontinue use

unset SLURM_GTIDS
export MPI_IC_ORDER='tcp'
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"
echo "SLURM_SUBMIT_DIR =" $SLURM_SUBMIT_DIR
echo "SLURM_TMPDIR = " $SLURM_TMPDIR

rm -f testst1* testst2*

mkdir $SLURM_TMPDIR/scratch
cd $SLURM_TMPDIR
while sleep 6h; do
   echo "Saving data due to time limit ..."
   cp -fv * $SLURM_SUBMIT_DIR 2>/dev/null
done &
WPID=$!

if [[ $EBVERSIONABAQUS -eq 2021 ]]; then
   /cvmfs/soft.computecanada.ca/gentoo/2023/x86-64-v3/usr/bin/unshare \
   --fork --pid --mount-proc --user --map-user $USER \
   abaqus job=testst1 input=$SLURM_SUBMIT_DIR/mystd-sim.inp \
   scratch=$SLURM_TMPDIR/scratch cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB" \
   #gpus=$SLURM_GPUS_ON_NODE  # uncomment this line to use gpu
elif [[ $EBVERSIONABAQUS -ge 2026 ]]; then
   abaqus job=testst1 input=$SLURM_SUBMIT_DIR/mystd-sim.inp \
   scratch=$SLURM_TMPDIR/scratch cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB" \
   #gpus=$SLURM_GPUS_ON_NODE  # uncomment this line to use gpu
fi

{ kill $WPID && wait $WPID; } 2>/dev/null
cp -fv * $SLURM_SUBMIT_DIR

```

To write restart data every N=12 time increments specify in the input file:

```
*RESTART, WRITE, OVERLAY, FREQUENCY=12

```

To write restart data for a total of 12 time increments specify instead:

```
*RESTART, WRITE, OVERLAY, NUMBER INTERVAL=12, TIME MARKS=NO

```

To check the completed restart information do:

```
egrep -i "step|start" testst*.com testst*.msg testst*.sta

```

**File :** "scriptst2.txt"

```
#!/bin/bash
#SBATCH --account=def-group     # Specify account
#SBATCH --time=00-06:00         # Specify days-hrs:mins
#SBATCH --cpus-per-task=4       # Specify number of cores
#SBATCH --mem=8G                # Specify total memory > 5G
#SBATCH --nodes=1               # Do not change !
##SBATCH --constraint=granite   # Uncomment to specify a node type
##SBATCH --gpus-per-node=h100:1 # Uncomment to specify [type:]number

module load abaqus/2026         # Latest version
#module load StdEnv/2020        # Legacy version
#module load abaqus/2021        # Discontinue use

unset SLURM_GTIDS
export MPI_IC_ORDER='tcp'
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"
echo "SLURM_SUBMIT_DIR =" $SLURM_SUBMIT_DIR
echo "SLURM_TMPDIR = " $SLURM_TMPDIR

rm -f testst2* testst1.lck
cp testst1* $SLURM_TMPDIR
mkdir $SLURM_TMPDIR/scratch
cd $SLURM_TMPDIR
while sleep 6h; do
   echo "Saving data due to time limit ..."
   cp -fv testst2* $SLURM_SUBMIT_DIR 2>/dev/null
done &
WPID=$!

if [[ $EBVERSIONABAQUS -eq 2021 ]]; then
   /cvmfs/soft.computecanada.ca/gentoo/2023/x86-64-v3/usr/bin/unshare \
   --fork --pid --mount-proc --user --map-user $USER \
   abaqus job=testst2 oldjob=testst1 input=$SLURM_SUBMIT_DIR/mystd-sim-restart.inp \
   scratch=$SLURM_TMPDIR/scratch cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB" \
   #gpus=$SLURM_GPUS_ON_NODE  # uncomment this line to use gpu
elif [[ $EBVERSIONABAQUS -ge 2026 ]]; then
   abaqus job=testst2 oldjob=testst1 input=$SLURM_SUBMIT_DIR/mystd-sim-restart.inp \
   scratch=$SLURM_TMPDIR/scratch cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB" \
   #gpus=$SLURM_GPUS_ON_NODE  # uncomment this line to use gpu
fi

{ kill $WPID && wait $WPID; } 2>/dev/null
cp -fv testst2* $SLURM_SUBMIT_DIR

```

The restart input file should contain:

```
*HEADING
*RESTART, READ

```

### Multiple node computing

Users with large memory or compute needs (and correspondingly access to a large licenses) can use the following script to perform mpi-based computing over an arbitrary range of nodes ideally left to the scheduler to automatically determine. A companion template script to perform restart of multinode jobs is not provided due to additional limitations when they can be used. Only abaqus/2026 or newer maybe used with this script.

**File :** "scriptsp1-mpi.txt"

```
!/bin/bash
#SBATCH --account=def-group    # Specify account
#SBATCH --time=00-06:00        # Specify days-hrs:mins
##SBATCH --nodes=2             # Uncomment to specify (optional)
#SBATCH --ntasks=8             # Specify number of cores
#SBATCH --mem-per-cpu=4G       # Specify memory per core
##SBATCH --tasks-per-node=4    # Uncomment to specify (optional)
#SBATCH --cpus-per-task=1      # Do not change !

module load abaqus/2026         # Latest version

unset SLURM_GTIDS
#export MPI_IC_ORDER='tcp'
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"

rm -f testsp1-mpi*

unset hostlist
nodes="$(slurm_hl2hl.py --format MPIHOSTLIST | xargs)"
for i in `echo "$nodes" | xargs -n1 | uniq`; do hostlist=${hostlist}$(echo "['${i}',$(echo "$nodes" | xargs -n1 | grep $i | wc -l)],"); done
hostlist="$(echo "$hostlist" | sed 's/,$//g')"
mphostlist="mp_host_list=[$(echo "$hostlist")]"
export $mphostlist
echo "$mphostlist" > abaqus_v6.env

abaqus job=testsp1-mpi input=mystd-sim.inp \
scratch=$SLURM_TMPDIR cpus=$SLURM_NTASKS interactive mp_mode=mpi \
#mp_host_split=1  # number of dmp processes per node >= 1 (uncomment to specify)

```

## Explicit analysis

Abaqus solvers support thread-based and mpi-based parallelization. Scripts for each type are provided below for running explicit analysis type jobs on single or multiple nodes respectively. Template scripts to perform multinode job restarts are not currently provided pending further testing.

### Single node computing

project directory scriptproject directory restart scripttemporary directory scripttemporary directory restart script

**File :** "scriptep1.txt"

```
#!/bin/bash
#SBATCH --account=def-group    # specify account
#SBATCH --time=00-06:00        # days-hrs:mins
#SBATCH --mem=8000M            # node memory > 5G
#SBATCH --cpus-per-task=4      # number cores > 1
#SBATCH --nodes=1              # do not change

module load abaqus/2026         # Latest version
#module load StdEnv/2020        # Legacy version
#module load abaqus/2021        # Discontinue use

unset SLURM_GTIDS
export MPI_IC_ORDER='tcp'
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"

rm -f testep1* testep2*

if [[ $EBVERSIONABAQUS -eq 2021 ]]; then
   /cvmfs/soft.computecanada.ca/gentoo/2023/x86-64-v3/usr/bin/unshare \
   --fork --pid --mount-proc --user --map-user $USER \
   abaqus job=testep1 input=myexp-sim.inp \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB"
elif [[ $EBVERSIONABAQUS -ge 2026 ]]; then
   abaqus job=testep1 input=myexp-sim.inp \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB"
fi

```

To write restart data for a total of 12 time increments specify in the input file:

```
*RESTART, WRITE, OVERLAY, NUMBER INTERVAL=12, TIME MARKS=NO

```

Check for completed restart information in relevant output files:

```
egrep -i "step|restart" testep*.com testep*.msg testep*.sta

```

**File :** "scriptep2.txt"

```
#!/bin/bash
#SBATCH --account=def-group    # specify account
#SBATCH --time=00-06:00        # days-hrs:mins
#SBATCH --mem=8000M            # node memory > 5G
#SBATCH --cpus-per-task=4      # number cores > 1
#SBATCH --nodes=1              # do not change

module load abaqus/2026         # Latest version
#module load StdEnv/2020        # Legacy version
#module load abaqus/2021        # Discontinue use

unset SLURM_GTIDS
export MPI_IC_ORDER='tcp'
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"

rm -f testep2* testep1.lck
for f in testep1*; do [[ -f ${f} ]] && cp -a "$f" "testep2${f#testep1}"; done

if [[ $EBVERSIONABAQUS -eq 2021 ]]; then
   /cvmfs/soft.computecanada.ca/gentoo/2023/x86-64-v3/usr/bin/unshare \
   --fork --pid --mount-proc --user --map-user $USER \
   abaqus job=testep2 input=myexp-sim.inp recover \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB"
elif [[ $EBVERSIONABAQUS -ge 2026 ]]; then
   abaqus job=testep2 input=myexp-sim.inp recover \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB"
fi

```

No input file modifications are required to restart the analysis.

**File :** "scriptet1.txt"

```
#!/bin/bash
#SBATCH --account=def-group    # specify account
#SBATCH --time=00-06:00        # days-hrs:mins
#SBATCH --mem=8000M            # node memory > 5G
#SBATCH --cpus-per-task=4      # number cores > 1
#SBATCH --nodes=1              # do not change

module load abaqus/2026         # Latest version
#module load StdEnv/2020        # Legacy version
#module load abaqus/2021        # Discontinue use

unset SLURM_GTIDS
export MPI_IC_ORDER='tcp'
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"
echo "SLURM_SUBMIT_DIR =" $SLURM_SUBMIT_DIR
echo "SLURM_TMPDIR = " $SLURM_TMPDIR

rm -f testet1* testet2*
cd $SLURM_TMPDIR
while sleep 6h; do
   cp -f * $SLURM_SUBMIT_DIR 2>/dev/null
done &
WPID=$!

if [[ $EBVERSIONABAQUS -eq 2021 ]]; then
   /cvmfs/soft.computecanada.ca/gentoo/2023/x86-64-v3/usr/bin/unshare \
   --fork --pid --mount-proc --user --map-user $USER \
   abaqus job=testet1 input=$SLURM_SUBMIT_DIR/myexp-sim.inp \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB"
elif [[ $EBVERSIONABAQUS -ge 2026 ]]; then
   abaqus job=testet1 input=$SLURM_SUBMIT_DIR/myexp-sim.inp \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB"
fi

{ kill $WPID && wait $WPID; } 2>/dev/null
cp -f * $SLURM_SUBMIT_DIR

```

To write restart data for a total of 12 time increments specify in the input file:

```
*RESTART, WRITE, OVERLAY, NUMBER INTERVAL=12, TIME MARKS=NO

```

Check for completed restart information in relevant output files:

```
egrep -i "step|restart" testet*.com testet*.msg testet*.sta

```

**File :** "scriptet2.txt"

```
#!/bin/bash
#SBATCH --account=def-group    # specify account
#SBATCH --time=00-06:00        # days-hrs:mins
#SBATCH --mem=8000M            # node memory > 5G
#SBATCH --cpus-per-task=4      # number cores > 1
#SBATCH --nodes=1              # do not change

module load abaqus/2026         # Latest version
#module load StdEnv/2020        # Legacy version
#module load abaqus/2021        # Discontinue use

unset SLURM_GTIDS
export MPI_IC_ORDER='tcp'
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"
echo "SLURM_SUBMIT_DIR =" $SLURM_SUBMIT_DIR
echo "SLURM_TMPDIR = " $SLURM_TMPDIR

rm -f testet2* testet1.lck
for f in testet1*; do cp -a "$f" $SLURM_TMPDIR/"testet2${f#testet1}"; done
cd $SLURM_TMPDIR
while sleep 3h; do
   cp -f * $SLURM_SUBMIT_DIR 2>/dev/null
done &
WPID=$!

if [[ $EBVERSIONABAQUS -eq 2021 ]]; then
   /cvmfs/soft.computecanada.ca/gentoo/2023/x86-64-v3/usr/bin/unshare \
   --fork --pid --mount-proc --user --map-user $USER \
   abaqus job=testet2 input=$SLURM_SUBMIT_DIR/myexp-sim.inp recover \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB"
elif [[ $EBVERSIONABAQUS -ge 2026 ]]; then
   abaqus job=testet2 input=$SLURM_SUBMIT_DIR/myexp-sim.inp recover \
   scratch=$SLURM_TMPDIR cpus=$SLURM_CPUS_ON_NODE interactive \
   mp_mode=threads memory="$((${SLURM_MEM_PER_NODE}-3072))MB"
fi

{ kill $WPID && wait $WPID; } 2>/dev/null
cp -f  * $SLURM_SUBMIT_DIR

```

No input file modifications are required to restart the analysis.

### Multiple node computing

Users with large memory or compute needs (and correspondingly access to a large licenses) can use the following script to perform mpi-based computing over an arbitrary range of nodes ideally left to the scheduler to automatically determine. A companion template script to perform restart of multinode jobs is not provided due to additional limitations how they can be used. Only abaqus/2026 or newer maybe used with this script.

**File :** "scriptep1-mpi.txt"

```
!/bin/bash
#SBATCH --account=def-group    # Specify account
#SBATCH --time=00-06:00        # Specify days-hrs:mins
#SBATCH --ntasks=8             # Specify number of cores
#SBATCH --mem-per-cpu=16000M   # Specify memory per core
# SBATCH --nodes=2             # Specify number of nodes (optional)
#SBATCH --cpus-per-task=1      # Do not change !

module load abaqus/2026        # Latest version

unset SLURM_GTIDS
export MPI_IC_ORDER='tcp'
#export I_MPI_HYDRA_TOPOLIB=ipl
echo "LM_LICENSE_FILE=$LM_LICENSE_FILE"
echo "ABAQUSLM_LICENSE_FILE=$ABAQUSLM_LICENSE_FILE"

rm -f testep1-mpi*

unset hostlist
nodes="$(slurm_hl2hl.py --format MPIHOSTLIST | xargs)"
for i in `echo "$nodes" | xargs -n1 | uniq`; do hostlist=${hostlist}$(echo "['${i}',$(echo "$nodes" | xargs -n1 | grep $i | wc -l)],"); done
hostlist="$(echo "$hostlist" | sed 's/,$//g')"
mphostlist="mp_host_list=[$(echo "$hostlist")]"
export $mphostlist
echo "$mphostlist" > abaqus_v6.env

abaqus job=testep1-mpi input=myexp-sim.inp \
scratch=$SLURM_TMPDIR cpus=$SLURM_NTASKS interactive mp_mode=mpi \
#mp_host_split=1  # number of dmp processes per node >= 1 (uncomment to specify)

```

## Memory estimates

### Single process

An estimate for the total slurm node memory (--mem=) required for a simulation to run fully in ram (without being virtualized to scratch disk) can be obtained by examining the Abaqus output `test.dat` file. For example, a simulation that requires a fairly large amount of memory might show:

```
                   M E M O R Y   E S T I M A T E
  
 PROCESS      FLOATING PT       MINIMUM MEMORY        MEMORY TO
              OPERATIONS           REQUIRED          MINIMIZE I/O
             PER ITERATION           (MB)               (MB)
  
     1          1.89E+14             3612              96345

```

Alternatively a total memory estimate for a single node threaded process can be obtained by running the simulation interactively on a compute node and then monitoring the memory use with the top (or ps) command as follows:
1) First obtain an allocation on a compute node and start your simulation running:

```
[name@server ~]$ module load StdEnv/2020
[name@server ~]$ module load abaqus/2021
[name@server ~]$ unset SLURM_GTIDS

```

2) Next ssh into the compute node (c50 according to the sq command) and then run top i.e.

```
[name@server ~]$ ssh c50
[name@server ~]$ top -u $USER

```

3) watch the VIRT and RES columns until steady peak memory values are observed

To completely satisfy the recommended "MEMORY TO OPERATIONS REQUIRED MINIMIZE I/O" (MRMIO) value, at least the same amount of non-swapped physical memory (RES) must be available to Abaqus. Since the RES will in general be less than the virtual memory (VIRT) by some relatively constant amount for a given simulation, it is necessary to slightly over-allocate the requested Slurm node memory `-mem=`. In the above sample Slurm script, this over-allocation has been hardcoded to a conservative value of 3072MB based on initial testing of the standard Abaqus solver. To avoid long queue wait times associated with large values of MRMIO, it may be worth investigating the simulation performance impact associated with reducing the RES memory that is made available to Abaqus significantly below the MRMIO. This can be done by lowering the `-mem=` value which in turn will set an artificially low value of `memory=` in the Abaqus command (found in the last line of the script). In doing this, the RES cannot dip below the MINIMUM MEMORY REQUIRED (MMR) otherwise Abaqus will exit due to Out of Memory (OOM). As an example, if your MRMIO is 96GB try running a series of short test jobs with `#SBATCH --mem=8G, 16G, 32G, 64G` until an acceptable minimal performance impact is found, noting that smaller values will result in increasingly larger scratch space used by temporary files.

### Multi process

To determine the required slurm memory for multi-node slurm scripts, memory estimates (per compute process) required to minimize I/O are given in the output dat file of completed jobs. If mp\_host\_split is not specified (or is set to 1) then the total number of compute processes will equal the number of nodes. The mem-per-cpu value can then be roughly determined by multiplying the largest memory estimate by the number of nodes and then dividing by the number or ntasks. If however a value for mp\_host\_split is specified (greater than 1) than the mem-per-cpu value can be roughly determined from the largest memory estimate times the number of nodes times the value of mp\_host\_split divided by the number of tasks. Note that mp\_host\_split must be less than or equal to the number of cores per node assigned by slurm at runtime otherwise Abaqus will terminate. This scenario can be controlled by uncommenting to specify a value for tasks-per-node. The following definitive statement is given in every output dat file and mentioned here for reference:

```
 THE UPPER LIMIT OF MEMORY THAT CAN BE ALLOCATED BY ABAQUS WILL IN GENERAL DEPEND ON THE VALUE OF
THE "MEMORY" PARAMETER AND THE AMOUNT OF PHYSICAL MEMORY AVAILABLE ON THE MACHINE. PLEASE SEE
THE "ABAQUS ANALYSIS USER'S MANUAL" FOR MORE DETAILS. THE ACTUAL USAGE OF MEMORY AND OF DISK
SPACE FOR SCRATCH DATA WILL DEPEND ON THIS UPPER LIMIT AS WELL AS THE MEMORY REQUIRED TO MINIMIZE
I/O. IF THE MEMORY UPPER LIMIT IS GREATER THAN THE MEMORY REQUIRED TO MINIMIZE I/O, THEN THE ACTUAL
MEMORY USAGE WILL BE CLOSE TO THE ESTIMATED "MEMORY TO MINIMIZE I/O" VALUE, AND THE SCRATCH DISK
USAGE WILL BE CLOSE-TO-ZERO; OTHERWISE, THE ACTUAL MEMORY USED WILL BE CLOSE TO THE PREVIOUSLY
MENTIONED MEMORY LIMIT, AND THE SCRATCH DISK USAGE WILL BE ROUGHLY PROPORTIONAL TO THE DIFFERENCE
BETWEEN THE ESTIMATED "MEMORY TO MINIMIZE I/O" AND THE MEMORY UPPER LIMIT. HOWEVER ACCURATE
ESTIMATE OF THE SCRATCH DISK SPACE IS NOT POSSIBLE.

```

# Graphical use

It is recommended to use an OpenOnDemand or JupyterLab to run graphical applications at the Alliance.

## OnDemand

1. Start an OnDemand desktop session by clicking one of the following OnDemand links:

```
NIBI: https://ondemand.sharcnet.ca
TRILLIUM: https://ondemand.scinet.utoronto.ca

```

2. Open a new terminal window within your desktop and load :

```
module load abaqus/2026

```

3. Start the application in graphical mode using the cae option. If you are on either: 1) a node without a GPU or 2) a node with a GPU but without VirtualGL support, then append to use the mesa option:

```
abaqus cae -mesa

```

4. If you require better graphical performance and are on a node with a GPU and VirtualGL support then start abaqus without the -mesa option. When using the nibi OnDemand desktop a full h100 (80GB) GPU from the GPU pulldown must be selected.

```
abaqus cae

```

5. To start Abaqus in gui mode there must be at least **one** unused cae license according to :

```
$ abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | grep "Users of cae"
Users of cae:  (Total of 4 licenses issued;  Total of 3 licenses in use)

```

## JupyterLab

1. Start a JupyterHub desktop session by clicking one of the following JupyterHub links

```
FIR: https://jupyterhub.fir.alliancecan.ca
NARVAL:  https://portail.narval.calculquebec.ca/
RORQUAL: https://jupyterhub.rorqual.alliancecan.ca

```

2. Highlight an abaqus module such as `abaqus/2026` in the left hand side Available Module section  
3. Click Load for the highlighted module and a `Abaqus (VNC)` Icon will appear in desktop  
4. Click the Icon and abaqus should automatically be started in a remote Juypter desktop

## VncViewer

This approach is considered obsolete please use the above OnDemand/JuypterHub desktop instead.

1. Connect with a VncViewer client to a login or compute node without a GPU by following [TigerVNC](VNC.md)  
2. Open a new terminal window and enter the following

```
module load abaqus/2026

```

3. Start the application with

```
abaqus cae -mesa

```

# Site-specific use

## SHARCNET license

The SHARCNET license has been renewed until 17-jan-2027 and is operational. It provides a small shared free pool consisting of 3 cae and 54 execute tokens for all researchers. Maximum usage limits are currently set at: 1cae/user, 10 tokens/user and 15 tokens/group. These free tokens are available on a first come first serve basis and mainly intended for testing and light usage before deciding whether or not to purchase dedicated tokens. Costs for dedicated tokens (in 2021) were approximately CAD$110 per compute token and CAD$400 per GUI token: submit a ticket to request an official quote if interested. The free SHARCNET license can be used by any registered Alliance researcher, but only on SHARCNET hardware, and only after agreeing to the below Academic License User Agreement. Groups that purchase dedicated tokens to run on the SHARCNET license server may likewise ONLY use them on SHARCNET hardware (as dictated by the negotiated license agreement with Simulia) including the SHARCNET [OOD](https://docs.alliancecan.ca/wiki/Nibi#Access_through_Open_OnDemand_(OOD)) system (to run Abaqus in graphical mode) or Nibi/Dusky clusters (for submitting compute batch jobs to the queue). Before you can use the license, you must contact [technical support](Technical_Support.md) and request access. In your email 1) mention that it is for use on SHARCNET systems and 2) include a copy/paste of the following `License Agreement` statement with your full name and username entered in the indicated locations. Please note that every user must do this it cannot be done one time only for a group; this includes PIs who have purchased their own dedicated tokens.

### License agreement

```
----------------------------------------------------------------------------------
Subject: Abaqus SHARCNET Academic License User Agreement

This email is to confirm that i "_____________" with username "___________" will
only use “SIMULIA Academic Software” with tokens from the SHARCNET license server
for the following purposes:

1) on SHARCNET hardware where the software is already installed
2) in affiliation with a Canadian degree-granting academic institution
3) for education, institutional or instruction purposes and not for any commercial
   or contract-related purposes where results are not publishable
4) for experimental, theoretical and/or digital research work, undertaken primarily
   to acquire new knowledge of the underlying foundations of phenomena and observable
   facts, up to the point of proof-of-concept in a laboratory    
-----------------------------------------------------------------------------------
```

### Configure license file

Configure your license file as follows, noting that it is only usable on SHARCNET systems such as nibi and dusky clusters or the SHARCNET OOD desktop system. Note that the old license3.sharcnet.ca server has been permanently shutdown thus you must update your abaqus.lic file as follows to use the free SHARCNET license:

```
[l2 (nibi login node):~] cat ~/.licenses/abaqus.lic
prepend_path("ABAQUSLM_LICENSE_FILE","27050@license1.computecanada.ca")

```

If your Abaqus job fails with the error message [\*\*\* ABAQUS/eliT\_CheckLicense rank 0 terminated by signal 11 (Segmentation fault)] then verify your `abaqus.lic` file contains ABAQUSLM\_LICENSE\_FILE when using abaqus/202X modules. If your Abaqus jobs fails with error message [License server machine is down or not responding, etc.] and you are using abaqus/6.14.1 then replace ABAQUSLM\_LICENSE\_FILE with LM\_LICENSE\_FILE.

### Query license server

Log into nibi cluster, load abaqus and then run one of the following:

```
ssh nibi.alliancecan.ca
module load StdEnv/2020
module load abaqus

```

I) Check the SHARCNET license server for started and queued jobs:

```
abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | egrep "Users|start|queued"

```

II) Check the SHARCNET license server for started and queued jobs also showing reservations by purchasing groups:

```
abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | egrep "Users|start|queued|RESERVATION"

```

III) Check the SHARCNET license server for only cae, standard and explicit product availability:

```
abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | grep "Users of" | egrep "cae|standard|explicit"

```

When the output of query I) above indicates that a job for a particular username is queued this means the job has entered the "R"unning state from the perspective of `squeue -j jobid` or `sacct -j jobid` and is therefore idle on a compute node waiting for a license. This will have the same impact on your account priority as if the job were performing computations and consuming CPU time. Eventually when sufficient licenses come available the queued job will start.

#### Example

The following shows the situation where a user submitted two 6-core jobs (each requiring 12 tokens) in quick succession. The scheduler then started each job on a different node in the order they were submitted. Since the user had 10 Abaqus compute tokens, the first job (27527287) was able to acquire exactly enough (10) tokens for the solver to begin running. The second job (27527297) not having access to any more tokens entered an idle "queued" state (as can be seen from the lmstat output) until the first job completed, wasting the available resources and depreciating the user's fair share level in the process ...

```
[l2 (nibi login node):~] sq
           JOBID     USER              ACCOUNT           NAME  ST  TIME_LEFT NODES CPUS TRES_PER_N MIN_MEM NODELIST (REASON) 
        27530366  roberpj         cc-debug_cpu  scriptsp2.txt   R    9:56:13     1    6        N/A      8G     c107  (None) 
        27530407  roberpj         cc-debug_cpu  scriptsp2.txt   R    9:59:37     1    6        N/A      8G     c292  (None) 

```
```
[l2 (nibi login node):~] abaqus licensing lmstat -c $ABAQUSLM_LICENSE_FILE -a | egrep "Users|start|queued"
Users of abaqus:  (Total of 78 licenses issued;  Total of 53 licenses in use)
   roberpj c107 /dev/tty (v62.6) (license3.sharcnet.ca/27050 1042), start Mon 11/25 17:15, 10 licenses
   roberpj c292 /dev/tty (v62.6) (license3.sharcnet.ca/27050 125) queued for 10 licenses

```

To avoid license shortage problems when submitting multiple jobs when working with expensive Abaqus tokens either use a [job dependency](https://docs.alliancecan.ca/wiki/Running_jobs#Cancellation_of_jobs_with_dependency_conditions_which_cannot_be_met), [job array](https://docs.alliancecan.ca/wiki/Job_arrays) or at the very least set up a slurm [email notification](https://docs.alliancecan.ca/wiki/Running_jobs#Email_notification) to know when your job completes before manually submitting another one.

### Specify job resources

To ensure optimal usage of both your Abaqus tokens and our resources, it's important to carefully specify the required memory and ncpus in your Slurm script. The values can be determined by submitting a few short test jobs to the queue then checking their utilization. For **completed** jobs use `seff JobNumber` to show the total *Memory Utilized* and *Memory Efficiency*. If the *Memory Efficiency* is less than ~90%, decrease the value of the `#SBATCH --mem=` setting in your Slurm script accordingly. Notice that the `seff JobNumber` command also shows the total *CPU (time) Utilized* and *CPU Efficiency*. If the *CPU Efficiency* is less than ~90%, perform scaling tests to determine the optimal number of CPUs for optimal performance and then update the value of `#SBATCH --cpus-per-task=` in your Slurm script. For **running** jobs, use the `srun --jobid=29821580 --pty top -d 5 -u $USER` command to watch the %CPU, %MEM and RES for each Abaqus parent process on the compute node. The %CPU and %MEM columns display the percent usage relative to the total available on the node while the RES column shows the per process resident memory size (in human readable format for values over 1GB). Further information regarding how to [monitor jobs](Scheduler.md#Monitoring_jobs) is available on our documentation wiki

### Core token mapping

```
TOKENS 5  6  7  8  10  12  14  16  19  21  25  28  34  38
CORES  1  2  3  4   6   8  12  16  24  32  48  64  96 128

```

where TOKENS = floor[5 X CORES^0.422]

Each GPU used requires 1 additional TOKEN

## Western license

[[ The `abaqus.lic` file given below no longer works since the license4 machine has been shutdown and retired. Therefore all abaqus license checkout requests on dusky cluster from the Western/Robarts abaqus license server currently will fail. A replacement server for license4 is currently be worked on. Once it is ready for use `abaqus.lic` will be updated with the new server name and this red warning message removed. In the meantime the SHARCNET License maybe used instead by following the above procedure to request access. ]]

The Western site license may only be used by Western researchers on hardware located at Western's campus. Currently, only the Dusky cluster satisfies this condition. Nibi and SHARCNET OOD system are excluded since they are located on Waterloo's campus. Contact the Western Abaqus license server administrator <jmilner@robarts.ca> to inquire about using the Western Abaqus license. You will need to provide your username and possibly make arrangements to purchase tokens. If you are granted access then you may proceed to configure your `abaqus.lic` file to point to the Western license server:

### Configure license file

```
[dus241:~] cat .licenses/abaqus.lic
prepend_path("LM_LICENSE_FILE","27000@license4.sharcnet.ca")
prepend_path("ABAQUSLM_LICENSE_FILE","27000@license4.sharcnet.ca")

```

Once configured, submit your job as described in the *Cluster job submission* section above. If there are any problems submit a problem ticket to [technical support](Technical_Support.md). Specify that you are using the Abaqus Western license on dusky and provide the failed job number along with a paste of any error messages as applicable.