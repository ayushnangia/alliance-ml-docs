# RDKit

Other languages:

- English
- [français](RDKit_fr.md)

[RDKit](https://www.rdkit.org/) is a collection of cheminformatics and machine-learning software written in C++ and Python.

# Available versions

`rdkit` C++ libraries and Python bindings are available as a module.

You can find available versions with:

```
[name@server ~]$ module spider rdkit

```

and look for more information on a specific version with:

```
[name@server ~]$ module spider rdkit/X.Y.Z

```

where `X.Y.Z` is the exact desired version, for instance `2024.03.5`.

# Python bindings

The module contains bindings for multiple Python versions. To discover which are the compatible Python versions, run:

```
[name@server ~]$ module spider rdkit/X.Y.Z

```

where X.Y.Z represents the desired version.

## rdkit as a Python package dependency

When `rdkit` is a dependency of another package, the dependency needs to be fulfilled:

1. Deactivate any Python virtual environment.

```
[name@server ~]$ test $VIRTUAL_ENV && deactivate

```

**Note:** If you had a virtual environment activated, it is important to deactivate it first, then load the module, before reactivating your virtual environment.

2. Load the module.

```
[name@server ~]$ module load rdkit/2024.03.5 python/3.12

```

3. Check that it is visible by `pip`

```
[name@server ~]$ pip list | grep rdkit
rdkit            2024.3.5

```

```
[name@server ~]$ python -c 'import rdkit'

```

If no errors are raised, then everything is OK!

4. [Create a virtual environment and install your packages](Python.md#Creating_and_using_a_virtual_environment).

# Troubleshooting

## ModuleNotFoundError: No module named 'rdkit'

If `rdkit` is not accessible, you may get the following error when importing it:
`ModuleNotFoundError: No module named 'rdkit'`

Possible solutions:

- check which Python versions are compatible with your loaded RDKit module using `module spider rdkit/X.Y.Z`. Once a compatible Python module is loaded, check that `python -c 'import rdkit'` works.
- load the module before activating your virtual environment: please see the rdkit as a package dependency section above.

See also [ModuleNotFoundError: No module named 'X'](Python.md#ModuleNotFoundError:_No_module_named_'X').