# MPI-IO

Other languages:

- English
- [français](MPI-IO_fr.md)

## Description

**MPI-IO** is a family of [MPI](MPI.md) routines that makes it possible to do file read and write operations in parallel. MPI-IO is a part of the MPI-2 standard. The main advantage of MPI-IO is that it allows, in a simple and efficient fashion, to write and to read data that is partitioned on multiple processes, to and from a single file that is common to all processes. This is particularly useful when the manipulated data are vectors or matrices that are cut up in a structured manner between the different processes involved. This page gives a few guidelines on the use of MPI-IO and some references to more complete documentation.

## Using MPI-IO

### Operations through offsets

The simplest way to perform parallel read and write operations is to use offsets. Each process can read from or write to the file with a defined offset. This can be done in two operations ([MPI\_File\_seek](http://www.open-mpi.org/doc/current/man3/MPI_File_seek.3.php) followed by [MPI\_File\_read](http://www.open-mpi.org/doc/current/man3/MPI_File_read.3.php) or by [MPI\_File\_write](http://www.open-mpi.org/doc/current/man3/MPI_File_write.3.php)), or even in a single operation ([MPI\_File\_read\_at](http://www.open-mpi.org/doc/current/man3/MPI_File_read_at.3.php) or [MPI\_File\_write\_at](http://www.open-mpi.org/doc/current/man3/MPI_File_write_at.3.php)). Usually the offset is computed as a function of the process rank.

**File :** mpi\_rw\_at.c

```
#include <mpi.h>

#define BLOCKSIZE  80
#define NBRBLOCKS  32

int main(int argc, char** argv) {

    MPI_File f;
    char*    filename  = "testmpi.txt";
    char     buffer[TAILLEBLOC];
    int      rank, size;
    int      i;

    /* MPI Initialization */ 
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    /* Buffer initialization */
    memset(buffer, 'a'+rank, BLOCKSIZE);
    buffer[BLOCKSIZE - 1] = '\n';

    MPI_File_open(MPI_COMM_WORLD, filename, (MPI_MODE_WRONLY | MPI_MODE_CREATE), MPI_INFO_NULL, &f);

    /* Write data alternating between the processes: aabbccddaabbccdd... */
    MPI_File_seek(f, rank*BLOCKSIZE, MPI_SEEK_SET); /* Go to position rank * BLOCKSIZE */
    for (i=0; i<NBRBLOCKS; ++i) {
        MPI_File_write(f, buffer, BLOCKSIZE, MPI_CHAR, MPI_STATUS_IGNORE);
        /* Advance (size-1)*BLOCKSIZE bytes */
        MPI_File_seek(f, (size-1)*BLOCKSIZE, MPI_SEEK_CUR);
    }

    MPI_File_close(&f);

    MPI_File_open(MPI_COMM_WORLD, filename, MPI_MODE_RDONLY, MPI_INFO_NULL, &f);

    /* Read data in a serial fashion for each process. Each process reads: aabbccdd */
    for (i=0; i<NBRBLOCKS; ++i) {
        MPI_File_read_at(f, rank*i*NBRBLOCKS*BLOCKSIZE, buffer, BLOCKSIZE, MPI_CHAR, MPI_STATUS_IGNORE);
    }

    MPI_File_close(&f);
    MPI_Finalize();

    return 0;
}

```

### Using views

Using views, each process can *see* a section of the file as if it were the entire file. In this way it is no longer necessary to compute the file offsets as a function of the process rank. Once the view is defined, it is a lot simpler to perform operations on this file, without risking conflicts with operations performed by other processes. A view is defined using the function [MPI\_File\_set\_view](http://www.open-mpi.org/doc/current/man3/MPI_File_set_view.3.php). Here is a program identical to the previous one, but using views instead.

**File :** mpi\_view.c

```
#include <stdio.h>
#include <mpi.h>

#define BLOCKSIZE  80
#define NBRBLOCKS  32

int main(int argc, char** argv) {

    MPI_File f;
    MPI_Datatype type_intercomp;
    MPI_Datatype type_contiguous;
    char*    filename  = "testmpi.txt";
    char     buffer[BLOCKSIZE];
    int      rank, size;
    int      i;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    /* Buffer initialization */
    memset(buffer, 'a'+rank, BLOCKSIZE);
    buffer[BLOCKSIZE - 1] = '\n';

    MPI_File_open(MPI_COMM_WORLD,
        filename,
        (MPI_MODE_WRONLY | MPI_MODE_CREATE),
        MPI_INFO_NULL,
        &f);

    /* Write data alternating between the processes: aabbccddaabbccdd... */
    MPI_Type_contiguous(BLOCKSIZE, MPI_CHAR, &type_intercomp);
    MPI_Type_commit(&type_intercomp);
    for (i=0; i<NBRBLOCKS; ++i) {
        MPI_File_set_view(f, rank*BLOCKSIZE+i*size*BLOCKSIZE, MPI_CHAR, type_intercomp, "native", MPI_INFO_NULL);
        MPI_File_write(f, buffer, BLOCKSIZE, MPI_CHAR, MPI_STATUS_IGNORE);
    }

    MPI_File_close(&f);

    MPI_File_open(MPI_COMM_WORLD,
        filename,
        MPI_MODE_RDONLY,
        MPI_INFO_NULL,
        &f);

    /* Read data in a serial fashion for each process. Each process reads: aabbccdd */
    MPI_Type_contiguous(NBRBLOCKS*BLOCKSIZE, MPI_CHAR, &type_contiguous);
    MPI_Type_commit(&type_contiguous);
    MPI_File_set_view(f, rank*NBRBLOCKS*BLOCKSIZE, MPI_CHAR, type_contiguous, "native", MPI_INFO_NULL);
    for (i=0; i<NBRBLOCKS; ++i) {
        MPI_File_read(f,  buffer, BLOCKSIZE, MPI_CHAR, MPI_STATUS_IGNORE);
    }

    MPI_File_close(&f);
    MPI_Finalize();

    return 0;
}

```

**Warning!** Some file systems do not support file locks. Consequently some operations are not possible, in particular using views on disjoint file sections.

## References

- [OpenMPI documentation](http://www.open-mpi.org/doc/current/)
- [Course on parallel I/O](https://scinet.courses/215)