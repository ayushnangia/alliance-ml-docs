# XGBoost

Other languages:

- English
- [français](XGBoost_fr.md)

**[XGBoost](https://xgboost.readthedocs.io/en/latest/)** *is an optimized distributed gradient boosting library designed to be highly efficient, flexible and portable*. It is a popular package used for a wide variety of machine learning and datascience tasks, serving the role of a convenient, domain-agnostic black box classifier. XGBoost provides GPU accelerated learning for some problems, and Compute Canada provides a GPU enabled build.

For detailed documentation on using the library, please consult the [xgboost documentation](https://xgboost.readthedocs.io/en/latest/get_started.html). There is a [separate section for GPU-enabled training](https://xgboost.readthedocs.io/en/latest/gpu/index.html).

## Python Module Installation

A very common way to use XGBoost is though its python interface, provided as the `xgboost` python module. Compute Canada provides an optimized, multi-GPU enabled build as a [Python](Python.md) wheel; readers can should familiarize themselves with the use of [Python virtual environments](Python.md#Creating_and_using_a_virtual_environment) before starting an XGBoost project.

Currently, version 0.81 of XGBoost is available. The following commands illustrate the needed package and module:

```
(myvenv) name@server $ module load nixpkgs/16.09 intel/2018.3 cuda/10.0.130
(myvenv) name@server $ module load nccl/2.3.5
(myvenv) name@server $ pip install xgboost==0.81 --no-index

```