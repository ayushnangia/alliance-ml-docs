# Python Environment Setup on Alliance Clusters

## Loading Python

```bash
module avail python          # See available versions
module load python/3.11      # Load your chosen version
```

Always load a Python module explicitly. The system default Python is outdated and missing package support.

## Creating a virtual environment

```bash
module load python/3.11
virtualenv --no-download ~/ENV
source ~/ENV/bin/activate
pip install --no-index --upgrade pip
```

The `--no-download` flag prevents virtualenv from downloading packages from the internet, using only locally available ones.

### Where to create your virtualenv

- **`$HOME`**: Good default. Persistent, backed up, accessible from all nodes. Create virtualenv on a login node, source it in job scripts.
- **`$SLURM_TMPDIR`**: Best performance. Create inside jobs for maximum I/O speed. Must recreate each job.
- **`$PROJECT`**: Use if sharing with group members.
- **Never `$SCRATCH`**: May get partially deleted by purging.

On **Trillium specifically**, create virtualenvs from a login node in `$HOME` and source them in job scripts (recommended approach).

## Installing packages

Use `--no-index` to install from Alliance pre-built wheels:

```bash
pip install --no-index torch torchvision torchaudio
pip install --no-index numpy scipy pandas scikit-learn
pip install --no-index transformers datasets tokenizers
pip install --no-index deepspeed
```

### Why `--no-index`?

Alliance provides optimized wheels compiled for cluster hardware and CUDA versions. Benefits:
- Pre-compiled with correct CUDA/cuDNN versions
- Optimized for cluster CPUs (AVX-512, etc.)
- Avoids dependency conflicts
- Faster installation (no compilation)

Without `--no-index`, pip may download from PyPI, which can cause CUDA version mismatches or compilation failures.

### Check available wheels

```bash
avail_wheels torch            # See available PyTorch versions
avail_wheels --all            # List all available wheels
avail_wheels "transformers*"  # Search with wildcards
```

### Installing from PyPI (when no wheel exists)

If a package isn't available as a wheel:

```bash
pip install some-rare-package  # Falls back to PyPI
```

This is fine for pure-Python packages. For packages that need compilation, you may need to load additional modules first (e.g., `module load cuda`).

### Installing multiple packages

Install related packages together so pip can resolve dependencies correctly:

```bash
pip install --no-index torch torchvision torchaudio transformers
```

This is better than installing one at a time.

## SciPy stack

Common scientific packages are available as a module:

```bash
module load python/3.11 scipy-stack
```

This provides: NumPy, SciPy, Matplotlib, pandas, IPython, SymPy, and nose. Load it before creating your virtualenv if you need these.

## Why not Conda/Anaconda?

Alliance explicitly asks users to avoid Anaconda. Reasons:
1. **Conda installs its own CUDA/cuDNN** which conflicts with cluster-optimized versions
2. **Conda environments are huge** (many small files) which strains the parallel filesystem
3. **Package conflicts** between Conda and system libraries
4. **Wastes storage quota** by duplicating system libraries

**Migration is easy**: Install the same packages with `pip install --no-index` instead. Skip CUDA/cuDNN (already available via modules).

## Creating virtualenvs inside jobs (best performance)

For single-node jobs, creating the virtualenv on the node's local disk gives the best performance:

```bash
#!/bin/bash
#SBATCH --account=def-someuser
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-03:00

module load python/3.11

# Create virtualenv on fast local disk
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index torch torchvision

python train.py
```

This avoids slow parallel filesystem access when Python imports modules. The trade-off is spending a minute or two on setup each job.

## Requirements files

Save your environment for reproducibility:

```bash
pip freeze > requirements.txt

# In a new env:
pip install --no-index -r requirements.txt
```

## Common issues

### "No matching distribution found"

The package isn't available as a wheel. Try:
```bash
avail_wheels package_name    # Check if it exists
pip install package_name     # Without --no-index, falls back to PyPI
```

### Python version compatibility

Alliance provides wheels for the 3 most recent Python versions. Older Python versions may have dependency issues. When in doubt, use the latest available Python.

### H100 GPUs require torch >= 2.5.1

On Trillium, Fir, Nibi, and other H100 clusters, make sure you install a recent enough PyTorch version:

```bash
avail_wheels torch           # Check latest version
pip install --no-index torch>=2.5.1
```
