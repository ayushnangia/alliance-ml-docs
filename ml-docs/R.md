# R

Other languages:

- English
- [français](R_fr.md)

R is a system for statistical computation and graphics. It consists of a language plus a runtime environment with graphics, a debugger, access to certain system functions, and the ability to run programs stored in script files.

Even though R was not developed for high-performance computing (HPC), its popularity with scientists from a variety of disciplines, including engineering, mathematics, statistics, bioinformatics, etc. makes it an essential tool on HPC installations dedicated to academic research. Features such as C extensions, byte-compiled code and parallelization allow for reasonable performance in single-node jobs. Thanks to R’s modular nature, users can customize the R functions available to them by installing packages from the Comprehensive R Archive Network ([CRAN](https://cran.r-project.org/)) into their home directories.

User Julie Fortin has written a blog post, ["How to run your R script with Compute Canada"](https://medium.com/the-nature-of-food/how-to-run-your-r-script-with-compute-canada-c325c0ab2973) which you might find useful.

## The R interpreter

You need to begin by loading an R module; there will typically be several versions available and you can see a list of all of them using the command

```
[name@server ~]$ module spider r

```

You can load a particular R module using a command like

```
[name@server ~]$ module load r/4.5.0

```

For more on this, see [Using modules.](Utiliser_des_modules.md)

Now you can start the R interpreter and type R code inside that environment:

```
[name@server ~]$ R
R version 4.5.0 (2025-04-11) -- "How About a Twenty-Six"
Copyright (C) 2025 The R Foundation for Statistical Computing
Platform: x86_64-pc-linux-gnu

R is free software and comes with ABSOLUTELY NO WARRANTY.
You are welcome to redistribute it under certain conditions.
Type 'license()' or 'licence()' for distribution details.

R is a collaborative project with many contributors.
Type 'contributors()' for more information and
'citation()' on how to cite R or R packages in publications.

Type 'demo()' for some demos, 'help()' for on-line help, or
'help.start()' for an HTML browser interface to help.
Type 'q()' to quit R.

> values <- c(3,5,7,9)
> values[1]
[1] 3
> q()

```

To execute an R script non-interactively, use `Rscript` with the file containing the R commands as an argument:

```
[name@server ~]$ Rscript computation.R

```

`Rscript` will automatically pass scripting-appropriate options `--slave` and `--no-restore` to the R interpreter. These also imply the `--no-save` option, preventing the creation of useless workspace files on exit.

Note that **any calculations lasting more than two or three minutes should not be run on the login node**.
They should be run via the job scheduler.

A simple job script looks like this:

**File :** job.sh

```
#!/bin/bash
#SBATCH --account=def-someacct   # replace this with your own account
#SBATCH --mem-per-cpu=2000M      # memory; default unit is megabytes
#SBATCH --time=0-00:15           # time (DD-HH:MM)
module load StdEnv/2023 r/4.5.0  # Adjust version as needed

Rscript computation.R

```

See [Running jobs](Scheduler.md) for more information.

## Installing R packages

### install.packages()

To install packages from [CRAN](https://cran.r-project.org/), you can use `install.packages` in an interactive R session on a cluster login node. Since the compute nodes on most clusters do not have access to the Internet, installing R packages in a batch or interactive job is not possible. Many R packages are developed using the GNU family of compilers so we recommend that you load a `gcc` [module](Utiliser_des_modules.md) before trying to install any R packages. Use the same version of the `gcc` for all packages you install.

```
[name@server ~]$ module load gcc/12.3.0 r/4.5.0

```

#### Installing for a specific R version

For example, to install the `sp` package that provides classes and methods for spatial data, use the following command on a login node:

```
[name@server ~]$ R
[...]
> install.packages('sp', repos='https://cloud.r-project.org/')

```

If the argument `repos` is not specified, you will be asked to select an appropriate mirror for download. Ideally, it will be geographically close to the cluster you're working on.

Some packages require defining the environment variable `TMPDIR` before installing.

#### Installing for one or many R versions

Specify the local installation directory according to the R module that is currently loaded.

```
[name@server ~]$ mkdir -p ~/.local/R/$EBVERSIONR/
[name@server ~]$ export R_LIBS=~/.local/R/$EBVERSIONR/

```

Install the package.

```
[name@server ~]$ R -e 'install.packages("sp", repos="https://cloud.r-project.org/")'

```

In your submission script, you then have to load the desired R module and set the local library directory with `export R_LIBS=~/.local/R/$EBVERSIONR/`.

### Dependencies

Some packages depend on external libraries which are already installed on our clusters. If the library you need is listed at [Available software](Available_software.md), then load the appropriate [module](Utiliser_des_modules.md) before installing the package that requires it.

For example, the package `rgdal` requires a library called `gdal`. Running `module spider gdal/3.9.1` shows how to load this module.

If any package fails to install, be sure to read the error message carefully as it might give you details concerning additional modules you need to load. See [Using modules](Utiliser_des_modules.md) for more on the `module` family of commands.

### Downloaded packages

To install a package that you downloaded (i.e. not using `install.packages()`), you can install it as follows. Assuming the package is named `archive_package.tgz`, run the following command in a shell:

```
[name@server ~]$ R CMD INSTALL -l 'path for your local (home) R library' archive_package.tgz

```

## Using system calls in R

Using the R command `system()` you can execute commands in the ambient environment from inside R. On our clusters, this can lead to problems because R will give an incorrect value to the environment variable `LD_LIBRARY_PATH`. You can avoid this problem by using the syntax `system("LD_LIBRARY_PATH=$RSNT_LD_LIBRARY_PATH <my system call>")` in your R system calls.

## Passing arguments to R scripts

Sometimes it can be useful to pass parameters as arguments to R scripts, to avoid having to either change the R script for every job or having to manage multiple copies of otherwise identical scripts. This can be useful for specifying the names for input- or output files, as well as specifying numerical parameters. For example, instead of specifying the name of an input file and/or a numerical parameter like this

**File :**

```
filename = "input.csv"
iterations = 5

```

and changing the code every time either of these changes, parameters can be passed to the R-script when starting it:

```
[name@server ~]$ Rscript myscript.R  input_1.csv  5

```

and the next

```
[name@server ~]$ Rscript myscript.R  input_2.csv  10

```

The following example expects exactly two arguments. The first one should be a string which will be used for the variable "name" and the second one should be an integer for the variable "number".

**File :** arguments\_test.R

```
args = commandArgs(trailingOnly=TRUE)

# test if there is at least two arguments: if not, return an error
if (length(args)<2) {
  stop("At least two arguments must be supplied ('name' (text) and 'numer' (integer) )", call.=FALSE)
}

name      <- args[1]                # read first argument as string
number    <- as.integer( args[2] )  # read second argument as integer

print(paste("Processing with name:'", name, "' and number:'", number,"'", sep = ''))

```

This script can be used like this:

```
[name@server ~]$  Rscript arguments_test.R  Hello  42
[1] "Processing with name:'Hello' and number:'42'"

```

## Exploiting parallelism in R

The processors on our clusters are quite ordinary.
What makes these supercomputers *super* is that you have access to thousands of CPU cores with a high-performance network.
In order to take advantage of this hardware, you must run code "in parallel." However, note that prior to investing a lot of time and effort
in parallelizing your R code, you should first ensure that your serial implementation is as efficient as possible. As an interpreted
language, the use of loops in R, and especially nested loops, constitutes a significant performance bottleneck. Whenever possible you
should try to use vectorized forms of R functions and more functional elements of the R programming language like the family of
`apply` functions and the `ifelse` function. This will frequently offer you a far better performance gain by eliminating
a loop altogether instead of simply parallelizing the (slow) execution of this loop across several CPU cores.

The [CRAN Task View on High-Performance and Parallel Computing with R](https://cran.r-project.org/web/views/HighPerformanceComputing.html)
describes a bewildering collection of interrelated R packages for parallel computing.
For an excellent overview and advice, see the October 2023 Compute Ontario colloquium
["High-Performance R"](https://education.scinet.utoronto.ca/course/view.php?id=1333)
([slides](https://education.scinet.utoronto.ca/mod/resource/view.php?id=2887)).

The following subsections contain some further notes and examples.

**A note on terminology:** In most of our documentation the term 'node' refers
to an individual machine, also called a 'host', and a collection of such nodes makes up a 'cluster'.
In a lot of R documentation however, the term 'node' refers to a worker process and a 'cluster' is a
collection of such processes. As an example, consider the following quote, "Following **snow**, a pool
of worker processes listening *via* sockets for commands from the master is called a 'cluster' of
nodes."[1].

### doParallel and foreach

#### Usage

Foreach can be considered as a unified interface for all backends (i.e. doMC, doMPI, doParallel, doRedis, etc.). It works on all platforms, assuming that the backend works. doParallel acts as an interface between foreach and the parallel package and can be loaded alone. There are some [known efficiency issues](Scalability.md) when using foreach to run a very large number of very small tasks. Therefore, keep in mind that the following code is not the best example of an optimized use of the foreach() call but rather that the function chosen was kept at a minimum for demonstration purposes.

You must register the backend by feeding it the number of cores available. If the backend is not registered, foreach will assume that the number of cores is 1 and will proceed to go through the iterations serially.

The general method to use foreach is:

1. to load both foreach and the backend package;
2. to register the backend;
3. to call foreach() by keeping it on the same line as the %do% (serial) or %dopar% operator.

#### Running

1. Place your R code in a script file, in this case the file is called *test\_foreach.R*.

**File :** test\_foreach.R

```
# library(foreach) # optional if using doParallel
library(doParallel) #

# a very simple function
test_func <- function(var1, var2) {
    # some heavy workload
    sum <- 0
    for (i in c(1:3141593)) {
        sum <- sum + var1 * sin(var2 / i)
    }
    return(sqrt(sum))
}

# we will iterate over two sets of values, you can modify this to explore the mechanism of foreach
var1.v = c(1:8)
var2.v = seq(0.1, 1, length.out = 8)

# Use the environment variable SLURM_CPUS_PER_TASK to set the number of cores.
# This is for SLURM. Replace SLURM_CPUS_PER_TASK by the proper variable for your system.
# Avoid manually setting a number of cores.
ncores = Sys.getenv("SLURM_CPUS_PER_TASK") 

registerDoParallel(cores=ncores)# Shows the number of Parallel Workers to be used
print(ncores) # this how many cores are available, and how many you have requested.
getDoParWorkers()# you can compare with the number of actual workers

# be careful! foreach() and %dopar% must be on the same line!
foreach(var1=var1.v, .combine=rbind) %:% foreach(var2=var2.v, .combine=rbind) %dopar% {test_func(var1=var1, var2=var2)}

```

2. Copy the following content in a job submission script called *job\_foreach.sh*:

**File :** job\_foreach.sh

```
#!/bin/bash
#SBATCH --account=def-someacct   # replace this with your supervisors account
#SBATCH --nodes=1                # number of node MUST be 1
#SBATCH --cpus-per-task=4        # number of processes
#SBATCH --mem-per-cpu=2048M      # memory; default unit is megabytes
#SBATCH --time=0-00:15           # time (DD-HH:MM)

module load StdEnv/2023 r/4.5.0

export R_LIBS=~/local/R_libs/
R CMD BATCH --no-save --no-restore test_foreach.R

```

3. Submit the job with:

```
[name@server ~]$ sbatch job_foreach.sh

```

For more on submitting jobs, see [Running jobs](Scheduler.md).

### doParallel and makeCluster

#### Usage

You must register the backend by feeding it the nodes name multiplied by the desired number of processes. For instance, with two nodes (node1 and node2) and two processes, we would create a cluster composed of : `node1 node1 node2 node2` hosts. The *PSOCK* cluster type will run commands through SSH connections into the nodes.

#### Running

1. Place your R code in a script file, in this case the file is called `test_makecluster.R`.

**File :** test\_makecluster.R

```
library(doParallel)

# Create an array from the NODESLIST environnement variable
nodeslist = unlist(strsplit(Sys.getenv("NODESLIST"), split=" "))

# Create the cluster with the nodes name. One process per count of node name.
# nodeslist = node1 node1 node2 node2, means we are starting 2 processes on node1, likewise on node2.
cl = makeCluster(nodeslist, type = "PSOCK") 
registerDoParallel(cl)

# Compute (Source : https://cran.r-project.org/web/packages/doParallel/vignettes/gettingstartedParallel.pdf)
x <- iris[which(iris[,5] != "setosa"), c(1,5)]
trials <- 10000

foreach(icount(trials), .combine=cbind) %dopar%
    {
    ind <- sample(100, 100, replace=TRUE)
    result1 <- glm(x[ind,2]~x[ind,1], family=binomial(logit))
    coefficients(result1)
    }

# Don't forget to release resources
stopCluster(cl)

```

2. Copy the following content in a job submission script called `job_makecluster.sh`:

**File :** job\_makecluster.sh

```
#!/bin/bash
#SBATCH --account=def-someacct  # replace this with your supervisors account
#SBATCH --ntasks=4              # number of processes
#SBATCH --mem-per-cpu=512M      # memory; default unit is megabytes
#SBATCH --time=00:05:00         # time (HH:MM:SS)

module load StdEnv/2023 r/4.5.0

# Export the nodes names. 
# If all processes are allocated on the same node, NODESLIST contains : node1 node1 node1 node1
# Cut the domain name and keep only the node name
export NODESLIST=$(echo $(srun hostname | cut -f 1 -d '.'))
R -f test_makecluster.R

```

In the above example the scheduler might place all four processes on just one node.
This is okay, but if you wish to prove that the same job works even if the processes happen
to be placed on different nodes, then add the line `#SBATCH --ntasks-per-node=2`

3. Submit the job with:

```
[name@server ~]$ sbatch job_makecluster.sh

```

For more information on submitting jobs, see [Running jobs](Scheduler.md).

### Rmpi

#### Installing

This next procedure installs [Rmpi](https://cran.r-project.org/web/packages/Rmpi/index.html), an interface (wrapper) to MPI routines, which allow R to run in parallel.

1. See the available R modules by running:

```
module spider r

```

2. Select the R version and load the required OpenMPI module.

```
module load gcc/12.3
module load openmpi/4.1.5
module load r/4.5.0

```

3. Download [the latest Rmpi version](https://cran.r-project.org/web/packages/Rmpi/index.html); change the version number to whatever is desired.

```
wget https://cran.r-project.org/src/contrib/Rmpi_0.7-3.3.tar.gz

```

4. Specify the directory where you want to install the package files; you must have write permission for this directory. The directory name can be changed if desired.

```
mkdir -p ~/local/R_libs/
export R_LIBS=~/local/R_libs/

```

5. Run the install command.

```
R CMD INSTALL --configure-args="--with-Rmpi-include=$EBROOTOPENMPI/include   --with-Rmpi-libpath=$EBROOTOPENMPI/lib --with-Rmpi-type='OPENMPI' " Rmpi_0.7-3.3.tar.gz

```

Again, carefully read any error message that comes up when packages fail to install and load the required modules to ensure that all your packages are successfully installed.

#### Running

1. Place your R code in a script file, in this case the file is called *test.R*.

**File :** test.R

```
#Tell all slaves to return a message identifying themselves.
library("Rmpi")
sprintf("TEST mpi.universe.size() =  %i", mpi.universe.size())
ns <- mpi.universe.size() - 1
sprintf("TEST attempt to spawn %i slaves", ns)
mpi.spawn.Rslaves(nslaves=ns)
mpi.remote.exec(paste("I am",mpi.comm.rank(),"of",mpi.comm.size()))
mpi.remote.exec(paste(mpi.comm.get.parent()))
#Send execution commands to the slaves
x<-5
#These would all be pretty correlated one would think
x<-mpi.remote.exec(rnorm,x)
length(x)
x
mpi.close.Rslaves()
mpi.quit()

```

2. Copy the following content in a job submission script called *job.sh*:

**File :** job.sh

```
#!/bin/bash
#SBATCH --account=def-someacct   # replace this with your supervisors account
#SBATCH --ntasks=5               # number of MPI processes
#SBATCH --mem-per-cpu=2048M      # memory; default unit is megabytes
#SBATCH --time=0-00:15           # time (DD-HH:MM)

module load StdEnv/2023 gcc/12.3 openmpi/4.1.5 r/4.5.0

export R_LIBS=~/local/R_libs/
mpirun -np 1 R CMD BATCH test.R test.txt

```

3. Submit the job with:

```
sbatch job.sh

```

For more on submitting jobs, see [Running jobs](Scheduler.md).

1. ↑ Core package "parallel" vignette, [https://stat.ethz.ch/R-manual/R-devel/library/parallel/doc/parallel.pdf](https://stat.ethz.ch/R-manual/R-devel/library/parallel/doc/parallel.pdf)