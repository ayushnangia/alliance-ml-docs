# MXNet

Other languages:

- English
- [français](MXNet_fr.md)

[Apache MXNet](https://mxnet.incubator.apache.org/) is a deep learning framework designed for both efficiency and flexibility. It allows you to mix symbolic and imperative programming to maximize efficiency and productivity. At its core, MXNet contains a dynamic dependency scheduler that automatically parallelizes both symbolic and imperative operations on the fly. A graph optimization layer on top of that makes symbolic execution fast and memory efficient. MXNet is portable and lightweight, scalable to many GPUs and machines.

# Available wheels

You can list available wheels using the avail\_wheels command.

```
[name@server ~]$ avail_wheels mxnet
name    version    python    arch
------  ---------  --------  ------
mxnet   1.9.1      cp39      avx2
mxnet   1.9.1      cp38      avx2
mxnet   1.9.1      cp310     avx2

```

# Installing in a Python virtual environment

1. Create and activate a Python virtual environment.

```
[name@server ~]$ module load python/3.10
[name@server ~]$ virtualenv --no-download ~/env
[name@server ~]$ source ~/env/bin/activate

```

2. Install MXNet and its Python dependencies.

```
(env) [name@server ~] pip install --no-index mxnet

```

3. Validate it.

```
(env) [name@server ~] python -c "import mxnet as mx;print((mx.nd.ones((2, 3))*2).asnumpy());"
[[2. 2. 2.]
 [2. 2. 2.]]

```

# Running a job

A single Convolution layer:

**File :** mxnet-conv-ex.py

```
#!/bin/env python

import mxnet as mx
import numpy as np

num_filter = 32
kernel = (3, 3)
pad = (1, 1)
shape = (32, 32, 256, 256)

x = mx.sym.Variable('x')
w = mx.sym.Variable('w')
y = mx.sym.Convolution(data=x, weight=w, num_filter=num_filter, kernel=kernel, no_bias=True, pad=pad)

device = mx.gpu() if mx.context.num_gpus() > 0 else mx.cpu()

# On CPU will use MKLDNN, or will use cuDNN
exe = y.simple_bind(device, x=shape)

exe.arg_arrays[0][:] = np.random.normal(size=exe.arg_arrays[0].shape)
exe.arg_arrays[1][:] = np.random.normal(size=exe.arg_arrays[1].shape)

exe.forward(is_train=False)
o = exe.outputs[0]
t = o.asnumpy()
print(t)

```

2. Edit the following submission script according to your needs.

CPUGPU

**File :** mxnet-conv.sh

```
#!/bin/bash

#SBATCH --job-name=mxnet-conv
#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=01:00:00           # adjust this to match the walltime of your job
#SBATCH --cpus-per-task=2         # adjust this to match the number of cores
#SBATCH --mem=20G                 # adjust this according to the memory you need

# Load modules dependencies
module load python/3.10

# Generate your virtual environment in $SLURM_TMPDIR
virtualenv --no-download ${SLURM_TMPDIR}/env
source ${SLURM_TMPDIR}/env/bin/activate

# Install MXNet and its dependencies
pip install --no-index mxnet==1.9.1

# Will use MKLDNN
python mxnet-conv-ex.py

```

**File :** mxnet-conv.sh

```
#!/bin/bash

#SBATCH --job-name=mxnet-conv
#SBATCH --account=def-someprof    # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=01:00:00           # adjust this to match the walltime of your job
#SBATCH --cpus-per-task=2         # adjust this to match the number of cores
#SBATCH --mem=20G                 # adjust this according to the memory you need
#SBATCH --gres=gpu:1              # adjust this to match the number of GPUs, unless distributed training, use 1

# Load modules dependencies
module load python/3.10

# Generate your virtual environment in $SLURM_TMPDIR
virtualenv --no-download ${SLURM_TMPDIR}/env
source ${SLURM_TMPDIR}/env/bin/activate

# Install MXNet and its dependencies
pip install --no-index mxnet==1.9.1

# Will use cuDNN
python mxnet-conv-ex.py

```

3. Submit the job to the scheduler.

```
[name@server ~]$ sbatch mxnet-conv.sh

```

# High Performance with MXNet

## MXNet with Multiple CPUs or a Single GPU

Similar to PyTorch and TensorFlow, MXNet contains both CPU and GPU-based parallel implementations of operators commonly used in Deep Learning, such as matrix multiplication and convolution, using OpenMP and MKLDNN (CPU) or CUDA and CUDNN (GPU). Whenever you run MXNet code that performs such operations, they will either automatically leverage multi-threading over as many CPU cores as are available to your job, or run on the GPU if your job requests one.

With the above being said, when training small scale models we strongly recommend using **multiple CPUs instead of using a GPU**. While training will almost certainly run faster on a GPU (except in cases where the model is very small), if your model and your dataset are not large enough, the speed up relative to CPU will likely not be very significant and your job will end up using only a small portion of the GPU's compute capabilities. This might not be an issue on your own workstation, but in a shared environment like our HPC clusters this means you are unnecessarily blocking a resource that another user may need to run actual large scale computations! Furthermore, you would be unnecessarily using up your group's allocation and affecting the priority of your colleagues' jobs.

Simply put, **you should not ask for a GPU** if your code is not capable of making a reasonable use of its compute capacity. The following example illustrates how to train a Convolutional Neural Network using MXNet with or without a GPU:

**File :** mxnet-example.sh

```
#!/bin/bash
#SBATCH --nodes 1
#SBATCH --tasks-per-node=1 
#SBATCH --cpus-per-task=1 # change this parameter to 2,4,6,... to see the effect on performance
#SBATCH --gres=gpu:1 # Remove this line to run using CPU only 

#SBATCH --mem=8G      
#SBATCH --time=0:05:00
#SBATCH --output=%N-%j.out
#SBATCH --account=<your account>

module load python # Using Default Python version - Make sure to choose a version that suits your application

virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install mxnet --no-index

echo "starting training..."

python mxnet-example.py

```

**File :** mxnet-example.py

```
import numpy as np
import time

from mxnet import context
from mxnet import autograd, gpu, cpu
from mxnet.gluon import nn, Trainer
from mxnet.gluon.loss import SoftmaxCrossEntropyLoss
from mxnet.gluon.data.vision import transforms
from mxnet.gluon.data.vision.datasets import CIFAR10
from mxnet.gluon.data import DataLoader

import argparse

parser = argparse.ArgumentParser(description='cifar10 classification models, cpu performance test')
parser.add_argument('--lr', default=0.1, help='')
parser.add_argument('--batch_size', type=int, default=512, help='')
parser.add_argument('--num_workers', type=int, default=0, help='')

def main():

    args = parser.parse_args()

    ctx = gpu() if context.num_gpus() > 0 else cpu()

    net = nn.Sequential()

    net.add(nn.Conv2D(channels=6, kernel_size=5, activation='relu'),
        nn.MaxPool2D(pool_size=2, strides=2),
        nn.Conv2D(channels=16, kernel_size=5, activation='relu'),
        nn.MaxPool2D(pool_size=2, strides=2),
        nn.Flatten(),
        nn.Dense(120, activation="relu"),
        nn.Dense(84, activation="relu"),
        nn.Dense(10))

    net.initialize(ctx=ctx)

    criterion = SoftmaxCrossEntropyLoss()
    trainer = Trainer(net.collect_params(),'sgd', {'learning_rate': args.lr})

    transform_train = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    dataset_train = CIFAR10(root='./data', train=True).transform_first(transform_train)
    train_loader = DataLoader(dataset_train, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers)

    perf = []

    for inputs, targets in train_loader:

       inputs = inputs.as_in_context(ctx)
       targets = targets.as_in_context(ctx)

       start = time.time()

       with autograd.record():

          outputs = net(inputs)
          loss = criterion(outputs, targets)

       loss.backward()
       trainer.step(batch_size=args.batch_size)

       batch_time = time.time() - start
       images_per_sec = args.batch_size/batch_time
       perf.append(images_per_sec)

       print(f"Current Loss: {loss.mean().asscalar()}")

    print(f"Images processed per second: {np.mean(perf)}")

if __name__=='__main__':
   main()

```