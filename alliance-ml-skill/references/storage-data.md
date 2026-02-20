# Storage and Data Management for ML Workloads

## Storage tiers overview

| Filesystem | Path | Default Quota | Speed | Backed up | Purged | Best for |
|------------|------|---------------|-------|-----------|--------|----------|
| Home | `$HOME` | 50 GB, 500K files | Medium | Yes | No | Code, scripts, small configs |
| Scratch | `$SCRATCH` | 20 TB, 1M files | Fast | No | 60 days | Temp files, intermediate outputs |
| Project | `$PROJECT` | 1 TB, 500K files | Medium | Yes | No | Shared datasets, final results |
| SLURM_TMPDIR | `$SLURM_TMPDIR` | Varies (up to 1 TB) | Very fast | No | Job end | Training data during a job |
| Nearline | `/nearline` | 2 TB, 5K files | Slow (tape) | Yes | No | Long-term archive |

### Check your usage

```bash
diskusage_report
```

## Choosing storage for ML datasets

### Small datasets (< 10 GB)
Load entirely into memory at the start of training. No special I/O needed.

### Medium datasets (< 100 GB)
Copy to `$SLURM_TMPDIR` at job start. This is local NVMe/SSD storage on the compute node, orders of magnitude faster than shared filesystems.

```bash
#!/bin/bash
#SBATCH ...

# Copy dataset to fast local storage
cp $PROJECT/datasets/imagenet.tar $SLURM_TMPDIR/
cd $SLURM_TMPDIR && tar xf imagenet.tar

python train.py --data-dir $SLURM_TMPDIR/imagenet
```

### Large datasets (> 100 GB)
May need to stay on `$PROJECT` or `$SCRATCH`. Use large sequential reads, not random access to many small files.

## Handling image datasets (many small files)

Parallel filesystems hate millions of small files. This is the #1 performance issue for ML workloads.

### Archive your dataset

```bash
# Create a tar archive (no compression for speed)
cd /project/def-someuser/datasets
tar cf imagenet.tar imagenet/

# Or with compression
tar czf imagenet.tar.gz imagenet/
```

### Extract to local disk in your job

```bash
#!/bin/bash
#SBATCH --gpus-per-node=h100:1
#SBATCH --time=0-12:00

# Extract to fast local storage
tar xf $PROJECT/datasets/imagenet.tar -C $SLURM_TMPDIR/

python train.py --data $SLURM_TMPDIR/imagenet
```

### Use DALI or WebDataset for streaming

For very large datasets, consider:
- **NVIDIA DALI**: GPU-accelerated data loading pipeline
- **WebDataset**: Reads data from tar files sequentially (no extraction needed)

## Transferring data

### Globus (recommended for large transfers)

The fastest way to move data between clusters or from your institution. Set up at https://globus.alliancecan.ca/.

Collection names:
- `alliancecan#trillium`
- `alliancecan#narval`
- `alliancecan#cedar`
- `alliancecan#graham`

### scp/rsync (for smaller transfers)

```bash
# Upload to cluster
scp -r local_data/ username@narval.alliancecan.ca:~/scratch/

# Download from cluster
rsync -avz username@narval.alliancecan.ca:~/scratch/results/ ./results/
```

For Trillium, use the dedicated data transfer nodes:
```bash
scp data.tar username@tri-dm2.scinet.utoronto.ca:~/scratch/
```

## Scratch purging policy

Files on `$SCRATCH` older than **60 days** (not accessed or modified) are automatically purged. This means:
- Don't store anything important only in scratch
- Copy final results to `$PROJECT`
- Checkpoints are fine in scratch as long as you're actively training

## Best practices

1. **Archive before storing**: Use `tar` to bundle directories with many files into single archives.
2. **Copy to `$SLURM_TMPDIR`**: Always copy training data to local disk at job start for best I/O.
3. **Use `$PROJECT` for shared data**: Datasets your lab shares should go in project space.
4. **Don't fill `$HOME`**: Keep code and configs in home. Large files go elsewhere.
5. **Clean up regularly**: Remove old experiments from scratch. Archive completed projects to nearline.
6. **Check file counts**: File count quotas are often hit before space quotas. Use `diskusage_report` to check.

## Quota increases

- **Rapid Access Service (RAS)**: Quick increases up to 40 TB project space. PI writes to support.
- **Resource Allocation Competition (RAC)**: Annual competition for larger allocations. Apply through CCDB.
