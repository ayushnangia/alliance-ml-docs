# Open Babel

Other languages:

- English
- [français](Open_Babel_fr.md)

## General

[Open Babel](https://openbabel.org/) is a chemical toolbox designed to speak the many languages of chemical data.
It's an open, collaborative project allowing anyone to search, convert, analyze, or store data from molecular modeling, chemistry, solid-state materials, biochemistry, or related areas.

For further information on how to use Open Babel, please refer to the
[Open Babel User Guide](https://openbabel.org/docs/).

On our clusters we have two kinds of modules for Open Babel installed:

## `openbabel`

This is the serial version of Open Babel which can safely be used even on login nodes to convert chemical structure files between different formats.
This is the right module for most users.

#### Example

```
[user@login1]$ module load openbabel
[user@login1]$ wget "https://www.chemspider.com/FilesHandler.ashx?type=str&3d=yes&id=171" -O acetic_acid.mol
[user@login1]$ obabel  -i mol  acetic_acid.mol  -o pdb  -O acetic_acid.pdb

```

Notes:

- The `wget` command downloads `acetic_acid.mol` as an example file.
- The `obabel` command converts the molecule described in 'acetic\_acid.mol' from `.mol` format to `.pdb` format.

## `openbabel-omp`

This is the version of Open Babel which has OpenMP parallelization enabled.

| This module should not be used on login nodes, because even for simple tasks it will create as many threads as it detects CPUs on the machine, in turn causing load-spikes which will be disruptive for other users. |
| --- |

The parallel version of Open Babel is useful when converting very large numbers of molecule structures or
calculating large numbers of cheminformatics descriptors for multiple molecules.

Make sure to set the environment variable `OMP_NUM_THREADS`
in order to tell Open Babel how many CPUs it is allowed to use.

#### Example

The following job takes the [Structural Data File](https://en.wikipedia.org/wiki/Chemical_table_file#SDF) `many_molecules.sdf`,
which in this case should contain a database with many molecules, and generates Canonical [SMILES](https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system) representations for each of them, using two CPU-cores.

**File :** parallel\_openbabel\_job.sh

```
#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=1000M
module load openbabel-omp
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-1}"

obabel  -i sdf  many_molecules.sdf  -o can  -O many_canonical_smiles.txt

```

## Python

Open Babel's functionality can be used from other languages such as Python.
The [Python interface for Open Babel](https://openbabel.org/docs/UseTheLibrary/Python.html) has been added to the both `openbabel` and `openbabel-omp` modules as extensions.
Therefore both the `openbabel` and `pybel` packages can be used after loading both `openbabel` and a compatible Python module.

#### Example

```
$ module load python/3.11 openbabel/3.1.1
$ python
Python 3.11.5 (main, Sep 19 2023, 19:49:15) [GCC 11.3.0] on linux
>>> import openbabel
>>> print(openbabel.__version__)
3.1.1.1
>>> from openbabel import pybel
>>>

```