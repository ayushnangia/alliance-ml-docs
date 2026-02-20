# ML Researcher's Guide to Alliance Canada HPC

> A curated collection of 156 essential documentation pages from the Digital Research Alliance of Canada, selected specifically for machine learning researchers. Covers everything from getting your first GPU job running to distributed training with DeepSpeed across multiple nodes.

---

## Table of Contents

- [Getting Started](#getting-started) (10 pages) — Essential first steps for accessing Alliance HPC clusters.
- [SSH & Remote Access](#ssh-remote-access) (12 pages) — Connecting to clusters and forwarding ports for Jupyter/TensorBoard.
- [Cluster Specifications](#cluster-specifications) (16 pages) — Hardware specs — CPU, GPU, memory, storage for each cluster.
- [Submitting & Managing Jobs](#submitting-managing-jobs) (12 pages) — How to run training jobs with Slurm.
- [Storage & Data Management](#storage-data-management) (15 pages) — Where to store datasets, checkpoints, and results.
- [Python Environment](#python-environment) (9 pages) — Setting up Python, virtualenvs, and Jupyter.
- [Software Modules & Containers](#software-modules-containers) (11 pages) — Loading software and using containers.
- [GPU & CUDA Programming](#gpu-cuda-programming) (9 pages) — CUDA, GPU monitoring, multi-GPU, MIG.
- [AI & Machine Learning Frameworks](#ai-machine-learning-frameworks) (24 pages) — PyTorch, TensorFlow, and other ML frameworks.
- [ML Experiment Tracking & Performance](#ml-experiment-tracking-performance) (7 pages) — Logging, tracking, and optimizing experiments.
- [Distributed & Parallel Computing](#distributed-parallel-computing) (7 pages) — MPI, NCCL, and scaling training across nodes.
- [Datasets & Data Formats](#datasets-data-formats) (7 pages) — Common datasets and data handling.
- [Debugging & Profiling](#debugging-profiling) (3 pages) — Finding and fixing issues in ML code.
- [Cloud Computing](#cloud-computing) (6 pages) — Running ML workloads on Alliance cloud with GPUs.
- [Programming Tools](#programming-tools) (5 pages) — Git, R, Julia, and other programming resources.
- [Resource Allocation](#resource-allocation) (3 pages) — Getting GPU time and compute allocations.

---

## Getting Started
*Essential first steps for accessing Alliance HPC clusters.*

- [Getting Started](Getting_Started.md): Complete onboarding guide — accounts, SSH, first job
- [Apply for a CCDB account](Apply_for_a_CCDB_account.md): How to register for an Alliance account
- [Linux introduction](Linux_introduction.md): Linux/command-line basics for cluster usage
- [What is a scheduler](What_is_a_scheduler.md): What Slurm is and why you need it
- [Multifactor authentication](Multifactor_authentication.md): Setting up MFA (required for login)
- [System status](System_status.md): Check if clusters are up
- [Technical Support](Technical_Support.md): How to get help
- [Frequently Asked Questions](Frequently_Asked_Questions.md): Common questions and answers
- [Acknowledging the Alliance](Acknowledging_the_Alliance.md): How to cite Alliance in papers
- [Self-paced courses](Self-paced_courses.md): Free training materials

## SSH & Remote Access
*Connecting to clusters and forwarding ports for Jupyter/TensorBoard.*

- [SSH](SSH.md): SSH connection guide — keys, X11, clients
- [SSH Keys](SSH_Keys.md): Generating and using SSH keys
- [SSH tunnelling](SSH_tunnelling.md): Port forwarding for Jupyter, TensorBoard, etc.
- [SSH configuration file](SSH_configuration_file.md): Simplify logins with SSH config
- [Generating SSH keys in Windows](Generating_SSH_keys_in_Windows.md): Windows SSH key generation
- [Using SSH keys in Linux](Using_SSH_keys_in_Linux.md): Linux/Mac SSH key setup
- [Connecting with MobaXTerm](Connecting_with_MobaXTerm.md): MobaXTerm client (Windows)
- [Connecting with PuTTY](Connecting_with_PuTTY.md): PuTTY client (Windows)
- [Visual Studio Code](Visual_Studio_Code.md): VS Code remote development on clusters
- [Prolonging terminal sessions](Prolonging_terminal_sessions.md): tmux/screen to keep sessions alive
- [VNC](VNC.md): Remote desktop via VNC
- [Windows Subsystem for Linux WSL](Windows_Subsystem_for_Linux_WSL.md): WSL for Windows users

## Cluster Specifications
*Hardware specs — CPU, GPU, memory, storage for each cluster.*

- [National systems](National_systems.md): Overview of all national systems
- [Trillium](Trillium.md): 1224 CPU + 63 GPU nodes (H100 80GB), 29PB NVMe — U of T
- [Narval](Narval.md): GPU nodes with A100 80GB — ETS Montreal
- [Cedar](Cedar.md): GPU nodes (P100, V100) — SFU
- [Graham](Graham.md): GPU nodes (P100, V100, T4) — U of Waterloo
- [Beluga](Beluga.md): GPU nodes (V100 32GB) — ETS Montreal
- [Fir](Fir.md): New cluster at SFU with GPUs
- [Nibi](Nibi.md): New cluster with GPUs
- [Rorqual](Rorqual.md): New cluster at ETS Montreal
- [Killarney](Killarney.md): New cluster
- [Vulcan](Vulcan.md): New cluster
- [Niagara](Niagara.md): 80k CPU cores for large parallel jobs — U of T
- [Mist](Mist.md): Power9 + V100 GPUs — SciNet
- [Arbutus](Arbutus.md): Cloud with GPU instances — UVic
- [Trillium Quickstart](Trillium_Quickstart.md): Trillium-specific quick start
- [Niagara Quickstart](Niagara_Quickstart.md): Niagara-specific quick start

## Submitting & Managing Jobs
*How to run training jobs with Slurm.*

- [Running jobs](Running_jobs.md): Complete Slurm guide — sbatch, resources, memory, time, examples
- [Using GPUs with SLURM](Using_GPUs_with_SLURM.md): GPU jobs — --gres=gpu, GPU types, multi-GPU, selecting GPUs
- [Job arrays](Job_arrays.md): Array jobs for hyperparameter sweeps
- [Monitoring jobs](Monitoring_jobs.md): squeue, sacct, email notifications, checking GPU usage
- [Job scheduling](Job_scheduling.md): Scheduling policies, priority, fairshare
- [Best practices for job submission](Best_practices_for_job_submission.md): Tips for efficient job submission
- [Advanced MPI scheduling](Advanced_MPI_scheduling.md): MPI job layouts for distributed training
- [GNU Parallel](GNU_Parallel.md): Run many serial tasks in one job
- [GLOST](GLOST.md): Another tool for serial task farming
- [META-Farm](META-Farm.md): High-throughput job farming framework
- [Managing Slurm accounts](Managing_Slurm_accounts.md): Slurm accounts and project allocations
- [Allocations and compute scheduling](Allocations_and_compute_scheduling.md): How compute allocations work

## Storage & Data Management
*Where to store datasets, checkpoints, and results.*

- [Filesystem](Filesystem.md): Storage overview — home, scratch, project, nearline quotas
- [Scratch purging policy](Scratch_purging_policy.md): IMPORTANT: scratch files auto-deleted after 60 days
- [Project Layout](Project_Layout.md): Project directory structure and group access
- [Transferring data](Transferring_data.md): SCP, rsync, SFTP, Globus for moving data
- [Globus](Globus.md): Globus for large dataset transfers
- [Using SLURM TMPDIR](Using_SLURM_TMPDIR.md): Fast node-local SSD for training data
- [Handling large collections of files](Handling_large_collections_of_files.md): Strategies for datasets with millions of files
- [Nearline](Nearline.md): Tape archive for long-term model/data storage
- [Archiving and compressing files](Archiving_and_compressing_files.md): tar, gzip, zip for bundling data
- [Sharing data](Sharing_data.md): Share datasets between users/projects
- [HDF5](HDF5.md): HDF5 data format
- [Tuning Lustre](Tuning_Lustre.md): Lustre I/O performance tuning
- [Diskusage Explorer](Diskusage_Explorer.md): Check disk usage and quotas
- [Tar](Tar.md): Tar tutorial
- [Data Management at Niagara](Data_Management_at_Niagara.md): Niagara-specific storage

## Python Environment
*Setting up Python, virtualenvs, and Jupyter.*

- [Python](Python.md): Python on clusters — virtualenvs, pip, wheels, common issues
- [Available Python wheels](Available_Python_wheels.md): Pre-built wheels available (torch, tensorflow, etc.)
- [Anaconda](Anaconda.md): Why Anaconda/Conda is NOT recommended and what to use instead
- [Conda](Conda.md): Conda alternatives and workarounds
- [Jupyter](Jupyter.md): Running Jupyter on clusters
- [JupyterHub](JupyterHub.md): JupyterHub web interface
- [JupyterLab](JupyterLab.md): JupyterLab on clusters
- [JupyterNotebook](JupyterNotebook.md): Jupyter Notebook setup
- [Advanced Jupyter configuration](Advanced_Jupyter_configuration.md): Custom kernels, extensions, multi-GPU Jupyter

## Software Modules & Containers
*Loading software and using containers.*

- [Available software](Available_software.md): All pre-installed software
- [Utiliser des modules](Utiliser_des_modules.md): Module system — module load, spider, avail
- [Modules](Modules.md): Module system overview
- [Standard software environments](Standard_software_environments.md): StdEnv versions and switching between them
- [Installing software in your home directory](Installing_software_in_your_home_directory.md): Building your own software
- [Apptainer](Apptainer.md): Running Docker/Singularity containers on clusters
- [Using Conda in Apptainer](Using_Conda_in_Apptainer.md): Using Conda inside Apptainer containers
- [EasyBuild](EasyBuild.md): EasyBuild for custom software installs
- [CVMFS](CVMFS.md): CVMFS distributed software repository
- [Accessing CVMFS](Accessing_CVMFS.md): Accessing Alliance software from outside
- [Recent changes to the software environment](Recent_changes_to_the_software_environment.md): What changed in recent StdEnv updates

## GPU & CUDA Programming
*CUDA, GPU monitoring, multi-GPU, MIG.*

- [CUDA](CUDA.md): CUDA toolkit — versions, compatibility, compilation
- [CUDA tutorial](CUDA_tutorial.md): CUDA programming tutorial — kernels, memory, optimization
- [Multi-Instance GPU](Multi-Instance_GPU.md): MIG — partitioning A100/H100 into smaller GPU instances
- [Hyper-Q   MPS](Hyper-Q___MPS.md): MPS for sharing GPUs between processes
- [NCCL](NCCL.md): NCCL — NVIDIA collective communication for distributed training
- [NVTOP](NVTOP.md): Monitor GPU utilization in real-time
- [Nvprof](Nvprof.md): NVIDIA profiler for GPU code
- [Using cloud vGPUs](Using_cloud_vGPUs.md): Virtual GPUs in cloud instances
- [Using cloud GPUs](Using_cloud_GPUs.md): Cloud GPU instances

## AI & Machine Learning Frameworks
*PyTorch, TensorFlow, and other ML frameworks.*

- [AI and Machine Learning](AI_and_Machine_Learning.md): ML overview — best practices, GPU usage, data loading, checkpointing
- [PyTorch](PyTorch.md): PyTorch — install, GPU, distributed training, DataLoader
- [TensorFlow](TensorFlow.md): TensorFlow — install, GPU config, distributed
- [Keras](Keras.md): Keras deep learning
- [Deepspeed](Deepspeed.md): DeepSpeed — ZeRO optimization, pipeline parallelism, config
- [Huggingface](Huggingface.md): HuggingFace Transformers, datasets, tokenizers on clusters
- [Large Language Models LLMs](Large_Language_Models_LLMs.md): Running LLMs — memory requirements, quantization, serving
- [VLLM](VLLM.md): vLLM for high-throughput LLM inference
- [XGBoost](XGBoost.md): XGBoost gradient boosting
- [SpaCy](SpaCy.md): SpaCy NLP on clusters
- [Dask](Dask.md): Dask parallel computing
- [RAPIDS](RAPIDS.md): RAPIDS GPU-accelerated data science
- [Ray](Ray.md): Ray distributed computing and Ray Tune
- [Faiss](Faiss.md): Faiss vector similarity search (GPU-accelerated)
- [Flax](Flax.md): Flax (JAX-based) neural networks
- [MXNet](MXNet.md): Apache MXNet
- [OpenCV](OpenCV.md): OpenCV computer vision
- [Torch](Torch.md): Torch (legacy, Lua-based)
- [Large Scale Machine Learning Big Data](Large_Scale_Machine_Learning_Big_Data.md): Large-scale ML with big data
- [AlphaFold2](AlphaFold2.md): AlphaFold2 protein structure prediction
- [AlphaFold3](AlphaFold3.md): AlphaFold3 setup and usage
- [AlphaFold](AlphaFold.md): AlphaFold overview
- [Interpretable AI](Interpretable_AI.md): Interpretable/explainable AI tools
- [Tutoriel Apprentissage machine](Tutoriel_Apprentissage_machine.md): ML tutorial

## ML Experiment Tracking & Performance
*Logging, tracking, and optimizing experiments.*

- [ML Performance Guide](ML_Performance_Guide.md): When to use GPUs, multi-GPU, profiling ML workloads
- [Weights Biases wandb](Weights_Biases_wandb.md): Weights & Biases experiment tracking
- [Cometml](Cometml.md): Comet.ml experiment tracking
- [MLflow](MLflow.md): MLflow experiment and model tracking
- [Tensorboard](Tensorboard.md): TensorBoard visualization for training curves
- [Optuna](Optuna.md): Optuna hyperparameter optimization
- [Points de contrôle](Points_de_contrôle.md): Checkpointing — save/resume long training runs

## Distributed & Parallel Computing
*MPI, NCCL, and scaling training across nodes.*

- [MPI](MPI.md): MPI — compilation, running, common issues
- [MPI4py](MPI4py.md): mpi4py for Python MPI (Horovod, custom distributed)
- [OpenMP](OpenMP.md): OpenMP shared-memory parallelism
- [BLAS and LAPACK](BLAS_and_LAPACK.md): Linear algebra libraries (underlying PyTorch/NumPy)
- [Scalability](Scalability.md): Testing and improving parallel scalability
- [Working with processors that have non-uniform memory access NUMA](Working_with_processors_that_have_non-uniform_memory_access_NUMA.md): NUMA awareness for multi-socket nodes
- [Parallel I O introductory tutorial](Parallel_I_O_introductory_tutorial.md): Parallel I/O for fast data loading

## Datasets & Data Formats
*Common datasets and data handling.*

- [ImageNet](ImageNet.md): ImageNet dataset on clusters
- [VoxCeleb](VoxCeleb.md): VoxCeleb speaker recognition dataset
- [Arrow](Arrow.md): Apache Arrow columnar data
- [NetCDF](NetCDF.md): NetCDF scientific data format
- [SQLite](SQLite.md): SQLite databases
- [Database servers](Database_servers.md): Database servers on Alliance
- [PyKeOps](PyKeOps.md): PyKeOps for kernel operations on GPU

## Debugging & Profiling
*Finding and fixing issues in ML code.*

- [Debugging and profiling](Debugging_and_profiling.md): Overview of debugging and profiling tools
- [Valgrind](Valgrind.md): Memory debugging with Valgrind
- [GBD page](GBD_page.md): GDB debugger

## Cloud Computing
*Running ML workloads on Alliance cloud with GPUs.*

- [Cloud](Cloud.md): Cloud overview — OpenStack, VMs, networking
- [Cloud Quick Start](Cloud_Quick_Start.md): Launch your first cloud VM
- [Using cloud vGPUs](Using_cloud_vGPUs.md): Virtual GPU instances in cloud
- [Virtual machine flavors](Virtual_machine_flavors.md): VM sizes and GPU options
- [Working with volumes](Working_with_volumes.md): Persistent storage in cloud
- [Spark](Spark.md): Apache Spark for distributed data processing

## Programming Tools
*Git, R, Julia, and other programming resources.*

- [Programming guide](Programming_guide.md): Languages, compilers, and tools overview
- [R](R.md): R for statistical ML (tidymodels, caret, etc.)
- [Julia](Julia.md): Julia for ML (Flux.jl, GPU support)
- [Git](Git.md): Git version control on clusters
- [Version control](Version_control.md): Version control overview

## Resource Allocation
*Getting GPU time and compute allocations.*

- [Resource Allocation Competition](Resource_Allocation_Competition.md): Annual allocation competition for dedicated resources
- [Rapid Access Service](Rapid_Access_Service.md): Quick-start allocations without competition
- [Using a RAC](Using_a_RAC.md): How to use your resource allocation

