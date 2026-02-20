# CMake

Other languages:

- English
- [français](CMake_fr.md)

## Description

[CMake](http://www.cmake.org/) is a free multi-language multi-platform compilation tool (the name stands for *cross-platform make*). Although [Autotools](Autotools.md) is the traditional tool used on Linux—by GNU projects among others—, various projects have changed to CMake during the last few years, for different reasons, including for example KDE and MySQL. Those who have already had difficulties with Autotools in their own project will probably find CMake much easier to use. In fact, according to KDE, the main reason for which they have changed from Autotools to CMake is that the compilation is a lot quicker and the build files are a lot easier to write.

## Basic usage

CMake works in the same way as that Autotools requires to run a `configure` script, followed by a build with `make`. However, instead of calling `./configure`, you call `cmake directory`. For example, if you are inside the directory where you would like to build the application, you run

```
[name@server ~]$ cmake .

```

Hence, to configure, build and install an application or a library, the simplest way to do this is with

```
[name@server ~]$ cmake . && make && make install

```

## Useful options on our clusters

Our clusters are configured such that compilation of a new software package will automatically add information to the resulting binary to ensure that it finds the libraries that it depends on. This is done through a mechanism called `RUNPATH` or `RPATH`. Some packages using CMake also do the same, through a feature provided by CMake. When both of these are used at the same time, it sometimes creates conflicts. In order to avoid errors related to this, you can add the option

- `-DCMAKE_SKIP_INSTALL_RPATH=ON`

to your command line. Moreover, our clusters have libraries installed in non-standard locations. This sometimes causes CMake not to find them easily. It can be useful to the following option to your `cmake` command invocation:

- `-DCMAKE_SYSTEM_PREFIX_PATH=$EBROOTGENTOO`

Sometimes, even this is not sufficient, and you may have to add more specific options for libraries that are used by your software package. For example:

- `-DCURL_LIBRARY=$EBROOTGENTOO/lib/libcurl.so -DCURL_INCLUDE_DIR=$EBROOTGENTOO/include`
- `-DPYTHON_EXECUTABLE=$EBROOTPYTHON/bin/python`
- `-DPNG_PNG_INCLUDE_DIR=$EBROOTGENTOO/include -DPNG_LIBRARY=$EBROOTGENTOO/lib/libpng.so`
- `-DJPEG_INCLUDE_DIR=$EBROOTGENTOO/include -DJPEG_LIBRARY=$EBROOTGENTOO/lib/libjpeg.so`
- `-DOPENGL_INCLUDE_DIR=$EBROOTGENTOO/include -DOPENGL_gl_LIBRARY=$EBROOTGENTOO/lib/libGL.so -DOPENGL_glu_LIBRARY=$EBROOTGENTOO/lib/libGLU.so`
- `-DZLIB_ROOT=$EBROOTGENTOO`

## Customizing the configuration

Just like with `autotools`, it is possible to customize the configuration of an application or a library. This can be done by different command line options, but also using a command line interface with the `ccmake` command.

### `ccmake`

You call `ccmake` in the same way as you call `cmake`, by giving the directory to build from. So if this is the current directory, you should call

```
[name@server ~]$ ccmake .

```

You should run `ccmake` *after* having ran `cmake`. So, generally you would do

```
[name@server ~]$ cmake . && ccmake .

```

`ccmake` gives you then a list of options that are defined by the project. You will then see a relatively short list like this:

```
[name@server ~]$ cmake . && ccmake .
Page 1 of 1
 ARPACK_LIBRARIES                 ARPACK_LIBRARIES-NOTFOUND
 CMAKE_BUILD_TYPE
 CMAKE_INSTALL_PREFIX             /usr/local
 CMAKE_OSX_ARCHITECTURES
 CMAKE_OSX_DEPLOYMENT_TARGET
 CMAKE_OSX_SYSROOT                /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.8.sdk
 GSL_CONFIG                       /opt/local/bin/gsl-config
 GSL_CONFIG_PREFER_PATH           /bin;;/bin;
 GSL_EXE_LINKER_FLAGS             -Wl,-rpath,/opt/local/lib
 NON_TEMPLATES_DISABLED           ON
 NO_SQUACK_WARNINGS               ON
 PRECOMPILED_TEMPLATES            ON
 USE_GSL_OMP                      OFF
 USE_OMP                          OFF
Press [enter] to edit option                                                                                                                                                         CMake Version 2.8.8
Press [c] to configure
Press [h] for help           Press [q] to quit without generating
Press [t] to toggle advanced mode (Currently Off)

```

As is written at the bottom of this display, you can edit a value by pressing the `enter` key. If you modify a value, you will want to press the `c` key to try out the configuration with this new value. If this new configuration succeeds with that new value, you will then have the option `g` to generate the `Makefile` with the new configuration, or you can quit using the `q` key. Lastly, you can activate advanced mode using the `t` key. You will then have a much longer list of variables which allows you to precisely configure the application. Here is a list of options

**File :** ccmake\_output.txt

```
ARPACK_LIBRARIES                 ARPACK_LIBRARIES-NOTFOUND
 BLAS_Accelerate_LIBRARY          /System/Library/Frameworks/Accelerate.framework
 BLAS_acml_LIBRARY                BLAS_acml_LIBRARY-NOTFOUND
 BLAS_acml_mp_LIBRARY             BLAS_acml_mp_LIBRARY-NOTFOUND
 BLAS_complib.sgimath_LIBRARY     BLAS_complib.sgimath_LIBRARY-NOTFOUND
 BLAS_cxml_LIBRARY                BLAS_cxml_LIBRARY-NOTFOUND
 BLAS_dxml_LIBRARY                BLAS_dxml_LIBRARY-NOTFOUND
 BLAS_essl_LIBRARY                BLAS_essl_LIBRARY-NOTFOUND
 BLAS_f77blas_LIBRARY             BLAS_f77blas_LIBRARY-NOTFOUND
 BLAS_goto2_LIBRARY               BLAS_goto2_LIBRARY-NOTFOUND
 BLAS_scsl_LIBRARY                BLAS_scsl_LIBRARY-NOTFOUND
 BLAS_sgemm_LIBRARY               BLAS_sgemm_LIBRARY-NOTFOUND
 BLAS_sunperf_LIBRARY             BLAS_sunperf_LIBRARY-NOTFOUND
 CMAKE_AR                         /opt/local/bin/ar
 CMAKE_BUILD_TYPE
 CMAKE_COLOR_MAKEFILE             ON
 CMAKE_CXX_COMPILER               /opt/local/bin/c++
 CMAKE_CXX_FLAGS
 CMAKE_CXX_FLAGS_DEBUG            -g
 CMAKE_CXX_FLAGS_MINSIZEREL       -Os -DNDEBUG
 CMAKE_CXX_FLAGS_RELEASE          -O3 -DNDEBUG
 CMAKE_CXX_FLAGS_RELWITHDEBINFO   -O2 -g
 CMAKE_C_COMPILER                 /opt/local/bin/gcc
 CMAKE_C_FLAGS
 CMAKE_C_FLAGS_DEBUG              -g
 CMAKE_C_FLAGS_MINSIZEREL         -Os -DNDEBUG
 CMAKE_C_FLAGS_RELEASE            -O3 -DNDEBUG
 CMAKE_C_FLAGS_RELWITHDEBINFO     -O2 -g
 CMAKE_EXE_LINKER_FLAGS
 CMAKE_EXE_LINKER_FLAGS_DEBUG
 CMAKE_EXE_LINKER_FLAGS_MINSIZE
 CMAKE_EXE_LINKER_FLAGS_RELEASE
 CMAKE_EXE_LINKER_FLAGS_RELWITH
 CMAKE_EXPORT_COMPILE_COMMANDS    OFF
 CMAKE_INSTALL_NAME_TOOL          /opt/local/bin/install_name_tool
 CMAKE_INSTALL_PREFIX             /usr/local
 CMAKE_LINKER                     /opt/local/bin/ld
 CMAKE_MAKE_PROGRAM               /Applications/Xcode.app/Contents/Developer/usr/bin/make
 CMAKE_MODULE_LINKER_FLAGS
 CMAKE_MODULE_LINKER_FLAGS_DEBU
 CMAKE_MODULE_LINKER_FLAGS_MINS
 CMAKE_MODULE_LINKER_FLAGS_RELE
 CMAKE_MODULE_LINKER_FLAGS_RELW
 CMAKE_NM                         /opt/local/bin/nm
 CMAKE_OBJCOPY                    CMAKE_OBJCOPY-NOTFOUND
 CMAKE_OBJDUMP                    CMAKE_OBJDUMP-NOTFOUND
 CMAKE_OSX_ARCHITECTURES
 CMAKE_OSX_DEPLOYMENT_TARGET
 CMAKE_OSX_SYSROOT                /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.8.sdk
 CMAKE_RANLIB                     /opt/local/bin/ranlib
 CMAKE_SHARED_LINKER_FLAGS
 CMAKE_SHARED_LINKER_FLAGS_DEBU
 CMAKE_SHARED_LINKER_FLAGS_MINS
 CMAKE_SHARED_LINKER_FLAGS_RELE
 CMAKE_SHARED_LINKER_FLAGS_RELW
 CMAKE_SKIP_INSTALL_RPATH         OFF
 CMAKE_SKIP_RPATH                 OFF
 CMAKE_STRIP                      /opt/local/bin/strip
 CMAKE_USE_RELATIVE_PATHS         OFF
 CMAKE_VERBOSE_MAKEFILE           OFF
 CMAKE_XCODE_SELECT               /usr/bin/xcode-select
 DOXYGEN_DOT_EXECUTABLE           /usr/local/bin/dot
 DOXYGEN_DOT_PATH                 /usr/local/bin
 DOXYGEN_EXECUTABLE               /Applications/Doxygen.app/Contents/Resources/doxygen
 GSL_CONFIG                       /opt/local/bin/gsl-config
 GSL_CONFIG_PREFER_PATH           /bin;;/bin;
 GSL_EXE_LINKER_FLAGS             -Wl,-rpath,/opt/local/lib
 GSL_INCLUDE_DIR                  /opt/local/include
 GTEST_INCLUDE_DIR                /opt/local/include
 GTEST_LIBRARY                    /opt/local/lib/libgtest.dylib
 GTEST_LIBRARY_DEBUG              GTEST_LIBRARY_DEBUG-NOTFOUND
 GTEST_MAIN_LIBRARY               /opt/local/lib/libgtest_main.dylib
 GTEST_MAIN_LIBRARY_DEBUG         GTEST_MAIN_LIBRARY_DEBUG-NOTFOUND
 LAPACK_Accelerate_LIBRARY        /System/Library/Frameworks/Accelerate.framework
 LAPACK_goto2_LIBRARY             LAPACK_goto2_LIBRARY-NOTFOUND
 NON_TEMPLATES_DISABLED           ON
 NO_SQUACK_WARNINGS               ON
 PRECOMPILED_TEMPLATES            ON
 USE_GSL_OMP                      OFF
 USE_OMP                          OFF

```

As you can see, `ccmake` in advanced mode displays equally well the libraries that were found as those that were not found. If you would like to use a specific version of [BLAS](BLAS_and_LAPACK.md) for example, you will immediately know which one was found by CMake, and modify this if necessary. `ccmake` also displays the list of flags that are passed to the C, C++, and other compilers, to the linker, depending on the build type.

### Command line options

All command line options that are displayed by `ccmake` can be modified on the command line, using the following syntax:

```
[name@server ~]$ cmake . -DVARIABLE=VALUE

```

For example, to specify the install location:

```
[name@server ~]$ cmake . -DCMAKE_INSTALL_PREFIX=/home/user/my_directory

```

To configure the compilation, you might want to change the following values:

| Option | Description |
| --- | --- |
| CMAKE_C_COMPILER | Change the C compiler |
| CMAKE_CXX_COMPILER | Change the C++ compiler |
| CMAKE_LINKER | Change the linker |
| CMAKE_C_FLAGS | Change the flags passed to the C compiler |
| CMAKE_CXX_FLAGS | Change the flags passed to the C++ compiler |
| CMAKE_SHARED_LINKER_FLAGS | Change the flags passed to the linker |

A more exhaustive list option is available [on the official CMake page](http://www.cmake.org/Wiki/CMake_Useful_Variables).

If you do not want to get into adventures with these specific options, CMake also provides a simpler option, called `CMAKE_BUILD_TYPE`. This option defines which compilation type must be used. Possible values are

| Option | Description |
| --- | --- |
| - | No value |
| Debug | Activate debugging options, deactivate optimization options |
| Release | Deactivate debugging options, activate usual optimizations |
| MinSizeRel | Deactivate debugging options, activate optimization options that minimize the binary's size |
| RelWithDebInfo | Activate debugging options and usual optimizations |

These different compilation types define compiler options that vary from compiler to compiler. So you do not need to check which exact compiler flags have to be used.

## References

- [A simple example](http://www.cmake.org/cmake/help/examples.html) on the official site.
- [A tutorial](http://www.cmake.org/cmake/help/cmake_tutorial.html) that is more complete on the official site.