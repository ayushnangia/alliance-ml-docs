# Remote Development on Alliance Clusters (Claude Code, Cursor, VSCode, Codex)

## Critical rule

**NEVER run Claude Code, Cursor, VSCode, Codex, or any AI/IDE tool directly on login nodes.**

Login nodes are shared by all users. These tools spawn background processes, file watchers, indexers, and language servers that consume CPU, memory, and I/O — enough to degrade the node for everyone and potentially crash it.

| Cluster | Login node policy |
|---------|-------------------|
| **Fir** | VSCode, Claude, ChatGPT **explicitly banned** on login nodes |
| **tamIA** | VSCode **explicitly banned** on login nodes |
| **All clusters** | **Always use a compute node** — even where not yet banned, these tools hurt everyone on the login node |

**The correct approach:** Always request a compute node first, then connect your tool to that node.

**Never request GPUs for IDE sessions.** Claude Code, Cursor, VSCode, and Codex are CPU-only tools. They don't use GPU compute at all. Requesting a GPU for an IDE session wastes an expensive shared resource that someone else could be using for actual training or inference. Use the minimal resources: 2 CPUs, 4 GB RAM, no GPU. If you need to test GPU code, submit a separate `sbatch` job.

## Internet access on compute nodes

**Claude Code, Cursor (with AI features), and Codex require internet access** to reach their respective APIs. Most Alliance clusters **block internet on compute nodes**, which means these tools will not work without a workaround.

| Cluster | Internet on compute nodes | Claude Code works? |
|---------|--------------------------|-------------------|
| **Fir** | Yes | Yes |
| **Nibi** | Yes | Yes |
| **Vulcan** | Yes | Yes |
| **Killarney** | Yes | Yes |
| **Narval** | No (httpproxy available but blocks `api.anthropic.com`) | No — Squid proxy returns 403 for Anthropic API |
| **Rorqual** | No (httpproxy for eligible groups only) | Unlikely — same proxy infrastructure as Narval |
| **tamIA** | No (httpproxy for eligible groups only) | Unlikely — test with `curl -v https://api.anthropic.com` |
| **Trillium** | No | No |
| **Cedar** | No | No |
| **Graham** | No | No |

**If your cluster has no internet on compute nodes:**
- Use a cluster that does (Fir, Nibi, Vulcan, Killarney)
- On Narval/Rorqual/tamIA: load the httpproxy module before launching Claude Code:
  ```bash
  module load httpproxy
  claude
  ```
  **Check if httpproxy works for you** (run on a compute node):
  ```bash
  module load httpproxy
  env | grep -i proxy                    # should show http_proxy/https_proxy pointing to squid
  curl -s https://api.anthropic.com      # should get a response, not a timeout
  ```
  If the proxy loads and curl succeeds, you're good. Add `module load httpproxy` to your `~/.bashrc` on that cluster so it's automatic.

  If it doesn't load or curl times out, your group may not be eligible — use a cluster with native internet (Fir, Nibi, Vulcan, Killarney) instead.
- Contact [technical support](https://docs.alliancecan.ca/wiki/Technical_support) to request an internet exception if you have a justified need

## Workflow overview

```
Local machine ──SSH──▶ Login node ──salloc──▶ (reservation)
                                   srun ────▶ Compute node
                                                    ▲
Local IDE (Cursor/VSCode/Claude Code) ──SSH─────────┘
                                      (via ProxyJump, Narval/Rorqual only)
```

**Manual steps:**
1. SSH to the login node from a **regular terminal** (not your IDE)
2. Request an interactive compute node with `salloc`
3. Use `srun --pty bash` to get a shell on the compute node
4. Connect your IDE/tool to that compute node (ProxyJump on Narval/Rorqual, or use `cluster-claude`/`cluster-cursor` scripts for all clusters)

**Or use the one-command script** (see [Seamless workflow](#seamless-workflow-local-to-cluster-in-one-command) below).

## Seamless workflow: local to cluster in one command

### `cluster-claude` — allocate a node and launch Claude Code automatically

Save this as `~/.local/bin/cluster-claude` (or anywhere in your `$PATH`):

```bash
#!/usr/bin/env bash
set -euo pipefail

# Usage: cluster-claude <cluster> [account] [salloc-args...]
# Example: cluster-claude narval def-yourpi
# Example: cluster-claude killarney                     # auto-detect if single account
# Example: cluster-claude narval def-yourpi --mem=8G    # extra salloc args
#
# NOTE: This script requests CPU-only resources. Claude Code, Cursor, and
# VSCode do NOT need GPUs. Never waste GPU allocations on IDE sessions.

CLUSTER="${1:?Usage: cluster-claude <cluster> [account] [salloc-args...]}"
shift

# Check if second arg looks like an account (starts with def-, rrg-, aip-, etc.)
ACCOUNT=""
if [[ "${1:-}" =~ ^(def-|rrg-|rpp-|ctb-|aip-) ]]; then
  ACCOUNT="$1"
  shift
fi
EXTRA_ARGS="$*"

# ── Prompt for session duration if not set via TIME env var ──
if [ -z "${TIME:-}" ]; then
  echo ""
  echo "How long do you need? (shorter = starts faster)"
  echo "  1) 1 hour"
  echo "  2) 2 hours"
  echo "  3) 3 hours (default)"
  echo "  4) Custom (enter HH:MM:SS)"
  printf "Choice [3]: "
  read -r TIME_CHOICE
  case "${TIME_CHOICE:-3}" in
    1) TIME="1:00:00" ;;
    2) TIME="2:00:00" ;;
    3|"") TIME="3:00:00" ;;
    4)
      printf "Enter time (HH:MM:SS): "
      read -r TIME
      ;;
    *) TIME="$TIME_CHOICE" ;;  # allow direct HH:MM:SS input
  esac
fi

# Minimal resources for IDE use — no GPU
MEM="${MEM:-4G}"
CPUS="${CPUS:-2}"

# Build salloc command based on cluster and args
ACCOUNT_FLAG=""
[ -n "$ACCOUNT" ] && ACCOUNT_FLAG="--account=$ACCOUNT"

# Cluster-specific defaults
case "$CLUSTER" in
  trillium)
    # Trillium: whole-node scheduling, no --mem or --cpus needed
    # --ntasks=1 prevents default 192-task warning
    if [ -n "$EXTRA_ARGS" ]; then
      SALLOC_CMD="salloc --time=$TIME $ACCOUNT_FLAG --nodes=1 --ntasks=1 $EXTRA_ARGS"
    else
      SALLOC_CMD="salloc --time=$TIME $ACCOUNT_FLAG --nodes=1 --ntasks=1"
    fi
    ;;
  killarney|tamia|vulcan)
    # Killarney/tamIA/Vulcan: must submit from /scratch on killarney
    # These clusters typically use aip- accounts (Vector Institute)
    if [ "$CLUSTER" = "killarney" ]; then
      CD_CMD="cd /scratch/\\\$USER && "
    else
      CD_CMD=""
    fi
    if [ -n "$EXTRA_ARGS" ]; then
      SALLOC_CMD="${CD_CMD}salloc --time=$TIME $ACCOUNT_FLAG $EXTRA_ARGS"
    else
      SALLOC_CMD="${CD_CMD}salloc --time=$TIME $ACCOUNT_FLAG --mem=$MEM --cpus-per-task=$CPUS"
    fi
    ;;
  *)
    if [ -n "$EXTRA_ARGS" ]; then
      SALLOC_CMD="salloc --time=$TIME $ACCOUNT_FLAG $EXTRA_ARGS"
    else
      SALLOC_CMD="salloc --time=$TIME $ACCOUNT_FLAG --mem=$MEM --cpus-per-task=$CPUS"
    fi
    ;;
esac

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  cluster-claude: $CLUSTER"
if [ -n "$ACCOUNT" ]; then
  echo "║  Account: $ACCOUNT"
else
  echo "║  Account: (auto — single account on cluster)"
fi
echo "║  Time:    $TIME"
echo "║  Mem:     $MEM   CPUs: $CPUS   GPU: none"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "→ Requesting compute node on $CLUSTER..."
echo "  (Approve Duo MFA on your phone if prompted)"
echo "  (Tip: run 'ssh $CLUSTER' first to establish ControlMaster — skip Duo next time)"
echo ""

# SSH to login node → salloc → srun on compute node → launch claude
# srun is required: salloc alone runs on the login node, srun runs on the compute node
# --pty gives claude a proper interactive terminal
# This works on ALL clusters (no ProxyJump needed)
ssh -t "$CLUSTER" "bash -l -c '
  $SALLOC_CMD srun --pty bash -c \"
    NODE=\\\$(hostname)
    echo \\\"\\\"
    echo \\\"════════════════════════════════════════\\\"
    echo \\\"  Compute node: \\\$NODE\\\"
    echo \\\"  Job ID:       \\\$SLURM_JOB_ID\\\"
    echo \\\"  TMPDIR:       \\\$SLURM_TMPDIR\\\"
    echo \\\"════════════════════════════════════════\\\"
    echo \\\"\\\"
    cd ~ && claude
  \"
'"
```

Make it executable: `chmod +x ~/.local/bin/cluster-claude`

**Usage:**
```bash
# Interactive (prompts for time):
cluster-claude narval def-yourpi

# Skip the prompt with TIME env var:
TIME=2:00:00 cluster-claude narval def-yourpi

# Auto-detect account (if you only have one):
cluster-claude killarney

# Extra salloc args (e.g., more memory for large codebases):
cluster-claude narval def-yourpi --mem=8G
```

> **Do NOT request GPUs for IDE sessions.** Claude Code, Cursor, and VSCode are CPU-only tools — they don't use GPU compute. Requesting a GPU wastes an expensive shared resource that could be used for actual training. If you need to test GPU code, submit a separate `sbatch` job.

**What happens:**
1. Prompts you for session duration (shorter jobs start faster)
2. SSHs to the login node (you approve Duo once)
3. Runs `salloc` to reserve a CPU-only compute node (waits for allocation)
4. Uses `srun --pty` to launch a shell on the compute node (not the login node)
5. Runs Claude Code inside that shell
6. When you exit Claude Code, the allocation is released

**Finding your account name:** If you don't know your account, try running `salloc` without `--account` — if you have only one, it will be used automatically. If you have multiple, the error message will list them. You can also check on any cluster with:
```bash
sacctmgr show associations where user=$USER format=account%30
```

**Which account to use:**
| Cluster | Typical account prefix | Notes |
|---------|----------------------|-------|
| Killarney, tamIA, Vulcan | `aip-` | Vector Institute allocations |
| Narval, Cedar, Graham, Trillium, Fir, others | `def-`, `rrg-` | Standard Alliance allocations |

### `cluster-cursor` — allocate a node and print Cursor/VSCode connection info

Save as `~/.local/bin/cluster-cursor`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Usage: cluster-cursor <cluster> [account] [salloc-args...]
# Example: cluster-cursor narval def-yourpi
# Example: cluster-cursor killarney                     # auto-detect if single account
#
# NOTE: This script requests CPU-only resources. Cursor and VSCode
# do NOT need GPUs. Never waste GPU allocations on IDE sessions.

CLUSTER="${1:?Usage: cluster-cursor <cluster> [account] [salloc-args...]}"
shift

# Check if next arg looks like an account (starts with def-, rrg-, aip-, etc.)
ACCOUNT=""
if [[ "${1:-}" =~ ^(def-|rrg-|rpp-|ctb-|aip-) ]]; then
  ACCOUNT="$1"
  shift
fi
EXTRA_ARGS="$*"

# ── Prompt for session duration if not set via TIME env var ──
if [ -z "${TIME:-}" ]; then
  echo ""
  echo "How long do you need? (shorter = starts faster)"
  echo "  1) 1 hour"
  echo "  2) 2 hours"
  echo "  3) 3 hours (default)"
  echo "  4) Custom (enter HH:MM:SS)"
  printf "Choice [3]: "
  read -r TIME_CHOICE
  case "${TIME_CHOICE:-3}" in
    1) TIME="1:00:00" ;;
    2) TIME="2:00:00" ;;
    3|"") TIME="3:00:00" ;;
    4)
      printf "Enter time (HH:MM:SS): "
      read -r TIME
      ;;
    *) TIME="$TIME_CHOICE" ;;
  esac
fi

# Minimal resources for IDE use — no GPU
MEM="${MEM:-4G}"
CPUS="${CPUS:-2}"

# Build salloc command based on cluster and args
ACCOUNT_FLAG=""
[ -n "$ACCOUNT" ] && ACCOUNT_FLAG="--account=$ACCOUNT"

case "$CLUSTER" in
  trillium)
    if [ -n "$EXTRA_ARGS" ]; then
      SALLOC_CMD="salloc --time=$TIME $ACCOUNT_FLAG --nodes=1 --ntasks=1 $EXTRA_ARGS"
    else
      SALLOC_CMD="salloc --time=$TIME $ACCOUNT_FLAG --nodes=1 --ntasks=1"
    fi
    ;;
  killarney|tamia|vulcan)
    if [ "$CLUSTER" = "killarney" ]; then
      CD_CMD="cd /scratch/\\\$USER && "
    else
      CD_CMD=""
    fi
    if [ -n "$EXTRA_ARGS" ]; then
      SALLOC_CMD="${CD_CMD}salloc --time=$TIME $ACCOUNT_FLAG $EXTRA_ARGS"
    else
      SALLOC_CMD="${CD_CMD}salloc --time=$TIME $ACCOUNT_FLAG --mem=$MEM --cpus-per-task=$CPUS"
    fi
    ;;
  *)
    if [ -n "$EXTRA_ARGS" ]; then
      SALLOC_CMD="salloc --time=$TIME $ACCOUNT_FLAG $EXTRA_ARGS"
    else
      SALLOC_CMD="salloc --time=$TIME $ACCOUNT_FLAG --mem=$MEM --cpus-per-task=$CPUS"
    fi
    ;;
esac

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  cluster-cursor: $CLUSTER"
if [ -n "$ACCOUNT" ]; then
  echo "║  Account: $ACCOUNT"
else
  echo "║  Account: (auto — single account on cluster)"
fi
echo "║  Time:    $TIME"
echo "║  Mem:     $MEM   CPUs: $CPUS   GPU: none"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "→ Requesting compute node on $CLUSTER..."
echo "  (Approve Duo MFA on your phone if prompted)"
echo ""

# srun is required: salloc alone runs on the login node, srun runs on the compute node
ssh -t "$CLUSTER" "bash -l -c '
  $SALLOC_CMD srun --pty bash -c \"
    NODE=\\\$(hostname)
    env | grep SLURM_ | sed \\\"s/^\(.*\)=\(.*\)$/export \1=\\\\\\\"\2\\\\\\\"/g\\\" > ~/slurm_var.sh
    echo \\\"\\\"
    echo \\\"╔══════════════════════════════════════════════╗\\\"
    echo \\\"║  Compute node ready!                         \\\"
    echo \\\"╠══════════════════════════════════════════════╣\\\"
    echo \\\"║  Node:     \\\$NODE                             \\\"
    echo \\\"║  Job ID:   \\\$SLURM_JOB_ID                    \\\"
    echo \\\"║  TMPDIR:   \\\$SLURM_TMPDIR                    \\\"
    echo \\\"╠══════════════════════════════════════════════╣\\\"
    echo \\\"║  Connect your IDE:                            \\\"
    echo \\\"║  Cursor/VSCode: Remote-SSH → \\\$NODE           \\\"
    echo \\\"║  Claude Code:   ssh -t \\\$NODE claude           \\\"
    echo \\\"║  Codex:         ssh -t \\\$NODE codex            \\\"
    echo \\\"╠══════════════════════════════════════════════╣\\\"
    echo \\\"║  In IDE terminal run: source ~/slurm_var.sh   \\\"
    echo \\\"║  Press Ctrl+C or exit to release the node     \\\"
    echo \\\"╚══════════════════════════════════════════════╝\\\"
    echo \\\"\\\"
    echo \\\"Keeping allocation alive... (Ctrl+C to release)\\\"
    sleep infinity
  \"
'"
```

**Usage:**
```bash
# Interactive (prompts for time):
cluster-cursor narval def-yourpi

# Skip the prompt:
TIME=2:00:00 cluster-cursor killarney aip-yourpi

# Auto-detect account:
cluster-cursor narval
```

### Claude Code Desktop SSH (most seamless for repeat use)

If you use the Claude Code Desktop app, you can save compute nodes as SSH hosts:

1. Run `cluster-cursor` to get a compute node
2. In Claude Code Desktop → **New Session** → **SSH**
3. Enter: `your_username@<node-name>` (e.g., `your_username@nc10305`)
4. It will ProxyJump through the login node automatically (if configured in `~/.ssh/config`)

The Desktop app runs Claude on the compute node with full access to cluster files.

### Keeping your project in sync (local ↔ cluster)

For seamless code continuity between local Claude Code and cluster Claude Code:

```bash
# Local machine: push your work
cd ~/my-project
git add -A && git commit -m "wip" && git push

# On cluster (or the cluster-claude script does this automatically):
cd ~/my-project
git pull
claude    # picks up CLAUDE.md, .claude/ settings, and project context
```

**What carries over automatically:**
- `CLAUDE.md` — project instructions, conventions, context
- `.claude/` settings — project-specific Claude Code config
- Git history — Claude can read commits, diffs, blame
- Code context — Claude reads the codebase fresh each session

**What does NOT carry over:**
- Conversation history (each session is fresh)
- Auto-memory (`~/.claude/projects/`) is per-machine
- Running tasks or background processes

**Tip:** Keep project-critical context in `CLAUDE.md` rather than relying on conversation memory. This way, whether you're working locally or on the cluster, Claude always knows the project context.

## Important: ProxyJump only works on some clusters

Not all clusters allow external SSH to compute nodes. Tested (March 2026):

| Cluster | ProxyJump from local to compute? | Compute node auth |
|---------|--------------------------------|-------------------|
| **Narval** | **Yes** | publickey (via `~/.ssh/authorized_keys`) |
| **Rorqual** | **Likely yes** (same pattern as Narval per Alliance docs) | publickey |
| **Killarney** | **No** | internal password/hostbased only |
| **Trillium** | **No** | hostbased only |
| **tamIA** | **Unknown** — test with `ssh <compute-node> hostname` | — |
| **Others** | **Unknown** — test per cluster | — |

**What this means:**
- **Claude Code / Codex (terminal):** Works on ALL clusters via `cluster-claude` script (runs through one SSH session, no ProxyJump needed)
- **Cursor / VSCode (ProxyJump):** Only works on Narval and Rorqual. For other clusters, use `salloc` from login node then run `code tunnel` from the compute node, or use JupyterLab code-server

## Step 1: Add your SSH key to the cluster's authorized_keys (Narval/Rorqual only)

**This is required for ProxyJump to compute nodes on clusters that support it.** CCDB SSH key management only handles login node authentication. To SSH directly to compute nodes (via ProxyJump), your public key must also be in `~/.ssh/authorized_keys` on the cluster's shared filesystem.

Run this **once per cluster** (ControlMaster means no extra Duo after first login):

```bash
# First, SSH to the cluster (approve Duo):
ssh narval

# On the cluster, add your public key:
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Replace `YOUR_PUBLIC_KEY_HERE` with the contents of your local `~/.ssh/your_key.pub` (e.g., `cat ~/.ssh/computecanada.pub`).

Since clusters share the same home directory across login and compute nodes, this one addition lets you SSH to any compute node on that cluster.

**Note:** If you already added your key to CCDB, it handles login node auth. The `authorized_keys` file is separate and needed specifically for compute node access via ProxyJump.

**Is this secure?** Yes. Your `~/.ssh/` directory is protected by POSIX permissions (`700`/`600`) — only you can read or modify it. The same public key is already trusted by the login node via CCDB; you're extending that same trust to compute nodes within the cluster's internal network. Compute nodes are not internet-facing — they're only reachable via the login node (which already authenticated you with MFA). This is standard SSH practice.

## Step 2: Configure SSH ProxyJump for compute nodes

Compute nodes are not directly reachable from the internet. You jump through the login node. Add these to your **local** `~/.ssh/config`.

**Important:** ProxyJump to compute nodes requires `~/.ssh/authorized_keys` setup (Step 1) and only works on clusters where compute nodes accept publickey auth. See the [ProxyJump compatibility table](#important-proxyjump-only-works-on-some-clusters) above.

**Verified compute node hostname prefixes** (from `sinfo` on each cluster):

```
# ══════════════════════════════════════════════════════
# VERIFIED: ProxyJump works on these clusters
# ══════════════════════════════════════════════════════

# ── Narval compute nodes ──
# CPU: nc*, GPU: ng*, Large-mem: nl*
Host nc* ng* nl*
  ProxyJump narval
  User your_username
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  LogLevel ERROR

# ── Rorqual compute nodes ──
# CPU: rc*, GPU: rg*, Large-mem: rl*
Host rc* rg* rl*
  ProxyJump rorqual
  User your_username
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  LogLevel ERROR

# ══════════════════════════════════════════════════════
# OTHER CLUSTERS: ProxyJump may not work (compute nodes
# use internal auth). Keep these for convenience — they
# work if you are already on the login node doing
# `ssh <compute-node>`, and they won't interfere if
# ProxyJump is rejected.
# For these clusters, use cluster-claude/cluster-cursor
# (which runs through one SSH session, no ProxyJump).
# ══════════════════════════════════════════════════════

# ── Killarney compute nodes ──
# GPU (L40S/H100): kn*
Host kn*
  ProxyJump killarney
  User your_username
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  LogLevel ERROR

# ── Trillium compute nodes (SciNet) ──
# Main compute: tri*, Neptune partition: nept*
Host tri0* tri1* nept*
  ProxyJump trillium
  User your_username
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  LogLevel ERROR

# ── Cedar compute nodes ──
# Pattern: cdr*
Host cdr*
  ProxyJump cedar
  User your_username
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  LogLevel ERROR

# ── Vulcan compute nodes ──
# CPU: compute*, GPU: rack*
Host compute? compute?? rack*
  ProxyJump vulcan
  User your_username
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  LogLevel ERROR

# ── tamIA compute nodes ──
# CPU: tc*, GPU: tg*
Host tc* tg*
  ProxyJump tamia
  User your_username
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  LogLevel ERROR

# ── Fir compute nodes ──
# Verify prefix with: sinfo -N -h -o "%N" on fir
Host fg* fn* fl*
  ProxyJump fir
  User your_username
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
  LogLevel ERROR
```

Replace `your_username` with your Alliance username.

**Why `StrictHostKeyChecking no` for compute nodes?** Compute nodes are ephemeral — their host keys change and they're internal to the cluster. Since you're already authenticated through the login node (ProxyJump), the compute node connection is within the trusted cluster network. The `LogLevel ERROR` suppresses the "Warning: Permanently added..." noise.

### SSH connection multiplexing (officially recommended by Alliance)

Alliance Canada's MFA documentation explicitly recommends ControlMaster to reduce Duo prompts. Add this to `~/.ssh/config`:

```
# IMPORTANT: Include both FQDNs AND your SSH aliases (e.g., narval, trillium).
# SSH matches on the command-line hostname, NOT the resolved HostName.
# So "ssh narval" won't match "*.alliancecan.ca" — you need the alias listed too.
Host narval cedar graham beluga fir killarney trillium trillium-gpu vulcan tamia *.alliancecan.ca *.computecanada.ca
  ControlMaster auto
  ControlPath ~/.ssh/cm-%r@%h:%p
  ControlPersist 10m
  ServerAliveInterval 60
```

From the [Alliance MFA docs](https://docs.alliancecan.ca/wiki/Multifactor_authentication#Configuring_your_SSH_client_with_ControlMaster): *"This setting allows a first SSH session to ask for the first and second factors, but subsequent SSH connections on the same device will reuse the connection of the first session (without asking for authentication), even up to 10 minutes after that first session was disconnected."*

This means: SSH once (approve Duo), then all subsequent SSH commands reuse that connection — including `cluster-claude`, ProxyJump to compute nodes, etc. — with no additional Duo prompts.

The `ServerAliveInterval 60` prevents idle disconnections by sending a keepalive every 60 seconds.

**Note on automation nodes:** For fully unattended/automated workflows (CI/CD, cron jobs, scripts that run without a human), Alliance provides dedicated **automation nodes** (`robot.cluster.alliancecan.ca`) that skip MFA entirely but require special constrained SSH keys. See [Automation in the context of MFA](https://docs.alliancecan.ca/wiki/Automation_in_the_context_of_multifactor_authentication). This is NOT needed for interactive development — ControlMaster is sufficient.

## Step 3: Request a compute node

SSH to the login node from a **regular terminal**:

```bash
ssh narval   # or trillium, fir, killarney, etc.
```

Then request an interactive **CPU-only** session (no GPU needed for IDE work):

```bash
# ── General-purpose clusters (Narval, Cedar, Fir, Vulcan, tamIA) ──
salloc --time=3:00:00 --mem=4G --cpus-per-task=2 --account=def-yourpi

# ── Trillium (whole-node scheduling — no --mem or --cpus needed) ──
salloc --time=3:00:00 --nodes=1 --ntasks=1 --account=def-yourpi

# ── Killarney (Vector Institute — must submit from /scratch) ──
cd /scratch/$USER
salloc --time=3:00:00 --mem=4G --cpus-per-task=2 --account=aip-yourpi
```

> **Remember: no GPUs for IDE sessions.** 4 GB RAM and 2 CPUs is plenty for Claude Code, Cursor, or VSCode. Request only the time you actually need — shorter jobs start faster.

Once granted, note the compute node hostname:

```
salloc: Granted job allocation 1234567
salloc: Nodes nc10305 allocated
```

**Important:** `salloc` reserves the node but leaves you on the login node. To actually run on the compute node, use `srun`:

```bash
srun --pty bash       # get a shell on the compute node
```

You can also check the assigned node:

```bash
echo $SLURM_NODELIST   # from the login node (after salloc)
hostname               # from the compute node (after srun)
```

**Tip:** Interactive jobs of 3 hours or less start quickly — clusters have dedicated test nodes for short jobs. Longer interactive jobs may queue for hours.

## Step 4: Connect your tool

### Claude Code

Claude Code runs in the terminal — no extensions or remote servers needed.

**Option A — One-command script (works on ALL clusters, recommended):**
```bash
cluster-claude narval def-yourpi
cluster-claude killarney aip-yourpi
cluster-claude trillium def-yourpi
```

**Option B — ProxyJump SSH (Narval/Rorqual only):**
```bash
# From your local terminal (after salloc has given you a compute node):
ssh nc10305                    # ProxyJump routes through narval login node
cd ~/my-project
source ~/ENV/bin/activate      # if you need your Python env
claude                         # start Claude Code
```

**Option C — Use the sbatch helper script (see below) for long sessions:**
```bash
sbatch remote-dev.sh
# Wait for job to start...
cat remote-dev-*.out           # get the node name
ssh -t <node-name> "cd ~/my-project && claude"   # ProxyJump (Narval/Rorqual)
```

### Cursor / VSCode

**ProxyJump method (Narval, Rorqual only):** Connect directly to the compute node from your IDE.

**For other clusters (Killarney, Trillium, etc.):** Use the `cluster-cursor` script which runs everything through one SSH session, or use the `code tunnel` approach:

```bash
# After salloc, get onto the compute node:
srun --pty bash
# Then start the tunnel:
code tunnel --accept-server-license-terms
# This prints a URL — open it in your browser or connect from Cursor/VSCode
```

#### Required: One-time local settings

In Cursor/VSCode, press `Cmd+Shift+P` → **Preferences: Open User Settings (JSON)** and add:

```json
{
  "files.watcherExclude": {
    "**/.git/**": true,
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/build/**": true
  },
  "search.exclude": {
    "**/.git/objects/**": true,
    "**/.git/subtree-cache/**": true,
    "**/node_modules/**": true
  },
  "search.maxThreads": 2,
  "search.ripgrep.maxThreads": 2,
  "search.useIgnoreFiles": true,
  "remote.extensionKind": {
    "*": ["ui"],
    "ms-python.python": ["ui"]
  },
  "remote.defaultExtensionsIfInstalledLocally": [
    "GitHub.vscode-pull-request-github"
  ],
  "remote.SSH.showLoginTerminal": false,
  "remote.SSH.enableDynamicForwarding": false,
  "remote.SSH.enableServerAutoShutdown": 30,
  "workbench.startupEditor": "none"
}
```

#### Required: One-time remote setup (run once per cluster)

SSH to each cluster login node and run:

```bash
mkdir -p ~/.vscode-server/data/Machine/
cat > ~/.vscode-server/data/Machine/settings.json << 'SETTINGS'
{
  "files.watcherExclude": {
    "**/.git/**": true,
    "**/node_modules/**": true,
    "**/dist/**": true,
    "**/build/**": true,
    "/**": true
  },
  "search.exclude": {
    "**/.git/objects/**": true,
    "**/.git/subtree-cache/**": true,
    "**/node_modules/**": true,
    "/**": true
  },
  "search.followSymlinks": false,
  "search.maxThreads": 2,
  "search.ripgrep.maxThreads": 2,
  "search.useIgnoreFiles": true,
  "search.searchOnType": false,
  "extensions.autoCheckUpdates": false,
  "extensions.autoUpdate": false,
  "update.mode": "none",
  "remote.extensionKind": { "*": ["ui"], "ms-python.python": ["ui"] },
  "chat.agent.enabled": false,
  "github.copilot.enable": { "*": false },
  "telemetry.enableTelemetry": false,
  "telemetry.enableCrashReporter": false,
  "telemetry.telemetryLevel": "off",
  "telemetry.feedback.enabled": false,
  "git.autofetch": false,
  "git.enableStatusBarSync": false,
  "remote.SSH.showLoginTerminal": false,
  "remote.SSH.enableDynamicForwarding": false,
  "remote.SSH.enableServerAutoShutdown": 30,
  "workbench.startupEditor": "none"
}
SETTINGS
```

**Why these settings matter:** They disable file watchers scanning the entire parallel filesystem, turn off telemetry/auto-updates/Copilot background processes, and limit search threads. Without these, VSCode/Cursor will thrash the shared filesystem and use excessive CPU on the node.

#### Connecting

1. Start your `salloc` job and note the compute node name (e.g., `kn003`)
2. In Cursor/VSCode: `Cmd+Shift+P` → **Remote-SSH: Connect to Host...**
3. Enter the compute node name: `kn003`
4. If prompted for OS type, select **Linux**
5. Open your project folder (e.g., `~/my-project`)

You're now running on a compute node — run and debug freely.

#### When you're done

1. `Cmd+Shift+P` → **Remote-SSH: Kill VS Code Server on Host...** → select the compute node
2. **File** → **Close Remote Connection**
3. In your terminal, `exit` from the salloc session

**Always kill the VS Code server** — it keeps running otherwise and wastes your allocation.

### Codex CLI

Codex (OpenAI's CLI) works similarly to Claude Code — it runs in the terminal:

```bash
# Option A — One-command script (works on ALL clusters):
# (same as cluster-claude but replace 'claude' with 'codex' in the script)

# Option B — ProxyJump SSH (Narval/Rorqual only):
ssh nc10305                    # ProxyJump routes through login node
cd ~/my-project
source ~/ENV/bin/activate
codex                          # start Codex

# Option C — One-liner (Narval/Rorqual only):
ssh -t nc10305 "cd ~/my-project && codex"
```

## Helper scripts

### `remote-dev.sh` — Long CPU-only development session via sbatch

For IDE sessions longer than 3 hours (where `salloc` might queue for a long time), submit a batch job. **No GPU** — IDE tools don't need one:

```bash
#!/bin/bash
#SBATCH --time=8:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=2
#SBATCH --account=def-yourpi
#SBATCH --output=remote-dev-%j.out

NODE=$(hostname)
echo "============================================"
echo "  Remote development session ready"
echo "============================================"
echo "  Compute node:  $NODE"
echo "  SSH command:    ssh $NODE"
echo "  Job ID:         $SLURM_JOB_ID"
echo "  SLURM_TMPDIR:   $SLURM_TMPDIR"
echo "  Cancel:         scancel $SLURM_JOB_ID"
echo "============================================"
echo ""
echo "  From your local machine:"
echo "    ssh $NODE                              # terminal access"
echo "    ssh -t $NODE 'cd ~/project && claude'  # Claude Code"
echo "    Cursor/VSCode: Remote-SSH → $NODE      # IDE"
echo "============================================"

# Save SLURM vars so IDE terminals can source them
env | grep SLURM_ | sed 's/^\(.*\)=\(.*\)$/export \1="\2"/g' > ~/slurm_var.sh

# Keep the job alive until cancelled or time runs out
sleep infinity
```

Usage:
```bash
sbatch remote-dev.sh
# Wait for job to start...
cat remote-dev-*.out     # get connection info
ssh <node-name>          # connect from local machine
# When done:
scancel <job-id>
```

### `remote-dev-gpu.sh` — GPU session (for training with IDE access)

Use this **only** when you need a GPU for actual training/inference and want to SSH in to monitor or debug. The GPU is for your training script, not for the IDE itself:

```bash
#!/bin/bash
#SBATCH --time=4:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=8
#SBATCH --gpus-per-node=1
#SBATCH --account=def-yourpi
#SBATCH --output=remote-dev-gpu-%j.out

NODE=$(hostname)
echo "============================================"
echo "  GPU development session ready"
echo "============================================"
echo "  Compute node:  $NODE"
echo "  SSH command:    ssh $NODE"
echo "  Job ID:         $SLURM_JOB_ID"
echo "  GPU:            $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'checking...')"
echo "  SLURM_TMPDIR:   $SLURM_TMPDIR"
echo "  Cancel:         scancel $SLURM_JOB_ID"
echo "============================================"
echo ""
echo "  From your local machine:"
echo "    ssh $NODE"
echo "    ssh -t $NODE 'cd ~/project && claude'"
echo "    Cursor/VSCode: Remote-SSH → $NODE"
echo "============================================"

env | grep SLURM_ | sed 's/^\(.*\)=\(.*\)$/export \1="\2"/g' > ~/slurm_var.sh
sleep infinity
```

## Vector Institute Killarney workflow

For Vector Institute users on Killarney, the [vec-playbook](https://github.com/VectorInstitute/vec-playbook/tree/main/getting-started/slurm-examples/jupyter-server) provides a Jupyter server example that demonstrates the sbatch → get node → connect pattern.

### The Jupyter server job script

```bash
#!/bin/bash
#SBATCH --ntasks-per-gpu=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:l40s:1
#SBATCH --time=2:00:00
#SBATCH --output=jupyter-server.%j.out

source jupyter-server-venv/bin/activate
jupyter notebook --ip $(hostname --fqdn) --no-browser
```

### Setup and connection

```bash
# One-time setup on Killarney:
python3 -m venv jupyter-server-venv
source jupyter-server-venv/bin/activate
pip install jupyter

# Submit the job:
sbatch jupyter-server.sh

# Wait for it to start, then get the compute node:
cat jupyter-server.*.out | grep vectorinstitute
# Output: http://kn055.paice.vectorinstitute.ai:8888/tree?token=...

# From your LOCAL machine, create an SSH tunnel:
ssh username@killarney.alliancecan.ca -L 8888:kn055:8888

# Open in browser:
cat jupyter-server.*.out | grep "127.0.0.1"
# Copy the URL and open in your browser
```

### Using the same node for IDE access

Once you have the compute node name (`kn055`), you can also connect your IDE:

```bash
# Claude Code:
ssh -t kn055 "cd ~/my-project && claude"

# Cursor/VSCode:
# Remote-SSH: Connect to Host → kn055
```

The key insight: **any sbatch job that keeps a node alive gives you a compute node you can SSH into** — whether it's Jupyter, `sleep infinity`, or your actual training script.

## Saving SLURM environment variables for your IDE

When you connect an IDE to a compute node via Remote-SSH, SLURM environment variables (`$SLURM_TMPDIR`, `$SLURM_JOB_ID`, etc.) won't be in the IDE's terminal sessions. The helper scripts above automatically save them, but you can also do it manually:

```bash
# On the compute node (in your salloc session):
env | grep SLURM_ | sed 's/^\(.*\)=\(.*\)$/export \1="\2"/g' > ~/slurm_var.sh

# In your IDE's terminal on the compute node:
source ~/slurm_var.sh
echo $SLURM_TMPDIR   # should now be set
```

This matters because `$SLURM_TMPDIR` is fast node-local storage — ideal for datasets during training.

## Verified compute node hostnames

Verified via `sinfo -N` on each cluster (March 2026):

| Cluster | CPU nodes | GPU nodes | Login node hostname |
|---------|-----------|-----------|-------------------|
| **Narval** | `nc*` (e.g., `nc10101`) | `ng*` | `narval3` |
| **Cedar** | `cdr*` | `cdr*` | `cedar*` |
| **Trillium** | `tri0*` (e.g., `tri0005`) | `nept*` (e.g., `nept0002`) | `tri-login*` |
| **Killarney** | — | `kn*` (e.g., `kn001`) | `klogin01` |
| **Vulcan** | `compute*` (e.g., `compute1`) | `rack*` (e.g., `rack01-01`) | `vulcan2` |
| **tamIA** | `tc*` (e.g., `tc10701`) | `tg*` (e.g., `tg10501`) | `tamia2` |
| **Fir** | verify with `sinfo -N` | verify with `sinfo -N` | `fir*` |
| **Rorqual** | `rc*` | `rg*` | `rorqual*` |

## Troubleshooting

**"Permission denied" when connecting to compute node:**
- Verify your `salloc` job is still running: `sq`
- Check ProxyJump config has the correct username
- Compute nodes are only accessible while your job allocation is active

**IDE is slow or unresponsive:**
- Ensure remote machine settings are applied (file watchers disabled)
- Open only the specific project folder, not `~` or `/`
- Disable extensions you don't need on the remote side
- Use `$SLURM_TMPDIR` for data-heavy work (fast local SSD)

**Duo MFA prompts every time:**
- Enable SSH connection multiplexing (ControlMaster) as shown above
- Run `ssh-add ~/.ssh/your_key` to keep your key in the agent

**Connection drops after a while:**
- The `ServerAliveInterval 60` in your SSH config prevents idle disconnections
- Your salloc/sbatch job may have hit its time limit — check with `sq`
- For long sessions, use the `remote-dev.sh` sbatch script instead of `salloc`

**"command not found: claude" on compute node:**
- Claude Code needs to be installed in your environment on the cluster
- Either install it in your virtualenv or ensure it's in your `$PATH`
- You may need `module load nodejs` first, then `npm install -g @anthropic-ai/claude-code`

**SLURM variables not available in IDE terminal:**
- Source the saved vars: `source ~/slurm_var.sh`
- The helper scripts above auto-save these, or save them manually before connecting your IDE
