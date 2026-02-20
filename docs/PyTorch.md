# PyTorch

Other languages:

- English
- [français](PyTorch_fr.md)

[PyTorch](http://pytorch.org/) is a Python package that provides two high-level features:

- Tensor computation (like NumPy) with strong GPU acceleration
- Deep neural networks built on a tape-based autograd system

If you are porting a PyTorch program to one of our clusters, you should follow [our tutorial on the subject](Tutoriel_Apprentissage_machine.md).

# Disambiguation

PyTorch has a distant connection with [Torch](Torch.md), but for all practical purposes you can treat them as separate projects.

PyTorch developers also offer LibTorch, which allows one to implement extensions to PyTorch using C++, and to implement pure C++ machine learning applications. Models written in Python using PyTorch can be converted and used in pure C++ through [TorchScript](https://pytorch.org/tutorials/advanced/cpp_export.html).

# Installation

## Latest available wheels

To see the latest version of PyTorch that we have built:

```
[name@server ~]$ avail_wheels torch

```

For more information, see [Available wheels](Python.md#Available_wheels).

## Installing our wheel

The preferred option is to install it using the Python [wheel](https://pythonwheels.com/) as follows:

:   1. Load a Python [module](Utiliser_des_modules.md#Sub-command_load), thus `module load python`
:   2. Create and start a [virtual environment](Python.md#Creating_and_using_a_virtual_environment).
:   3. Install PyTorch in the virtual environment with `pip install`.

#### GPU and CPU

```
(venv) [name@server ~] pip install --no-index torch

```

| With H100 GPUs, Torch 2.5.1 and higher is required. |
| --- |

#### Extra

In addition to `torch`, you can install `torchvision`, `torchtext` and `torchaudio`:

```
(venv) [name@server ~] pip install --no-index torch torchvision torchtext torchaudio

```

# Job submission

Here is an example of a job submission script using the python wheel, with a virtual environment inside a job:

**File :** pytorch-test.sh

```
#!/bin/bash
#SBATCH --gres=gpu:1       # Request GPU "generic resources"
#SBATCH --cpus-per-task=6  # Cores proportional to GPUs.
#SBATCH --mem=32000M       # Memory proportional to GPUs.
#SBATCH --time=0-03:00
#SBATCH --output=%N-%j.out

module load python/<select version> # Make sure to choose a version that suits your application
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install torch --no-index

python pytorch-test.py

```

See [Ratios in bundles](Allocations_and_compute_scheduling.md#Ratios_in_bundles) for more information on the appropriate number of CPUs and Memory per GPU for each cluster.

The Python script `pytorch-test.py` has the form

**File :** pytorch-test.py

```
import torch
x = torch.Tensor(5, 3)
print(x)
y = torch.rand(5, 3)
print(y)
# let us run the following only if CUDA is available
if torch.cuda.is_available():
    x = x.cuda()
    y = y.cuda()
    print(x + y)

```

You can then submit a PyTorch job with:

```
[name@server ~]$ sbatch pytorch-test.sh

```

# High performance with PyTorch

## TF32: Performance vs numerical accuracy

On version 1.7.0 PyTorch has introduced support for [Nvidia's TensorFloat-32 (TF32) Mode](https://blogs.nvidia.com/blog/2020/05/14/tensorfloat-32-precision-format/), which in turn is available only on Ampere and later Nvidia GPU architectures. This mode of executing tensor operations has been shown to yield up to 20x speed-ups compared to equivalent single precision (FP32) operations and is enabled by default in PyTorch versions 1.7.x up to 1.11.x. However, such gains in performance come at the cost of potentially decreased accuracy in the results of operations, which may become problematic in cases such as when dealing with ill-conditioned matrices, or when performing long sequences of tensor operations as is common in deep learning models. Following calls from its user community, TF32 is now **disabled by default for matrix multiplications**, but still **enabled by default for convolutions** starting with PyTorch version 1.12.0.

On clusters equipped with A100, H100, or newer Nvidia GPUs, users should be cognizant of the following:

1. You may notice a significant slowdown when running the exact same GPU-enabled code with `torch < 1.12.0` and `torch >= 1.12.0`.
2. You may get different results when running the exact same GPU-enabled code with `torch < 1.12.0` and `torch >= 1.12.0`.

To enable or disable TF32 on `torch >= 1.12.0` set the following flags to `True` or `False` accordingly:

```
torch.backends.cuda.matmul.allow_tf32 = False # Enable/disable TF32 for matrix multiplications
torch.backends.cudnn.allow_tf32 = False # Enable/disable TF32 for convolutions

```

For more information, see [PyTorch's official documentation](https://pytorch.org/docs/stable/notes/cuda.html#tf32-on-ampere)

## Running on CPU

PyTorch natively supports parallelizing work across multiple CPUs in two ways: intra-op parallelism and inter-op parallelism.

- **intra-op** refers to PyTorch's parallel implementations of operators commonly used in Deep Learning, such as matrix multiplication and convolution, using [OpenMP](https://www.openmp.org) directly or through low-level libraries like [MKL](https://en.wikipedia.org/wiki/Math_Kernel_Library) and [OneDNN](https://www.intel.com/content/www/us/en/develop/documentation/oneapi-programming-guide/top/api-based-programming/intel-oneapi-deep-neural-network-library-onednn.html). Whenever you run PyTorch code that performs such operations, they will automatically leverage multi-threading over as many CPU cores as are available to your job.
- **inter-op** parallelism on the other hand refers to PyTorch's ability to execute different parts of your code concurrently. This modality of parallelism typically requires that you explicitly design your program such that different parts can run in parallel. Examples include code that leverages PyTorch's Just-In-Time compiler `torch.jit` to run asynchronous tasks in a [TorchScript](https://pytorch.org/docs/stable/jit.html#built-in-functions-and-modules) program.

With small scale models, we strongly recommend using **multiple CPUs instead of using a GPU**. While training will almost certainly run faster on a GPU (except in cases where the model is very small), if your model and your dataset are not large enough, the speed up relative to CPU will likely not be very significant and your job will end up using only a small portion of the GPU's compute capabilities. This might not be an issue on your own workstation, but in a shared environment like our HPC clusters, this means you are unnecessarily blocking a resource that another user may need to run actual large scale computations! Furthermore, you would be unnecessarily using up your group's allocation and affecting the priority of your colleagues' jobs.

The code example below contains many opportunities for intra-op parallelism.

**File :** cifar10-cpu.py

```
import numpy as np
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader

import argparse
import os

parser = argparse.ArgumentParser(description='cifar10 classification models, cpu performance test')
parser.add_argument('--lr', default=0.1, help='')
parser.add_argument('--batch_size', type=int, default=512, help='')
parser.add_argument('--num_workers', type=int, default=0, help='')

def main():

    args = parser.parse_args()
    torch.set_num_threads(int(os.environ['SLURM_CPUS_PER_TASK']))
    class Net(nn.Module):

       def __init__(self):
          super(Net, self).__init__()

          self.conv1 = nn.Conv2d(3, 6, 5)
          self.pool = nn.MaxPool2d(2, 2)
          self.conv2 = nn.Conv2d(6, 16, 5)
          self.fc1 = nn.Linear(16 * 5 * 5, 120)
          self.fc2 = nn.Linear(120, 84)
          self.fc3 = nn.Linear(84, 10)

       def forward(self, x):
          x = self.pool(F.relu(self.conv1(x)))
          x = self.pool(F.relu(self.conv2(x)))
          x = x.view(-1, 16 * 5 * 5)
          x = F.relu(self.fc1(x))
          x = F.relu(self.fc2(x))
          x = self.fc3(x)
          return x

    net = Net()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=args.lr)

    transform_train = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    ### This next line will attempt to download the CIFAR10 dataset from the internet if you don't already have it stored in ./data 
    ### Run this line on a login node with "download=True" prior to submitting your job, or manually download the data from 
    ### https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz and place it under ./data

    dataset_train = CIFAR10(root='./data', train=True, download=False, transform=transform_train)

    train_loader = DataLoader(dataset_train, batch_size=args.batch_size, num_workers=args.num_workers)

    perf = []

    total_start = time.time()

    for batch_idx, (inputs, targets) in enumerate(train_loader):

       start = time.time()

       outputs = net(inputs)
       loss = criterion(outputs, targets)

       optimizer.zero_grad()
       loss.backward()
       optimizer.step()

       batch_time = time.time() - start

       images_per_sec = args.batch_size/batch_time

       perf.append(images_per_sec)

    total_time = time.time() - total_start

if __name__=='__main__':
   main()

```

To test the above code, you first need to download the data:

```
[name@server ~]$ mkdir -p data && cd data

```

```
[name@server data]$ wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
[name@server data]$ tar zxf cifar-10-python.tar.gz
[name@server data]$ cd ..

```

By simply requesting more CPUs and without any code changes, we can observe the effect of PyTorch's native support for parallelism on performance:

**File :** pytorch-multi-cpu.sh

```
#!/bin/bash
#SBATCH --nodes 1
#SBATCH --tasks-per-node=1 
#SBATCH --cpus-per-task=1 # change this parameter to 2,4,6,... to see the effect on performance

#SBATCH --mem=8G      
#SBATCH --time=0:05:00
#SBATCH --output=%N-%j.out
#SBATCH --account=<your account>

module load python # Using Default Python version - Make sure to choose a version that suits your application
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install torch torchvision --no-index

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

echo "starting training..."

time python cifar10-cpu.py

```

## Running on GPU

There is a common misconception that you should definitely use a GPU for model training if one is available. While this may *almost always* hold true (training very small models is often faster on one or more CPUs) on your own local workstation equipped with a GPU, it is not the case on our HPC clusters.

Simply put, **you should not ask for a GPU** if your code is not capable of making a reasonable use of its compute capacity.

GPUs draw their performance advantage in Deep Learning tasks mainly from two sources:

1. Their ability to parallelize the execution of certain key numerical operations, such as [multiply-accumulate](https://en.wikipedia.org/wiki/Multiply–accumulate_operation), over many thousands of compute cores compared to the single-digit count of cores available in most common CPUs.
2. A much higher memory bandwidth than CPUs, which allows GPUs to efficiently use their massive number of cores to process much larger amounts of data per compute cycle.

Like in the multi-cpu case, PyTorch contains parallel implementations of operators commonly used in Deep Learning, such as matrix multiplication and convolution, using GPU-specific libraries like [CUDNN](https://developer.nvidia.com/cudnn) or [MIOpen](https://github.com/ROCmSoftwarePlatform/MIOpen), depending on the hardware platform. This means that for a learning task to be worth running on a GPU, it must be composed of elements that scale out with massive parallelism in terms of the number of operations that can be performed in parallel, the amount of data they require, or, ideally, both. Concretely this means, for example, large models (with large numbers of units and layers), large inputs, or, ideally, both.

In the example below, we adapt the multi-cpu code from the previous section to run on one GPU and examine its performance. We can observe that two parameters play an important role: `batch_size` and `num_workers`. The first influences performance by increasing the size of our inputs at each iteration, thus putting more of the GPU's capacity to use. The second influences performance by streamlining the movement of our inputs from the Host's (or the CPU's) memory to the GPU's memory, thus reducing the amount of time the GPU sits idle waiting for data to process.

Two takeaways emerge from this:

1. Increase your `batch_size` to as much as you can fit in the GPU's memory to optimize your compute performance.
2. Use a `DataLoader` with as many workers as you have `cpus-per-task` to streamline feeding data to the GPU.

Of course, `batch_size` is also an important parameter with respect to a model's performance on a given task (accuracy, error, etc.) and different schools of thought have different views on the impact of using large batches. This page will not go into this subject, but if you have reason to believe that a small (relative to space in GPU memory) batch size is best for your application, skip to Single GPU Data Parallelism to see how to maximize GPU utilization with small inputs.

**File :** pytorch-single-gpu.sh

```
#!/bin/bash
#SBATCH --nodes 1
#SBATCH --gres=gpu:1 # request a GPU
#SBATCH --tasks-per-node=1 
#SBATCH --cpus-per-task=1 # change this parameter to 2,4,6,... and increase "--num_workers" accordingly to see the effect on performance
#SBATCH --mem=8G      
#SBATCH --time=0:05:00
#SBATCH --output=%N-%j.out
#SBATCH --account=<your account>

module load python # Using Default Python version - Make sure to choose a version that suits your application
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install torch torchvision --no-index

echo "starting training..."
time python cifar10-gpu.py --batch_size=512 --num_workers=0

```

**File :** cifar10-gpu.py

```
import numpy as np
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader

import argparse

parser = argparse.ArgumentParser(description='cifar10 classification models, single gpu performance test')
parser.add_argument('--lr', default=0.1, help='')
parser.add_argument('--batch_size', type=int, default=512, help='')
parser.add_argument('--num_workers', type=int, default=0, help='')


def main():

    args = parser.parse_args()

    class Net(nn.Module):

       def __init__(self):
          super(Net, self).__init__()

          self.conv1 = nn.Conv2d(3, 6, 5)
          self.pool = nn.MaxPool2d(2, 2)
          self.conv2 = nn.Conv2d(6, 16, 5)
          self.fc1 = nn.Linear(16 * 5 * 5, 120)
          self.fc2 = nn.Linear(120, 84)
          self.fc3 = nn.Linear(84, 10)

       def forward(self, x):
          x = self.pool(F.relu(self.conv1(x)))
          x = self.pool(F.relu(self.conv2(x)))
          x = x.view(-1, 16 * 5 * 5)
          x = F.relu(self.fc1(x))
          x = F.relu(self.fc2(x))
          x = self.fc3(x)
          return x

    net = torch.compile(Net())
    net = net.cuda() # Load model on the GPU

    criterion = nn.CrossEntropyLoss().cuda() # Load the loss function on the GPU
    optimizer = optim.SGD(net.parameters(), lr=args.lr)

    transform_train = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    dataset_train = CIFAR10(root='./data', train=True, download=False, transform=transform_train)

    train_loader = DataLoader(dataset_train, batch_size=args.batch_size, num_workers=args.num_workers, pin_memory=True)

    perf = []

    total_start = time.time()

    for batch_idx, (inputs, targets) in enumerate(train_loader):

       start = time.time()
       
       inputs = inputs.cuda() 
       targets = targets.cuda()

       outputs = net(inputs)
       loss = criterion(outputs, targets)

       optimizer.zero_grad()
       loss.backward()
       optimizer.step()

       batch_time = time.time() - start

       images_per_sec = args.batch_size/batch_time

       perf.append(images_per_sec)

    total_time = time.time() - total_start

if __name__=='__main__':
   main()

```

## Data Parallelism

Data Parallelism, in this context, refers to methods to perform training over multiple replicas of a model in parallel, where each replica receives a different chunk of training data at each iteration. Gradients are then aggregated at the end of an iteration and the parameters of all replicas are updated in a synchronous or asynchronous fashion, depending on the method.

Using this approach may provide a significant speed-up by iterating through all examples in a large dataset approximately N times faster, where N is the number of model replicas.

An important caveat of this approach, is that in order to get a trained model that is equivalent to the same model trained without Data Parallelism, the user must scale either the learning rate or the desired batch size in function of the number of replicas. See [this discussion](https://discuss.pytorch.org/t/should-we-split-batch-size-according-to-ngpu-per-node-when-distributeddataparallel/72769/13) for more information.

In the multiple-GPU case, each GPU hosts a replica of your model. Consequently, the model must be **small enough to fit inside the memory of a single GPU**.

There are several ways to perform Data Parallelism using PyTorch. This section features tutorials on three of them: using the **DistributedDataParallel** class directly with one or multiple GPUs, and using the **PyTorch Lightning** package.

### Multi-GPU Data Parallelism

The **DistributedDataParallel** class is the way [recommended by PyTorch maintainers](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html#comparison-between-dataparallel-and-distributeddataparallel) to use multiple GPUs, whether they are all on a single node, or distributed across multiple nodes.

**File :** pytorch-ddp-test.sh

```
#!/bin/bash
#SBATCH --nodes 1             
#SBATCH --gres=gpu:2          # Request 2 GPU "generic resources”.
#SBATCH --tasks-per-node=2   # Request 1 process per GPU. You will get 1 CPU per process by default. Request more CPUs with the "cpus-per-task" parameter to enable multiple data-loader workers to load data in parallel.
#SBATCH --mem=8G      
#SBATCH --time=0-03:00
#SBATCH --output=%N-%j.out

module load python # Using Default Python version - Make sure to choose a version that suits your application
srun -N $SLURM_NNODES -n $SLURM_NNODES bash << EOF
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install torch torchvision --no-index
EOF

export TORCH_NCCL_ASYNC_HANDLING=1
export MASTER_ADDR=$(hostname) #Store the master node’s IP address in the MASTER_ADDR environment variable.

echo "r$SLURM_NODEID master: $MASTER_ADDR"
echo "r$SLURM_NODEID Launching python script"

# The $((SLURM_NTASKS_PER_NODE * SLURM_JOB_NUM_NODES)) variable tells the script how many processes are available for this execution. “srun” executes the script <tasks-per-node * nodes> times

source $SLURM_TMPDIR/env/bin/activate

srun python pytorch-ddp-test.py --init_method tcp://$MASTER_ADDR:3456 --world_size $((SLURM_NTASKS_PER_NODE * SLURM_JOB_NUM_NODES))  --batch_size 256

```

The Python script `pytorch-ddp-test.py` has the form

**File :** pytorch-ddp-test.py

```
import os
import time
import datetime

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.backends.cudnn as cudnn

import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader

import torch.distributed as dist
import torch.utils.data.distributed

import argparse

parser = argparse.ArgumentParser(description='cifar10 classification models, distributed data parallel test')
parser.add_argument('--lr', default=0.1, help='')
parser.add_argument('--batch_size', type=int, default=768, help='')
parser.add_argument('--max_epochs', type=int, default=4, help='')
parser.add_argument('--num_workers', type=int, default=0, help='')

parser.add_argument('--init_method', default='tcp://127.0.0.1:3456', type=str, help='')
parser.add_argument('--dist-backend', default='nccl', type=str, help='')
parser.add_argument('--world_size', default=1, type=int, help='')
parser.add_argument('--distributed', action='store_true', help='')

def main():
    print("Starting...")

    args = parser.parse_args()

    local_rank = int(os.environ.get("SLURM_LOCALID")) 
    rank = int(os.environ.get("SLURM_PROCID"))
    current_device = local_rank

    torch.cuda.set_device(current_device)

    """ this block initializes a process group and initiate communications
		between all processes running on all nodes """

    print('From Rank: {}, ==> Initializing Process Group...'.format(rank))
    #init the process group
    dist.init_process_group(backend=args.dist_backend, init_method=args.init_method, world_size=args.world_size, rank=rank)
    print("process group ready!")

    print('From Rank: {}, ==> Making model..'.format(rank))

    class Net(nn.Module):

       def __init__(self):
          super(Net, self).__init__()

          self.conv1 = nn.Conv2d(3, 6, 5)
          self.pool = nn.MaxPool2d(2, 2)
          self.conv2 = nn.Conv2d(6, 16, 5)
          self.fc1 = nn.Linear(16 * 5 * 5, 120)
          self.fc2 = nn.Linear(120, 84)
          self.fc3 = nn.Linear(84, 10)

       def forward(self, x):
          x = self.pool(F.relu(self.conv1(x)))
          x = self.pool(F.relu(self.conv2(x)))
          x = x.view(-1, 16 * 5 * 5)
          x = F.relu(self.fc1(x))
          x = F.relu(self.fc2(x))
          x = self.fc3(x)
          return x

    net = torch.compile(Net())

    net.cuda()
    net = torch.nn.parallel.DistributedDataParallel(net, device_ids=[current_device])

    print('From Rank: {}, ==> Preparing data..'.format(rank))

    transform_train = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    dataset_train = CIFAR10(root='./data', train=True, download=False, transform=transform_train)

    train_sampler = torch.utils.data.distributed.DistributedSampler(dataset_train)
    train_loader = DataLoader(dataset_train, batch_size=args.batch_size, shuffle=(train_sampler is None), num_workers=args.num_workers, sampler=train_sampler, pin_memory=True)

    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = optim.SGD(net.parameters(), lr=args.lr, momentum=0.9, weight_decay=1e-4)

    for epoch in range(args.max_epochs):

        train_sampler.set_epoch(epoch)

        train(epoch, net, criterion, optimizer, train_loader, rank)

def train(epoch, net, criterion, optimizer, train_loader, train_rank):

    train_loss = 0
    correct = 0
    total = 0

    epoch_start = time.time()

    for batch_idx, (inputs, targets) in enumerate(train_loader):

       start = time.time()

       inputs = inputs.cuda()
       targets = targets.cuda()
       outputs = net(inputs)
       loss = criterion(outputs, targets)

       optimizer.zero_grad()
       loss.backward()
       optimizer.step()

       train_loss += loss.item()
       _, predicted = outputs.max(1)
       total += targets.size(0)
       correct += predicted.eq(targets).sum().item()
       acc = 100 * correct / total

       batch_time = time.time() - start

       elapse_time = time.time() - epoch_start
       elapse_time = datetime.timedelta(seconds=elapse_time)
       print("From Rank: {}, Training time {}".format(train_rank, elapse_time))

if __name__=='__main__':
   main()

```

### Using PyTorch Lightning

**PyTorch Lightning** is a Python package that provides interfaces to PyTorch to make many common, but otherwise code-heavy tasks, more straightforward. This includes training on multiple GPUs. The following is the same tutorial from the section above, but using PyTorch Lightning instead of explicitly leveraging the DistributedDataParallel class:

**File :** pytorch-ddp-test-pl.sh

```
#!/bin/bash
#SBATCH --nodes 1             
#SBATCH --gres=gpu:2          # Request 2 GPU "generic resources”.
#SBATCH --tasks-per-node=2    # Request 1 process per GPU. You will get 1 CPU per process by default. Request more CPUs with the "cpus-per-task" parameter to enable multiple data-loader workers to load data in parallel.
#SBATCH --mem=8G      
#SBATCH --time=0-03:00
#SBATCH --output=%N-%j.out

module load python # Using Default Python version - Make sure to choose a version that suits your application
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install torchvision pytorch-lightning --no-index

export TORCH_NCCL_ASYNC_HANDLING=1

# PyTorch Lightning will query the environment to figure out if it is running inside a SLURM batch job
# If it is, it expects the user to have requested one task per GPU.
# If you do not ask for 1 task per GPU, and you do not run your script with "srun", your job will fail!

srun python pytorch-ddp-test-pl.py  --batch_size 256

```

**File :** pytorch-ddp-test-pl.py

```
import datetime

import torch
from torch import nn
import torch.nn.functional as F

import pytorch_lightning as pl

import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader

import argparse

parser = argparse.ArgumentParser(description='cifar10 classification models, pytorch-lightning parallel test')
parser.add_argument('--lr', default=0.1, help='')
parser.add_argument('--max_epochs', type=int, default=4, help='')
parser.add_argument('--batch_size', type=int, default=768, help='')
parser.add_argument('--num_workers', type=int, default=0, help='')


def main():
    print("Starting...")

    args = parser.parse_args()

    class Net(pl.LightningModule):

       def __init__(self):
          super(Net, self).__init__()

          self.conv1 = nn.Conv2d(3, 6, 5)
          self.pool = nn.MaxPool2d(2, 2)
          self.conv2 = nn.Conv2d(6, 16, 5)
          self.fc1 = nn.Linear(16 * 5 * 5, 120)
          self.fc2 = nn.Linear(120, 84)
          self.fc3 = nn.Linear(84, 10)

       def forward(self, x):
          x = self.pool(F.relu(self.conv1(x)))
          x = self.pool(F.relu(self.conv2(x)))
          x = x.view(-1, 16 * 5 * 5)
          x = F.relu(self.fc1(x))
          x = F.relu(self.fc2(x))
          x = self.fc3(x)
          return x

       def training_step(self, batch, batch_idx):
          x, y = batch
          y_hat = self(x)
          loss = F.cross_entropy(y_hat, y)
          return loss

       def configure_optimizers(self):
          return torch.optim.Adam(self.parameters(), lr=args.lr)

    net = Net()

    """ Here we initialize a Trainer() explicitly with 1 node and 2 GPUs per node.
        To make this script more generic, you can use torch.cuda.device_count() to set the number of GPUs
        and you can use int(os.environ.get("SLURM_JOB_NUM_NODES")) to set the number of nodes. 
        We also set progress_bar_refresh_rate=0 to avoid writing a progress bar to the logs, 
        which can cause issues due to updating logs too frequently."""

    trainer = pl.Trainer(accelerator="gpu", devices=2, num_nodes=1, strategy='ddp', max_epochs = args.max_epochs, enable_progress_bar=False) 

    transform_train = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    dataset_train = CIFAR10(root='./data', train=True, download=False, transform=transform_train)

    train_loader = DataLoader(dataset_train, batch_size=args.batch_size, num_workers=args.num_workers)

    trainer.fit(net,train_loader)


if __name__=='__main__':
   main()

```

### Single GPU Data Parallelism

In cases where a model is fairly small, such that it does not take up a large portion of GPU memory and it cannot use a reasonable amount of its compute capacity, it is **not advisable to use a GPU**. Use one or more CPUs instead. However, in a scenario where you have such a model, but have a very large dataset and wish to perform training with a small batch size, taking advantage of Data parallelism on a GPU becomes a viable option.

In the example that follows, we adapt the code from the previous section to run on a single GPU. This task is fairly small - with a batch size of 512 images, our model takes up about 1GB of GPU memory space, and it uses only about 6% of its compute capacity during training. This is a model that **should not** be trained on a GPU on our clusters. However, using Data Parallelism, we can fit several replicas of this model on a single GPU and increase our resource usage, while getting a nice speed-up. We use Nvidia's [Multi-Process Service (MPS)](https://docs.nvidia.com/deploy/mps/index.html), along with [MPI](https://docs.computecanada.ca/wiki/MPI) to efficiently place multiple model replicas on one GPU:

**File :** pytorch-gpu-mps.sh

```
#!/bin/bash
#SBATCH --nodes 1
#SBATCH --gres=gpu:1 # request a GPU
#SBATCH --tasks-per-node=8 # This is the number of model replicas we will place on the GPU. Change this to 10,12,14,... to see the effect on performance  
#SBATCH --cpus-per-task=1 # increase this parameter and increase "--num_workers" accordingly to see the effect on performance
#SBATCH --mem=8G      
#SBATCH --time=0:05:00
#SBATCH --output=%N-%j.out
#SBATCH --account=<your account>

module load python # Using Default Python version - Make sure to choose a version that suits your application
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install torch torchvision --no-index

# Activate Nvidia MPS:
export CUDA_MPS_PIPE_DIRECTORY=/tmp/nvidia-mps
export CUDA_MPS_LOG_DIRECTORY=/tmp/nvidia-log
nvidia-cuda-mps-control -d

echo "starting training..."
time srun --cpus-per-task=$SLURM_CPUS_PER_TASK python cifar10-gpu-mps.py --batch_size=512 --num_workers=0

```

**File :** cifar10-gpu-mps.py

```
import os
import time
import datetime
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader

import torch.distributed as dist
import torch.utils.data.distributed

import argparse

parser = argparse.ArgumentParser(description='cifar10 classification models, distributed data parallel maps test')
parser.add_argument('--lr', default=0.1, help='')
parser.add_argument('--batch_size', type=int, default=512, help='')
parser.add_argument('--num_workers', type=int, default=0, help='')
parser.add_argument('--init_method', default='tcp://127.0.0.1:3456', type=str, help='')

def main():
    print("Starting...")

    args = parser.parse_args()

    rank = os.environ.get("SLURM_LOCALID")

    current_device = 0
    torch.cuda.set_device(current_device)

    """ this block initializes a process group and initiate communications
                between all processes that will run a model replica """

    print('From Rank: {}, ==> Initializing Process Group...'.format(rank))

    dist.init_process_group(backend="mpi", init_method=args.init_method) # Use backend="mpi" or "gloo". NCCL does not work on a single GPU due to a hard-coded multi-GPU topology check.
    print("process group ready!")

    print('From Rank: {}, ==> Making model..'.format(rank))

    class Net(nn.Module):

       def __init__(self):
          super(Net, self).__init__()

          self.conv1 = nn.Conv2d(3, 6, 5)
          self.pool = nn.MaxPool2d(2, 2)
          self.conv2 = nn.Conv2d(6, 16, 5)
          self.fc1 = nn.Linear(16 * 5 * 5, 120)
          self.fc2 = nn.Linear(120, 84)
          self.fc3 = nn.Linear(84, 10)

       def forward(self, x):
          x = self.pool(F.relu(self.conv1(x)))
          x = self.pool(F.relu(self.conv2(x)))
          x = x.view(-1, 16 * 5 * 5)
          x = F.relu(self.fc1(x))
          x = F.relu(self.fc2(x))
          x = self.fc3(x)
          return x

    net = Net()

    net.cuda()
    net = torch.nn.parallel.DistributedDataParallel(net, device_ids=[current_device]) # Wrap the model with DistributedDataParallel

    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = optim.SGD(net.parameters(), lr=args.lr)

    print('From Rank: {}, ==> Preparing data..'.format(rank))

    transform_train = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    dataset_train = CIFAR10(root='~/data', train=True, download=False, transform=transform_train)

    train_sampler = torch.utils.data.distributed.DistributedSampler(dataset_train)
    train_loader = DataLoader(dataset_train, batch_size=args.batch_size, shuffle=(train_sampler is None), num_workers=args.num_workers, sampler=train_sampler)

    perf = []

    total_start = time.time()

    for batch_idx, (inputs, targets) in enumerate(train_loader):

       start = time.time()
       
       inputs = inputs.cuda() 
       targets = targets.cuda()

       outputs = net(inputs)
       loss = criterion(outputs, targets)

       optimizer.zero_grad()
       loss.backward()
       optimizer.step()

       batch_time = time.time() - start

       images_per_sec = args.batch_size/batch_time

       perf.append(images_per_sec)

    total_time = time.time() - total_start

if __name__=='__main__':
   main()

```

## Fully Sharded Data Parallelism

Similar to [Deepspeed](Deepspeed.md), Fully Sharded Data Parallelism ([FSDP](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)) enables distributed storage and computing of different elements of a training task - such as optimizer states, model weights, model gradients and model activations - across multiple devices, including GPU, CPU, local hard disk, and/or combinations of these devices. This "pooling" of resources, notably for storage, allows models with massive amounts of parameters to be trained efficiently, across multiple nodes.

Note that, with FSDP, a model layer that gets sharded across devices may be collected inside a single device during a forward or backward pass. You should not use FSDP if your model has layers that do not fit entirely in the memory of a single GPU. See the section on Tensor Parallelism to see how to deal with this case.

## Tensor Parallelism

Tensor Parallelism (TP) is a model sharding approach that differs from FSDP in that the computation of a forward or backward pass through a model layer is split along with the layers' weights across multiple devices. In other words, while FSDP shards model weights across devices, it must still collect shards together in the same device during certain computation steps. This introduces overhead from having to move model shards across devices, and it implies that individual FSDP layers, or sharded model blocks, must fit entirely in the memory of a single device. With TP on the other hand, computation steps are done locally in the device where a model shard is placed.

## Pipeline Parallelism

Pipeline Parallelism (PP) is a model sharding approach where the shards are groups of consecutive of layers of a model. Each shard, or block of sequential layers, gets placed on a different device, thus a forward or backward pass through the model means performing computations on each device *in sequence*. This means that the farther away a block of layers is from the current block being used in a computation at any given time, the longer the device hosting it will have to wait for its turn to perform any computations. To mitigate this, in PP, every input batch is broken into *"micro-batches"*, which are fed to the model in sequence. This ensures all devices stay busy as the first micro-batch reaches the last model block.

# Creating model checkpoints

Whether or not you expect your code to run for long time periods, it is a good habit to create Checkpoints during training. A checkpoint is a snapshot of your model at a given point during the training process (after a certain number of iterations or after a number of epochs) that is saved to disk and can be loaded at a later time. It is a handy way of breaking up jobs that are expected to run for a very long time, into multiple shorter jobs that may get allocated on the cluster more quickly. It is also a good way of avoiding losing progress in case of unexpected errors in your code or node failures.

## With PyTorch Lightning

To create a checkpoint when training with `pytorch-lightning`, we recommend using the callbacks parameter of the `Trainer()` class. The following example shows how to instruct PyTorch to create a checkpoint at the end of every training epoch. Make sure the path where you want to create the checkpoint exists.

```
callbacks = [pl.callbacks.ModelCheckpoint(dirpath="./ckpt",every_n_epochs=1)]
trainer = pl.Trainer(callbacks=callbacks) 
trainer.fit(model)

```

This code snippet will also load a checkpoint from `./ckpt`, if there is one, and continue training from that point. For more information, please refer to the [official PyTorch Lightning documentation](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.callbacks.model_checkpoint.html).

## With custom training loops

Please refer to the [official PyTorch documentation](https://pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html) for examples on how to create and load checkpoints inside of a training loop.

## During distributed training

Checkpointing can also be done while running a distributed training program. With PyTorch Lightning, no extra code is required other than using the checkpoint callback as described above. If you are using DistributedDataParallel or Horovod however, checkpointing should be done only by one process (one of the ranks) of your program, since all ranks will have the same state at the end of each iteration. The following example uses the first process (rank 0) to create a checkpoint:

```
if global_rank == 0:
       torch.save(ddp_model.state_dict(), "./checkpoint_path")

```

You must be careful when loading a checkpoint created in this manner. If a process tries to load a checkpoint that has not yet been saved by another, you may see errors or get wrong results. To avoid this, you can add a barrier to your code to make sure the process that will create the checkpoint finishes writing it to disk before other processes attempt to load it. Also note that `torch.load` will attempt to load tensors to the GPU that saved them originally (`cuda:0` in this case) by default. To avoid issues, pass `map_location` to `torch.load` to load tensors on the correct GPU for each rank.

```
torch.distributed.barrier()
map_location = f"cuda:{local_rank}"  
ddp_model.load_state_dict(
torch.load("./checkpoint_path", map_location=map_location))

```

# Troubleshooting

## CUDA error: no kernel image is available for execution on the device

This exception means that the current torch installation does not support the compute architecture or the device (gpu) used.
Either update torch to a more recent version or request a different GPU compatible with the current version used.

# LibTorch

LibTorch allows one to implement both C++ extensions to PyTorch and **pure C++ machine learning applications**. It contains "all headers, libraries and CMake configuration files required to depend on PyTorch", as described in the [documentation](https://pytorch.org/cppdocs/installing.html).

### How to use LibTorch

#### Setting up the environment

Load the modules required by Libtorch, then install PyTorch in a Python virtual environment:

StdEnv/2023StdEnv/2020

```
module load StdEnv/2023 gcc cuda/12.2 cmake protobuf cudnn python/3.11 abseil  cusparselt  opencv/4.8.1
virtualenv --no-download --clear ~/ENV && source ~/ENV/bin/activate 
pip install --no-index torch numpy 

```

Note that the versions for the abseil, cusparselt and opencv modules may need to be adjusted,
depending on the version of the torch package. In order to find out which version of those
modules was used to compile the Python wheel for torch, use the following command:

```
$ ldd $VIRTUAL_ENV/lib/python3.11/site-packages/torch/lib/libtorch_cuda.so | sed -n 's&^.*/\(\(opencv\|abseil\|cusparselt\)/[^/]*\).*&\1&p' | sort -u
abseil/20230125.3
cusparselt/0.5.0.1
opencv/4.8.1

```

```
module load gcc cuda/11.4 cmake protobuf cudnn python/3.10
virtualenv --no-download --clear ~/ENV && source ~/ENV/bin/activate 
pip install --no-index torch numpy 

```

#### Compiling a minimal example

Create the following two files:

**File :** example.cpp

```
#include <torch/torch.h>
#include <iostream>

int main() 
{
    torch::Device device(torch::kCPU);
    if (torch::cuda::is_available()) 
    {
        std::cout << "CUDA is available! Using GPU." << std::endl;
        device = torch::Device(torch::kCUDA);
    }

    torch::Tensor tensor = torch::rand({2, 3}).to(device);
    std::cout << tensor << std::endl;
}

```

**File :** CMakeLists.txt

```
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(example)

find_package(Torch REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example "${TORCH_LIBRARIES}")
set_property(TARGET example PROPERTY CXX_STANDARD 14)
```

With the python virtualenv activated, configure the project and compile the program:

StdEnv/2023StdEnv/2020

```
cmake -B build -S . -DCMAKE_PREFIX_PATH=$VIRTUAL_ENV/lib/python3.11/site-packages \
                    -DCMAKE_EXE_LINKER_FLAGS=-Wl,-rpath=$VIRTUAL_ENV/lib/python3.11/site-packages/torch/lib,-L$EBROOTCUDA/extras/CUPTI/lib64 \
                    -DCMAKE_SKIP_RPATH=ON -DTORCH_CUDA_ARCH_LIST="6.0;7.0;7.5;8.0;9.0"
cmake --build build

```

```
cmake -B build -S . -DCMAKE_PREFIX_PATH=$VIRTUAL_ENV/lib/python3.10/site-packages \
                    -DCMAKE_EXE_LINKER_FLAGS=-Wl,-rpath=$VIRTUAL_ENV/lib/python3.10/site-packages/torch/lib \
                    -DCMAKE_SKIP_RPATH=ON
cmake --build build 

```

Run the program:

```
build/example

```

To test an application with CUDA, request an [interactive job](Running_jobs.md#Interactive_jobs) with a [GPU](Using_GPUs_with_Slurm.md).

# rTorch

In order to install rTorch, from a login node:

1. Load required modules:

```
[name@server ~]$ module load r/4.5 cuda/12.6 cudnn

```

2. Create your installation directory following [installing R packages](R.md#Installing_for_one_or_many_R_versions):

```
[name@server ~]$ mkdir -p ~/.local/R/$EBVERSIONR/
[name@server ~]$ export R_LIBS=~/.local/R/$EBVERSIONR/

```

3. Install the latest rtorch available

```
[name@server ~]$ R -e 'install.packages("torch", repos="https://cloud.r-project.org/")'

```

4. Install dependencies

```
[name@server ~]$ R -e 'torch::install_torch()'

```

5. Patch the downloaded shared library (lantern):

```
[name@server ~]$ setrpaths.sh --path $R_LIBS/torch/lib/liblantern.so --add_path $EBROOTCUDACORE/lib --any_interpreter

```

6. Run a quick CPU test

```
[name@server ~]$ R -e 'torch::torch_tensor(1)'
> torch::torch_tensor(1)
torch_tensor
 1
[ CPUFloatType{1} ]

```

7. Run a quick GPU test

```
[name@server ~]$ srun --mem=3500M --gpus=h100_1g.10gb:1 -- R -e 'torch::torch_tensor(1)$cuda()'
> torch::torch_tensor(1)$cuda()
torch_tensor
 1
[ CUDAFloatType{1} ]

```

# Resources

[https://pytorch.org/cppdocs/](https://pytorch.org/cppdocs/)