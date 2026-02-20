# FreeSurfer

Other languages:

- English
- [français](FreeSurfer_fr.md)

# Introduction

[FreeSurfer](https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferWiki) is a set of tools for the analysis and visualization of structural and functional brain imaging data. FreeSurfer contains a fully automatic structural imaging stream for processing cross sectional and longitudinal data.

# FreeSurfer 5.3 as a global module

In our software stack, you may load the `freesurfer/5.3.0` module.

FreeSurfer comes up with a script `FreeSurferEnv.sh` that should be sourced to correctly set up environment variables such as PATH and PERL5LIB:

```
[name@server ~]$ module load freesurfer/5.3.0
[name@server ~]$ source $EBROOTFREESURFER/FreeSurferEnv.sh

```

# FreeSurfer 6.0 and newer versions

Due to a change in the [license terms](https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferSoftwareLicense), we **no longer** install the code as a central module. If needed, please install it in your /home directory or in your /project space with EasyBuild. Please follow the instructions below and if needed, contact the [technical support](Technical_Support.md) for assistance.

## Download the software

Select a version (6.0.0 or newer) in the [download repository](https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/) and download the corresponding `freesurfer-Linux*vX.Y.Z.tar.gz` archive on your favorite cluster.

## Installation in your /home directory with EasyBuild

The following procedure will install FreeSurfer 6.0.0 in `/home/$USER/.local/easybuild/software/2020/Core/freesurfer/6.0.0/`. The installation requires some memory and due to the restrictions of memory stack size on the login nodes on our clusters, the installation may fail because of the memory. To overcome this issue, you may need to use an [interactive job](Scheduler.md#Interactive_jobs) by asking for enough memory (8 GB or so) to install the code.

1. Go to the folder that contains the `freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.0.tar.gz` archive.
2. Unload all modules with `module purge`.
3. Install with [EasyBuild](EasyBuild.md) using `eb FreeSurfer-6.0.0-centos6_x86_64.eb --disable-enforce-checksums`.
4. Register for the FreeSurfer license key [[1]](https://surfer.nmr.mgh.harvard.edu/registration.html).
5. Your user license will have to go in

```
[name@server ~]$ module load freesurfer/6.0.0
[name@server ~]$ cd $FREESURFER_HOME

```

Use nano or any other text editor of your choice and create a file `/home/$USER/.license` and add the license text (example):

```
name.name@university.ca
12345
*A1BCdEfGHiJK
ABCd0EFgHijKl

```

To load the private module:
`module load freesurfer/6.0.0`

As of August 2020, we were supporting up to version 6.0.1. You can check for [newer versions here](https://github.com/ComputeCanada/easybuild-easyconfigs/tree/computecanada-master/easybuild/easyconfigs/f/FreeSurfer).

## EasyBuild recipes

You can check the EasyBuild recipes for FreeSurfer [online](https://github.com/ComputeCanada/easybuild-easyconfigs/tree/computecanada-master/easybuild/easyconfigs/f/FreeSurfer) on GitHub or via a command line ,`eb -S FreeSurfer`, from any of our clusters. If the version you are looking for is not listed, you may try to install the program with the option `--try-software-version=<the new version>`. If that did not work, please contact the [technical support](Technical_Support.md) for help.

## Installation in a shared folder

Using EasyBuild, it is possible to install the program in a shared location (like /project) and make the code available for any other member of the group. The following will install FreeSurfer under the directory `/home/$USER/projects/def-someuser/$USER/software` and the module under the user's directory `/home/$USER/.local/easybuild/modules/2020/Core/freesurfer`.

```
newgrp def-someuser
installdir=/home/$USER/projects/def-someuser/$USER
moduledir=/home/$USER/.local/easybuild/modules/2020
pathtosrc=/home/$USER/software
eb FreeSurfer-6.0.1-centos6_x86_64.eb --installpath-modules=${moduledir} --prefix=${installdir} --sourcepath=${pathtosrc}

```

If it complains about **checksums**, add the option `--disable-enforce-checksums` to the `eb` command.

To make the program accessible for all members of the group, two more steps are required:

- You need to give all members of your group read and exec access to the installation directory `/home/$USER/projects/def-someuser/$USER`. To see how to give them access to this directory, please read [Changing the permissions of existing files](Sharing_data.md#Changing_the_permissions_of_existing_files).
- Each member of the group will need to put the module file in their own /home directories. The module file `6.0.1.lua` is located under the directory:

```
/home/$USER/.local/easybuild/modules/2020/Core/freesurfer/</code>

```

Each member of the group will need to create the directory `/home/$USER/.local/easybuild/modules/2020/Core/freesurfer` where they will put the file `6.0.1.lua`:

```
[name@server ~]$ mkdir -p /home/$USER/.local/easybuild/modules/2020/Core/freesurfer
[name@server ~]$ cp 6.0.1.lua /home/$USER/.local/easybuild/modules/2020/Core/freesurfer/

```

The above will set the module (only the module file that points to the installation directory under /project) in their own directory.

The module can be loaded from their own accounts using:

```
[name@server ~]$ module load freesurfer/6.0.1

```

## Hippocampus and brainstem processing

To perform processing of the hippocampus and brainstem, download and install MATLAB runtime 2012b from the FreeSurfer website:

```
module load freesurfer/6.0.0
cd $FREESURFER_HOME
curl "http://surfer.nmr.mgh.harvard.edu/fswiki/MatlabRuntime?action=AttachFile&do=get&target=runtime2012bLinux.tar.gz" -o "matlab_runtime2012bLinux.tar.gz"
tar xvf matlab_runtime2012bLinux.tar.gz 

```

## Example of working batch script for FreeSurfer version >= 6.0.0

**File :** mysub.sh

```
#!/bin/bash

#SBATCH --account=def-someuser
#SBATCH --mem=16G
#SBATCH --time=10:00:00

# Load the module:

module load freesurfer/6.0.0

# set the variables:

export SUBJECTS_DIR=<User_Defined_DIR>
source $EBROOTFREESURFER/FreeSurferEnv.sh

echo "Starting run at: `date`"

recon-all command

echo "Program finished with exit code $? at: `date`"

```

## Examples of required walltimes

- recon-all -all : `#SBATCH --time=08:00:00`
- recon-all -qcache : `#SBATCH --time=00:20:00`
- recon-all -base -tp1 -tp2 : `#SBATCH --time=10:00:00`
- recon-all -long subjid -base base : `#SBATCH --time=10:00:00`
- recon-all -hippocampal-subfields-T1 : `#SBATCH --time=00:40:00`
- recon-all -brainstem-structures: `#SBATCH --time=00:30:00`