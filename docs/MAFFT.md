# MAFFT

Other languages:

- English
- [français](MAFFT_fr.md)

[MAFFT](https://mafft.cbrc.jp/alignment/software/) is a multiple sequence alignment program for unix-like operating systems. It offers a range of multiple alignment methods, L-INS-i (accurate; for alignment of <∼200 sequences), FFT-NS-2 (fast; for alignment of <∼30,000 sequences), etc.

## Single node

MAFFT can benefit from multiple cores on a single node. For more information: [https://mafft.cbrc.jp/alignment/software/multithreading.html](https://mafft.cbrc.jp/alignment/software/multithreading.html)

**Note**: The MAFFT\_TMPDIR is set to $SLURM\_TMPDIR/maffttmp when you load the module.

**File :** mafft\_submit.sh

```
#!/bin/bash

#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=0

module load gcc/9.3.0 mafft

mafft --globalpair --thread $SLURM_CPUS_PER_TASK input > output

```

## Multiple nodes (MPI)

MAFFT can use MPI to align a large number of sequences: [https://mafft.cbrc.jp/alignment/software/mpi.html](https://mafft.cbrc.jp/alignment/software/mpi.html)

**Note**: MAFFT\_TMPDIR is set to $SCRATCH/maffttmp when you load the module.
If you change this temporary directory, it must be shared by all hosts.

**File :** mafft\_mpi\_submit.sh

```
#!/bin/bash

#SBATCH --time=04:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G

module load gcc/9.3.0 mafft-mpi

srun mafft --mpi --large --globalpair --thread $SLURM_CPUS_PER_TASK input > output

```