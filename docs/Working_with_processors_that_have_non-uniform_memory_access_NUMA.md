# Working with processors that have non-uniform memory access (NUMA)

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

Non-uniform memory access (NUMA) is a feature of memory design that is found on most modern processors with a large number of cores. It is possible to control the execution of your program to optimize the use of these features. This is something that you would only need to do if you want to optimize your program to get the best performance possible.

The essence of NUMA is that CPU cores and memory is divided into subsets, called NUMA nodes. The cores belonging to a particular NUMA node can access the memory belonging to that node faster than they can access the memory belonging to other nodes. Therefore, for some programs where performance depends on latency of memory access, it is beneficial to place all cores and memory used by the program within a single NUMA node.

NUMA features are not supported by the Slurm scheduler at present, i.e. you cannot submit a job to run on a particular NUMA node. However, you can submit a job that utilizes a full node, in which you can then have full control of various NUMA features as you launch your programs.

The NUMA layout is typically different for each type of processor. If you want to use NUMA features in your job scripts, they should be targeted for a particular type of processor. For example, this is the NUMA layout on one of the Graham broadwell nodes.

```
[usergra245 ~]$ numactl --hardware
available: 2 nodes (0-1)
node 0 cpus: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
node 0 size: 64030 MB
node 0 free: 61453 MB
node 1 cpus: 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
node 1 size: 64508 MB
node 1 free: 61016 MB
node distances:
node   0   1 
 0:  10  21 
 1:  21  10 

```

In this case the processor has two NUMA nodes, each with 16 processor cores and 64 GB of memory.

The following job script submits a job that requests that type of node, with two multi-threaded OpenMP tasks, each utilizing one NUMA node.

**File :** array\_job.sh

```
#!/bin/bash
 #SBATCH --nodes=1
 #SBATCH --exclusive
 #SBATCH --constraint=broadwell
 #SBATCH --mem=0
 #SBATCH --ntasks=2
 #SBATCH --cpus-per-task=16
 #SBATCH -t 0:00:05            # time (D-HH:MM)
 #SBATCH --account=def-someuser

 export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

 numactl --cpunodebind=0 --membind=0 ./test.x &
 numactl --cpunodebind=1 --membind=1 ./test.x &

 wait

```