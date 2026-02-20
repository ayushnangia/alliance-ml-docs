# SpaCy

Other languages:

- English
- [français](SpaCy_fr.md)

[spaCy](https://spacy.io/) is a Python package that provides industrial-strength natural language processing.

# Installation

## Latest available wheels

To see the latest version of spaCy that we have built:

```
[name@server ~]$ avail_wheels spacy thinc thinc_gpu_ops

```

For more information on listing wheels, see [listing available wheels](Python.md#Listing_available_wheels).

## Pre-build

The preferred option is to install it using the python [wheel](https://pythonwheels.com/) that we compile, as follows:

:   1. Load python 3.6 module: python/3.6
:   2. Create and activate a [virtual environment](Python.md#Creating_and_using_a_virtual_environment).
:   3. Install spaCy in the virtual environment with `pip install`. For both GPU and CPU support:

```
(venv) [name@server ~] pip install spacy[cuda] --no-index

```

:   If you only need CPU support:

```
(venv) [name@server ~] pip install spacy --no-index

```

**GPU version**: At the present time, in order to use the GPU version you need to add the CUDA libraries to LD\_LIBRARY\_PATH:

```
(venv) [name@server ~] module load gcc/5.4.0 cuda/9
(venv) [name@server ~] export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

```

If you want to use the [Pytorch](https://docs.computecanada.ca/wiki/PyTorch) wrapper with thinc, you'll also need to install the torch\_cpu or torch\_gpu wheel.