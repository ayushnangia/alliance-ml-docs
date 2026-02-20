# FEniCS

Other languages:

- English
- [français](FEniCS_fr.md)

[FEniCS](https://fenicsproject.org) is a popular open-source computing platform for solving partial differential equations (PDEs).

FEniCS can be built with various extensions, so we do not offer a single, global installation. Please choose between

- Installation in a virtual environment
- Using a Singularity container

# Installation in a virtual environment

These are instructions for installing FEniCS version 2019.1.0, under StdEnv/2020 with OpenMPI and GCC 9.3.0.

You can run the script below by copying it to the cluster you are using and running **bash fenics-install.sh**.

Note that the installation will warn you that it will create (or replace) the application directory, and
will give usage instructions when the installation is successful. The script can be modified to change
the installation directory if needed.

**File :** fenics-install.sh

```
#!/usr/bin/env bash
# =============================================================================
# Compile script for FEniCS 2019.1.0
# =============================================================================

set -e

FENICS_INSTALL=$HOME/fenics
FENICS_VERSION=2019.1.0
PYBIND11_VERSION=2.2.3
export PYTHONPATH=$PYTHONPATH:$FENICS_INSTALL/lib/python3.10/site-packages

module purge
module load StdEnv/2020
module load gcc/9.3.0
module load hdf5-mpi/1.10.6
module load boost/1.72.0
module load eigen
module load python/3.10.2
module load scipy-stack/2023b
module load mpi4py/3.0.3
module load petsc/3.17.1
module load slepc/3.17.2
module load scotch/6.0.9
module load fftw-mpi/3.3.8
module load ipp/2020.1.217
module load swig
module load flexiblas

main () {
    warning_install
    make_fenics_directory
    download_py_packages $FENICS_VERSION
    make_py_packages
    make_pybind11
    make_dolfin
    print_instructions
}

warning_install () {
    echo "---------------------------------------------------------------"
    echo "WARNING: THE FENICS/DOLFIN INSTALL WILL WIPE OUT THIS DIRECTORY"
    echo "     $FENICS_INSTALL "
    echo
    echo "IF YOU DON'T WANT THIS TO HAPPEN, PRESS CTRL-C TO ABORT"
    echo "PRESS ANY KEY TO CONTINUE"
    echo "---------------------------------------------------------------"
    read -n 1
}

print_instructions () {
    echo "---------------------------------------------------------------"
    echo "TO USE FENICS/DOLFIN, YOU NEED TO DO:"
    echo
    echo "module load $MODULES"
    echo "source $FENICS_INSTALL/bin/activate"
    echo "source $FENICS_INSTALL/share/dolfin/dolfin.conf"
    echo "---------------------------------------------------------------"
}

make_fenics_directory () {
    rm -rf $FENICS_INSTALL
    mkdir -p $FENICS_INSTALL && cd $FENICS_INSTALL
}

download_py_packages () {
    version=release
    cd $FENICS_INSTALL
    git clone --branch=$version https://bitbucket.org/fenics-project/fiat.git
    git clone --branch=$version https://bitbucket.org/fenics-project/dijitso.git
    git clone https://bitbucket.org/fenics-project/ufc-deprecated.git ufc
    git clone --branch=$version https://bitbucket.org/fenics-project/ufl.git
    git clone --branch=$version https://bitbucket.org/fenics-project/ffc.git
    git clone --branch=$version https://bitbucket.org/fenics-project/dolfin.git
    git clone --branch=$version https://bitbucket.org/fenics-project/mshr.git
    git clone --branch=v$PYBIND11_VERSION \
        https://github.com/pybind/pybind11.git

    chmod u+w ~/fenics/*/.git/objects/pack/*

    mkdir -p $FENICS_INSTALL/pybind11/build
    mkdir -p $FENICS_INSTALL/dolfin/build
    mkdir -p $FENICS_INSTALL/mshr/build
}

make_pybind11 () {
    cd $FENICS_INSTALL/pybind11/build

    source $FENICS_INSTALL/bin/activate

    cmake -DPYBIND11_TEST=off \
          -DCMAKE_INSTALL_PREFIX=$HOME/fenics \
          -DPYBIND11_CPP_STANDARD=-std=c++11 ..
    make -j8 install
}

make_py_packages () {
    cd $FENICS_INSTALL
    virtualenv --no-download $FENICS_INSTALL
    source $FENICS_INSTALL/bin/activate
    pip3 install ply
    pip3 install numpy
    cd $FENICS_INSTALL/fiat    && pip3 install .
    cd $FENICS_INSTALL/dijitso && pip3 install .
    cd $FENICS_INSTALL/ufl     && pip3 install .
    cd $FENICS_INSTALL/ffc     && pip3 install .
}

make_dolfin () {
    cd $FENICS_INSTALL/dolfin/build

    source $FENICS_INSTALL/bin/activate

    cmake .. -DDOLFIN_SKIP_BUILD_TESTS=true \
          -DCMAKE_EXE_LINKER_FLAGS="-lpthread" \
          -DEIGEN3_INCLUDE_DIR=$EBROOTEIGEN/include \
          -DCMAKE_INSTALL_PREFIX=$HOME/fenics \
          -DCMAKE_SKIP_RPATH=ON \
          -DRT_LIBRARY=$EBROOTGENTOO/lib64/librt.so \
          -DHDF5_C_LIBRARY_dl=$EBROOTGENTOO/lib64/libdl.so \
          -DHDF5_C_LIBRARY_m=$EBROOTGENTOO/lib64/libm.so \
          -DHDF5_C_LIBRARY_pthread=$EBROOTGENTOO/lib64/libpthread.so \
          -DHDF5_C_LIBRARY_z=$EBROOTGENTOO/lib64/libz.so \
          -DSCOTCH_DIR=$EBROOTSCOTCH -DSCOTCH_LIBRARIES=$EBROOTSCOTCH/lib \
          -DSCOTCH_INCLUDE_DIRS=$EBROOTSCOTCH/include \
          -DBLAS_blas_LIBRARY=$EBROOTFLEXIBLAS/lib/libflexiblas.so

    make -j 8 install
    cd $FENICS_INSTALL/dolfin/python && pip3 install .
}

main

```

Outdated for `StdEnv/2020`

**Some information in this page is outdated.** . In particular, it displays advice which may no longer be applicable in our new `StdEnv/2020` environment. Our team is aware of it and is working to update the documentation. In the mean time, the information in this page should not necessarily be considered currently factual or authoritative.

## FEniCS add-ons

**This section has not been updated to work with StdEnv/2020**.

First install FEniCS following instructions above.

### mshr

**File :** mshr\_install.sh

```
module load hdf5-mpi/1.8.18 boost eigen python/3.5 scipy-stack/2017b petsc/3.7.5 fftw-mpi/3.3.6

export CMAKE_PREFIX_PATH=/home/$USER/software/dolfin/share/dolfin/cmake/:$CMAKE_PREFIX_PATH

git clone https://bitbucket.org/fenics-project/mshr.git
cd mshr
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/software/mshr   -DCMAKE_BUILD_TYPE=Release -DCMAKE_SKIP_RPATH=ON -DCMAKE_PREFIX_PATH=$NIXUSER_PROFILE:$CMAKE_PREFIX_PATH -DEIGEN3_INCLUDE_DIR=$EBROOTEIGEN/include 

make
make install

```

Then run

**File :** fenics\_mshr\_run.sh

```
module load hdf5-mpi/1.8.18 boost eigen python/3.5 scipy-stack/2017b petsc/3.7.5 fftw-mpi/3.3.6
source ~/software/dolfin/share/dolfin/dolfin.conf
source ~/fenics/bin/activate
export PYTHONPATH=$HOME/software/mshr/lib/python3.5/site-packages:$PYTHONPATH
export LD_LIBRARY_PATH=$HOME/software/mshr/lib:$LD_LIBRARY_PATH

```

# Using a Singularity container

The following Singularity Recipe will download the FEniCS Docker image, install it, and download additional packages, e.g., various Python packages. This recipe must be run on your own machine, that is, a Linux machine with Singularity installed where **you have root access**.

To build your FEniCS image using this recipe, run the following command:

```
 sudo singularity build FEniCS.simg FEniCS-ComputeCanada-Singularity-Recipe

```

and then upload `FEniCS.simg` to your account. The FEniCS Docker image places a number of files in `/home/fenics`.

**File :** FEniCS-ComputeCanada-Singularity-Recipe

```
Bootstrap: docker
From: quay.io/fenicsproject/stable:latest

%post
  sudo apt-get -qq update
  sudo apt-get -y upgrade
  sudo apt-get -y install python-bitstring python3-bitstring
  sudo apt-get -y install python-certifi python3-certifi
  sudo apt-get -y install python-cryptography python3-cryptography
  sudo apt-get -y install python-cycler python3-cycler
  sudo apt-get -y install cython cython3
  sudo apt-get -y install python-dateutil python3-dateutil
  sudo apt-get -y install python-deap python3-deap
  sudo apt-get -y install python-decorator python3-decorator
  sudo apt-get -y install python-ecdsa python3-ecdsa
  sudo apt-get -y install python-ecdsa python3-ecdsa
  sudo apt-get -y install python-enum34
  sudo apt-get -y install python-funcsigs python3-funcsigs
  sudo apt-get -y install ipython ipython3 python-ipython-genutils python3-ipython-genutils
  sudo apt-get -y install python-jinja2 python3-jinja2
  sudo apt-get -y install python-jsonschema python3-jsonschema
  sudo apt-get -y install python-lockfile python3-lockfile
  sudo apt-get -y install python-markupsafe python3-markupsafe
  sudo apt-get -y install python-matplotlib python3-matplotlib
  sudo apt-get -y install python-mistune python3-mistune
  sudo apt-get -y install python-mock python3-mock
  sudo apt-get -y install python-mpmath python3-mpmath
  sudo apt-get -y install python-netaddr python3-netaddr
  sudo apt-get -y install python-netifaces python3-netifaces
  sudo apt-get -y install python-nose python3-nose
  sudo apt-get -y install ipython-notebook ipython3-notebook
  sudo apt-get -y install python-numpy python3-numpy
  sudo apt-get -y install python-pandas python3-pandas
  sudo apt-get -y install python-paramiko python3-paramiko
  sudo apt-get -y install python-path python3-path
  sudo apt-get -y install python-pathlib
  sudo apt-get -y install python-pbr python3-pbr
  sudo apt-get -y install python-pexpect python3-pexpect
  sudo apt-get -y install python-pickleshare python3-pickleshare
  sudo apt-get -y install python-prompt-toolkit python3-prompt-toolkit
  sudo apt-get -y install python-ptyprocess python3-ptyprocess
  sudo apt-get -y install python-pycryptopp
  sudo apt-get -y install python-pygments python3-pygments
  sudo apt-get -y install python-pyparsing python3-pyparsing
  sudo apt-get -y install python-zmq python3-zmq
  sudo apt-get -y install python-requests python3-requests
  sudo apt-get -y install python-scipy python3-scipy
  sudo apt-get -y install python-setuptools python3-setuptools
  sudo apt-get -y install python-simplegeneric python3-simplegeneric
  sudo apt-get -y install python-singledispatch python3-singledispatch
  sudo apt-get -y install python-six python3-six
  sudo apt-get -y install python-sympy python3-sympy
  sudo apt-get -y install python-terminado python3-terminado
  sudo apt-get -y install python-tornado python3-tornado
  sudo apt-get -y install python-traitlets python3-traitlets
  sudo apt-get -y install automake git-core libopenmpi-dev libtool mercurial openmpi-bin 
  sudo apt-get -y install python3-pip python3-venv

  # Clean up downloaded and temporary files...
  sudo apt-get clean
  sudo rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

```

# FEniCS Legacy (2019) Installation on Trillium

Go to your home directory and follow the instructions below to set up and test the container for the legacy FEniCS 2019 version.

## 1. Download the Docker image as an Apptainer SIF

```
apttainer pull fenics-legacy.sif docker://ghcr.io/scientificcomputing/fenics-gmsh:2024-05-30

```

## 2. Make a writable sandbox directory

Create a writable directory tree (*fenics-legacy.sandbox*) from the SIF file so you can modify or install extra packages:

```
apptainer build --sandbox fenics-legacy.sandbox fenics-legacy.sif

```

**Note:**

- *fenics-legacy.sandbox* is just a directory name the command will create.
- You can call it something else (e.g. *fenics-dev/* or *my\_rw\_image/*).
- The *.sandbox* suffix is just a convention, not required.

## 3. Fix pip certificate bundle path

Inside the sandbox, create a certs folder and symlink the CA bundle so pip/SSL trusts HTTPS:

```
apptainer exec --writable fenics-legacy.sandbox sh -c "mkdir -p /etc/pki/tls/certs && ln -s /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt"

```

## 4. Create a new SIF from the sandbox

After modifications, create a new read-only image (portable, reproducible):

```
apptainer build fenics-legacy-updated.sif fenics-legacy.sandbox

```

## 5. Run quick tests

```
apptainer exec --bind $PWD:/root/shared --pwd /root/shared fenics-legacy-updated.sif python3 -c "import ufl_legacy; print('ufl_legacy ok. version:', ufl_legacy.__version__)"

```

**Note:**

- `--bind $PWD:/root/shared` mounts your current host directory in the container.
- `--pwd` sets the working directory there.

## Important Notes

- FEniCS Legacy (2019.1.x) requires UFL Legacy, already bundled.
- The Python package is named `ufl_legacy`, not `ufl`.
- Compatible UFL version is 2022.3.0 (provided by `ufl_legacy`).
- A plain `import ufl` should fail, while `import ufl_legacy` should succeed.

## Aliasing ufl\_legacy as ufl

Some downstream packages (like Oasis) assume `import ufl`. To avoid patching them all, you can provide a shim package that re-exports `ufl_legacy` as `ufl`.

Create the file `/pyshims/ufl/__init__.py` with the following contents:

```
import sys
import ufl_legacy as ufl

api = [k for k in ufl.__dict__.keys() if not k.startswith('__') and not k.endswith('__')]
for key in api:
    sys.modules['ufl.{}'.format(key)] = getattr(ufl, key)
del api

```

## Test the aliasing

Prepend the shim path to PYTHONPATH when launching inside the container:

```
APPTAINERENV_PYTHONPATH=<path_to_shim>:$PYTHONPATH apptainer exec --bind /scratch:/scratch ~/fenics-legacy-updated.sif python3 -c "from ufl.tensors import ListTensor; print('UFL tensors ok')"

```