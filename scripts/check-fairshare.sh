#!/usr/bin/env zsh
# Check fairshare across all Alliance clusters
# Usage: ./check-fairshare.sh
#
# Configure CCDB_USER and CLUSTER_MAP below with your username and accounts.
# Requires active SSH ControlMaster connections or will trigger Duo for each cluster.
# Tip: ssh into each cluster first to establish multiplexed connections.

# ==================== CONFIGURATION ====================
# Set your Alliance username
CCDB_USER="${CCDB_USER:-$(whoami)}"

# Cluster -> Slurm accounts (comma-separated)
# Regular clusters append _cpu/_gpu to the account name automatically.
# Trillium uses unsuffixed accounts. PAICE clusters use aip- prefix.
# Run: sacctmgr show associations where user=$CCDB_USER format=Account,Cluster -P
# to discover your accounts, then fill in below.
typeset -A CLUSTER_MAP
CLUSTER_MAP=(
  # fir       "def-piname_cpu,def-piname_gpu"
  # narval    "def-piname_cpu,def-piname_gpu"
  # nibi      "def-piname_cpu,def-piname_gpu"
  # rorqual   "def-piname_cpu,def-piname_gpu"
  # trillium  "def-piname"
  # vulcan    "aip-piname"
  # tamia     "aip-piname"
  # killarney "aip-piname"
)

# List of clusters to query (must match keys in CLUSTER_MAP)
CLUSTERS=()

# Auto-populate CLUSTERS from CLUSTER_MAP keys
if [[ ${#CLUSTERS[@]} -eq 0 ]]; then
  CLUSTERS=(${(k)CLUSTER_MAP})
fi
# ==================== END CONFIGURATION ================

if [[ ${#CLUSTER_MAP} -eq 0 ]]; then
  echo "ERROR: No clusters configured."
  echo "Edit CLUSTER_MAP in this script with your accounts, or run:"
  echo "  sacctmgr show associations where user=\$USER format=Account,Cluster -P"
  echo "on any cluster to discover your accounts."
  exit 1
fi

TMPDIR_FS=$(mktemp -d)
trap "rm -rf $TMPDIR_FS" EXIT

# Notes per cluster
typeset -A NOTES
NOTES=(
  trillium  "whole-node, 24h max"
  fir       "per-core, 7d max, internet"
  narval    "per-core, 7d max, A100-40GB"
  nibi      "per-core, 7d max"
  rorqual   "per-core, 7d max"
  vulcan    "PAICE, L40S"
  tamia     "PAICE, whole-node H100/H200"
  killarney "PAICE, H100/L40S"
)

# --- Fetch all clusters in parallel ---
echo ""
echo "Fetching fairshare from ${#CLUSTERS[@]} clusters..."

for cluster in $CLUSTERS; do
  (
    accounts=(${(s:,:)CLUSTER_MAP[$cluster]})
    cmd=""
    for acct in $accounts; do
      cmd+="echo MARKER:${acct}; sshare -lnP -A ${acct} -u ${CCDB_USER} 2>/dev/null; "
    done

    # Killarney needs login shell for Slurm to be in PATH
    if [[ "$cluster" == "killarney" ]]; then
      result=$(ssh -o ConnectTimeout=10 -o BatchMode=yes "$cluster" "bash -l -c '$cmd'" 2>/dev/null)
    else
      result=$(ssh -o ConnectTimeout=10 -o BatchMode=yes "$cluster" "$cmd" 2>/dev/null)
    fi

    if [[ $? -eq 0 && -n "$result" ]]; then
      echo "$result" > "$TMPDIR_FS/${cluster}.raw"
      echo "  OK $cluster"
    else
      echo "  FAIL $cluster"
      touch "$TMPDIR_FS/${cluster}.fail"
    fi
  ) &
done
wait
echo ""

# --- Parse raw files into a single TSV ---
# Format: cluster \t account \t type \t proj_shares \t proj_levelfs \t user_levelfs

for cluster in $CLUSTERS; do
  [[ -f "$TMPDIR_FS/${cluster}.fail" ]] && echo "$cluster\t-\tFAIL\t-\t-\t-" >> "$TMPDIR_FS/all.tsv" && continue
  [[ ! -f "$TMPDIR_FS/${cluster}.raw" ]] && continue

  awk -v cluster="$cluster" -v user="$CCDB_USER" '
  BEGIN { FS="|"; acct="" }
  /^MARKER:/ {
    if (acct != "" && proj_lfs != "") {
      atype = "GPU+CPU"
      if (acct ~ /_gpu$/) atype = "GPU"
      if (acct ~ /_cpu$/) atype = "CPU"
      printf "%s\t%s\t%s\t%s\t%s\t%s\n", cluster, acct, atype, proj_shares, proj_lfs, (user_lfs != "" ? user_lfs : "n/a")
    }
    sub(/^MARKER:/, "")
    acct = $0
    proj_shares = ""; proj_lfs = ""; user_lfs = ""
    next
  }
  NF < 3 { next }
  {
    gsub(/^[ \t]+|[ \t]+$/, "", $1)
    gsub(/^[ \t]+|[ \t]+$/, "", $2)
    gsub(/^[ \t]+|[ \t]+$/, "", $3)
    gsub(/^[ \t]+|[ \t]+$/, "", $9)

    if ($2 == "" && $1 != "") {
      proj_shares = $3
      proj_lfs = $9
    } else if ($2 == user) {
      user_lfs = $9
    }
  }
  END {
    if (acct != "" && proj_lfs != "") {
      atype = "GPU+CPU"
      if (acct ~ /_gpu$/) atype = "GPU"
      if (acct ~ /_cpu$/) atype = "CPU"
      printf "%s\t%s\t%s\t%s\t%s\t%s\n", cluster, acct, atype, proj_shares, proj_lfs, (user_lfs != "" ? user_lfs : "n/a")
    }
  }
  ' "$TMPDIR_FS/${cluster}.raw" >> "$TMPDIR_FS/all.tsv"
done

# --- Print report ---

echo "=============================================================================="
echo "  FAIRSHARE REPORT — ${CCDB_USER} — $(date '+%Y-%m-%d %H:%M')"
echo "=============================================================================="

# GPU table
echo ""
echo "  GPU FAIRSHARE (sorted by project priority)"
echo "  ---------------------------------------------------------------------------"
printf "  %-11s %-20s %-4s %8s %12s %12s  %s\n" \
  "Cluster" "Account" "RAC" "Shares" "Proj LvlFS" "Your LvlFS" "Rating"
echo "  ---------------------------------------------------------------------------"

awk -F'\t' '$3 == "GPU" || $3 == "GPU+CPU"' "$TMPDIR_FS/all.tsv" 2>/dev/null | \
  awk -F'\t' '{
    lfs = $5
    if (lfs ~ /[eE]/) lfs = lfs + 0
    print (lfs+0) "\t" $0
  }' | sort -t$'\t' -k1 -rg | cut -f2- | \
  awk -F'\t' '{
    cluster=$1; acct=$2; shares=$4; plfs=$5; ulfs=$6
    rac = (shares+0 > 100) ? "YES" : "no"
    v = plfs + 0
    if (plfs == "inf") rating = "-----"
    else if (v > 10) rating = "*****"
    else if (v > 1)  rating = "***  "
    else if (v > 0.3) rating = "**   "
    else if (v > 0.05) rating = "*    "
    else rating = "     "
    printf "  %-11s %-20s %-4s %8s %12s %12s  %s\n", cluster, acct, rac, shares, plfs, ulfs, rating
  }'

echo "  ---------------------------------------------------------------------------"

# CPU table
echo ""
echo "  CPU FAIRSHARE (sorted by project priority)"
echo "  ---------------------------------------------------------------------------"
printf "  %-11s %-20s %-4s %8s %12s %12s  %s\n" \
  "Cluster" "Account" "RAC" "Shares" "Proj LvlFS" "Your LvlFS" "Rating"
echo "  ---------------------------------------------------------------------------"

awk -F'\t' '$3 == "CPU"' "$TMPDIR_FS/all.tsv" 2>/dev/null | \
  awk -F'\t' '{
    lfs = $5; if (lfs ~ /[eE]/) lfs = lfs + 0
    print (lfs+0) "\t" $0
  }' | sort -t$'\t' -k1 -rg | cut -f2- | \
  awk -F'\t' '{
    cluster=$1; acct=$2; shares=$4; plfs=$5; ulfs=$6
    rac = (shares+0 > 100) ? "YES" : "no"
    v = plfs + 0
    if (plfs == "inf") rating = "-----"
    else if (v > 10) rating = "*****"
    else if (v > 1)  rating = "***  "
    else if (v > 0.3) rating = "**   "
    else if (v > 0.05) rating = "*    "
    else rating = "     "
    printf "  %-11s %-20s %-4s %8s %12s %12s  %s\n", cluster, acct, rac, shares, plfs, ulfs, rating
  }'

echo "  ---------------------------------------------------------------------------"

# Best account per cluster for GPU
echo ""
echo "  BEST ACCOUNT PER CLUSTER (GPU)"
echo "  ---------------------------------------------------------------------------"
printf "  %-11s %-20s %12s  %s\n" "Cluster" "--account=" "Proj LvlFS" "Notes"
echo "  ---------------------------------------------------------------------------"

awk -F'\t' '$3 == "GPU" || $3 == "GPU+CPU"' "$TMPDIR_FS/all.tsv" 2>/dev/null | \
  awk -F'\t' '{
    lfs = $5; if (lfs ~ /[eE]/) lfs = lfs + 0
    print (lfs+0) "\t" $0
  }' | sort -t$'\t' -k1 -rg | cut -f2- | \
  awk -F'\t' '!seen[$1]++ { print }' | \
while IFS=$'\t' read -r cluster acct atype shares plfs ulfs; do
  display="${acct%_gpu}"
  printf "  %-11s %-20s %12s  %s\n" "$cluster" "$display" "$plfs" "${NOTES[$cluster]}"
done

echo "  ---------------------------------------------------------------------------"
echo ""

# Failed clusters
failed=()
for cluster in $CLUSTERS; do
  [[ -f "$TMPDIR_FS/${cluster}.fail" ]] && failed+=($cluster)
done
if [[ ${#failed[@]} -gt 0 ]]; then
  echo "  UNREACHABLE: ${failed[*]}"
  echo "  (establish SSH connection first, then re-run)"
  echo ""
fi

echo "  Legend:  LevelFS > 1 = under-served (high priority)  |  < 1 = over-served"
echo "          RAC = Resource Allocation Competition grant   |  ***** = best"
echo ""
