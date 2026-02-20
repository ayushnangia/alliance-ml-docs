# Large Scale Machine Learning (Big Data)

Other languages:

- English
- [français](Large_Scale_Machine_Learning_Big_Data_fr.md)

In the field of Deep Learning, the widespread use of mini-batching strategies along with first-order iterative solvers makes most common training tasks naturally scalable to large quantities of data. Whether you are looking at training Deep Neural Networks on a few thousand examples, or hundreds of millions of them, the flow of your code will look pretty much the same: load a few examples from a target source (from disk, from memory, from a remote source...) and iterate through them, computing gradients and using them to update the parameters of the model as you go. Conversely, in many Traditional Machine Learning packages --notably `scikit-learn`-- scaling your code to train on very large datasets is often not trivial. Many algorithms that fit common models such as Generalized Linear Models (GLMs) and Support Vector Machines (SVMs) for example, may have default implementations that require the entire training set to be loaded in memory and often do not leverage any manner of thread or process parallelism. Some of these implementations also rely on memory-intensive solvers, which may require several times the size of your training set's worth of memory to work properly.

This page covers options to scale out traditional machine learning methods to very large datasets. Whether your training workload is too massive to fit even in a large memory node, or just big enough to take a really long time to process serially, the sections that follow may provide some insights to help you train models on Big Data.

# Scikit-learn

[Scikit-learn](https://scikit-learn.org/stable/index.html) is a Python module for machine learning that is built on top of SciPy and distributed under the 3-Clause BSD license. This popular package features an intuitive API that makes building fairly complex machine learning pipelines very straightforward. However, many of its implementations of common methods such as GLMs and SVMs assume that the entire training set can be loaded in memory, which might be a showstopper when dealing with massive datasets. Furthermore, some of these algorithms opt for memory-intensive solvers by default. In some cases, you can avoid these limitations using the ideas that follow.

## Stochastic gradient solvers

If your training set is small enough that it can be loaded entirely in memory, but you are experiencing Out-Of-Memory (OOM) errors during training, the culprit is likely a memory-intensive solver. Many common machine learning methods in `scikit-learn` have variations of [stochastic gradient descent (SGD)](https://en.wikipedia.org/wiki/Stochastic_gradient_descent) available as an option and replacing the default solver by an SGD-based one is often a straightforward solution to OOM errors.

The following example compares a [Ridge Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html) performed using the default solver with an SGD-based one. You can monitor memory usage by running the command `htop` on the terminal while the Python code runs.

**File :** ridge-default.py

```
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge

X,y = make_regression(n_samples=100000, n_features=10000, n_informative=50)

model = Ridge()

model.fit(X,y)

```

**File :** ridge-saga.py

```
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge

X,y = make_regression(n_samples=100000, n_features=10000, n_informative=50)

model = Ridge(solver='saga')

model.fit(X,y)

```

Another option that reduces memory usage even more, is to use [SGDRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html) instead of Ridge. This class implements many types of generalized linear models for regression, using a vanilla stochastic gradient descent as a solver. One caveat of using SGDRegressor is that it only works if the output is unidimensional (a scalar).

**File :** ridge-sgd\_regressor.py

```
from sklearn.datasets import make_regression
from sklearn.linear_model import SGDRegressor

X,y = make_regression(n_samples=100000, n_features=10000, n_informative=50)

model = SGDRegressor(penalty='l2') # set penalty='l2' to perform a ridge regression

model.fit(X,y)

```

## Batch learning

In cases where your dataset is too large to fit in memory --or just large enough that it does not leave enough memory free for training-- it is possible to leave your data on disk and load it in batches during training, similar to how deep learning packages work. Scikit-learn refers to this as [*out-of-core learning*](https://scikit-learn.org/stable/computing/scaling_strategies.html) and it is a viable option whenever an estimator has the `partial_fit` [method available](https://scikit-learn.org/stable/computing/scaling_strategies.html?highlight=partial_fit#incremental-learning). In the examples below, we perform out-of-core learning by iterating over datasets stored on disk.

In this first example, we use [SGDClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html) to fit a linear SVM classifier with batches of data coming from a pair of **numpy** arrays. These arrays are stored on disk as [npy files](https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html#npy-format) and we will keep them there by [memory-mapping](https://numpy.org/doc/stable/reference/generated/numpy.memmap.html) these files. Since `SGDClassifier` has the `partial_fit` method, we can iterate through our large memory-mapped files loading only a small batch of rows from the arrays in memory at a time. Each call to `partial_fit` will then run one epoch of stochastic gradient descent over a batch of data.

**File :** svm-sgd-npy.py

```
import numpy as np
from sklearn.linear_model import SGDClassifier

def batch_loader(X, y, batch_size):
    return ((X[idx:idx + batch_size],y[idx:idx + batch_size]) for idx in range(0, len(X), batch_size)) # function returns a Generator

inputs = np.memmap('./x_array.npy',dtype='float64',shape=(100000,10000))
targets = np.memmap('./y_array.npy',dtype='int8',shape=(100000,))

model = SGDClassifier(loss='hinge') # Using loss='hinge' is equivalent to fitting a Linear SVM

for batch in batch_loader(inputs, targets, batch_size=512):
    X,y = batch
    model.partial_fit(X,y)

```

Another common method of storing data for Machine Learning is using CSV files. In this example, we train a LASSO regression model reading data in batches from a CSV file using the [pandas](https://pandas.pydata.org) package.

**File :** lasso-sgd-csv.py

```
import pandas as pd
from sklearn.linear_model import SGDRegressor

model = SGDRegressor(penalty='l1')

for batch in pd.read_csv("./data.csv", chunksize=512, iterator=True):
    X = batch.drop('target', axis=1)
    y = batch['target']
    model.partial_fit(X,y)

```

# Snap ML

[Snap ML](https://snapml.readthedocs.io/en/latest/) is a closed-source machine learning library developed by IBM that currently supports a number of classical machine learning models and scales gracefully to datasets with billions of examples and/or features. It offers distributed training, GPU acceleration and supports sparse data structures. It features an API very similar to scikit-learn and can be used as a replacement for that library when dealing with massive datasets.

## Installation

### Latest available wheels

To see the latest version of Snap ML that we have built:

```
[name@server ~]$ avail_wheels "snapml"

```

For more information, see [Available wheels](Python.md#Available_wheels).

### Installing the wheel

The preferred option is to install it using the Python [wheel](https://pythonwheels.com/) as follows:

:   1. Load a Python [module](Utiliser_des_modules.md#Sub-command_load), thus `module load python`
:   2. Create and start a [virtual environment](Python.md#Creating_and_using_a_virtual_environment).
:   3. Install SnapML in the virtual environment with `pip install`.

```
(venv) [name@server ~] pip install --no-index snapml

```

## Multithreading

All estimators in Snap ML support thread parallelism, which can be controlled via the `n_jobs` parameter. Setting this parameter to the number of cores available in your job will typically deliver a good speedup relative to the scikit-learn implementation of the same estimator. The following is a performance comparison of `Ridge` between scikit-learn and Snap ML.

**File :** ridge-snap-vs-sklearn.py

```
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from snapml import LinearRegression
import time

X,y = make_regression(n_samples=100000, n_features=10000, n_informative=50)

model_sk = Ridge(solver='saga')

print("Running Ridge with sklearn...")
tik = time.perf_counter()
model_sk.fit(X,y)
tok = time.perf_counter()

print(f"sklearn took {tok-tik:0.2f} seconds to fit.")

model_snap = LinearRegression(penalty='l2',n_jobs=4)

print("Running Ridge with SnapML...")
tik = time.perf_counter()
model_snap.fit(X,y)
tok = time.perf_counter()

print(f"SnapML took {tok-tik:0.2f} seconds to fit.")

```

## Training on GPU

All estimators in `Snap ML` support GPU acceleration, with one or multiple GPUs. For single GPU training, simply set the parameter `use_gpu=True`. For multiple GPU training, in addition to setting `use_gpu`, pass a list containing the GPU IDs available to your job to `device_ids`. For example, inside a job that requested 2 GPUs, set `device_ids=[0,1]` to use both GPUs for training. The following example extends the performance comparison from the previous section to include training on GPU with Snap ML, this time training an SVM classifier with a non-linear kernel.

**File :** ridge-snap-vs-sklearn2.py

```
from sklearn.datasets import make_classification
from sklearn.svm import SVC 
from snapml import SupportVectorMachine
import time

X,y = make_classification(n_samples=100000, n_features=10000, n_classes=3, n_informative=50)

model_sk = SVC(kernel='rbf') #sklearn's SVM fit-time scales at least quadratically with the number of samples... this will take a loooong time.

print("Running SVM Classifier with sklearn...")
tik = time.perf_counter()
model_sk.fit(X,y)
tok = time.perf_counter()

print(f"sklearn took {tok-tik:0.2f} seconds to fit.")

model_snap = SupportVectorMachine(kernel='rbf',n_jobs=4)

print("Running SVM Classifier with SnapML without GPU...")
tik = time.perf_counter()
model_snap.fit(X,y)
tok = time.perf_counter()

print(f"SnapML took {tok-tik:0.2f} seconds to fit without GPU.")

model_snap_gpu = SupportVectorMachine(kernel='rbf',n_jobs=4, use_gpu=True)

print("Running SVM Classifier with SnapML with GPU...")
tik = time.perf_counter()
model_snap_gpu.fit(X,y)
tok = time.perf_counter()

print(f"SnapML took {tok-tik:0.2f} seconds to fit with GPU.")

```

## Out-of-memory training

All estimators in Snap ML use first-order iterative solvers, similar to SGD, by default. It is thus possible to perform training in batches and avoid loading entire datasets in memory. Unlike scikit-learn however, Snap ML accepts memory-mapped numpy arrays as inputs directly.

**File :** snap-npy.py

```
import numpy as np
from snapml import LogisticRegression

X = np.memmap('./x_array.npy',dtype='float64',shape=(100000,10000))
y = np.memmap('./y_array.npy',dtype='int8',shape=(100000,))

model = LogisticRegression(n_jobs=4)

model.fit(X,y)

```

## MPI

Snap ML features distributed implementations of many estimators. To run in distributed mode, call your Python script using `mpirun` or `srun`.

# Spark ML

[Spark ML](https://spark.apache.org/docs/latest/ml-guide.html) is a machine learning library built on top of [Apache Spark](Spark.md). It enables users to scale out many machine learning methods to massive amounts of data, over multiple nodes, without worrying about distributing datasets or explicitly writing distributed/parallel code. The library also includes many useful tools for distributed linear algebra and statistics. Please see our tutorial on [submitting Spark jobs](Spark.md#Usage) before trying out the examples on the official [Spark ML documentation](https://spark.apache.org/docs/latest/ml-guide.html).