# Parasail

Other languages:

- English
- [français](Parasail_fr.md)

[parasail](https://github.com/jeffdaily/parasail) is a SIMD C (C99) library containing implementations of the Smith-Waterman (local), Needleman-Wunsch (global), and various semi-global pairwise sequence alignment algorithms.

| From StdEnv/2023 onwards, the parasail-python extension is bundled in the parasail module. However, with StdEnv/2020, the parasail module needs to be loaded for the Python extension to be installed in a virtual environment. |
| --- |

# Usage

Find the required versions using

```
[name@server ~]$ module spider parasail

```

and load the library using

```
[name@server ~]$ module load parasail/2.6.2

```

## parasail\_aligner Example

When using the binary parasail\_aligner, it is important to set the number of threads according to the number of cores allocated in our job. We can set it with

```
parasail_aligner -t ${SLURM_CPUS_PER_TASK:-1} ...}}

```

## Python extension

The module contains bindings for multiple Python versions.
To discover which are the compatible Python versions, run

```
[name@server ~]$ module spider parasail/1.3.4

```

### Usage

1. Load the required modules.

```
[name@server ~]$ module load parasail/2.6.2 python/3.11 scipy-stack/2023b

```

2. Import parasail 1.3.4.

```
[name@server ~]$ python -c "import parasail"

```

If the command displays nothing, the import was successful.

### Example

Run a quick local alignment score comparison between BioPython and parasail.

1. Write the Python script:

**File :** parasail-sw.py

```
import parasail
from Bio.Align import PairwiseAligner

A = "ACGT" * 1000

# parasail
matrix = parasail.matrix_create("ACGT", 1, 0)
parasail_score = parasail.sw(A, A, 1, 1, matrix).score

# biopython
bio_score = PairwiseAligner().align(A, A)[0].score

print('parasail:', parasail_score)
print('biopython:', bio_score)

```

2. Write the job submission script:

Default StdEnvStdEnv/2020

**File :** submit-parasail.sh

```
#!/bin/bash
#SBATCH --account=def-someuser  # replace with your PI account
#SBATCH --cpus-per-task=1 
#SBATCH --mem-per-cpu=3G      # increase as needed
#SBATCH --time=1:00:00

module load parasail/2.6.2 python/3.11 scipy-stack/2023b

# Install any other requirements, such as Biopython
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index biopython==1.83

python parasail-sw.py

```

2.1. Identify available wheels first :

```
[name@server ~]$ avail_wheel parasail
name      version    python    arch
--------  ---------  --------  -------
parasail  1.2.4      py2,py3   generic

```

Install the desired version in your virtual environment:

**File :** submit-parasail.sh

```
#!/bin/bash
#SBATCH --account=def-someuser  # replace with your PI account
#SBATCH --cpus-per-task=1 
#SBATCH --mem-per-cpu=3G      # increase as needed
#SBATCH --time=1:00:00

module load StdEnv/2020 gcc parasail/2.5 python/3.10

# Install any other requirements, such as Biopython:
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index parasail==1.2.4 biopython==1.83

python parasail-sw.py

```

3. Submit the job with

```
[name@server ~]$ sbatch submit-parasail.sh

```

4. When the job has run, the output will be in the Slurm output file:

```
[name@server ~]$ less slurm-*.out
parasail: 4000
biopython: 4000.0

```

#### Available Python packages

Other Python packages that depend on parasail will have their requirement satisfied by loading the parasail module:

```
[name@server ~]$ pip list | grep parasail
parasail                           1.3.4

```