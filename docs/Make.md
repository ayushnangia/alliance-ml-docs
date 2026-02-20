# Make

Other languages:

- English
- [français](Make_fr.md)

## Description

[make](http://en.wikipedia.org/wiki/Makefile) is a utility that automatically builds files, such as executables or libraries, from other files, such as source code.

The make command interprets and executes the instructions within a file named makefile. Unlike a simple script, make only executes the commands that are necessary. The goal is to arrive at a result (compiled or installed software, formatted documentation, etc.) without needing to redo all steps.

The makefile contains information on *dependencies*.
For example, if the makefile indicates that an object (.o) file depends on a source file, and the source file has changed, then the source file is recompiled to update the object file.
In the same way, if an executable depends on any object files which have changed then the linking step will be rerun to update the executable.
All dependencies must be included in the makefile. Then it is not necessary to recompile all files for every modification; the make command takes care of recompiling and relinking only what is necessary.

## Examples for using make

The main argument of the make command is the *target*. The *target* may be the name of some file that make should build, or it may be an abstract target such as *all*, *test*, *check*, *clean*, or *install*.
The targets that are available depend on the contents of the makefile, but the ones just listed are conventional and are
specified in many makefiles. If make is invoked with no target specified, like so:

```
[name@server ~]$ make

```

then the typical behaviour is to construct everything, equivalent to:

```
[name@server ~]$ make all

```

The *test* or *check* targets are generally used to run tests to validate if the application or compiled library functions correctly. Usually these targets depend on the *all* target. Hence you can verify the compilation using

```
[name@server ~]$ make all && make check

```

or

```
[name@server ~]$ make all && make test

```

The *clean* target erases all previously compiled binary files to be able to recompile from scratch. There is sometimes also a *distclean* target, which not only deletes files made by make, but also files created at configuration time by [configure](Autotools.md) or [cmake](CMake.md). So to clean the compilation directory, you can usually run

```
[name@server ~]$ make clean

```

and sometimes

```
[name@server ~]$ make distclean

```

The *install* target normally installs a compiled program or library. Where the installation is put depends on the makefile, but can often be modified using an additional *prefix* parameter, like this:

```
[name@server ~]$ make install prefix=$HOME/PROGRAM

```

The targets all, test, check, clean, distclean and install are only conventions and a makefile author could very well choose another convention. To get more information on typical target names, notably supported by all GNU applications, visit [this page](http://www.gnu.org/software/make/manual/make.html#Standard-Targets). Options to configure installation and other directories are [listed here](http://www.gnu.org/software/make/manual/make.html#Directory-Variables).

## Example of a Makefile

The following example, of general use, includes a lot of explanations and comments. For a detailed guide on how to create a makefile, visit [the GNU Make web site](http://www.gnu.org/software/make/manual/make.html#Introduction).

**File :** Makefile

```
# Makefile to easily update the compilation of a program (.out)
# --------
#
# by Alain Veilleux, 4 August 1993
#    Last revision : 30 March 1998
#
# GOAL AND FUNCTIONING OF THIS SCRIPT:
#    Script in the form of a "Makefile" allowing to update a program containing
#    multiple separated routines on the disk. This script is not executed by itself,
#    but is instead read and interpreted by the "make" command. When it is called,
#    the "make" command verifies the dates of the various components your program is
#    built from. Only routines that were modified after the last compilation of the
#    program are recompiled in object form (files ending in .o). Recompiled .o files
#    are subsequently linked together to form an updated version of the final program.
#
# TO ADAPT THIS SCRIPT TO YOUR PROGRAM:
#    Modify the contents of the variables hereunder. Comments will guide you how and
#    where.
#
# USING "make" ON THE UNIX COMMAND LINE:
#    1- Type "make" to update the whole program.
#    2- Type "make RoutineName" to only update the RoutineName routine.
#


#====================  Definition of variables  =====================
# Remark : variables are sometimes called "macros" in Makefiles.

# Compiler to use (FORTRAN, C or other)
CompilerName= xlf

# Compilation options: the below options are usually used to compile FORTRAN
#                      code. You can assign other values than those suggested
#                      in the "CompilationOptions" variables.
#CompilationOptions= -O3
# Remove the below "#" to activate compilation in debug mode
#CompilationOptions= -g
# Remove the below "#" to use "gprof", which indicates the computation time in
#    each subroutine
#CompilationOptions= -O3 -pg

# List of routines to compile: here we list all object files that are needed.
# Put a "\" at the end of each line that if you want to continue the list of
#    routines on the following line.
ObjectFiles= trnb3-1.part.o mac4251.o inith.o dsite.o initv.o main.o \
             entree.o gcals.o defvar1.o defvar2.o magst.o mesure.o

# Name of the final executable
ProgramOut= trnb3-1.out
#=====  End of variable definitions =====
#===============  There is nothing to change below this line  =============


# Defines a rule: how to build an object file (ending in ".o")
#                 from a source file (ending in ".f")
# note: "$<" symbols will be replaced by the name of the file that is compiled
# Compiling Fortran files:
.f.o:
	$(CompilerName) $(CompilationOptions) -c $<

# Defines a rule: how to build an object file (ending in ".o")
#                from a source file (ending in ".c")
# note: "$<" symbols will be replaced by the name of the file that is compiled
# Compiling C files:
.c.o:
	$(CompilerName) $(CompilationOptions) -c $<

# Defines a rule: how to build an object file (ending in ".o")
#                 from a source file (ending in ".C")
# note: "$<" symbols will be replaced by the name of the file that is compiled
# Compiling C++ files:
.C.o:
	$(CompilerName) $(CompilationOptions) -c $<

# Dependencies of the main executable on the object files (".o") it is built from.
# The dependency of object files on source files (".f" and ".c") is implied by the above
# implicit rules.
$(ProgramOut): $(ObjectFiles)
	$(CompilerName) $(CompilationOptions) -o $(ProgramOut) \
							$(ObjectFiles)

```