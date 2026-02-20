# Arrow

Other languages:

- English
- [français](Arrow_fr.md)

[Apache Arrow](https://arrow.apache.org/) is a cross-language development platform for in-memory data. It uses a standardized language-independent columnar memory format for flat and hierarchical data, organized for efficient analytic operations. It also provides computational libraries and zero-copy streaming messaging and interprocess communication. Languages currently supported include C, C++, C#, Go, Java, JavaScript, MATLAB, Python, R, Ruby, and Rust.

## CUDA

Arrow is also available with CUDA.

```
[name@server ~]$ module load gcc arrow/X.Y.Z cuda

```

where X.Y.Z represent the desired version.

## Python bindings

The module contains bindings for multiple Python versions.
To discover which are the compatible Python versions, run

```
[name@server ~]$ module spider arrow/X.Y.Z

```

where X.Y.Z represent the desired version.

Or search directly *pyarrow*, by running

```
[name@server ~]$ module spider pyarrow

```

### PyArrow

The Arrow Python bindings (also named *PyArrow*) have first-class integration with NumPy, Pandas, and built-in Python objects. They are based on the C++ implementation of Arrow.

1. Load the required modules.

```
[name@server ~]$ module load gcc arrow/X.Y.Z python/3.11

```

where X.Y.Z represent the desired version.

2. Import PyArrow.

```
[name@server ~]$ python -c "import pyarrow"

```

If the command displays nothing, the import was successful.

For more information, see the [Arrow Python](https://arrow.apache.org/docs/python/) documentation.

#### Fulfilling other Python package dependency

Other Python packages depends on PyArrow in order to be installed.
With the `arrow` module loaded, your package dependency for `pyarrow` will be satisfied.

```
[name@server ~]$ pip list | grep pyarrow
pyarrow    17.0.0

```

#### Apache Parquet format

The [Parquet](http://parquet.apache.org/) file format is available.

To import the Parquet module, execute the previous steps for `pyarrow`, then run

```
[name@server ~]$ python -c "import pyarrow.parquet"

```

If the command displays nothing, the import was successful.

## R bindings

The Arrow package exposes an interface to the Arrow C++ library to access many of its features in R. This includes support for analyzing large, multi-file datasets ([open\_dataset()](https://arrow.apache.org/docs/r/reference/open_dataset.html)), working with individual Parquet files ([read\_parquet()](https://arrow.apache.org/docs/r/reference/read_parquet.html), [write\_parquet()](https://arrow.apache.org/docs/r/reference/write_parquet.html)) and Feather files ([read\_feather()](https://arrow.apache.org/docs/r/reference/read_feather.html), [write\_feather()](https://arrow.apache.org/docs/r/reference/write_feather.html)), as well as lower-level access to the Arrow memory and messages.

### Installation

1. Load the required modules.

```
[name@server ~]$ module load StdEnv/2020 gcc/9.3.0 arrow/8 r/4.1 boost/1.72.0

```

2. Specify the local installation directory.

```
[name@server ~]$ mkdir -p ~/.local/R/$EBVERSIONR/
[name@server ~]$ export R_LIBS=~/.local/R/$EBVERSIONR/

```

3. Export the required variables to ensure you are using the system installation.

```
[name@server ~]$ export PKG_CONFIG_PATH=$EBROOTARROW/lib/pkgconfig
[name@server ~]$ export INCLUDE_DIR=$EBROOTARROW/include
[name@server ~]$ export LIB_DIR=$EBROOTARROW/lib

```

4. Install the bindings.

```
[name@server ~]$ R -e 'install.packages("arrow", repos="https://cloud.r-project.org/")'

```

### Usage

After the bindings are installed, they have to be loaded.

1. Load the required modules.

```
[name@server ~]$ module load StdEnv/2020 gcc/9.3.0 arrow/8 r/4.1

```

2. Load the library.

```
[name@server ~]$ R -e "library(arrow)"
> library("arrow")
Attaching package: ‘arrow’

```

For more information, see the [Arrow R documentation](https://arrow.apache.org/docs/r/index.html)