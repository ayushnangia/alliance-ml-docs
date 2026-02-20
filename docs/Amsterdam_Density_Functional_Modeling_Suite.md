# ADF

Other languages:

- English
- [français](ADF_fr.md)

## Introduction

**Important:** ADF has been renamed to AMS since the 2020 version. Significant changes such as the input and output formats have been made in the new AMS. Please refer to [AMS](AMS.md) for more information.

The [SCM (Software for Chemistry and Materials) Amsterdam Modeling Suite](https://www.scm.com/) originally the ADF (Amsterdam Density Functional) Modeling Suite, offers powerful computational chemistry tools for many research areas such as homogeneous and heterogeneous catalysis, inorganic chemistry, heavy element chemistry, various types of spectroscopy, and biochemistry.

Compute Canada users have access to the following products:

- ADF
- ADF-GUI
- BAND
- BAND-GUI
- DFTB
- ReaxFF
- COSMO-RS
- QE-GUI
- NBO6

## Running SCM on Graham

The `adf` module is installed only on [Graham](Graham.md) due to license restrictions. To check what versions are available use the `module spider` command as follows:

```
[name@server $] module spider adf

```

For module commands, please see [Using modules](Utiliser_des_modules.md).

### Job submission

Graham uses the Slurm scheduler; for details about submitting jobs, see [Running jobs](Scheduler.md).

#### Single ADF or BAND run

This mysub.sh script is for a whole-node job. The last two lines load version 2019.305 and call ADF directly.

**File :** mysub.sh

```
#!/bin/bash
#SBATCH --nodes=1 --ntasks-per-node=32  # 1 node with 32 cpus, you can modify it
#SBATCH --mem=0                         # request all memory on node
#SBATCH --time=00-03:00                 # time (DD-HH:MM)
#SBATCH --output=adf_test-%j.log        # output file

module unload openmpi
module load adf/2019.305
ADF adf_test.inp

```

This is the input file used in the script:

**File :** adf\_test.inp

```
Title WATER Geometry Optimization with Delocalized Coordinates

 Atoms
    O             0.000000     0.000000     0.000000
    H             0.000000    -0.689440    -0.578509
    H             0.000000     0.689440    -0.578509
 End

 Basis
 Type TZP
 Core Small
 End

 Geometry
  Optim Deloc
  Converge 0.0000001
 End

 End Input

```

#### Multiple ADF or BAND runs

Multiple calculations can be combined into a single job by creating a input file such as this:

**File :** GO\_H2O.run

```
#!/bin/bash
if test -z "$SCM_TESTOUTPUT" ; then SCM_TESTOUTPUT=GO_H2O.out; fi

$ADFBIN/adf << eor > $SCM_TESTOUTPUT
Title WATER Geometry Optimization with Delocalized Coordinates

Atoms
   O             0.000000     0.000000     0.000000
   H             0.000000    -0.689440    -0.578509
   H             0.000000     0.689440    -0.578509
End

Basis
Type TZP
Core Small
End

Geometry
 Optim Deloc
 Converge 0.0000001
End

End Input
eor

rm TAPE21 logfile
$ADFBIN/adf << eor >> $SCM_TESTOUTPUT
Title WATER Geometry Optimization in Cartesians with new optimizer

Atoms
    O             0.000000     0.000000     0.000000
    H             0.000000    -0.689440    -0.578509
    H             0.000000     0.689440    -0.578509
End

Basis
 Type TZP
 Core Small
End

Geometry
  Optim Cartesian
  Branch New
  Converge 0.0000001
End

End Input
eor

rm TAPE21 logfile
$ADFBIN/adf << eor >> $SCM_TESTOUTPUT
Title WATER Geometry Optimization with Internal Coordinates

Atoms    Z-Matrix
 1. O   0 0 0
 2. H   1 0 0   rOH
 3. H   1 2 0   rOH  theta
End

Basis
 Type TZP
 Core Small
End

GeoVar
 rOH=0.9
 theta=100
End
Geometry
  Converge 0.0000001
End

End Input
eor

rm TAPE21 logfile
$ADFBIN/adf << eor >> $SCM_TESTOUTPUT
Title WATER   optimization with (partial) specification of Hessian

Atoms    Z-Matrix
 1. O   0 0 0
 2. H   1 0 0   rOH
 3. H   1 2 0   rOH  theta
End

GeoVar
 rOH=0.9
 theta=100
End
HessDiag  rad=1.0  ang=0.1

Fragments
 H   t21.H
 O   t21.O
End

Geometry
  Converge 0.0000001
End

End Input
eor

rm TAPE21 logfile
$ADFBIN/adf << eor >> $SCM_TESTOUTPUT
Title WATER Geometry Optimization in Cartesians

Geometry
  Optim Cartesian
  Converge 0.0000001
End

Define
 rOH=0.9
 theta=100
End

Atoms    Z-Matrix
 1. O   0 0 0
 2. H   1 0 0   rOH
 3. H   1 2 0   rOH theta
End

Fragments
 H   t21.H
 O   t21.O
End

End Input
eor

mv TAPE21 H2O.t21

```

The following slurm script is identical to the one used for a single run (mysub.sh), except the last line calls the GO\_H2O.run script, instead of ADF.

**File :** GO\_H2O.sh

```
#!/bin/bash
#SBATCH --nodes=1 --ntasks-per-node=32  # 1 node with 32 cpus, you can modify it
#SBATCH --mem=0                         # request all memory on node
#SBATCH --time=00-03:00                 # time (DD-HH:MM)
#SBATCH --output=GO_H2O_%j.log          # output file

module unload openmpi
module load adf/2019.305
bash GO_H2O.run                         # run the shell script

```

### Examples

Example input/output for ADF can be found on Graham under

```
/home/jemmyhu/tests/test_ADF/2019.305/test_adf/

```

The same procedure applies to BAND jobs, see band\_test.inp and band\_test.sh examples under

```
/home/jemmyhu/tests/test_ADF/2019.305/test_band/

```

## Running SCM-GUI

Rendering over an SSH connection with X11 forwarding is very slow for GUI applications such as ADF-GUI. We recommend you use [VNC](VNC.md) to connect if you will be running ADF-GUI.

### Graham

ADF can be run interactively in graphical mode on a Graham compute node (3hr time limit) over TigerVNC with these steps:

1. [Install a TigerVNC](VNC.md#Setup) client on your desktop
2. [Connect](VNC.md#Compute_Nodes) to a compute node with vncviewer
3. `module load adf`
4. `adfinput`

### Gra-vdi

Adf can be run interactively in graphical mode on gra-vdi (no connection time limit) over TigerVNC with these steps:

1. [Install a TigerVNC](VNC.md#Setup) client on your desktop
2. [Connect](VNC.md#VDI_Nodes) to gra-vdi.computecanada.ca with vncviewer
3. `module load clumod`
4. `module load adf`
5. `adfinput`

A tutorial pdf showing how to install, connect and run ADF-GUI using TigerVNC on gra-vdi can be found
[here](https://www.sharcnet.ca/~jemmyhu/TigerVNC-for-ADF-GUI.pdf).

### Locally

SCM has a separate license to run ADF-GUI on a local desktop machine. If you are interested contact license@scm.com to purchase your own license.