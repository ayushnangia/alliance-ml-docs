# OpenACC Tutorial

Other languages:

- English
- [français](OpenACC_Tutorial_fr.md)

This tutorial is strongly inspired from the OpenACC Bootcamp session presented at [GPU Technology Conference 2016](http://www.gputechconf.com/).

OpenACC is an application programming interface (API) for porting code onto accelerators such as GPU and coprocessors. It has been developed by Cray, CAPS, NVidia and PGI. Like in [OpenMP](OpenMP.md), the programmer annotates C, C++ or Fortran code to identify portions that should be parallelized by the compiler.

A self-paced course on this topic is available from SHARCNET: [Introduction to GPU Programming](https://training.sharcnet.ca/courses/enrol/index.php?id=173).

Prerequisites for this tutorial

This tutorial uses OpenACC to accelerate C, C++ or Fortran code. A working knowledge of one of these languages is therefore required to gain the most benefit out of it.

Getting ready

This tutorial is based on examples. You can download all of the examples in this [Github repository](https://github.com/calculquebec/cq-formation-openacc).

## Lesson plan

- [Introduction](OpenACC_Tutorial_-_Introduction.md)
- [Gathering a profile and getting compiler information](OpenACC_Tutorial_-_Profiling.md)
- [Expressing parallelism with OpenACC directives](OpenACC_Tutorial_-_Adding_directives.md)
- [Expressing data movement](OpenACC_Tutorial_-_Data_movement.md)
- [Optimizing loops](OpenACC_Tutorial_-_Optimizing_loops.md)

## External references

Here are some useful external references:

- [OpenACC Programming and Best Practices Guide (PDF)](https://www.openacc.org/sites/default/files/inline-files/openacc-guide.pdf)
- [OpenACC API 2.7 Reference Guide (PDF)](https://www.openacc.org/sites/default/files/inline-files/API%20Guide%202.7.pdf)
- [Getting Started with OpenACC](https://developer.nvidia.com/blog/getting-started-openacc/)
- [PGI Compiler](https://docs.nvidia.com/hpc-sdk/pgi-compilers/legacy.html)
- [PG Profiler](http://www.pgroup.com/resources/pgprof-quickstart.htm)
- [NVIDIA Visual Profiler](http://docs.nvidia.com/cuda/profiler-users-guide/index.html#visual-profiler)