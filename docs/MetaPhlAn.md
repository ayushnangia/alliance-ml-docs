# MetaPhlAn

Other languages:

- English
- [français](MetaPhlAn_fr.md)

MetaPhlAn is a "computational tool for profiling the composition of microbial communities (Bacteria, Archaea and Eukaryotes) from metagenomic shotgun sequencing data (i.e. not 16S) with species-level. With StrainPhlAn, it is possible to perform accurate strain-level microbial profiling", according to its [GitHub repository](https://github.com/biobakery/MetaPhlAn). While the software stack on our clusters does contain modules for a couple of older versions (2.2.0 and 2.8) of this software, we now expect users to install recent versions using a [Python virtual environment](Python.md#Creating_and_using_a_virtual_environment).

For more information on how to use MetaPhlan, see their [wiki](https://github.com/biobakery/MetaPhlAn/wiki/MetaPhlAn-4)

# Available wheels

You can list available wheels using the avail\_wheels command:

```
[name@server ~]$ avail_wheels metaphlan --all-versions
name       version    python    arch
---------  ---------  --------  -------
MetaPhlAn  4.0.3      py3       generic
MetaPhlAn  3.0.7      py3       generic

```

# Downloading databases

Note that MetaPhlAn requires a set of databases to be downloaded into the $SCRATCH.

**Important:** The database must live in the $SCRATCH

Databases can be downloaded from [Segatalab FTP](http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases).

1. From a login node, create the data folder:

```
[name@server ~]$ export DB_DIR=$SCRATCH/metaphlan_databases
[name@server ~]$ mkdir -p $DB_DIR
[name@server ~]$ cd $DB_DIR

```

2. Download the data:

```
[name@server ~]$ parallel wget ::: http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vJan21_CHOCOPhlAnSGB_202103.tar http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vJan21_CHOCOPhlAnSGB_202103_marker_info.txt.bz2 http://cmprod1.cibio.unitn.it/biobakery4/metaphlan_databases/mpa_vJan21_CHOCOPhlAnSGB_202103_species.txt.bz2

```

Note that this step **cannot** be done from a compute node but must be done from a login node.

3. Extract the downloaded data, for example using an interactive job:

```
[name@server ~]$ salloc --account=<your account> --cpus-per-task=2 --mem=10G

```

Untar and unzip the databases:

```
[name@server ~]$ tar -xf mpa_vJan21_CHOCOPhlAnSGB_202103.tar
[name@server ~]$ parallel bunzip2 ::: *.bz2

```

# Running MetaPhlAn

Once the database files have been downloaded and extracted, you can submit a job. You may edit the following job submission script
according to your needs:

**File :** metaphlan-job.sh

```
#!/bin/bash

#SBATCH --account=def-someuser
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=4        # Number of cores
#SBATCH --mem=15G                # requires at least 15 GB of memory

# Load the required modules
module load gcc blast samtools bedtools bowtie2 python/3.10

# Move to the scratch
cd $SCRATCH

DB_DIR=$SCRATCH/metaphlan_databases

# Generate your virtual environment in $SLURM_TMPDIR
virtualenv --no-download ${SLURM_TMPDIR}/env
source ${SLURM_TMPDIR}/env/bin/activate

# Install metaphlan and its dependencies
pip install --no-index --upgrade pip
pip install --no-index metaphlan==X.Y.Z  # EDIT: the required version here, e.g. 4.0.3

# Reuse the number of core allocated to our job from `--cpus-per-task=4`
# It is important to use --index and --bowtie2db so that MetaPhlAn can run inside the job
metaphlan metagenome.fastq --input_type fastq -o profiled_metagenome.txt --nproc $SLURM_CPUS_PER_TASK --index mpa_vJan21_CHOCOPhlAnSGB_202103 --bowtie2db $DB_DIR --bowtie2out metagenome.bowtie2.bz2

```

Then submit the job to the scheduler:

```
[name@server ~]$ sbatch metaphlan-job.sh

```