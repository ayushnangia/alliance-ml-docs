# OpenMolcas

## Introduction

[OpenMolcas](https://github.com/Molcas/OpenMolcas) is a quantum chemistry software package. It includes programs to apply many different electronic structure methods to chemical systems, but its key feature is the multiconfigurational approach, with methods like CASSCF and CASPT2.

OpenMolcas is not a fork or reimplementation of Molcas, it is a large part of the Molcas codebase that has been released as free and open-source software (FOSS) under the Lesser General Public License (LGPL). Some parts of Molcas remain under a different license by decision of their authors (or impossibility to reach them), and are therefore not included in OpenMolcas.

## Running OpenMolcas on national clusters

The `OpenMolcas` module is installed on national clusters. To check what versions are available use the `module spider` command as follows:

```
[name@server $] module spider openmolcas

```

For module commands, please see [Using modules](Utiliser_des_modules.md).

### Job submission

The national clusters use the Slurm scheduler; for details about submitting jobs, see [Running jobs](Scheduler.md).

#### Example script for serial OpenMolcas job

Currently only serial job works for OpenMolcas. OpenMolcas's parallel implementation uses Global Array which does not work on the clusters.

**File :** PrO2\_serial.sh

```
#!/bin/bash
#SBATCH --account=def-pi          # change this to your own account
#SBATCH --ntasks=1                # 1 process/cpu
#SBATCH --time=01-00:00           # runtime (DD-HH:MM)
#SBATCH --output=PrO2_serial.log  # output
#SBATCH --mem-per-cpu=3000        # memory per cpu in MB

module load openmolcas/20.10

export MOLCAS_NPROCS=1       # serial (1 cpu) openmolcas job
export MOLCAS_MEM=2000       # normally ~75% of the physical memory defined in --mem-per-cpu 
export MOLCAS_WorkDir=/PATH to the input and .sh file directory
export MOLCASDISK=0
export MOLCASRAMD=0
export MOLCAS_MOLDEN=ON

pymolcas PrO2.inp            # PrO2.inp is the input file

```

#### Example input file for PrO2.inp

**File :** PrO2.inp

```
// This module sets up the structure and basis sets etc.
&GATEWAY  
  AMFI    // Requests Atomic Mean Field Integrals for SOC
  Coord
  3

  Pr1.ANO-RCC-VTZP       0.0000000       0.0000000       0.0000000
  O1.ANO-RCC-VDZP       0.0000000       0.0000000      -1.8000000
  O2.ANO-RCC-VDZP       0.0000000       0.0000000       1.8000000
  Angmom= 0.0 0.0 0.0 ANGSTROM // Sets origin of orbital angular momentum - should be same as metal atom
  group= NoSym

// This module performs all the one and two electron integrals for the given strucutre and basis sets
&SEWARD
  High Cholesky  // Approximation for two-electron integrals

// This module is to do a CASSCF or RASSCF calculation
&RASSCF
  Spin= 3    // Spin multiplicity
  Charge= -1
  CiRoot= 21 21 1  // How many states are you calculting
  ORBA= FULL   // Print option
  MAXORB= 1    // Print option
  Nactel= 2 0 0   // How many electrons in Ras2 (active space), holes in Ras1, electrons in Ras3
  RAS2= 7   // Size of complete active space
>> COPY $Project.JobIph 1_IPH
>> COPY $Project.RasOrb 1.RasOrb

&RASSCF
  Typeindex   // Read nature of active space from orbital file
  Spin= 1
  Charge= -1
  FILEORB= 1.RasOrb   // Give a set of input orbitals, should read from previous output
  CiRoot= 28 28 1
  ORBA= FULL
  MAXORB= 1
  Nactel= 2 0 0
>> COPY $Project.JobIph 2_IPH
>> COPY $Project.RasOrb 2.RasOrb

// This module performs a state interaction calculation between multiple CASSCF states of different spin
&RASSI
  SPIN   // Turn on SOC
  MEES   // Print matrix elements
  EPRG= 7.0D-1   // Calculate g-values
  Nr of JobIph= 2 21 28   // How many input files, how many states in each, which states in each
  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
  IPHN   // Names of input files
  1_IPH
  2_IPH
  PROP   // Print out orbital angular momentum operators
  3
  'ANGMOM' 1
  'ANGMOM' 2
  'ANGMOM' 3

// The single aniso module can calculate magnetic properties - we don't use it anymore, but I've put it in here to show you how to use it
&SINGLE_ANISO
  CRYS= pr   // Determine CF parameters
  TINT= 0.0  330.0  330  0.0001   // Susceptibility temperatures
  HINT= 0.0  10.0  201   // Magnetisation fields
  TMAG= 6 1.8 2 4 5 10 20   // Magnetisation temperatures

```