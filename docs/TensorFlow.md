# TensorFlow

Other languages:

- English
- [français](TensorFlow_fr.md)

[TensorFlow](https://www.tensorflow.org/) is *an open-source software library for Machine Intelligence*.

If you are porting a TensorFlow program to an Alliance cluster, you should follow [our tutorial on machine learning](Tutoriel_Apprentissage_machine.md).

## Installing TensorFlow

These instructions install TensorFlow in your /home directory using Alliance's prebuilt [Python wheels](http://pythonwheels.com/). Custom Python wheels are stored in `/cvmfs/soft.computecanada.ca/custom/python/wheelhouse/`. To install a TensorFlow wheel, we will use the `pip` command and install it into a [Python virtual environment](Python.md#Creating_and_using_a_virtual_environment).

TF 2.xTF 1.x

Load modules required by TensorFlow. In some cases, other modules may be required (e.g. CUDA).

```
[name@server ~]$ module load python/3

```

Create a new Python virtual environment.

```
[name@server ~]$ virtualenv --no-download tensorflow

```

Activate your newly created Python virtual environment.

```
[name@server ~]$ source tensorflow/bin/activate

```

Install TensorFlow in your newly created virtual environment using the following command.

```
(tensorflow) [name@server ~]$ pip install --no-index tensorflow

```

Load modules required by TensorFlow. TF 1.x requires StdEnv/2018.

**Note: TF 1.x is not available on Narval, since StdEnv/2018 is not available on this cluster.**

```
[name@server ~]$ module load StdEnv/2018 python/3

```

Create a new Python virtual environment.

```
[name@server ~]$ virtualenv --no-download tensorflow

```

Activate your newly created Python virtual environment.

```
[name@server ~]$ source tensorflow/bin/activate

```

Install TensorFlow in your newly created virtual environment using one of the commands below, depending on whether you need to use a GPU.

**Do not** install the `tensorflow` package (without the `_cpu` or `_gpu` suffixes) as it has compatibility issues with other libraries.

### CPU-only

```
(tensorflow) [name@server ~]$ pip install --no-index tensorflow_cpu==1.15.0

```

### GPU

```
(tensorflow) [name@server ~]$ pip install --no-index tensorflow_gpu==1.15.0

```

### R package

To use TensorFlow in R, you will need to first follow the preceding instructions on creating a virtual environment and installing TensorFlow in it. Once this is done, follow these instructions.

Load the required modules.

```
[name@server ~]$ module load gcc r

```

Activate your Python virtual environment.

```
[name@server ~]$ source tensorflow/bin/activate

```

Launch R.

```
(tensorflow)_[name@server ~]$ R

```

In R, install package devtools, then tensorflow:

```
install.packages('devtools', repos='https://cloud.r-project.org')
devtools::install_github('rstudio/tensorflow')

```

You are then good to go. Do not call `install_tensorflow()` in R, as TensorFlow has already been installed in your virtual environment with `pi`p. To use the TensorFlow installed in your virtual environment, enter the following commands in R after the environment has been activated.

```
library(tensorflow)
use_virtualenv(Sys.getenv('VIRTUAL_ENV'))

```

## Submitting a TensorFlow job with a GPU

Once you have the above setup completed, you can submit a TensorFlow job.

```
[name@server ~]$ sbatch tensorflow-test.sh

```

The job submission script contains

**File :** tensorflow-test.sh

```
#!/bin/bash
#SBATCH --gres=gpu:1        # request GPU "generic resource"
#SBATCH --cpus-per-task=6   # maximum CPU cores per GPU request. See https://docs.alliancecan.ca/wiki/Allocations_and_compute_scheduling#Ratios_in_bundles
#SBATCH --mem=32000M        # memory per node
#SBATCH --time=0-03:00      # time (DD-HH:MM)
#SBATCH --output=%N-%j.out  # %N for node name, %j for jobID

module load cuda cudnn 
source tensorflow/bin/activate
python ./tensorflow-test.py

```

while the Python script has the form

TF 2.xTF 1.x

**File :** tensorflow-test.py

```
import tensorflow as tf
node1 = tf.constant(3.0)
node2 = tf.constant(4.0)
print(node1, node2)
print(node1 + node2)

```

**File :** tensorflow-test.py

```
import tensorflow as tf
node1 = tf.constant(3.0)
node2 = tf.constant(4.0)
print(node1, node2)
sess = tf.Session()
print(sess.run(node1 + node2))

```

Once the job has completed (should take less than a minute), you should see an output file called something like `node_id-job_id.out` with contents similar to the following (the logged messages from TensorFlow are only examples, expect different messages and more messages):

TF 2.xTF 1.x

**File :** node\_id-job\_id.out

```
2017-07-10 12:35:19.491097: I tensorflow/core/common_runtime/gpu/gpu_device.cc:961] DMA: 0
2017-07-10 12:35:19.491156: I tensorflow/core/common_runtime/gpu/gpu_device.cc:971] 0:   Y
2017-07-10 12:35:19.520737: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:0) -> (device: 0, name: Tesla P100-PCIE-12GB, pci bus id: 0000:82:00.0)
tf.Tensor(3.0, shape=(), dtype=float32) tf.Tensor(4.0, shape=(), dtype=float32)
tf.Tensor(7.0, shape=(), dtype=float32)

```

**File :** node\_id-job\_id.out

```
2017-07-10 12:35:19.491097: I tensorflow/core/common_runtime/gpu/gpu_device.cc:961] DMA: 0
2017-07-10 12:35:19.491156: I tensorflow/core/common_runtime/gpu/gpu_device.cc:971] 0:   Y
2017-07-10 12:35:19.520737: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Creating TensorFlow device (/gpu:0) -> (device: 0, name: Tesla P100-PCIE-12GB, pci bus id: 0000:82:00.0)
Tensor("Const:0", shape=(), dtype=float32) Tensor("Const_1:0", shape=(), dtype=float32)
7.0

```

TensorFlow can run on all GPU node types. See [Using GPUs with SLURM](Using_GPUs_with_SLURM.md) for more information.

## Monitoring

It is possible to connect to the node running a job and execute processes. This can be used to monitor resources used by TensorFlow and to visualize the progress of the training. See [Attaching to a running job](Running_jobs.md#Attaching_to_a_running_job) for examples.

### TensorBoard

TensorFlow comes with a suite of visualization tools called [TensorBoard](https://www.tensorflow.org/programmers_guide/summaries_and_tensorboard). TensorBoard operates by reading TensorFlow events and model files. To know how to create these files, read [TensorBoard tutorial on summaries](https://www.tensorflow.org/programmers_guide/summaries_and_tensorboard#serializing_the_data).

TensorBoard requires too much processing power to be run on a login node. Users are strongly encouraged to execute it in the same job as the Tensorflow process. To do so, launch TensorBoard in the background by calling it before your python script, and appending an ampersand (`&`) to the call:

```
# Your SBATCH arguments here

tensorboard --logdir=/tmp/your_log_dir --host 0.0.0.0 --load_fast false &
python train.py  # example

```

Once the job is running, to access TensorBoard with a web browser, you need to create a connection between your computer and the compute node running TensorFlow and TensorBoard. To do this you first need the hostname of the compute node running the Tensorboard server. Show the list of your jobs using the command `sq`; find the job, and note the value in the "NODELIST" column (this is the hostname).

To create the connection, use the following command on your local computer:

```
[name@my_computer ~]$ ssh -N -f -L localhost:6006:computenode:6006 userid@cluster.computecanada.ca

```

Replace `computenode` with the node hostname you retrieved from the preceding step, `userid` by your Alliance username, `cluster` by the cluster hostname (i.e.: `rorqual`, `fir`, `nibi`, etc.). If port 6006 was already in use, tensorboard will be using another one (e.g. 6007, 6008...).

Once the connection is created, go to [http://localhost:6006](http://localhost:6006).

## TensorFlow with multi-GPUs

TensorFlow offers a number of different strategies to make use of multiple GPUs through the high-level API `tf.distribute`. In the following sections, we provide code examples of each strategy using Keras for simplicity. For more details, please refer to the official [TensorFlow documentation](https://www.tensorflow.org/api_docs/python/tf/distribute).

#### Mirrored strategy

##### Single node

**File :** tensorflow-singleworker.sh

```
#!/bin/bash
#SBATCH --nodes 1
#SBATCH --gres=gpu:4

#SBATCH --mem=8G      
#SBATCH --time=0-00:30
#SBATCH --output=%N-%j.out

module load python/3
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index tensorflow

export NCCL_BLOCKING_WAIT=1  #Set this environment variable if you wish to use the NCCL backend for inter-GPU communication.

python tensorflow-singleworker.py

```

The Python script `tensorflow-singleworker.py` has the form:

**File :** tensorflow-singleworker.py

```
import tensorflow as tf
import numpy as np

import argparse


parser = argparse.ArgumentParser(description='cifar10 classification models, tensorflow MirroredStrategy test')
parser.add_argument('--lr', default=0.001, help='')
parser.add_argument('--batch_size', type=int, default=256, help='')

args = parser.parse_args()

strategy = tf.distribute.MirroredStrategy()

with strategy.scope():

    model = tf.keras.Sequential()

    model.add(tf.keras.layers.Conv2D(32, (3, 3), padding='same',
                 input_shape=(32,32,3)))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Conv2D(32, (3, 3)))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Dropout(0.25))

    model.add(tf.keras.layers.Conv2D(64, (3, 3), padding='same'))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Conv2D(64, (3, 3)))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Dropout(0.25))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(512))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(10))

    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
         optimizer=tf.keras.optimizers.SGD(learning_rate=args.lr),metrics=['accuracy'])

### This next line will attempt to download the CIFAR10 dataset from the internet if you don't already have it stored in ~/.keras/datasets. 
### Run this line on a login node prior to submitting your job, or manually download the data from 
### https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz, rename to "cifar-10-batches-py.tar.gz" and place it under ~/.keras/datasets

(x_train, y_train),_ = tf.keras.datasets.cifar10.load_data()

dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(args.batch_size)

model.fit(dataset, epochs=2)

```

##### Multiple nodes

The syntax to use multiple GPUs distributed across multiple nodes is very similar to the single node case, the most notable difference being the use of `MultiWorkerMirroredStrategy()`. Here, we use `SlurmClusterResolver()` to tell TensorFlow to acquire all the necessary job information from SLURM, instead of manually assigning master and worker nodes, for example. We also need to add `CommunicationImplementation.NCCL` to the distribution strategy to specify that we want to use Nvidia's NCCL backend for inter-GPU communications. This was not necessary in the single-node case, as NCCL is the default backend with `MirroredStrategy()`.

**File :** tensorflow-multiworker.sh

```
#!/bin/bash
#SBATCH --nodes 2              # Request 2 nodes so all resources are in two nodes.
#SBATCH --gres=gpu:2          # Request 2 GPU "generic resources”. You will get 2 per node.

#SBATCH --ntasks-per-node=2   # Request 1 process per GPU. You will get 1 CPU per process by default. Request more CPUs with the "cpus-per-task" parameter if your input pipeline can handle parallel data-loading/data-transforms

#SBATCH --mem=8G      
#SBATCH --time=0-00:30
#SBATCH --output=%N-%j.out


srun -N $SLURM_NNODES -n $SLURM_NNODES config_env.sh

module load gcc/9.3.0 cuda/11.8
export NCCL_BLOCKING_WAIT=1  #Set this environment variable if you wish to use the NCCL backend for inter-GPU communication.
export XLA_FLAGS=--xla_gpu_cuda_data_dir=$CUDA_HOME

srun launch_training.sh

```

Where `config_env.sh` has the form:

**File :** config\_env.sh

```
#!/bin/bash

module load python

virtualenv --no-download $SLURM_TMPDIR/ENV

source $SLURM_TMPDIR/ENV/bin/activate

pip install --upgrade pip --no-index

pip install --no-index tensorflow

echo "Done installing virtualenv!"

```

The script `launch_training.sh` has the form:

**File :** launch\_training.sh

```
#!/bin/bash

source $SLURM_TMPDIR/ENV/bin/activate

python tensorflow-multiworker.py

```

And the Python script `tensorflow-multiworker.py` has the form:

**File :** tensorflow-multiworker.py

```
import tensorflow as tf
import numpy as np

import argparse


parser = argparse.ArgumentParser(description='cifar10 classification models, tensorflow MultiWorkerMirrored test')
parser.add_argument('--lr', default=0.001, help='')
parser.add_argument('--batch_size', type=int, default=256, help='')

args = parser.parse_args()

cluster_config = tf.distribute.cluster_resolver.SlurmClusterResolver()
comm_options = tf.distribute.experimental.CommunicationOptions(implementation=tf.distribute.experimental.CommunicationImplementation.NCCL)

strategy = tf.distribute.MultiWorkerMirroredStrategy(cluster_resolver=cluster_config, communication_options=comm_options)

with strategy.scope():

    model = tf.keras.Sequential()

    model.add(tf.keras.layers.Conv2D(32, (3, 3), padding='same',
                 input_shape=(32,32,3)))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Conv2D(32, (3, 3)))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Dropout(0.25))

    model.add(tf.keras.layers.Conv2D(64, (3, 3), padding='same'))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Conv2D(64, (3, 3)))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Dropout(0.25))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(512))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(10))

    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
         optimizer=tf.keras.optimizers.SGD(learning_rate=args.lr),metrics=['accuracy'])

### This next line will attempt to download the CIFAR10 dataset from the internet if you don't already have it stored in ~/.keras/datasets. 
### Run this line on a login node prior to submitting your job, or manually download the data from 
### https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz, rename to "cifar-10-batches-py.tar.gz" and place it under ~/.keras/datasets

(x_train, y_train),_ = tf.keras.datasets.cifar10.load_data()

dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(args.batch_size)

model.fit(dataset, epochs=2)

```

## Creating model checkpoints

Whether or not you expect your code to run for long time periods, it is a good habit to create Checkpoints during training. A checkpoint is a snapshot of your model at a given point during the training process (after a certain number of iterations or after a number of epochs) that is saved to disk and can be loaded at a later time. It is a handy way of breaking jobs that are expected to run for a very long time, into multiple shorter jobs that may get allocated on the cluster more quickly. It is also a good way of avoiding losing progress in case of unexpected errors in your code or node failures.

### With Keras

To create a checkpoint when training with `keras`, we recommend using the `callbacks` parameter of the `model.fit()` method. The following example shows how to instruct TensorFlow to create a checkpoint at the end of every training epoch:

```
callbacks = [tf.keras.callbacks.ModelCheckpoint(filepath="./ckpt",save_freq="epoch")] # Make sure the path where you want to create the checkpoint exists

model.fit(dataset, epochs=10 , callbacks=callbacks)

```

For more information, please refer to the [official TensorFlow documentation](https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/ModelCheckpoint).

### With a custom training loop

Please refer to the [official TensorFlow documentation](https://www.tensorflow.org/guide/checkpoint#writing_checkpoints).

## Troubleshooting

### scikit image

If you are using the scikit-image library, you may get the following error:
`OMP: Error #15: Initializing libiomp5.so, but found libiomp5.so already initialized.`

This is because the tensorflow library tries to load a bundled version of OMP which conflicts with the system version. The workaround is as follows:

```
(tf_skimage_venv) name@server $ cd tf_skimage_venv
(tf_skimage_venv) name@server $ export LIBIOMP_PATH=$(strace python -c 'from skimage.transform import AffineTransform' 2>&1 | grep -v ENOENT | grep -ohP -e '(?<=")[^"]+libiomp5.so(?=")' | xargs realpath)
(tf_skimage_venv) name@server $ find -path '*_solib_local*' -name libiomp5.so -exec ln -sf $LIBIOMP_PATH {} \;

```

This will patch the tensorflow library installation to use the systemwide libiomp5.so.

### libcupti.so

Some tracing features of Tensorflow require libcupti.so to be available, and might give the following error if they are not:

`I tensorflow/stream_executor/dso_loader.cc:142] Couldn't open CUDA library libcupti.so.9.0. LD_LIBRARY_PATH: /usr/local/cuda-9.0/lib64`

The solution is to run the following before executing your script:

```
[name@server ~]$ module load cuda/9.0.xxx
[name@server ~]$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDA_HOME/extras/CUPTI/lib64/

```

Where xxx is the appropriate CUDA version, which can be found using `module av cuda`

### libiomp5.so invalid ELF header

Sometimes the `libiomp5.so` shared object file will be erroneously installed as a text file. This might result in errors like the following:

`/home/username/venv/lib/python3.6/site-packages/tensorflow/python/../../_solib_local/_U@mkl_Ulinux_S_S_Cmkl_Ulibs_Ulinux___Uexternal_Smkl_Ulinux_Slib/libiomp5.so: invalid ELF header`

The workaround for such errors is to access the directory mentioned in the error (i.e. `[...]/_U@mkl_Ulinux_S_S_Cmkl_Ulibs_Ulinux___Uexternal_Smkl_Ulinux_Slib`) and execute the following command:

```
[name@server ...Ulinux_Slib] $ ln -sf $(cat libiomp5.so) libiomp5.so

```

This will replace the text file with the correct symbolic link.

## Controlling the number of CPUs and threads

The config parameters `intra_op_parallelism_threads` and `inter_op_parallelism_threads` influence the number of threads used by TensorFlow. You can set those parameters with:

```
tf.config.threading.set_inter_op_parallelism_threads(num_threads)
tf.config.threading.set_intra_op_parallelism_threads(num_threads)

```

## Known issues

A bug sneaked into the Keras implementation of Tensorflow after version 2.8.3. It affects the performance of the layers used for data augmentation with prefix *tf.keras.layers.Random* (like *tf.keras.layers.RandomRotation*, *tf.keras.layers.RandomTranslation*, etc). It significantly slows down the training process by more than 100 times. The bug is fixed in version 2.12.