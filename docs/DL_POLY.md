# DL POLY

Other languages:

- English
- [français](DL_POLY_fr.md)

# General

DL\_POLY is a general purpose classical molecular dynamics (MD) simulation software. It provides scalable performance from a single processor workstation to a high performance parallel computer. DL\_POLY\_4 offers fully parallel I/O as well as a NetCDF alternative to the default ASCII trajectory file.

There is a mailing list [here.](https://www.jiscmail.ac.uk/cgi-bin/webadmin?A0=DLPOLY)

# License limitations

**DL\_POLY** is now [open source](https://gitlab.com/DL%20POLY%20Classic/dl%20poly) and it does not require registration. A new module **dl\_poly4/5.1.0** is already installed under **StdEnv/2023** and it is accessible for all users. However, if you would like to use the previous versions (**dl\_poly4/4.10.0** and/or **dl\_poly4/4.08**), you should contact [support](Technical_Support.md) and ask to be added to the POSIX group that controls access to DL\_POLY4. There is no need to register on DL\_POLY website.

# Modules

To see which versions of DL\_POLY are installed on our systems, run `module spider dl_poly4`. See [Using modules](Utiliser_des_modules.md) for more about `module` subcommands.

To load the version **5.x**, use:

`module load StdEnv/2023 intel/2023.2.1 openmpi/4.1.5 dl_poly4/5.1.0`

To load the previous version 4.10.0, use:

`module load StdEnv/2023 intel/2020.1.217 openmpi/4.0.3 dl_poly4/4.10.0`

Note that this version requires to be added to a POSIX group as explained above in  License limitations.

We do not currently provide a module for the Java GUI interface.

# Scripts and examples

The input files shown below (CONTROL and FIELD) were taken from example TEST01 that can be downloaded from the page of [DL\_POLY examples](ftp://ftp.dl.ac.uk/ccp5/DL_POLY/DL_POLY_4.0/DATA/).

To start a simulation, one must have at least three files:

- **CONFIG**: simulation box (atomic coordinates)
- **FIELD**: force field parameters
- **CONTROL**: simulation parameters (time step, number of MD steps, simulation ensemble, ...etc.)

CONTROLFIELDSerial jobMPI job

**File :** CONTROL

```
SODIUM CHLORIDE WITH (27000 IONS)

restart scale
temperature           500.0
equilibration steps   20
steps                 20
timestep              0.001

cutoff                12.0
rvdw                  12.0
ewald precision       1d-6  

ensemble nvt berendsen 0.01

print every           2
stats every           2
collect
job time              100
close time            10

finish
```

**File :** FIELD

```
SODIUM CHLORIDE WITH EWALD SUM (27000 IONS)
units internal
molecular types 1
SODIUM CHLORIDE
nummols 27
atoms 1000
Na+          22.9898         1.0  500
Cl-           35.453        -1.0  500
finish
vdw    3 
Na+     Na+     bhm      2544.35      3.1545      2.3400   1.0117e+4   4.8177e+3
Na+     Cl-     bhm      2035.48      3.1545      2.7550   6.7448e+4   8.3708e+4
Cl-     Cl-     bhm      1526.61      3.1545      3.1700   6.9857e+5   1.4032e+6
close
```

**File :** run\_serial\_dlp.sh

```
#!/bin/bash

#SBATCH --account=def-someuser
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2500M      # memory; default unit is megabytes.
#SBATCH --time=0-00:30           # time (DD-HH:MM).

# Load the module:

module load StdEnv/2023  
module load intel/2023.2.1  openmpi/4.1.5 dl_poly4/5.1.0

echo "Starting run at: `date`"

dlp_exec=DLPOLY.Z

${dlp_exec}

echo "Program finished with exit code $? at: `date`"

```

**File :** run\_mpi\_dlp.sh

```
#!/bin/bash

#SBATCH --account=def-someuser
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem-per-cpu=2500M      # memory; default unit is megabytes.
#SBATCH --time=0-00:30           # time (DD-HH:MM).

# Load the module:

module load StdEnv/2023  
module load intel/2023.2.1  openmpi/4.1.5 dl_poly4/5.1.0

echo "Starting run at: `date`"

dlp_exec=DLPOLY.Z

srun ${dlp_exec}

echo "Program finished with exit code $? at: `date`"

```

# Related software

- [VMD](VMD.md)
- [LAMMPS](LAMMPS.md)