# Debugging and profiling

Other languages:

- English
- [français](Debugging_and_profiling_fr.md)

An important step in the software development process, particularly for compiled languages like Fortran and C/C++, concerns the use of a program called a debugger to detect and identify the origin of runtime errors (e.g. memory leaks, floating point exceptions and so forth) so that they can be eliminated. Once the program's correctness is assured, a further step is profiling the software. This involves the use of another software tool, a profiler, determine what percentage of the total execution time each section of the source code is responsible for when run with a representative test case. A profiler can give information like how many times a particular function is called, which other functions are calling it and how many milli-seconds of time each invocation of this function costs on average.

# Debugging and profiling tools

Our national clusters offer a variety of debugging and profiling tools, both command line and those with a graphical user interface, whose use requires an X11 connection. Note that debugging sessions should be conducted using an [interactive job](Scheduler.md#Interactive_jobs) and not run on a login node.

## GNU debugger (gdb)

Please see the [GDB page](GBD_page.md).

## PGI debugger (pgdb)

Please see the [Pgdbg page](https://docs.alliancecan.ca/wiki/Pgdbg).

## ARM debugger (ddt)

Please see the [ARM software page](Allinea.md).

## GNU profiler (gprof)

Please see the [Gprof page](Gprof.md).

## Scalasca profiler (scalasca, scorep, cube)

Scalasca is an open source, GUI-driven parallel profiling tool set. It is currently available for **gcc 9.3.0** and **OpenMPI 4.0.3**, with AVX2 or AVX512 architecture. Its environment can be loaded with:

`module load StdEnv/2020 gcc/9.3.0 openmpi/4.0.3 scalasca`

The current version is **2.5**. More information can be found in the 2.x user guide, which contains workflow examples [here](https://apps.fz-juelich.de/scalasca/releases/scalasca/2.5/docs/manual/).

## PGI profiler (pgprof)

Please see the [Pgprof page](PGPROF.md).

## Nvidia command-line profiler (nvprof)

Please see the [nvprof page](Nvprof.md).

## Valgrind

Please see the [Valgrind page](Valgrind.md).

# External references

- [Introduction to (Parallel) Performance](https://docs.scinet.utoronto.ca/index.php/Introduction_To_Performance) from SciNet
- [Code profiling on Graham](https://www.youtube.com/watch?v=YsF5KMr9uEQ), video, 54 minutes.