# Faiss

Other languages:

- English
- [français](Faiss_fr.md)

[Faiss](https://github.com/facebookresearch/faiss/wiki) is a library for efficient similarity search and clustering of dense vectors. It contains algorithms that search in sets of vectors of any size, up to ones that possibly do not fit in RAM. It also contains supporting code for evaluation and parameter tuning. Faiss is written in C++ with complete wrappers for Python (versions 2 and 3). Some of the most useful algorithms are implemented on GPU. It is developed primarily at [Meta AI Research](https://research.facebook.com/) with help from external contributors.

## Python bindings

The module contains bindings for multiple Python versions.
To discover which are the compatible Python versions, run

```
[name@server ~]$ module spider faiss/X.Y.Z

```

Or search directly *faiss-cpu*, by running

```
[name@server ~]$ module spider faiss-cpu/X.Y.Z

```

where X.Y.Z represent the desired version.

### Usage

1. Load the required modules.

```
[name@server ~]$ module load StdEnv/2023 gcc cuda faiss/X.Y.Z python/3.11

```

where X.Y.Z represent the desired version.

2. Import Faiss.

```
[name@server ~]$ python -c "import faiss"

```

If the command displays nothing, the import was successful.

#### Available Python packages

Other Python packages depend on faiss-cpu or faiss-gpu bindings in order to be installed.
The `faiss` module provides:

- `faiss`
- `faiss-gpu`
- `faiss-cpu`

```
[name@server ~]$ pip list | fgrep faiss
faiss-gpu                          1.7.4
faiss-cpu                          1.7.4
faiss                              1.7.4

```

With the `faiss` module loaded, package dependency for the above extensions will be satisfied.