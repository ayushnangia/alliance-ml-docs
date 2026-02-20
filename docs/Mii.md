# Mii

Other languages:

- English
- [français](Mii_fr.md)

A smart search engine for module environments.

Mii works around an existing modules installation, efficiently searching and loading modules on-demand for users.

Once Mii is loaded, modules will be quietly autoloaded for any unambiguous commands. Ambiguous commands will interactively ask for modules to load.

It features:

- Support for Lmod and Environment Modules installations
- bash and zsh shell integration
- Module listing / individual information (via mii list, mii show)
- Searching for exact commands (via mii exact)
- Searching for similar commands (via mii search)
- Optional JSON export format

Important note

A module that is autoloaded does not persist after the command. The shell environment will be the same as it was before mii autoloaded a module.

# Activating Mii

To enable/load mii:

```
[name@server ~]$ module load mii

```

Once Mii is loaded, it will start making suggestion. When a command is not found, for example:

```
[name@server ~]$ cmd
[mii] cmd not found! Similar commands: "xcmd", "vmd", "c2d"

```

# Unambiguous commands

When a command or binary is known and unambiguous, it will be autoloaded:

```
[name@server ~]$ python3.9 --version
[mii] loading StdEnv/2020 python/3.9.6 ...
Python 3.9.6

```

# Ambiguous commands

When a command or binary is unknown or ambiguous, it will suggest a selection of potential candidates based on their relevance:

```
[name@server ~]$ blastn -version
[mii] Please select a module to run blastn:
       MODULE         PARENT(S)
    1  blast+/2.12.0  StdEnv/2020 gcc/9.3.0
    2  blast+/2.11.0  StdEnv/2020 gcc/9.3.0
    3  blast+/2.10.1  StdEnv/2020 gcc/9.3.0
    4  rmblast/2.10.0 StdEnv/2020 gcc/9.3.0
    5  blast+/2.10.1  nixpkgs/16.09 gcc/7.3.0
    6  blast+/2.10.0  nixpkgs/16.09 gcc/7.3.0
    7  blast+/2.9.0   nixpkgs/16.09 gcc/7.3.0
    8  blast+/2.8.1   nixpkgs/16.09 gcc/7.3.0
    9  blast+/2.7.1   nixpkgs/16.09 gcc/7.3.0
    10 blast+/2.4.0   nixpkgs/16.09 gcc/7.3.0
    11 igblast/1.9.0  nixpkgs/16.09 gcc/7.3.0
    12 rmblast/2.9.0  nixpkgs/16.09 gcc/7.3.0
    13 blast+/2.6.0   nixpkgs/16.09 gcc/5.4.0
    14 igblast/1.9.0  nixpkgs/16.09 gcc/5.4.0
    15 igblast/1.8.0  nixpkgs/16.09 gcc/5.4.0
    16 igblast/1.7.0  nixpkgs/16.09 gcc/5.4.0
    17 rmblast/2.6.0  nixpkgs/16.09 gcc/5.4.0
    18 igblast/1.8.0  nixpkgs/16.09 gcc/4.8.5
Make a selection (1-18, q aborts) [1]: 1
[mii] loading StdEnv/2020 gcc/9.3.0 blast+/2.12.0 ...

Lmod is automatically replacing "intel/2020.1.217" with "gcc/9.3.0".


Due to MODULEPATH changes, the following have been reloaded:
  1) openmpi/4.0.3

blastn: 2.12.0+
 Package: blast 2.12.0, build Sep 27 2021 15:23:34

```

As shown above, we selected one module (#1) out of the selection, and the command was then ran.

# Search with Mii

You can search for binaries to discover which modules provides it. The results are sorted by relevance:

```
[name@server ~]$ mii search pgc+
Results for "pgc+": (total 16)
    MODULE            COMMAND      PARENT(S)        RELEVANCE
    nvhpc/20.7        pgcc         StdEnv/2020      high
    nvhpc/20.7        pgc++        StdEnv/2020      high
    pgi/19.4          pgcc         nixpkgs/16.09    high
    pgi/19.4          pgc++        nixpkgs/16.09    high
    pgi/17.3          pgc          nixpkgs/16.09    high
    pgi/17.3          pgcc         nixpkgs/16.09    high
    pgi/17.3          pgc++        nixpkgs/16.09    high
    pgi/16.9          pgc          nixpkgs/16.09    high
    pgi/16.9          pgcc         nixpkgs/16.09    high
    pgi/16.9          pgc++        nixpkgs/16.09    high
    pgi/13.10         pgc          nixpkgs/16.09    high
    pgi/13.10         pgcc         nixpkgs/16.09    high
    pgi/13.10         pgc++        nixpkgs/16.09    high
    pgi/13.10         pgCC         nixpkgs/16.09    high
    gcccore/.9.3.0    gcc          StdEnv/2020      medium
    gcccore/.9.3.0    g++          StdEnv/2020      medium

```

# Disabling Mii

To disable mii:

```
[name@server ~]$ mii disable

```

## Re-enabling

To re-enable mii:

```
[name@server ~]$ mii enable

```