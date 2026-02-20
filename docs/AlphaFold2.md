# AlphaFold2

Other languages:

- English
- [français](AlphaFold2_fr.md)

[AlphaFold](https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology)
is a machine learning model for the prediction of protein folding.

This page discusses how to use AlphaFold v2.0, the version that was entered in CASP14 and published in Nature.

Source code and documentation for AlphaFold can be found at their [GitHub page](https://github.com/deepmind/alphafold).
Any publication that discloses findings arising from use of this source code or the model parameters should [cite](https://github.com/deepmind/alphafold#citing-this-work) the [AlphaFold paper](https://doi.org/10.1038/s41586-021-03819-2).

## Available versions

AlphaFold is available on our clusters as prebuilt Python packages (wheels). You can list available versions with `avail_wheels`.

```
[name@server ~]$ avail_wheels alphafold --all-versions
name       version    python    arch
---------  ---------  --------  -------
alphafold  2.3.1      py3       generic
alphafold  2.3.0      py3       generic
alphafold  2.2.4      py3       generic
alphafold  2.2.3      py3       generic
alphafold  2.2.2      py3       generic
alphafold  2.2.1      py3       generic
alphafold  2.1.1      py3       generic
alphafold  2.0.0      py3       generic

```

## Installing AlphaFold in a Python virtual environment

1. Load AlphaFold dependencies.

```
[name@server ~]$ module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 cuda/11.4 cudnn/8.2.0 kalign/2.03 hmmer/3.2.1 openmm-alphafold/7.5.1 hh-suite/3.3.0 python/3.8

```

As of July 2022, only Python 3.7 and 3.8 are supported.

2. Create and activate a Python virtual environment.

```
[name@server ~]$ virtualenv --no-download ~/alphafold_env
[name@server ~]$ source ~/alphafold_env/bin/activate

```

3. Install a specific version of AlphaFold and its Python dependencies.

```
(alphafold_env) [name@server ~] pip install --no-index --upgrade pip
(alphafold_env) [name@server ~] pip install --no-index alphafold==X.Y.Z

```

where `X.Y.Z` is the exact desired version, for instance `2.2.4`.
You can omit to specify the version in order to install the latest one available from the wheelhouse.

4. Validate it.

```
(alphafold_env) [name@server ~] run_alphafold.py --help

```

5. Freeze the environment and requirements set.

```
(alphafold_env) [name@server ~] pip freeze > ~/alphafold-requirements.txt

```

## Databases

Note that AlphaFold requires a set of databases.

The databases are available in
`/cvmfs/bio.data.computecanada.ca/content/databases/Core/alphafold2_dbs/`.

AlphaFold databases on CVMFS undergo yearly updates. In January 2024, the database was updated and is accessible in folder `2024_01`.

```
(alphafold_env) [name@server ~] export DOWNLOAD_DIR=/cvmfs/bio.data.computecanada.ca/content/databases/Core/alphafold2_dbs/2024_01/

```

You can also choose to download the databases locally into your `$SCRATCH` directory.

**Important:** The databases must live in the `$SCRATCH` directory.

GeneralGraham only

1. From a DTN or login node, create the data folder.

```
(alphafold_env) [name@server ~] export DOWNLOAD_DIR=$SCRATCH/alphafold/data
(alphafold_env) [name@server ~] mkdir -p $DOWNLOAD_DIR

```

2. With your modules loaded and virtual environment activated, you can download the data.

```
(alphafold_env) [name@server ~] download_all_data.sh $DOWNLOAD_DIR

```

Note that this step **cannot** be done from a compute node. It should be done on a data transfer node (DTN) on clusters that have them (see [Transferring data](Data_transfer.md)). On clusters that have no DTN, use a login node instead. Since the download can take up to a full day, we suggest using a [terminal multiplexer](Prolonging_terminal_sessions.md#Terminal_multiplexers). You may encounter a `Client_loop: send disconnect: Broken pipe` error message. See [Troubleshooting](AlphaFold.md#Broken_pipe_error_message) below.

1. Set `DOWNLOAD_DIR`.

```
(alphafold_env) [name@server ~] export DOWNLOAD_DIR=/datashare/alphafold

```

Afterwards, the structure of your data should be similar to

2.32.2

```
(alphafold_env) [name@server ~] tree -d $DOWNLOAD_DIR
$DOWNLOAD_DIR/                             # ~ 2.6 TB (total)
    bfd/                                   # ~ 1.8 TB
        # 6 files
    mgnify/                                # ~ 120 GB
        mgy_clusters.fa
    params/                                # ~ 5.3 GB
        # LICENSE
        # 15 models
        # 16 files (total)
    pdb70/                                 # ~ 56 GB
        # 9 files
    pdb_mmcif/                             # ~ 246 GB
        mmcif_files/
            # 202,764 files
        obsolete.dat
    pdb_seqres/                            # ~ 237 MB
        pdb_seqres.txt
    uniprot/                               # ~ 111 GB
        uniprot.fasta
    uniref30/                              # ~ 206 GB
        # 7 files
    uniref90/                              # ~ 73 GB
        uniref90.fasta

```

```
(alphafold_env) [name@server ~] tree -d $DOWNLOAD_DIR
$DOWNLOAD_DIR/                             # Total: ~ 2.2 TB (download: 428 GB)
    bfd/                                   # ~ 1.8 TB (download: 271.6 GB)
        # 6 files.
    mgnify/                                # ~ 64 GB (download: 32.9 GB)
        mgy_clusters.fa
    params/                                # ~ 3.5 GB (download: 3.5 GB)
        # 5 CASP14 models,
        # 5 pTM models,
        # LICENSE,
        # = 11 files.
    pdb70/                                 # ~ 56 GB (download: 19.5 GB)
        # 9 files.
    pdb_mmcif/                             # ~ 206 GB (download: 46 GB)
        mmcif_files/
            # About 180,000 .cif files.
        obsolete.dat
    uniclust30/                            # ~ 87 GB (download: 24.9 GB)
        uniclust30_2018_08/
            # 13 files.
    uniref90/                              # ~ 59 GB (download: 29.7 GB)
        uniref90.fasta

```

## Running AlphaFold

Performance

You can request at most 8 CPU cores when running AlphaFold because it is hardcoded to not use more and does not benefit from using more.

Edit one of following submission scripts according to your needs.

2.3 on CPU2.3 on GPU2.2 on CPU2.2 on GPU

**File :** alphafold-2.3-cpu.sh

```
#!/bin/bash

#SBATCH --job-name=alphafold_run
#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=08:00:00           # adjust this to match the walltime of your job
#SBATCH --cpus-per-task=8         # a MAXIMUM of 8 core, AlphaFold has no benefit to use more
#SBATCH --mem=20G                 # adjust this according to the memory you need

# Load modules dependencies.
module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 cuda/11.4 cudnn/8.2.0 kalign/2.03 hmmer/3.2.1 openmm-alphafold/7.5.1 hh-suite/3.3.0 python/3.8

DOWNLOAD_DIR=$SCRATCH/alphafold/data   # set the appropriate path to your downloaded data
INPUT_DIR=$SCRATCH/alphafold/input     # set the appropriate path to your input data
OUTPUT_DIR=${SCRATCH}/alphafold/output # set the appropriate path to your output data

# Generate your virtual environment in $SLURM_TMPDIR.
virtualenv --no-download ${SLURM_TMPDIR}/env
source ${SLURM_TMPDIR}/env/bin/activate

# Install AlphaFold and its dependencies.
pip install --no-index --upgrade pip
pip install --no-index --requirement ~/alphafold-requirements.txt

# Edit with the proper arguments and run your commands.
# run_alphafold.py --help
run_alphafold.py \
   --fasta_paths=${INPUT_DIR}/YourSequence.fasta,${INPUT_DIR}/AnotherSequence.fasta \
   --output_dir=${OUTPUT_DIR} \
   --data_dir=${DOWNLOAD_DIR} \
   --db_preset=full_dbs \
   --model_preset=multimer \
   --bfd_database_path=${DOWNLOAD_DIR}/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
   --mgnify_database_path=${DOWNLOAD_DIR}/mgnify/mgy_clusters_2022_05.fa \
   --pdb70_database_path=${DOWNLOAD_DIR}/pdb70/pdb70 \
   --template_mmcif_dir=${DOWNLOAD_DIR}/pdb_mmcif/mmcif_files \
   --obsolete_pdbs_path=${DOWNLOAD_DIR}/pdb_mmcif/obsolete.dat \
   --pdb_seqres_database_path=${DOWNLOAD_DIR}/pdb_seqres/pdb_seqres.txt \
   --uniprot_database_path=${DOWNLOAD_DIR}/uniprot/uniprot.fasta \
   --uniref30_database_path=${DOWNLOAD_DIR}/uniref30/UniRef30_2021_03 \
   --uniref90_database_path=${DOWNLOAD_DIR}/uniref90/uniref90.fasta \
   --hhblits_binary_path=${EBROOTHHMINSUITE}/bin/hhblits \
   --hhsearch_binary_path=${EBROOTHHMINSUITE}/bin/hhsearch \
   --jackhmmer_binary_path=${EBROOTHMMER}/bin/jackhmmer \
   --kalign_binary_path=${EBROOTKALIGN}/bin/kalign \
   --max_template_date=2022-01-01 \
   --use_gpu_relax=False

```

**File :** alphafold-2.3-gpu.sh

```
#!/bin/bash

#SBATCH --job-name=alphafold_run
#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=08:00:00           # adjust this to match the walltime of your job
#SBATCH --cpus-per-task=8         # a MAXIMUM of 8 core, AlphaFold has no benefit to use more
#SBATCH --gres=gpu:1              # a GPU helps to accelerate the inference part only
#SBATCH --mem=20G                 # adjust this according to the memory you need

# Load modules dependencies.
module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 cuda/11.4 cudnn/8.2.0 kalign/2.03 hmmer/3.2.1 openmm-alphafold/7.5.1 hh-suite/3.3.0 python/3.8

DOWNLOAD_DIR=$SCRATCH/alphafold/data   # set the appropriate path to your downloaded data
INPUT_DIR=$SCRATCH/alphafold/input     # set the appropriate path to your input data
OUTPUT_DIR=${SCRATCH}/alphafold/output # set the appropriate path to your output data

# Generate your virtual environment in $SLURM_TMPDIR.
virtualenv --no-download ${SLURM_TMPDIR}/env
source ${SLURM_TMPDIR}/env/bin/activate

# Install AlphaFold and its dependencies.
pip install --no-index --upgrade pip
pip install --no-index --requirement ~/alphafold-requirements.txt

# Edit with the proper arguments and run your commands.
# run_alphafold.py --help
run_alphafold.py \
   --fasta_paths=${INPUT_DIR}/YourSequence.fasta,${INPUT_DIR}/AnotherSequence.fasta \
   --output_dir=${OUTPUT_DIR} \
   --data_dir=${DOWNLOAD_DIR} \
   --db_preset=full_dbs \
   --model_preset=multimer \
   --bfd_database_path=${DOWNLOAD_DIR}/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
   --mgnify_database_path=${DOWNLOAD_DIR}/mgnify/mgy_clusters_2022_05.fa \
   --pdb70_database_path=${DOWNLOAD_DIR}/pdb70/pdb70 \
   --template_mmcif_dir=${DOWNLOAD_DIR}/pdb_mmcif/mmcif_files \
   --obsolete_pdbs_path=${DOWNLOAD_DIR}/pdb_mmcif/obsolete.dat \
   --pdb_seqres_database_path=${DOWNLOAD_DIR}/pdb_seqres/pdb_seqres.txt \
   --uniprot_database_path=${DOWNLOAD_DIR}/uniprot/uniprot.fasta \
   --uniref30_database_path=${DOWNLOAD_DIR}/uniref30/UniRef30_2021_03 \
   --uniref90_database_path=${DOWNLOAD_DIR}/uniref90/uniref90.fasta \
   --hhblits_binary_path=${EBROOTHHMINSUITE}/bin/hhblits \
   --hhsearch_binary_path=${EBROOTHHMINSUITE}/bin/hhsearch \
   --jackhmmer_binary_path=${EBROOTHMMER}/bin/jackhmmer \
   --kalign_binary_path=${EBROOTKALIGN}/bin/kalign \
   --max_template_date=2022-01-01 \
   --use_gpu_relax=True

```

**File :** alphafold-cpu.sh

```
#!/bin/bash

#SBATCH --job-name=alphafold_run
#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=08:00:00           # adjust this to match the walltime of your job
#SBATCH --cpus-per-task=8         # a MAXIMUM of 8 core, AlphaFold has no benefit to use more
#SBATCH --mem=20G                 # adjust this according to the memory you need

# Load modules dependencies.
module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 cuda/11.4 cudnn/8.2.0 kalign/2.03 hmmer/3.2.1 openmm-alphafold/7.5.1 hh-suite/3.3.0 python/3.8

DOWNLOAD_DIR=$SCRATCH/alphafold/data   # set the appropriate path to your downloaded data
INPUT_DIR=$SCRATCH/alphafold/input     # set the appropriate path to your input data
OUTPUT_DIR=${SCRATCH}/alphafold/output # set the appropriate path to your output data

# Generate your virtual environment in $SLURM_TMPDIR.
virtualenv --no-download ${SLURM_TMPDIR}/env
source ${SLURM_TMPDIR}/env/bin/activate

# Install AlphaFold and its dependencies.
pip install --no-index --upgrade pip
pip install --no-index --requirement ~/alphafold-requirements.txt

# Edit with the proper arguments and run your commands.
# Note that the `--uniclust30_database_path` option below was renamed to
# `--uniref30_database_path` in 2.3.
# run_alphafold.py --help
run_alphafold.py \
   --fasta_paths=${INPUT_DIR}/YourSequence.fasta,${INPUT_DIR}/AnotherSequence.fasta \
   --output_dir=${OUTPUT_DIR} \
   --data_dir=${DOWNLOAD_DIR} \
   --model_preset=monomer_casp14 \
   --bfd_database_path=${DOWNLOAD_DIR}/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
   --mgnify_database_path=${DOWNLOAD_DIR}/mgnify/mgy_clusters_2018_12.fa \
   --pdb70_database_path=${DOWNLOAD_DIR}/pdb70/pdb70 \
   --template_mmcif_dir=${DOWNLOAD_DIR}/pdb_mmcif/mmcif_files \
   --obsolete_pdbs_path=${DOWNLOAD_DIR}/pdb_mmcif/obsolete.dat \
   --uniclust30_database_path=${DOWNLOAD_DIR}/uniclust30/uniclust30_2018_08/uniclust30_2018_08  \
   --uniref90_database_path=${DOWNLOAD_DIR}/uniref90/uniref90.fasta  \
   --hhblits_binary_path=${EBROOTHHMINSUITE}/bin/hhblits \
   --hhsearch_binary_path=${EBROOTHHMINSUITE}/bin/hhsearch \
   --jackhmmer_binary_path=${EBROOTHMMER}/bin/jackhmmer \
   --kalign_binary_path=${EBROOTKALIGN}/bin/kalign \
   --max_template_date=2020-05-14 \
   --use_gpu_relax=False

```

**File :** alphafold-gpu.sh

```
#!/bin/bash

#SBATCH --job-name=alphafold_run
#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=08:00:00           # adjust this to match the walltime of your job
#SBATCH --gres=gpu:1              # a GPU helps to accelerate the inference part only
#SBATCH --cpus-per-task=8         # a MAXIMUM of 8 core, AlphaFold has no benefit to use more
#SBATCH --mem=20G                 # adjust this according to the memory you need

# Load modules dependencies.
module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 cuda/11.4 cudnn/8.2.0 kalign/2.03 hmmer/3.2.1 openmm-alphafold/7.5.1 hh-suite/3.3.0 python/3.8

DOWNLOAD_DIR=$SCRATCH/alphafold/data   # set the appropriate path to your downloaded data
INPUT_DIR=$SCRATCH/alphafold/input     # set the appropriate path to your input data
OUTPUT_DIR=${SCRATCH}/alphafold/output # set the appropriate path to your output data

# Generate your virtual environment in $SLURM_TMPDIR.
virtualenv --no-download ${SLURM_TMPDIR}/env
source ${SLURM_TMPDIR}/env/bin/activate

# Install AlphaFold  and its dependencies.
pip install --no-index --upgrade pip
pip install --no-index --requirement ~/alphafold-requirements.txt

# Edit with the proper arguments and run your commands.
# Note that the `--uniclust30_database_path` option below was renamed to
# `--uniref30_database_path` in 2.3.
# run_alphafold.py --help
run_alphafold.py \
   --fasta_paths=${INPUT_DIR}/YourSequence.fasta,${INPUT_DIR}/AnotherSequence.fasta \
   --output_dir=${OUTPUT_DIR} \
   --data_dir=${DOWNLOAD_DIR} \
   --model_preset=monomer_casp14 \
   --bfd_database_path=${DOWNLOAD_DIR}/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \
   --mgnify_database_path=${DOWNLOAD_DIR}/mgnify/mgy_clusters_2018_12.fa \
   --pdb70_database_path=${DOWNLOAD_DIR}/pdb70/pdb70 \
   --template_mmcif_dir=${DOWNLOAD_DIR}/pdb_mmcif/mmcif_files \
   --obsolete_pdbs_path=${DOWNLOAD_DIR}/pdb_mmcif/obsolete.dat \
   --uniclust30_database_path=${DOWNLOAD_DIR}/uniclust30/uniclust30_2018_08/uniclust30_2018_08  \
   --uniref90_database_path=${DOWNLOAD_DIR}/uniref90/uniref90.fasta  \
   --hhblits_binary_path=${EBROOTHHMINSUITE}/bin/hhblits \
   --hhsearch_binary_path=${EBROOTHHMINSUITE}/bin/hhsearch \
   --jackhmmer_binary_path=${EBROOTHMMER}/bin/jackhmmer \
   --kalign_binary_path=${EBROOTKALIGN}/bin/kalign \
   --max_template_date=2020-05-14 \
   --use_gpu_relax=True

```

Then, submit the job to the scheduler.

```
(alphafold_env) [name@server ~] sbatch --job-name alphafold-X alphafold-gpu.sh

```

## Troubleshooting

### Broken pipe error message

When downloading the database, you may encounter a `Client_loop: send disconnect: Broken pipe` error message. It is hard to find the exact cause for this error message. It could be as simple as an unusually high number of users working on the login node, leaving less space for you to upload data.

- One solution is to use a [terminal multiplexer](Prolonging_terminal_sessions.md#Terminal_multiplexers). Note that you could still encounter this error message but less are the chances.

- A second solution is to use the database that is already present on the cluster. `/cvmfs/bio.data.computecanada.ca/content/databases/Core/alphafold2_dbs/2023_07/`.

- Another option is to download the full database in sections. To have access to the different download scripts, after loading the module and activated your virtual environment, you simply enter `download_` in your terminal and tap twice on the `tab` keyboard key to visualize all the scripts that are available. You can manually download sections of the database by using the available script, as for instance `download_pdb.sh`.