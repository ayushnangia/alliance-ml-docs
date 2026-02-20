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

```
$HOME/              # 50 GB, backed up, for code/scripts
$HOME/scratch -> $SCRATCH/   # 20 TB, purged after 60 days
$HOME/projects -> $PROJECT/  # 1 TB+, shared with group
```

### Loading software (modules)

Alliance clusters use Lmod for managing software. Key commands:

```bash
module avail python          # List available Python versions
module spider pytorch        # Search for a package
module load python/3.11      # Load a specific version
module list                  # Show loaded modules
module purge                 # Unload all modules
```

### Standard software environment

Clusters use a standard environment (StdEnv). The default is usually the latest, but you can switch:

```bash
module load StdEnv/2023      # Load specific standard environment
```

### Login node etiquette

Login nodes are shared. You can:
- Edit files, compile code
- Run short tasks (< 10 CPU-minutes, < 4 GB RAM)
- Submit and monitor jobs

Do NOT run training or heavy computation on login nodes. Use `sbatch` to submit jobs.
