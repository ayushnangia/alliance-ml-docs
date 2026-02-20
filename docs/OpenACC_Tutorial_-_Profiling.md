# OpenACC Tutorial - Profiling

Other languages:

- English
- [français](OpenACC_Tutorial_-_Profiling_fr.md)

Learning objectives

- Understand what a profiler is
- Understand how to use the NVPROF profiler
- Understand how the code is performing
- Understand where to focus your time and rewrite most time consuming routines

## Code profiling

Why would one need to profile code? Because it's the only way to understand:

- Where time is being spent (hotspots)
- How the code is performing
- Where to focus your development time

What is so important about hotspots in the code?
The [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law) says that
"Parallelizing the most time-consuming routines (i.e. the hotspots) will have the most impact".

## Build the Sample Code

For the following example, we use a code from this [Git repository](https://github.com/calculquebec/cq-formation-openacc).
You are invited to [download and extract the package](https://github.com/calculquebec/cq-formation-openacc/archive/refs/heads/main.zip), and go to the `cpp` or the `f90` directory.
The object of this example is to compile and link the code, obtain an executable, and then profile its source code with a profiler.

Which compiler ?

Being pushed by [Cray](https://www.cray.com/) and by [NVIDIA](https://www.nvidia.com) through its
[Portland Group](https://www.pgroup.com/support/release_archive.php) division until 2020 and now through its [HPC SDK](https://developer.nvidia.com/hpc-sdk), these two lines of compilers offer the most advanced OpenACC support.

As for the [GNU compilers](https://gcc.gnu.org/wiki/OpenACC), since GCC version 6, the support for OpenACC 2.x kept improving.
As of July 2022, GCC versions 10, 11 and 12 support OpenACC version 2.6.

For the purpose of this tutorial, we use the
[NVIDIA HPC SDK](https://developer.nvidia.com/nvidia-hpc-sdk-releases), version 22.7.
Please note that NVIDIA compilers are free for academic usage.

```
[name@server ~]$ module load nvhpc/22.7
Lmod is automatically replacing "intel/2020.1.217" with "nvhpc/22.7".

The following have been reloaded with a version change:
  1) gcccore/.9.3.0 => gcccore/.11.3.0        3) openmpi/4.0.3 => openmpi/4.1.4
  2) libfabric/1.10.1 => libfabric/1.15.1     4) ucx/1.8.0 => ucx/1.12.1

```

```
[name@server ~]$ make 
nvc++    -c -o main.o main.cpp
nvc++ main.o -o cg.x

```

Once the executable `cg.x` is created, we are going to profile its source code:
the profiler will measure function calls by executing and monitoring this program.
**Important:** this executable uses about 3GB of memory and one CPU core at near 100%.
Therefore, **a proper test environment should have at least 4GB of available memory and at least two (2) CPU cores**.

Which profiler ?

For the purpose of this tutorial, we use two profilers:

- **[NVIDIA `nvprof`](https://docs.nvidia.com/cuda/profiler-users-guide/)** - a command line text-based profiler that can analyze non-GPU codes.
- **[NVIDIA Visual Profiler `nvvp`](OpenACC_Tutorial_-_Adding_directives.md#NVIDIA_Visual_Profiler)** - a graphical cross-platform analyzing tool for the codes written with OpenACC and CUDA C/C++ instructions.

Since our previously built `cg.x` is not yet using the GPU, we will start the analysis with the `nvprof` profiler.

### NVIDIA `nvprof` Command Line Profiler

NVIDIA usually provides `nvprof` with its HPC SDK,
but the proper version to use on our clusters is included with a CUDA module:

```
[name@server ~]$ module load cuda/11.7

```

To profile a pure CPU executable, we need to add the arguments `--cpu-profiling on` to the command line:

```
[name@server ~]$ nvprof --cpu-profiling on ./cg.x 
...
<Program output >
...
======== CPU profiling result (bottom up):
Time(%)      Time  Name
 83.54%  90.6757s  matvec(matrix const &, vector const &, vector const &)
 83.54%  90.6757s  | main
  7.94%  8.62146s  waxpby(double, vector const &, double, vector const &, vector const &)
  7.94%  8.62146s  | main
  5.86%  6.36584s  dot(vector const &, vector const &)
  5.86%  6.36584s  | main
  2.47%  2.67666s  allocate_3d_poisson_matrix(matrix&, int)
  2.47%  2.67666s  | main
  0.13%  140.35ms  initialize_vector(vector&, double)
  0.13%  140.35ms  | main
...
======== Data collected at 100Hz frequency

```

From the above output, the `matvec()` function is responsible for 83.5% of the execution time, and this function call can be found in the `main()` function.

## Compiler Feedback

Before working on the routine, we need to understand what the compiler is actually doing by asking ourselves the following questions:

- What optimizations were applied automatically by the compiler?
- What prevented further optimizations?
- Can very minor modifications of the code affect performance?

The NVIDIA compiler offers a `-Minfo` flag with the following options:

- `all` - Print almost all types of compilation information, including:
  - `accel` - Print compiler operations related to the accelerator
  - `inline` - Print information about functions extracted and inlined
  - `loop,mp,par,stdpar,vect` - Print various information about loop optimization and vectorization
- `intensity` - Print compute intensity information about loops
- (none) - If `-Minfo` is used without any option, it is the same as with the `all` option, but without the `inline` information

### How to Enable Compiler Feedback

- Edit the `Makefile`:

```
 CXX=nvc++
 CXXFLAGS=-fast -Minfo=all,intensity
 LDFLAGS=${CXXFLAGS}

```

- Rebuild

```
[name@server ~]$ make clean; make
...
nvc++ -fast -Minfo=all,intensity   -c -o main.o main.cpp
initialize_vector(vector &, double):
     20, include "vector.h"
          36, Intensity = 0.0
              Memory set idiom, loop replaced by call to __c_mset8
dot(const vector &, const vector &):
     21, include "vector_functions.h"
          27, Intensity = 1.00
              Generated vector simd code for the loop containing reductions
          28, FMA (fused multiply-add) instruction(s) generated
waxpby(double, const vector &, double, const vector &, const vector &):
     21, include "vector_functions.h"
          39, Intensity = 1.00
              Loop not vectorized: data dependency
              Generated vector simd code for the loop
              Loop unrolled 2 times
              FMA (fused multiply-add) instruction(s) generated
          40, FMA (fused multiply-add) instruction(s) generated
allocate_3d_poisson_matrix(matrix &, int):
     22, include "matrix.h"
          43, Intensity = 0.0
              Loop not fused: different loop trip count
          44, Intensity = 0.0
              Loop not vectorized/parallelized: loop count too small
          45, Intensity = 0.0
              Loop unrolled 3 times (completely unrolled)
          57, Intensity = 0.0
          59, Intensity = 0.0
              Loop not vectorized: data dependency
matvec(const matrix &, const vector &, const vector &):
     23, include "matrix_functions.h"
          29, Intensity = (num_rows*((row_end-row_start)*         2))/(num_rows+(num_rows+(num_rows+((row_end-row_start)+(row_end-row_start)))))
          33, Intensity = 1.00
              Generated vector simd code for the loop containing reductions
          37, FMA (fused multiply-add) instruction(s) generated
main:
     38, allocate_3d_poisson_matrix(matrix &, int) inlined, size=41 (inline) file main.cpp (29)
          43, Intensity = 0.0
              Loop not fused: different loop trip count
          44, Intensity = 0.0
              Loop not vectorized/parallelized: loop count too small
          45, Intensity = 0.0
              Loop unrolled 3 times (completely unrolled)
          57, Intensity = 0.0
              Loop not fused: function call before adjacent loop
          59, Intensity = 0.0
              Loop not vectorized: data dependency
     42, allocate_vector(vector &, unsigned int) inlined, size=3 (inline) file main.cpp (24)
     43, allocate_vector(vector &, unsigned int) inlined, size=3 (inline) file main.cpp (24)
     44, allocate_vector(vector &, unsigned int) inlined, size=3 (inline) file main.cpp (24)
     45, allocate_vector(vector &, unsigned int) inlined, size=3 (inline) file main.cpp (24)
     46, allocate_vector(vector &, unsigned int) inlined, size=3 (inline) file main.cpp (24)
     48, initialize_vector(vector &, double) inlined, size=5 (inline) file main.cpp (34)
          36, Intensity = 0.0
              Memory set idiom, loop replaced by call to __c_mset8
     49, initialize_vector(vector &, double) inlined, size=5 (inline) file main.cpp (34)
          36, Intensity = 0.0
              Memory set idiom, loop replaced by call to __c_mset8
     52, waxpby(double, const vector &, double, const vector &, const vector &) inlined, size=10 (inline) file main.cpp (33)
          39, Intensity = 0.0
              Memory copy idiom, loop replaced by call to __c_mcopy8
     53, matvec(const matrix &, const vector &, const vector &) inlined, size=19 (inline) file main.cpp (20)
          29, Intensity = [symbolic], and not printable, try the -Mpfi -Mpfo options
              Loop not fused: different loop trip count
          33, Intensity = 1.00
              Generated vector simd code for the loop containing reductions
     54, waxpby(double, const vector &, double, const vector &, const vector &) inlined, size=10 (inline) file main.cpp (33)
          27, FMA (fused multiply-add) instruction(s) generated
          36, FMA (fused multiply-add) instruction(s) generated
          39, Intensity = 0.67
              Loop not fused: different loop trip count
              Loop not vectorized: data dependency
              Generated vector simd code for the loop
              Loop unrolled 4 times
              FMA (fused multiply-add) instruction(s) generated
     56, dot(const vector &, const vector &) inlined, size=9 (inline) file main.cpp (21)
          27, Intensity = 1.00
              Loop not fused: function call before adjacent loop
              Generated vector simd code for the loop containing reductions
     61, Intensity = 0.0
     62, waxpby(double, const vector &, double, const vector &, const vector &) inlined, size=10 (inline) file main.cpp (33)
          39, Intensity = 0.0
              Memory copy idiom, loop replaced by call to __c_mcopy8
     65, dot(const vector &, const vector &) inlined, size=9 (inline) file main.cpp (21)
          27, Intensity = 1.00
              Loop not fused: different controlling conditions
              Generated vector simd code for the loop containing reductions
     67, waxpby(double, const vector &, double, const vector &, const vector &) inlined, size=10 (inline) file main.cpp (33)
          39, Intensity = 0.67
              Loop not fused: different loop trip count
              Loop not vectorized: data dependency
              Generated vector simd code for the loop
              Loop unrolled 4 times
     72, matvec(const matrix &, const vector &, const vector &) inlined, size=19 (inline) file main.cpp (20)
          29, Intensity = [symbolic], and not printable, try the -Mpfi -Mpfo options
              Loop not fused: different loop trip count
          33, Intensity = 1.00
              Generated vector simd code for the loop containing reductions
     73, dot(const vector &, const vector &) inlined, size=9 (inline) file main.cpp (21)
          27, Intensity = 1.00
              Loop not fused: different loop trip count
              Generated vector simd code for the loop containing reductions
     77, waxpby(double, const vector &, double, const vector &, const vector &) inlined, size=10 (inline) file main.cpp (33)
          39, Intensity = 0.67
              Loop not fused: different loop trip count
              Loop not vectorized: data dependency
              Generated vector simd code for the loop
              Loop unrolled 4 times
     78, waxpby(double, const vector &, double, const vector &, const vector &) inlined, size=10 (inline) file main.cpp (33)
          39, Intensity = 0.67
              Loop not fused: function call before adjacent loop
              Loop not vectorized: data dependency
              Generated vector simd code for the loop
              Loop unrolled 4 times
     88, free_vector(vector &) inlined, size=2 (inline) file main.cpp (29)
     89, free_vector(vector &) inlined, size=2 (inline) file main.cpp (29)
     90, free_vector(vector &) inlined, size=2 (inline) file main.cpp (29)
     91, free_vector(vector &) inlined, size=2 (inline) file main.cpp (29)
     92, free_matrix(matrix &) inlined, size=5 (inline) file main.cpp (73)

```

### Interpretation of the Compiler Feedback

The *Computational Intensity* of a loop is a measure of how much work is being done compared to memory operations.
Basically:

Computational Intensity=Compute OperationsMemory Operations

In the compiler feedback, an `Intensity` ≥ 1.0 suggests that the loop might run well on a GPU.

## Understanding the code

Let's look closely at the main loop in the
[`matvec()` function implemented in `matrix_functions.h`](https://github.com/calculquebec/cq-formation-openacc/blob/main/cpp/matrix_functions.h#L29):

```
  for(int i=0;i<num_rows;i++) {
    double sum=0;
    int row_start=row_offsets[i];
    int row_end=row_offsets[i+1];
    for(int j=row_start; j<row_end;j++) {
      unsigned int Acol=cols[j];
      double Acoef=Acoefs[j]; 
      double xcoef=xcoefs[Acol]; 
      sum+=Acoef*xcoef;
    }
    ycoefs[i]=sum;
  }

```

Given the code above, we search for data dependencies:

- Does one loop iteration affect other loop iterations?
  - For example, when generating the **[Fibonacci sequence](https://en.wikipedia.org/wiki/Fibonacci_number)**, each new value depends on the previous two values. Therefore, efficient parallelism is very difficult to implement, if not impossible.
- Is the accumulation of values in `sum` a data dependency?
  - No, it’s a **[reduction](https://en.wikipedia.org/wiki/Reduction_operator)**! And modern compilers are good at optimizing such reductions.
- Do loop iterations read from and write to the same array, such that written values are used or overwritten in other iterations?
  - Fortunately, that does not happen in the above code.

Now that the code analysis is done, we are ready to add directives to the compiler.

[<- Previous unit: *Introduction*](OpenACC_Tutorial_-_Introduction.md) | [^- Back to the lesson plan](OpenACC_Tutorial.md) | [Onward to the next unit: *Adding directives* ->](OpenACC_Tutorial_-_Adding_directives.md)