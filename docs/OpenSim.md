# OpenSim

## Description

"[OpenSim](https://simtk.org/projects/opensim) is a freely available, user extensible software system that lets users develop models of musculoskeletal structures and create dynamic simulations of movement. "
OpenSim includes Python and Matlab APIs. It is commonly used with [OpenSim Moco](https://opensim-org.github.io/opensim-moco-site/).

The OpenSim module available through our software stack includes support for OpenSim Moco, as well as bindings to enable scripting in Python or Matlab.

## Using OpenSim via Matlab

### Setup

Before first use of OpenSim on a cluster, you must configure the necessary Java paths, by running:

```
[name@server ~]$ matlab -batch "cd ${EBROOTOPENSIM}/share/doc/OpenSim/Code/Matlab/; configureOpenSim"

```

After exiting and relaunching Matlab, you can verify that OpenSim is imported by running in Matlab:  `org.opensim.modeling.opensimCommon.GetVersion()`

## Using OpenSim via Python

In order to use the OpenSim Python package, an OpenSim module must be loaded, and a numpy package must be available through a [virtual environment](Python.md#Creating_and_using_a_virtual_environment) or loading a [scipy-stack](Python.md#SciPy_stack) module. You should subsequently be able to import the `opensim` package in Python.