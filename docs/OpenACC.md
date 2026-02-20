# OpenACC

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

OpenACC makes it relatively easy to offload vectorized code to accelerators such as GPUs, for example. Unlike [CUDA](CUDA.md) and OpenCL where kernels need to be coded explicitly, OpenACC minimizes the amount of modifications to do on a serial or [OpenMP](OpenMP.md) code. The compiler converts the OpenACC code into a binary executable that can make use of accelerators. The performance of OpenACC codes can be similar to the one of a [CUDA](CUDA.md) code, except that OpenACC requires less code development.

# OpenACC directives

Similar to [OpenMP](OpenMP.md), OpenACC can convert a `for` loop into parallel code that would run on an accelerator. This can be achieved with compiler directives `#pragma acc ...` before structured blocks of code like, for example, a `for` loop. All supported `pragma` directives are described in the [OpenACC specification](https://www.openacc.org/specification).

# Code examples

OpenACC can be used in [Fortran](Fortran.md), [C](C.md) and [C++](C.md), which we illustrate here using a simple program that computes a decimal approximation to π based on a definite integral which is equal to arctan(1), i.e. π/4.

CC++

**File :** pi.c

```
#include <stdio.h>

const int vl = 512;
const long long N = 2000000000;

int main(int argc,char** argv) {
  double pi = 0.0f;
  long long i;

  #pragma acc parallel vector_length(vl) 
  #pragma acc loop reduction(+:pi)
  for (i = 0; i < N; i++) {
    double t = (double)((i + 0.5) / N);
    pi += 4.0 / (1.0 + t * t);
  }
  printf("pi = %11.10f\n", pi / N);
  return 0;
}

```

**File :** pi.cxx

```
#include <iostream>
#include <iomanip>

const int vl = 512;
const long long N = 2000000000;

int main(int argc,char** argv) {
  double pi = 0.0f;
  long long i;

  #pragma acc parallel vector_length(vl)
  #pragma acc loop reduction(+:pi)
  for (i = 0; i < N; i++) {
    double t = double((i + 0.5) / N);
    pi += 4.0/(1.0 + t * t);
  }
  std::cout << std::fixed;
  std::cout << std::setprecision(10);
  std::cout << "pi = " << pi/double(N) << std::endl;
  return 0;
}

```

# Compilers

## PGI

- Module `pgi`, any version from 13.10
  - Newer versions support newest GPU capabilities.

Compilation example:

```
# TODO

```

## GCC

- Module `gcc`, any version from 9.3.0
  - Newer versions support newest GPU capabilities.

Compilation example:

```
gcc -fopenacc -march=native -O3 pi.c -o pi

```

# Tutorial

See our [OpenACC\_Tutorial](OpenACC_Tutorial.md).

# References

- [OpenACC official documentation - Specification 3.1 (PDF)](https://www.openacc.org/sites/default/files/inline-images/Specification/OpenACC-3.1-final.pdf)
- [NVIDIA OpenACC API - Quick Reference Guide (PDF)](https://www.nvidia.com/docs/IO/116711/OpenACC-API.pdf)