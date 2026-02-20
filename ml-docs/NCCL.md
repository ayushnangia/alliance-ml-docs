# NCCL

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

# What is NCCL

Please see the [NVIDIA webpage](https://developer.nvidia.com/nccl).

# Troubleshooting

To activate NCCL debug outputs, set the following variable before running NCCL:

```
NCCL_DEBUG=info

```

To fix `Caught error during NCCL init [...] connect() timed out` errors, set the following variable before running NCCL:

```
export NCCL_BLOCKING_WAIT=1

```