# Getting Started with Alliance Canada Clusters

## Creating an account

1. Go to https://ccdb.alliancecan.ca/ and register for an account
2. You need a sponsor (usually your PI/supervisor) who has a Compute Canada Role Identifier (CCRI)
3. Once approved, you can SSH into any national cluster

## Connecting via SSH

```bash
ssh username@trillium.alliancecan.ca
```

Your username is typically something like `ansmith` (not your CCI like `abc-123`, not your email).

### Available cluster login nodes

| Cluster | Login node |
|---------|-----------|
| Trillium | `trillium.alliancecan.ca` |
| Narval | `narval.alliancecan.ca` |
| Cedar | `cedar.alliancecan.ca` |
| Graham | `graham.alliancecan.ca` |
| Fir | `fir.alliancecan.ca` |
| Nibi | `nibi.alliancecan.ca` |
| Rorqual | `rorqual.alliancecan.ca` |
| Niagara | `niagara.alliancecan.ca` |

For GPU-specific login (Trillium): `trillium-gpu.alliancecan.ca`

### SSH keys (recommended)

Generate a key pair and add the public key to your CCDB account:

```bash
ssh-keygen -t ed25519
# Copy contents of ~/.ssh/id_ed25519.pub to CCDB portal
```

### Multifactor authentication (MFA)

MFA is required on all clusters. Set it up at https://ccdb.alliancecan.ca/ under "My Account" -> "Multifactor Authentication". You can use:
- TOTP app (Google Authenticator, Authy, etc.)
- Duo Push

### SSH config for convenience

Add to `~/.ssh/config`:

```
Host trillium
    HostName trillium.alliancecan.ca
    User yourusername

Host narval
    HostName narval.alliancecan.ca
    User yourusername
```

Then connect with just `ssh trillium`.

### X11 forwarding (graphical apps)

```bash
ssh -Y username@trillium.alliancecan.ca
```

Requires an X11 server on your machine (XQuartz on macOS, built-in on Linux).

## First steps after login

### Check your storage quotas

```bash
diskusage_report
```

### Your directory structure

The symlink layout varies by cluster, but the environment variables (`$HOME`, `$SCRATCH`, `$PROJECT`) always work:

```bash
# Most clusters (Narval, Cedar, Graham, Nibi, Killarney, Vulcan, TamIA):
$HOME/                          # 50 GB, backed up, for code/scripts
~/scratch -> /scratch/$USER     # 20 TB, purged after 60 days
~/projects/def-piname/$USER/    # 1 TB+, shared with group

# Trillium & Rorqual (symlinks under $HOME/links/):
$HOME/links/scratch -> $SCRATCH
$HOME/links/projects/def-piname/$USER/

# Fir (symlinks directly in $HOME, singular "project"):
$HOME/scratch -> scratch storage
$HOME/project/def-piname/$USER/
```

**Always use `$SCRATCH`, `$PROJECT`, `$HOME`** in scripts — these env vars work on every cluster regardless of symlink layout.

### Loading software (modules)

Alliance clusters use **Lmod** for managing software. There are two key search commands:

```bash
module avail python          # List currently loadable Python versions
module spider pytorch        # Search ALL modules (even those not yet loadable)
module load python/3.11      # Load a specific version
module list                  # Show loaded modules
module purge                 # Unload all modules
```

**`module avail` vs `module spider`:**

| Command | What it searches | When to use |
|---------|-----------------|-------------|
| `module avail <name>` | Only modules loadable with your current environment | Quick check: "Can I load this right now?" |
| `module spider <name>` | All modules across all environments and compilers | Deep search: "Does this software exist on the cluster?" |

`module spider` is especially useful because many packages only become loadable after you load their dependencies (e.g., you can't see `pytorch` until you load `python`).

```bash
# Find what you need to load first
module spider pytorch/2.5.1
# Output tells you: "You will need to load ... before ..."
```

### Module hierarchy

Modules are organized in a tree:

```
StdEnv (trunk)
  └── Compiler (e.g., gcc/12.3)
        └── MPI (e.g., openmpi/4.1.5)
              └── Software (e.g., some-mpi-package)
```

This means some software only appears after you load the right compiler or MPI module. For ML work, you rarely need MPI modules — most packages are available after loading `python` and optionally `cuda`.

### Standard software environment (StdEnv)

The StdEnv module defines the default compiler, MPI, and CUDA versions. Two versions are relevant:

| Environment | Status | GCC | CUDA | Notes |
|-------------|--------|-----|------|-------|
| **StdEnv/2023** | **Current default** | 12.3 | 12.x | Use this for new projects |
| StdEnv/2020 | Deprecated | 9.3 | 11.x | Still works for CPU-only software; not supported on newer clusters |

```bash
# Explicitly load the current default (usually not needed)
module load StdEnv/2023

# Load the older environment (only if you have legacy dependencies)
module load StdEnv/2020
```

**For ML researchers:** StdEnv/2023 is almost always what you want. It provides CUDA 12 and GCC 12.3, which are required for modern GPU libraries (PyTorch 2.x, TensorFlow 2.x on H100 clusters).

### Login node etiquette

Login nodes are shared. You can:
- Edit files, compile code
- Run short tasks (< 10 CPU-minutes, < 4 GB RAM)
- Submit and monitor jobs

Do NOT run training or heavy computation on login nodes. Use `sbatch` to submit jobs.
