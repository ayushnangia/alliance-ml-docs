# Autotools

Other languages:

- English
- [français](Autotools_fr.md)

## Description

[**autoconf**](https://en.wikipedia.org/wiki/Autoconf) is a tool that belongs to the [autotools](http://en.wikipedia.org/wiki/GNU_build_system) suite, also known as the *GNU build system*. The tool automates the process of generating the custom [Makefiles](Make.md) necessary to build a program on different systems, with (perhaps) different compilers.
When a program is built with the help of *autoconf*, the first step is to call the *configure* script:

```
[name@server ~]$ ./configure

```

This verifies that compilers and other relevant software are installed on the computer and that appropriate versions are available, and generates a Makefile customized for your system.

After that, you call [make](Make.md) as usual:

```
[name@server ~]$ make

```

Finally, *make install* installs the files at the right places. If you don't want to install the software for all users of the server, but only for yourself, you normally need to specify where to install your software. You can (usually) do this in the following manner:

```
[name@server ~]$ mkdir $HOME/SOFTWARE
[name@server ~]$ make install --prefix=$HOME/SOFTWARE

```

In other cases you must supply the --prefix option to ./configure instead of to make; see the documentation for the particular software you are trying to install. You may also wish to create a module to show the system the paths to your newly installed software.

A basic compilation of a program using *autoconf* can thus be as simple as

```
[name@server ~]$ ./configure && make && make install --prefix=$HOME/SOFTWARE

```

## Frequently used options for *configure* scripts

*configure* scripts generally accept a large number of options. They vary from project to project. Nevertheless certain options are very common and deserve mentioning. In all cases you can run

```
[name@server ~]$ ./configure --help

```

to get a detailed list of all supported options.

### Installation directory

An option that is always available is --prefix. This option allows you to define the directory where the command make install installs the application or the library. For example, to install an application into the subdirectory programs within your home directory, you could use

```
[name@server ~]$ ./configure --prefix=$HOME/programs/

```

### Feature options

Most configuration scripts allow you to enable or to disable certain features of the program or library that you compile. Those options are generally of the type --enable-feature or --disable-feature. Within advanced computing, those options often include for example parallelization using threads or using MPI. You could thus have

```
[name@server ~]$ ./configure --enable-mpi

```

or also

```
[name@server ~]$ ./configure --enable-threads

```

Often there are also options like --with-... to configure some features specifically. **It is generally recommended to not use such options and let autoconf find the parameters automatically.** Nevertheless it is sometimes necessary to specify some parameters using --with-... options. For example, you could specify

```
[name@server ~]$ ./configure --enable-mpi --with-mpi-dir=$MPIDIR

```

### Options defined by variables

You can generally specify the compiler that is used and the options that should be passed to it by declaring variables after the ./configure command. For example, to define the C compiler and the options to give it, you could run

```
[name@server ~]$ ./configure CC=icc CFLAGS="-O3 -xHost"

```

The most commonly used variables include

| Option | Description |
| --- | --- |
| CFLAGS | Options to pass to the C compiler |
| CPPFLAGS | Options to pass to the preprocessor and to C, C++, Objective C, and Objective C++ compilers |
| CXXFLAGS | Options to pass to the C++ compiler |
| DEFS | Allows the definition of a preprocessor macro |
| FCFLAGS | Options to pass to the Fortran compiler |
| FFLAGS | Options to pass to the Fortran 77 compiler |
| LDFLAGS | Options to pass to the linker |
| LIBS | Libraries to link |

A more exhaustive list of variables and typical options is available [in the autoconf documentation](http://www.gnu.org/software/autoconf/manual/autoconf.html).