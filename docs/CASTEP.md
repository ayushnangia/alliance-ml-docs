# CASTEP

Other languages:

- English
- [français](CASTEP_fr.md)

## Installing CASTEP

For example, with version `20.11`:

1. You must [**get the archive file that contains the installer**](http://www.castep.org/get_castep); this file should be named `CASTEP-20.11.tar.gz`.
2. Upload the `CASTEP-20.11.tar.gz` file to your `/home/$USER` folder on the cluster you intend to use.
3. On the cluster, run the command:

```
[name@server ~]$ eb CASTEP-20.11-iofbf-2020a.eb --sourcepath=$HOME --disable-enforce-checksums

```

Once this command has completed, log out from the cluster and log back in.

## Using CASTEP

You should be able to load the module with:

```
[name@server ~]$ module load castep

```

On a compute node, the CASTEP executable can be used like an [MPI application](Scheduler.md#MPI_job):

```
[name@server ~]$ srun castep.mpi seedname

```

Where input files would be `seedname.cell` and `seedname.param` (i.e. "seedname" could be a different name).

## Reference

- [CASTEP User Documentation](https://castep-docs.github.io/castep-docs/)