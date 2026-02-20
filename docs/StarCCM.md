# Star-CCM+

Other languages:

- English
- [français](Star-CCM_fr.md)

[STAR-CCM+](https://mdx.plm.automation.siemens.com/star-ccm-plus) is a multidisciplinary engineering simulation suite to model acoustics, fluid dynamics, heat transfer, rheology, multiphase flows, particle flows, solid mechanics, reacting flows, electrochemistry, and electromagnetics. It is developed by Siemens.

# License limitations

We have the authorization to host STAR-CCM+ binaries on our servers, but we don't provide licenses. You will need to have your own license in order to use this software. A remote POD license can be purchased directly from [Siemens](https://www.plm.automation.siemens.com/global/en/buy/). Alternatively, a local license hosted at your institution can be used, providing it can be accessed through the firewall from the cluster where jobs are to be run.

## Configuring your account

To configure your account to use a license server with the Star-CCM+ module, create a license file `$HOME/.licenses/starccm.lic` with the following layout:

**File :** starccm.lic

```
SERVER <server> ANY <port>
USE_SERVER

```

where `<server>` and `<port>` should be changed to specify the hostname (or ip address) and the static vendor port of the license server respectively. Note that manually setting `CDLMD_LICENSE_FILE` equal to <port>@<server> in your slurm script is not required; Instead, when a Star-CCM+ module is loaded this variable is automatically set to your *$HOME/.licenses/starccm.lic* file.

### POD license file

Researchers with a POD license purchased from [Siemens](https://www.plm.automation.siemens.com/global/en/buy/) must manually set the `LM_PROJECT` environment variable equal to *YOUR CD-ADAPCO PROJECT ID* in your slurm script. Also the `~/.licenses/starccm.lic` file should be configured as follows on each cluster:

**File :** starccm.lic

```
SERVER flex.cd-adapco.com ANY 1999
USE_SERVER

```

# Cluster batch job submission

When submitting jobs on a cluster for the first time, you must set up the environment to use your license. If you are using Siemans remote *pay-on-usage* license server then create a `~/.licenses/starccm.lic` file as shown in the **Configuring your account- POD license file** section above and license checkouts should immediately work. If however you are using an institutional license server, then after creating your `~/.licenses/starccm.lic` file you must also submit a problem ticket to [technical support](Technical_Support.md) so we can help co-ordinate the necessary one time network firewall changes required to access it (assuming the server has never been setup to be accessed from the Alliance cluster you will be using). If you still have problems getting the licensing to work then try removing or renaming file `~/.flexlmrc` since previous search paths and/or license server settings maybe stored in it. Note that temporary output files from starccm jobs runs may accumulate in hidden directories named `~/.star-version_number` consuming valuable quota space. These can be removed by periodically running `rm -ri ~/.starccm*` and replying yes when prompted.

## Slurm scripts

NibiFir/Narval/RorqualTrillium

**File :** starccm\_job-nibi-nogpu.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify some account
#SBATCH --time=00-01:00       # Time limit: dd-hh:mm
#SBATCH --nodes=1             # Specify 1 or more nodes
#SBATCH --cpus-per-task=16    # Specify cores per node (192 max)
#SBATCH --mem=64G             # Specify memory per node (0 max)
#SBATCH --ntasks-per-node=1   # Do not change this value
#SBATCH --constraint=granite  # Use intel compute nodes (no gpu)
#SBATCH --switches=1          # Use 1 network switch (optional)

module load StdEnv/2023

#module load starccm/20.04.007-R8    # Specify 18.04.009, 18.06.007, 19.04.009,
module load starccm-mixed/20.04.007  # 19.06.009, 20.02.008, 20.04.007 or newer
module list

SIM_FILE='mysample.sim'       # Specify your input sim filename
#JAVA_FILE='mymacros.java'    # Uncomment to specify an input java filename

# Comment the next line when using an institutional license server
LM_PROJECT='my22digitpodkey'  # Specify your Siemens Power on Demand (PoD) Key

# ------- no changes required below this line --------

slurm_hl2hl.py --format STAR-CCM+ > $SLURM_TMPDIR/machinefile
NCORE=$((SLURM_NNODES * SLURM_CPUS_PER_TASK * SLURM_NTASKS_PER_NODE))

echo "Checking $CDLMD_LICENSE_FILE ..."
server=$(head -n1 $CDLMD_LICENSE_FILE | awk '{print $2}')
port=$(cat $CDLMD_LICENSE_FILE | grep -Eo '[0-9]+$')
nmap $server -Pn -p $port | grep -v '^$'; echo

export FLEXIBLAS=StarMKL
echo "FLEXIBLAS=$FLEXIBLAS"
STAR_MPI="-mpi intel"
STAR_FABRIC="-fabric tcp"

if [ -n "$LM_PROJECT" ]; then
   echo "Siemens PoD license server ..."
   starccm+ -jvmargs -Xmx4G -jvmargs -Djava.io.tmpdir=$SLURM_TMPDIR -batch -power -podkey $LM_PROJECT -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $JAVA_FILE $SIM_FILE $STAR_MPI $STAR_FABRIC
else
   echo "Institutional license server ..."
   [ $(command -v lmutil) ] && lmutil lmstat -c ~/.licenses/starccm.lic -a | egrep "license1|UP|use|$USER"; echo
   starccm+ -jvmargs -Xmx4G -jvmargs -Djava.io.tmpdir=$SLURM_TMPDIR -batch -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $JAVA_FILE $SIM_FILE $STAR_MPI $STAR_FABRIC
fi

```

**File :** starccm\_job-fnr-nogpu.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify some account
#SBATCH --time=00-01:00       # Time limit: dd-hh:mm
#SBATCH --nodes=1             # Specify 1 or more nodes
#SBATCH --cpus-per-task=16    # Specify cores per node (192 max)
#SBATCH --mem=64G             # Specify memory per node (0 max)
#SBATCH --ntasks-per-node=1   # Do not change this value
##SBATCH --constraint=genoa   # Uncomment on rorqual (optional)

module load StdEnv/2023

#module load starccm/20.04.007-R8    # Specify 18.04.009, 18.06.007, 19.04.009,
module load starccm-mixed/20.04.007  # 19.06.009, 20.02.008, 20.04.007 or newer
module list

SIM_FILE='mysample.sim'       # Specify your input sim filename
#JAVA_FILE='mymacros.java'    # Uncomment to specify an input java filename

# Comment the next line when using an institutional license server
LM_PROJECT='my22digitpodkey'  # Specify your Siemens Power on Demand (PoD) Key

# ------- no changes required below this line --------

slurm_hl2hl.py --format STAR-CCM+ > $SLURM_TMPDIR/machinefile
NCORE=$((SLURM_NNODES * SLURM_CPUS_PER_TASK * SLURM_NTASKS_PER_NODE))

echo "Checking $CDLMD_LICENSE_FILE ..."
server=$(head -n1 $CDLMD_LICENSE_FILE | awk '{print $2}')
port=$(cat $CDLMD_LICENSE_FILE | grep -Eo '[0-9]+$')
nmap $server -Pn -p $port | grep -v '^$'; echo

export FLEXIBLAS=NETLIB
STAR_MPI="-mpi openmpi"
if [ "$RSNT_CPU_VENDOR_ID" == intel ]; then
  export FLEXIBLAS=StarMKL
  STAR_MPI="-mpi intel"
elif [ "$RSNT_CPU_VENDOR_ID" == amd ]; then
  export FLEXIBLAS=StarAOCL
fi
echo "FLEXIBLAS=$FLEXIBLAS"

if [ "${EBVERSIONSTARCCM:0:2}" -lt 20 ]; then
  STAR_FABRIC="-fabric ofi"
else 
  STAR_FABRIC="-fabric ucx" 
fi

if [ -n "$LM_PROJECT" ]; then
   echo "Siemens PoD license server ..."
   starccm+ -jvmargs -Xmx4G -jvmargs -Djava.io.tmpdir=$SLURM_TMPDIR -batch -power -podkey $LM_PROJECT -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $JAVA_FILE $SIM_FILE $STAR_MPI $STAR_FABRIC
else
   echo "Institutional license server ..."
   [ $(command -v lmutil) ] && lmutil lmstat -c ~/.licenses/starccm.lic -a | egrep "license1|UP|use|$USER"; echo
   starccm+ -jvmargs -Xmx4G -jvmargs -Djava.io.tmpdir=$SLURM_TMPDIR -batch -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $JAVA_FILE $SIM_FILE $STAR_MPI $STAR_FABRIC
fi

```

**File :** starccm\_job-trillium-nogpu.sh

```
#!/bin/bash

#SBATCH --account=def-group   # Specify some account
#SBATCH --time=00-01:00       # Time limit: dd-hh:mm
#SBATCH --nodes=1             # Specify 1 or more nodes
#SBATCH --cpus-per-task=192   # Specify cores per node (192 max)
#SBATCH --mem=0               # Specify memory per node (0 max)
#SBATCH --ntasks-per-node=1   # Do not change this value

module load StdEnv/2023

#module load starccm/20.04.007-R8    # Specify 18.04.009, 18.06.007, 19.04.009,
module load starccm-mixed/20.04.007  # 19.06.009, 20.02.008, 20.04.007 or newer
module list

SIM_FILE='mysample.sim'       # Specify input sim filename
#JAVA_FILE='mymacros.java'    # Uncomment to specify an input java filename

# Comment the next line when using an institutional license server
LM_PROJECT='my22digitpodkey'  # Specify your Siemens Power on Demand (PoD) Key

# These settings are used instead of your ~/.licenses/starccm.lic
# (settings shown will use the cd-adapco pod license server)
FLEXPORT=1999                    # Specify server static flex port
VENDPORT=2099                    # Specify server static vendor port
LICSERVER=flex.cd-adapco.com     # Specify license server hostname

# ------- no changes required below this line --------

export CDLMD_LICENSE_FILE="$FLEXPORT@127.0.0.1"
ssh tri-gw -L $FLEXPORT:$LICSERVER:$FLEXPORT -L $VENDPORT:$LICSERVER:$VENDPORT -N -f

slurm_hl2hl.py --format STAR-CCM+ > $SLURM_TMPDIR/machinefile
NCORE=$((SLURM_NNODES * SLURM_CPUS_PER_TASK * SLURM_NTASKS_PER_NODE))

export FLEXIBLAS=StarAOCL
echo "FLEXIBLAS=$FLEXIBLAS"
STAR_MPI="-mpi openmpi"
 
# Workaround for license failures: 
# until the exit status is equal to 0, we try to get Star-CCM+ to start (here, for at least 5 times).
i=1
RET=-1
while [ $i -le 5 ] && [ $RET -ne 0 ]; do
        [ $i -eq 1 ] || sleep 5
          echo "Attempt number: "$I
          if [ -n "$LM_PROJECT" ]; then
          echo "Siemens PoD license server ..."
          starccm+ -jvmargs -Xmx4G -jvmargs -Djava.io.tmpdir=$SLURM_TMPDIR -batch -power -podkey $LM_PROJECT -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $JAVA_FILE $SIM_FILE $STAR_MPI
        else
          echo "Institutional license server ..."
          starccm+ -jvmargs -Xmx4G -jvmargs -Djava.io.tmpdir=$SLURM_TMPDIR -batch -np $NCORE -nbuserdir $SLURM_TMPDIR -machinefile $SLURM_TMPDIR/machinefile $JAVA_FILE $SIM_FILE $STAR_MPI
        fi
        RET=$?
        i=$((i+1))
done
exit $RET

```

# Graphical use

To run starccm+ in graphical mode it is recommended to use an [OnDemand](https://docs.alliancecan.ca/wiki/Nibi#Access_through_Open_OnDemand_(OOD)) or JupyterLab system to start a remote desktop. In addition to configuring `~/.licenses/starccm.lic` research groups with a POD license should also run `export LM_PROJECT='CD-ADAPCO PROJECT ID'`and optionally append **-power** to the list of command `starccm+` line options below. Note that `module avail starccm-mixed` will display which starccm versions are available within the StdEnv/version that you currently have loaded. Alternatively running `module spider starccm-mixed` will show all available starccm module versions available within all StdEnv module versions.

## OnDemand

1. Connect to an OnDemand system using one of the following URLs in your laptop browser :

```
NIBI: https://ondemand.sharcnet.ca
FIR: https://jupyterhub.fir.alliancecan.ca
NARVAL:  https://portail.narval.calculquebec.ca/
RORQUAL: https://jupyterhub.rorqual.alliancecan.ca
TRILLIUM: https://ondemand.scinet.utoronto.ca

```

2. Open a new terminal window in your desktop and run one of:

:   **STAR-CCM+ 18.04.008 (or newer versions)**

    :   `module load StdEnv/2023` (default)
    :   `module load starccm-mixed/20.04.007` \*\*OR\*\* `starccm/20.04.007-R8`
    :   starccm+ -rr server
:   **STAR-CCM+ 15.04.010** --> **18.02.008 (version range)**

    :   `module load StdEnv/2020` (unsupported)
    :   `module load starccm-mixed/15.04.010` \*\*OR\*\* `starccm/15.04.010-R8`
    :   starccm+ -mesa

## VncViewer

1. Connect with a VncViewer client to a login or compute node by following [TigerVNC](VNC.md)  
2. Open a new terminal window in your desktop and run one of:

:   **STAR-CCM+ 18.04.008 (or newer versions)**

    :   `module load StdEnv/2023` (default)
    :   `module load starccm-mixed/20.04.007` \*\*OR\*\* `starccm/20.04.007-R8`
    :   starccm+ -rr server
:   **STAR-CCM+ 15.04.010** --> **18.02.008 (version range)**

    :   `module load StdEnv/2020` (unsupported)
    :   `module load starccm-mixed/17.02.007` \*\*OR\*\* `starccm/17.02.007-R8`
    :   starccm+