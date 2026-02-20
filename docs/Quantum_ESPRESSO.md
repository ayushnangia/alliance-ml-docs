# Quantum ESPRESSO

Other languages:

- English
- [français](Quantum_ESPRESSO_fr.md)

:   "*Quantum ESPRESSO is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials modeling at the nanoscale. It is based on density-functional theory, plane waves, and pseudopotentials.*
:   [...]

:   *Quantum ESPRESSO has evolved into a distribution of independent and inter-operable codes in the spirit of an open-source project. The Quantum ESPRESSO distribution consists of a “historical” core set of components, and a set of plug-ins that perform more advanced tasks, plus a number of third-party packages designed to be inter-operable with the core components.*[1]

# Usage

To use Quantum ESPRESSO, you need to load a module (see [Using modules](Utiliser_des_modules.md)). You can see available versions using `module avail quantumespresso` or `module spider quantumespresso`, and load one with (for example), `module load quantumespresso/6.6`.

**File :** qe\_ex1.sh

```
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --time=0-1:00           # DD-HH:MM
#SBATCH --nodes=1
#SBATCH --tasks-per-node=32     # MPI tasks
#SBATCH --mem=0                 # all memory on node
module load StdEnv/2020  intel/2020.1.217  openmpi/4.0.3
module load quantumespresso/6.6
srun pw.x < si.scf.in > si.scf.out

```

The above example requests 32 processes, which is more than needed for the silicon tutorial case. Please be aware that suitable selection of a process count is complicated, but it is your responsibility to choose an efficient number. See also [Advanced MPI scheduling](Advanced_MPI_scheduling.md).

# Known problems

## No pseudopotential files

There is no system-wide repository of pseudopotentials for Quantum ESPRESSO on our clusters. You must find or create and store your own pseudopotential files.

## Parameter error in Grimme-D3

Incorrect results may be obtained when running Grimme-D3 with the element barium (Ba).
The error comes from an incorrect value for one of the coefficients for barium,
specifically, the r2r4 parameter in the source code file `dft-d3/core.f90`.
The correct value should be 10.15679528, not 0.15679528.
The error has been confirmed by the QE developers to exist in all versions from 6.2.1 to 7.1.
[2]

1. ↑ [Quantum ESPRESSO web site](http://www.quantum-espresso.org/).
2. ↑ ["Wrong r2r4 value for Ba in the dft-d3 code", Quantum ESPRESSO mailing list, 2022 July 9](https://www.mail-archive.com/users@lists.quantum-espresso.org/msg42277.html).