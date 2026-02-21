# Apache Arrow & Data Formats on Alliance Clusters

## Overview

Apache Arrow is a cross-language in-memory columnar data format. On Alliance clusters, it's provided as a **system module** — you don't install it via pip. Arrow is a required dependency for HuggingFace `datasets` and `evaluate` packages.

## Loading Arrow

```bash
# Load Arrow (requires gcc as dependency)
module load gcc arrow

# With a specific version
module load gcc arrow/11.0.0

# With CUDA support
module load gcc arrow/11.0.0 cuda

# Check available versions
module spider arrow

# Check compatible Python versions for a specific Arrow version
module spider arrow/11.0.0
```

## PyArrow (Python bindings)

PyArrow is automatically available when the Arrow module is loaded — no pip install needed.

```bash
module load gcc arrow python/3.11

# Verify it's available
python -c "import pyarrow; print(pyarrow.__version__)"

# Check that pip sees it
pip list | grep pyarrow
```

### Integration with NumPy and Pandas

```python
import pyarrow as pa
import numpy as np
import pandas as pd

# NumPy array → Arrow
arr = pa.array(np.array([1, 2, 3, 4]))

# Pandas DataFrame → Arrow Table
df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
table = pa.Table.from_pandas(df)

# Arrow Table → Pandas (zero-copy when possible)
df_back = table.to_pandas()
```

## Parquet format

Parquet is a columnar storage format that's much more efficient than CSV for large datasets. PyArrow provides full Parquet support.

```python
import pyarrow.parquet as pq

# Read Parquet file
table = pq.read_table("data.parquet")

# Write Parquet file
pq.write_table(table, "output.parquet")

# Read only specific columns (saves memory)
table = pq.read_table("data.parquet", columns=["col1", "col2"])

# Read a directory of Parquet files
dataset = pq.ParquetDataset("/path/to/parquet_dir/")
table = dataset.read()
```

### Why Parquet on clusters

| Format | Read speed | File size | Column selection | Good for clusters? |
|--------|-----------|-----------|-----------------|-------------------|
| CSV | Slow | Large | No (reads all) | No |
| JSON | Slow | Very large | No | No |
| Parquet | Fast | Small (compressed) | Yes (reads only needed columns) | Yes |
| HDF5 | Fast | Medium | Yes | Yes |

Use Parquet when:
- Your dataset has many columns but you only need a few per experiment
- You want compressed storage on `$PROJECT`
- You're working with HuggingFace Datasets (uses Arrow/Parquet internally)

## Arrow as a dependency

Several Python packages on Alliance clusters depend on Arrow. When installing them, you must load the Arrow module first:

```bash
# These packages require `module load gcc arrow` BEFORE pip install:
pip install --no-index datasets       # HuggingFace Datasets
pip install --no-index evaluate       # HuggingFace Evaluate

# And you must load the arrow module every time you use them:
module load python/3.11 gcc arrow
source ~/ENV/bin/activate
python -c "from datasets import load_dataset"  # works
```

If you forget to load the Arrow module, you'll get:
```
ModuleNotFoundError: No module named 'pyarrow'
```

## Data format strategy for ML

### Recommended approach

1. **Store raw data** in Parquet or tar archives on `$PROJECT`
2. **At job start**, copy to `$SLURM_TMPDIR` (fast local SSD)
3. **Load with PyArrow** or HuggingFace Datasets for efficient in-memory access

```bash
#!/bin/bash
#SBATCH --account=def-yourpi
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32000M
#SBATCH --time=0-03:00

module load python/3.11 gcc arrow
source ~/ENV/bin/activate

# Copy dataset to fast local storage
cp $SCRATCH/dataset.parquet $SLURM_TMPDIR/

python train.py --data $SLURM_TMPDIR/dataset.parquet
```

### Converting CSV to Parquet (do once, on a login node)

```python
import pyarrow.csv as pv
import pyarrow.parquet as pq

# Read CSV
table = pv.read_csv("large_dataset.csv")

# Write Parquet (compressed, columnar)
pq.write_table(table, "large_dataset.parquet", compression="snappy")
```

### Large datasets with many small files

The parallel filesystem is slow with many small files. Archive them first:

```bash
# On login node: archive the dataset
cd $SCRATCH
tar cf imagenet.tar imagenet/

# In job script: extract to fast local storage
cp $SCRATCH/imagenet.tar $SLURM_TMPDIR/
cd $SLURM_TMPDIR && tar xf imagenet.tar
```

## CUDA-accelerated Arrow

For GPU-accelerated data processing:

```bash
module load gcc arrow cuda python/3.11
```

This enables GPU-accelerated operations on Arrow data structures, useful for preprocessing pipelines that feed directly into GPU training.
