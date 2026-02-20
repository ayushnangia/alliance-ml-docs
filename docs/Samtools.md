# Samtools

Other languages:

- English
- [français](Samtools_fr.md)

## Description

Samtools is a suite of programs for interacting with high-throughput sequencing data.
It is closely related to BCFtools and to HTSlib. Primary documentation for all three
of these packages can be found at [https://www.htslib.org/](https://www.htslib.org/)

- Samtools is for reading, writing, editing, indexing, and viewing files in SAM, BAM, or CRAM format
- BCFtools is for reading and writing files in BCF2, VCF, and gVCF format, and for calling, filtering, and summarizing SNP and short indel sequence variants
- HTSlib is a C-language library for reading and writing high-throughput sequencing data. It is used by both Samtools and BCFtools.

This page does not cover all features of Samtools. Please refer to [Samtools](http://www.htslib.org/doc/samtools.html) for the complete list of all subtools.

To load the default version of samtools use `module load samtools`, e.g.:

```
[name@server ~]$ module load samtools
[name@server ~]$ samtools

Program: samtools (Tools for alignments in the SAM format)
Version: 1.20 (using htslib 1.20)

Usage:   samtools <command> [options]

```

For more on the `module` command, including how to find other versions of samtools, see [Using modules](Utiliser_des_modules.md)

## General usage

SAMtools provides tools for manipulating alignments in SAM and BAM formats.
A common task is to convert SAM files ("Sequence Alignment/Map") to BAM files.
BAM files are compressed versions of SAM files and are much smaller in size; the "B" stands for "binary".
BAM files are easy to manipulate and are ideal for storing large nucleotide sequence alignments.

CRAM is a more recent format for the same type of data, and offers still greater compression.

### Converting a SAM file to a BAM file

Prior to converting, verify if your SAM file carries a header section with character “@”. You can inspect the header section using the view command:

```
[name@server ~]$ samtools view -H my_sample.sam

```

If the SAM file contains a header, either of these forms can be used to convert the data to BAM format:

```
[name@server ~]$ samtools view -bo my_sample.bam my_sample.sam
[name@server ~]$ samtools view -b my_sample.sam -o my_sample.bam

```

If headers are absent, you can use the reference FASTA file to map the reads:

```
[name@server ~]$ samtools view -bt ref_seq.fa -o my_sample.bam my_sample.sam

```

### Sorting and indexing BAM files

You may also have to sort and index BAM files for many downstream applications

```
[name@server ~]$ samtools sort my_sample.bam -o my_sample_sorted.bam
[name@server ~]$ samtools index my_sample_sorted.bam

```

You can also convert a SAM file directly to a sorted BAM file using the shell pipe:

```
[name@server ~]$ 
[name@server ~]$ samtools view -b my_sample.sam

```

A sorted BAM file, together with its index file with extension `.bai`, is a common prerequisite for many other processes such as variant calling, feature counting, etc.

### Processing multiple files with multithreading and/or GNU parallel

You will typically have more than one SAM file to process at one time.
A job script with a loop is a good way to handle multiple files, as in the following example:

**File :** samtools.sh

```
#!/bin/bash            
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G      
#SBATCH --time=3:00:00 

module load samtools/1.20

for FILE in *.sam
do
  time samtools view -b ${FILE} | samtools sort -o ${FILE%.*}_mt_sorted.bam
done

```

Samtools typically runs on a single core by default but in some cases it may improve your efficiency to use multithreading or GNU parallel.

Samtools can take advantage of multiple cores ("multithreading") if given the `-@` flag:

**File :** samtools\_multithreading.sh

```
#!/bin/bash
#SBATCH --cpus-per-task 4
#SBATCH --mem-per-cpu=4G
#SBATCH --time=3:00:00

module load samtools/1.20

for FILE in *.sam
do
  time samtools view -@ ${SLURM_CPUS_PER_TASK} -b ${FILE} | samtools sort -o ${FILE%.*}_mt_sorted.bam
done

```

A different way to take advantage of multiple cores is to use GNU parallel to process multiple files concurrently:

**File :** samtools\_gnuparallel.sh

```
#!/bin/bash
#SBATCH --cpus-per-task 4
#SBATCH --mem-per-cpu=4G
#SBATCH --time=3:00:00

module load samtools/1.20

find . -name "*.sam" | parallel -j ${SLURM_CPUS_PER_TASK} "time samtools view -bS {} | samtools sort -o {.}_mt_sorted.bam"

```

The above script will execute view and sort on four SAM files concurrently.
If you have more input files, modify the --cpous-per-task request.