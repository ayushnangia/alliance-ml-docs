# NVTOP

Other languages:

- English
- [français](NVTOP_fr.md)

[NVTOP](https://github.com/Syllo/nvtop) stands for Neat Videocard TOP, a (h)top like task monitor for GPUs and accelerators. It can handle multiple GPUs and print information about them in a htop-familiar way.

Because a picture is worth a thousand words:
[![](/mediawiki/images/thumb/a/a1/NVTOP.png/1121px-NVTOP.png)](FileNVTOPpng.md)

# Monitor GPUs usage

NVTOP can monitor single or multiple GPUs. It can show the GPU usage and its memory.
One can also select a specific device from the menu (F2 -> GPU Select).

NVTOP is useful to monitor and verify that your job is using the GPU as efficiently as possible.

## Monitor batch job

If you have submitted a non-interactive job and would like to see its current GPU usage.

1. From a login node, find the job id and select the one to monitor:

```
[name@server ~]$ sq

```

2. Attach to the running job:

```
[name@server ~]$ srun --pty --jobid JOBID nvtop

```

## Monitor interactive job

1. Start your interactive job with minimal resources.

2. In a second terminal, connect to the login node, find the job id:

```
[name@server ~]$ sq

```

3. Attach to the running job:

```
[name@server ~]$ srun --pty --jobid JOBID nvtop

```

You'll be able to see the usage in real time as you run your commands in the first terminal.

## Monitor a GPU on a specific node

When running multi-nodes jobs, it can be useful to verify that one or all GPUs are effectively used.

1. From a login node, find the job id and identify the node names:

```
[name@server ~]$ sq
[name@server ~]$ srun --jobid JOBID -n1 -c1 scontrol show hostname

```

2. Attach to the running job on the specific node:

```
[name@server ~]$ srun --pty --jobid JOBiD --nodelist NODENAME nvtop

```