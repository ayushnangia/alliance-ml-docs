# Nvprof

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

Nvprof is a command-line light-weight GUI-less profiler available for Linux, Windows, and Mac OS.
This tool allows you to collect and view profiling data of CUDA-related activities on both CPU and GPU, including kernel execution, memory transfers, etc. Profiling options should be provided to the profiler via the command-line options.

## Strengths

It is capable of providing a textual report :

- Summary of GPU and CPU activity
- Trace of GPU and CPU activity
- Event collection

Nvprof also features a headless profile collection with the help of the Nvidia Visual Profiler:

- First use Nvprof on headless node to collect data
- Then visualize timeline with Visual Profiler

# Quickstart guide

On [Béluga](Beluga.md) and [Narval](Narval.md), the
[NVIDIA Data Center GPU Manager (DCGM)](https://developer.nvidia.com/dcgm)
needs to be disabled, and this must be done while doing your job submission:

```
[name@server ~]$ DISABLE_DCGM=1 salloc --gres=gpu:1 ...

```

When your job starts, DCGM will eventually stop running in the following minute.
For convenience, the following loop awaits until the monitoring service has stopped
(that is as soon as `grep` returns nothing):

```
[name@server ~]$ while [ ! -z "$(dcgmi -v | grep 'Hostengine build info:')" ]; do sleep 5; done

```

## Environment modules

Before you start profiling with NVPROF, the appropriate [module](Utiliser_des_modules.md) needs to be loaded.

NVPROF is part of the CUDA package, so run `module avail cuda` to see what versions are currently available with the compiler and MPImodules you have loaded. For a comprehensive list of Cuda modules, run `module -r spider '.*cuda.*'`.
At the time this was written these were:

- cuda/10.0.130
- cuda/10.0
- cuda/9.0.176
- cuda/9.0
- cuda/8.0.44
- cuda/8.0

Use `module load cuda/version` to choose a version. For example, to load the CUDA compiler version 10.0, do:

```
[name@server ~]$ module load cuda/10.0

```

You also need to let nvprof where to find CUDA libraries. To do that, run this after loading the cuda module:

```
[name@server ~]$ export LD_LIBRARY_PATH=$EBROOTCUDA/lib64:$LD_LIBRARY_PATH

```

## Compile your code

To get useful information from Nvprof, you first need to compile your code with one of the Cuda compilers (`nvcc` for C).

## Profiling modes

Nvprof operates in one of the modes listed below.

### Summary mode

This is the default operating mode for Nvprof. It outputs a single result line for each instruction such as a kernel function or CUDA memory copy/set performed by the application. For each kernel function, Nvprof outputs the total time of all instances of the kernel or type of memory copy as well as the average, minimum, and maximum time.
In this example, the application is `a.out` and we run Nvprof to get the profiling :

```
[name@server ~]$ nvprof  ./a.out[ ] - Starting...
==27694== NVPROF is profiling process 27694, command: a.out
GPU Device 0: "GeForce GTX 580" with compute capability 2.0

MatrixA(320,320), MatrixB(640,320)
Computing result using CUDA Kernel...
done
Performance= 35.35 GFlop/s, Time= 3.708 msec, Size= 131072000 Ops, WorkgroupSize= 1024 threads/block
Checking computed result for correctness: OK

==27694== Profiling application: matrixMul
==27694== Profiling result:
Time(%)      Time     Calls       Avg       Min       Max  Name
 99.94%  1.11524s       301  3.7051ms  3.6928ms  3.7174ms  void matrixMulCUDA<int=32>(float*, float*, float*, int, int)
  0.04%  406.30us         2  203.15us  136.13us  270.18us  [CUDA memcpy HtoD]
  0.02%  248.29us         1  248.29us  248.29us  248.29us  [CUDA memcpy DtoH]

```