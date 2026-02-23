# Containers (Apptainer) on Alliance Clusters

## When to use containers

Use Apptainer containers when:
- You need software not available as a module or pre-built wheel
- You have a Docker image you want to run on the cluster
- You need a specific CUDA or library environment not provided by modules
- You need to reproduce an exact software stack

**Prefer modules and wheels first.** Alliance provides optimized pre-built software. Only use containers when modules/wheels don't cover your needs. Docker is **not available** on Alliance clusters — use Apptainer instead.

Apptainer (formerly Singularity) is the standard container runtime on HPC systems. It runs without root privileges and integrates with Slurm.

## Loading Apptainer

```bash
# Load the default version
module load apptainer

# Search for available versions
module spider apptainer
```

## Running programs in containers

### Execution commands

| Command | Behavior |
|---------|----------|
| `apptainer run image.sif <cmd>` | Runs `%runscript` first, then your command |
| `apptainer exec image.sif <cmd>` | Runs your command directly (skips `%runscript`) |
| `apptainer shell image.sif` | Opens interactive shell inside container |

**Recommendation:** Always use `apptainer run` unless you have a specific reason not to.

### Isolation flags (important!)

By default, Apptainer inherits your host shell environment, which can cause library conflicts. Use isolation flags:

| Flag | Effect |
|------|--------|
| `-C` | Full isolation: filesystems, PID, IPC, and environment. Requires bind mounts for any external data. |
| `-c` | Partial isolation: minimal `/dev`, empty `/tmp` and `/home`. Requires bind mounts for external data. |
| `-e` | Cleans environment variables for OCI/Docker compatibility. Implies `--containall`. |

### Working directory (`-W`)

On clusters, `/tmp` uses RAM (not disk). If your container writes temporary files, it can exhaust your job's memory allocation. Always set a disk-backed working directory:

```bash
apptainer run -C -W $SLURM_TMPDIR image.sif myprogram
```

## GPU access

Pass `--nv` for NVIDIA GPUs to ensure correct `/dev` entries and GPU libraries:

```bash
apptainer run --nv -C -W $SLURM_TMPDIR -B /project -B /scratch image.sif python train.py
```

This flag:
- Bind-mounts NVIDIA device files (`/dev/nvidia*`)
- Locates and binds GPU libraries from the host
- Sets `LD_LIBRARY_PATH` for GPU libraries inside the container

For AMD GPUs, use `--rocm` instead of `--nv`.

## Bind mounts

When using `-C` or `-c`, your cluster filesystems are not visible inside the container. Use `-B` to mount them:

```bash
# Mount project and scratch filesystems
apptainer run -C -B /project -B /scratch -W $SLURM_TMPDIR image.sif myprogram

# Mount home to an alternate path (recommended to avoid config conflicts)
apptainer run -C -B /home:/cluster_home -B /project -B /scratch -W $SLURM_TMPDIR image.sif myprogram
```

### Why use `-B /home:/cluster_home`?

Mounting `/home` directly can cause conflicts: programs in `$HOME/bin` or Python packages in `$HOME/.local/lib/python3.x` may override software inside your container. Mounting to `/cluster_home` avoids this.

### Important: do NOT mount CVMFS

Don't bind-mount CVMFS paths inside containers. Programs running inside a container should be fully contained — importing external module software defeats the purpose.

### Common bind mount patterns

```bash
# Access your data + write temp files to fast local storage
-B /project -B /scratch -W $SLURM_TMPDIR

# Map a host file to a specific container path
-B ./my_data.csv:/data/input.csv

# Full isolation with all common filesystems
-C -B /home:/cluster_home -B /project -B /scratch -W $SLURM_TMPDIR
```

## Building SIF images from Docker

### Direct from Docker Hub

```bash
module load apptainer
apptainer build myimage.sif docker://ubuntu:22.04
apptainer build pytorch.sif docker://pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime
```

### SIF vs sandbox

| Format | Type | Pros | Cons |
|--------|------|------|------|
| SIF file | Single compressed file | Fast I/O, tiny file count quota, read-only (safe) | Need rebuild to modify |
| Sandbox | Directory | Can modify in-place with `--writable` | Slow I/O, uses thousands of file count quota |

**Always prefer SIF files** on Alliance clusters. The parallel filesystem is optimized for large files, not thousands of small files.

### From a Dockerfile (on your local machine)

If you only have a Dockerfile, build on a machine where you have Docker + Apptainer installed:

```bash
# On your local machine (not on the cluster)
docker build -f Dockerfile -t myimage
docker save myimage -o myimage.tar
docker image rm myimage
apptainer build myimage.sif docker-archive://myimage.tar
rm myimage.tar

# Then transfer to cluster
scp myimage.sif username@narval.alliancecan.ca:~/
```

## Conda/Micromamba in containers

If you must use Conda (despite Alliance recommending modules/wheels), containerize it. This is a 3-step process:

### Step 1: Create environment.yml

```yaml
name: base
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - numpy
  - scipy
```

### Step 2: Create image definition file (image.def)

```
Bootstrap: docker
From: mambaorg/micromamba:latest

%files
    environment.yml /environment.yml

%post
    micromamba install -n base --file environment.yml && \
        micromamba clean --all --yes
```

### Step 3: Build the SIF image

```bash
module load apptainer
APPTAINER_BIND=' ' apptainer build image.sif image.def
```

Test it:

```bash
apptainer run image.sif python -c "import numpy; print(numpy.__version__)"
```

**Note:** Using Conda is subject to [Anaconda's Terms of Service](https://legal.anaconda.com/policies/en?name=terms-of-service#terms-of-service) and may require a commercial license. Micromamba from conda-forge avoids this.

## Cache management

Apptainer caches downloaded layers and images. Over time this grows large. Manage it:

```bash
# See cache location and size
apptainer cache list

# Clean the cache
apptainer cache clean
```

### Redirect cache to $SCRATCH (recommended)

Default cache goes to `$HOME`, which has limited quota. Redirect to `$SCRATCH`:

```bash
mkdir -p $SCRATCH/apptainer/{cache,tmp}
export APPTAINER_CACHEDIR="$SCRATCH/apptainer/cache"
export APPTAINER_TMPDIR="$SCRATCH/apptainer/tmp"
```

Add these exports to your `~/.bashrc` to make them permanent.

**Important:** Avoid building sandbox images on networked filesystems (Lustre/GPFS). Always set `APPTAINER_TMPDIR` to a local or scratch location.

## Complete GPU ML job example

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-03:00
#SBATCH --output=%N-%j.out

module load apptainer

# Run training inside container with GPU access
apptainer run --nv \
    -C \
    -W $SLURM_TMPDIR \
    -B /project -B /scratch \
    -B /home:/cluster_home \
    $PROJECT/containers/my_ml_image.sif \
    python /cluster_home/$USER/train.py \
        --data /scratch/$USER/dataset \
        --output /scratch/$USER/results
```

Key flags explained:
- `--nv` — GPU access (NVIDIA)
- `-C` — full isolation from host environment
- `-W $SLURM_TMPDIR` — disk-backed temp directory
- `-B /project -B /scratch` — access to cluster storage
- `-B /home:/cluster_home` — home at alternate path to avoid conflicts

Store your SIF images in `$PROJECT` (persistent, backed up) rather than `$SCRATCH` (purged after 60 days).
