# CESM

This article is a draft

**This is not a complete article**: This is a draft, a work in progress that is intended to be published into an article, which may or may not be ready for inclusion in the main wiki. It should not necessarily be considered factual or authoritative.

"The [Community Earth System Model](https://www.cesm.ucar.edu/) is a fully coupled global climate model developed in collaboration with colleagues in the research community. CESM provides state of the art computer simulations of Earth's past, present, and future climate states."

# Porting and Validating

The below configuration files and commands are designed for a local installation of CESM 2.1. Local installations allow for [source code changes](https://ncar.github.io/CESM-Tutorial/notebooks/sourcemods/sourcemods.html) which may be useful for specific research purposes. Before making the adaptations as described in the sections below, please [download CESM 2.1 from the CESM developers](https://www.cesm.ucar.edu/models/cesm2/download) in your local directory.

Version 2.1.5Version 2.1.3

This version is based on the [latest official release](https://github.com/ESCOMP/CESM/releases/latest).

```
[name@server ~]$ git clone -b release-cesm2.1.5 https://github.com/ESCOMP/CESM.git /path/to/CESM

```

This older version has been very popular in the research community, but it may become obsolete because this version is no longer officially supported.

```
[name@server ~]$ git clone -b release-cesm2.1.3 https://github.com/ESCOMP/CESM.git /path/to/CESM

```

To make this version work, **some external dependencies must be replaced** with newer versions which are no longer exactly matching the 2.1.3 version of CESM; researchers are responsible for confirming validity.

```
[name@server ~]$ sed -i 's/cam_cesm2_1_rel_41/cam_cesm2_1_rel_59/g' /path/to/CESM/Externals.cfg
[name@server ~]$ sed -i 's/cime5.6.32/cime5.6.51/g' /path/to/CESM/Externals.cfg
[name@server ~]$ sed -i 's/cism-release-cesm2.1.2_02/cism-release-cesm2.1.2_03/g' /path/to/CESM/Externals.cfg

```

## Checkout externals

Before your first use of CESM, you may checkout the individual model components by running the checkout\_externals script.

```
[name@server ~]$ /path/to/CESM/manage_externals/checkout_externals

```

You may need to accept a certificate from the CESM repository to download input files. To validate, run the same script with `-S`.

```
[name@server ~]$ /path/to/CESM/manage_externals/checkout_externals -S

```

See [this documentation page](https://escomp.github.io/CESM/versions/cesm2.1/html/downloading_cesm.html) for an example of a valid output.

## Local machine file

- Create and edit the file `~/.cime/config_machines.xml` from the following minimal content per cluster; **update both configuration lines** having `def-EDIT_THIS` with the compute account you want to use on the cluster.

  FirNibiNarvalNiagaraRorqual

  **File :** ~/.cime/config\_machines.xml

  ```
  <?xml version="1.0"?>

  <config_machines version="2.0">
    <machine MACH="fir">
      <DESC>https://docs.alliancecan.ca/wiki/Fir</DESC>
      <NODENAME_REGEX>r.*\.fir\.alliancecan</NODENAME_REGEX>

      <OS>LINUX</OS>
      <COMPILERS>intel,gnu</COMPILERS>
      <MPILIBS>openmpi</MPILIBS>

      <PROJECT>def-EDIT_THIS</PROJECT>
      <CHARGE_ACCOUNT>def-EDIT_THIS</CHARGE_ACCOUNT>

      <CIME_OUTPUT_ROOT>/scratch/$USER/cesm/output</CIME_OUTPUT_ROOT>
      <DIN_LOC_ROOT>/scratch/$USER/cesm/inputdata</DIN_LOC_ROOT>
      <DIN_LOC_ROOT_CLMFORC>${DIN_LOC_ROOT}/atm/datm7</DIN_LOC_ROOT_CLMFORC>
      <DOUT_S_ROOT>$CIME_OUTPUT_ROOT/archive/case</DOUT_S_ROOT>
      <GMAKE>make</GMAKE>
      <GMAKE_J>8</GMAKE_J>
      <BATCH_SYSTEM>slurm</BATCH_SYSTEM>
      <SUPPORTED_BY>support@tech.alliancecan.ca</SUPPORTED_BY>
      <MAX_TASKS_PER_NODE>192</MAX_TASKS_PER_NODE>
      <MAX_MPITASKS_PER_NODE>192</MAX_MPITASKS_PER_NODE>
      <PROJECT_REQUIRED>TRUE</PROJECT_REQUIRED>

      <mpirun mpilib="openmpi">
        <executable>srun</executable>
      </mpirun>
      <module_system type="module" allow_error="true">
        <init_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/perl</init_path>
        <init_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/env_modules_python.py</init_path>
        <init_path lang="csh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/csh</init_path>
        <init_path lang="sh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/sh</init_path>
        <cmd_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod perl</cmd_path>
        <cmd_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod python</cmd_path>
        <cmd_path lang="csh">module</cmd_path>
        <cmd_path lang="sh">module</cmd_path>
        <modules>
        <command name="purge"/>
   	<command name="load">StdEnv/2023</command>
        </modules>
        <modules compiler="intel">
  	<command name="load">intel/2023.2.1</command>
  	<command name="load">git-annex/10.20231129</command>
  	<command name="load">cmake/3.27.7</command>
        </modules>
        <modules mpilib="openmpi">
          <command name="load">openmpi/4.1.5</command>
          <command name="load">hdf5-mpi/1.14.2</command>
          <command name="load">netcdf-c++4-mpi/4.3.1</command>
          <command name="load">netcdf-fortran-mpi/4.6.1</command>
          <command name="load">netcdf-mpi/4.9.2</command>
  	<command name="load">xml-libxml/2.0208</command>
  	<command name="load">flexiblas/3.3.1</command>
        </modules>
      </module_system>
      <environment_variables>
              <env name="NETCDF_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/pnetcdf/1.12.3</env>
              <env name="NETCDF_FORTRAN_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-fortran-mpi/4.6.1/</env>
              <env name="NETCDF_C_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-c++4-mpi/4.3.1/</env>
              <env name="NETLIB_LAPACK_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v3/Core/imkl/2023.2.0/mkl/2023.2.0/</env>
  	    <env name="OMP_STACKSIZE">256M</env>
              <env name="I_MPI_CC">icc</env>
              <env name="I_MPI_FC">ifort</env>
              <env name="I_MPI_F77">ifort</env>
              <env name="I_MPI_F90">ifort</env>
              <env name="I_MPI_CXX">icpc</env>
      </environment_variables>
      <resource_limits>
        <resource name="RLIMIT_STACK">300000000</resource>
      </resource_limits>
    </machine>
  </config_machines>

  ```

  **File :** ~/.cime/config\_machines.xml

  ```
  <?xml version="1.0"?>

  <config_machines version="2.0">
    <machine MACH="nibi">
      <DESC>https://docs.alliancecan.ca/wiki/Nibi</DESC>
      <NODENAME_REGEX>*.nibi.sharcnet</NODENAME_REGEX>

      <OS>LINUX</OS>
      <COMPILERS>intel,gnu</COMPILERS>
      <MPILIBS>openmpi</MPILIBS>

      <PROJECT>def-EDIT_THIS</PROJECT>
      <CHARGE_ACCOUNT>def-EDIT_THIS</CHARGE_ACCOUNT>

      <CIME_OUTPUT_ROOT>/scratch/$USER/cesm/output</CIME_OUTPUT_ROOT>
      <DIN_LOC_ROOT>/scratch/$USER/cesm/inputdata</DIN_LOC_ROOT>
      <DIN_LOC_ROOT_CLMFORC>${DIN_LOC_ROOT}/atm/datm7</DIN_LOC_ROOT_CLMFORC>
      <DOUT_S_ROOT>$CIME_OUTPUT_ROOT/archive/case</DOUT_S_ROOT>
      <GMAKE>make</GMAKE>
      <GMAKE_J>8</GMAKE_J>
      <BATCH_SYSTEM>slurm</BATCH_SYSTEM>
      <SUPPORTED_BY>support@tech.alliancecan.ca</SUPPORTED_BY>
      <MAX_TASKS_PER_NODE>192</MAX_TASKS_PER_NODE>
      <MAX_MPITASKS_PER_NODE>192</MAX_MPITASKS_PER_NODE>
      <PROJECT_REQUIRED>TRUE</PROJECT_REQUIRED>

      <mpirun mpilib="openmpi">
        <executable>srun</executable>
      </mpirun>
      <module_system type="module" allow_error="true">
        <init_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/perl</init_path>
        <init_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/env_modules_python.py</init_path>
        <init_path lang="csh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/csh</init_path>
        <init_path lang="sh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/sh</init_path>
        <cmd_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod perl</cmd_path>
        <cmd_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod python</cmd_path>
        <cmd_path lang="csh">module</cmd_path>
        <cmd_path lang="sh">module</cmd_path>
        <modules>
        <command name="purge"/>
   	<command name="load">StdEnv/2023</command>
        </modules>
        <modules compiler="intel">
  	<command name="load">intel/2023.2.1</command>
  	<command name="load">git-annex/10.20231129</command>
  	<command name="load">cmake/3.27.7</command>
        </modules>
        <modules mpilib="openmpi">
          <command name="load">openmpi/4.1.5</command>
          <command name="load">hdf5-mpi/1.14.2</command>
          <command name="load">netcdf-c++4-mpi/4.3.1</command>
          <command name="load">netcdf-fortran-mpi/4.6.1</command>
          <command name="load">netcdf-mpi/4.9.2</command>
  	<command name="load">xml-libxml/2.0208</command>
  	<command name="load">flexiblas/3.3.1</command>
        </modules>
      </module_system>
      <environment_variables>
              <env name="NETCDF_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/pnetcdf/1.12.3</env>
              <env name="NETCDF_FORTRAN_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-fortran-mpi/4.6.1/</env>
              <env name="NETCDF_C_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-c++4-mpi/4.3.1/</env>
              <env name="NETLIB_LAPACK_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v3/Core/imkl/2023.2.0/mkl/2023.2.0/</env>
  	    <env name="OMP_STACKSIZE">256M</env>
              <env name="I_MPI_CC">icc</env>
              <env name="I_MPI_FC">ifort</env>
              <env name="I_MPI_F77">ifort</env>
              <env name="I_MPI_F90">ifort</env>
              <env name="I_MPI_CXX">icpc</env>
      </environment_variables>
      <resource_limits>
        <resource name="RLIMIT_STACK">300000000</resource>
      </resource_limits>
    </machine>
  </config_machines>

  ```

  Note: despite the Intel software dependencies, the below configuration works on Narval's AMD processors.

  **File :** ~/.cime/config\_machines.xml

  ```
  <?xml version="1.0"?>

  <config_machines version="2.0">
    <machine MACH="narval">
      <DESC>https://docs.alliancecan.ca/wiki/Narval/en</DESC>
      <NODENAME_REGEX>n[acgl].*.narval.calcul.quebec</NODENAME_REGEX>

      <OS>LINUX</OS>
      <COMPILERS>intel,gnu</COMPILERS>
      <MPILIBS>openmpi</MPILIBS>

      <PROJECT>def-EDIT_THIS</PROJECT>
      <CHARGE_ACCOUNT>def-EDIT_THIS</CHARGE_ACCOUNT>

      <CIME_OUTPUT_ROOT>/scratch/$USER/cesm/output</CIME_OUTPUT_ROOT>
      <DIN_LOC_ROOT>/scratch/$USER/cesm/inputdata</DIN_LOC_ROOT>
      <DIN_LOC_ROOT_CLMFORC>${DIN_LOC_ROOT}/atm/datm7</DIN_LOC_ROOT_CLMFORC>
      <DOUT_S_ROOT>$CIME_OUTPUT_ROOT/archive/case</DOUT_S_ROOT>
      <GMAKE>make</GMAKE>
      <GMAKE_J>8</GMAKE_J>
      <BATCH_SYSTEM>slurm</BATCH_SYSTEM>
      <SUPPORTED_BY>support@tech.alliancecan.ca</SUPPORTED_BY>
      <MAX_TASKS_PER_NODE>64</MAX_TASKS_PER_NODE>
      <MAX_MPITASKS_PER_NODE>64</MAX_MPITASKS_PER_NODE>
      <PROJECT_REQUIRED>TRUE</PROJECT_REQUIRED>

      <mpirun mpilib="openmpi">
        <executable>srun</executable>
      </mpirun>
      <module_system type="module" allow_error="true">
        <init_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/perl</init_path>
        <init_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/env_modules_python.py</init_path>
        <init_path lang="csh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/csh</init_path>
        <init_path lang="sh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/sh</init_path>
        <cmd_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod perl</cmd_path>
        <cmd_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod python</cmd_path>
        <cmd_path lang="csh">module</cmd_path>
        <cmd_path lang="sh">module</cmd_path>
        <modules>
        <command name="purge"/>
   	<command name="load">StdEnv/2023</command>
        </modules>
        <modules compiler="intel">
  	<command name="load">intel/2023.2.1</command>
  	<command name="load">git-annex/10.20231129</command>
  	<command name="load">cmake/3.27.7</command>
        </modules>
        <modules mpilib="openmpi">
          <command name="load">openmpi/4.1.5</command>
          <command name="load">hdf5-mpi/1.14.2</command>
          <command name="load">netcdf-c++4-mpi/4.3.1</command>
          <command name="load">netcdf-fortran-mpi/4.6.1</command>
          <command name="load">netcdf-mpi/4.9.2</command>
  	<command name="load">xml-libxml/2.0208</command>
  	<command name="load">flexiblas/3.3.1</command>
        </modules>
      </module_system>
      <environment_variables>
              <env name="NETCDF_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/pnetcdf/1.12.3</env>
              <env name="NETCDF_FORTRAN_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-fortran-mpi/4.6.1/</env>
              <env name="NETCDF_C_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-c++4-mpi/4.3.1/</env>
              <env name="NETLIB_LAPACK_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v3/Core/imkl/2023.2.0/mkl/2023.2.0/</env>
  	    <env name="OMP_STACKSIZE">256M</env>
              <env name="I_MPI_CC">icc</env>
              <env name="I_MPI_FC">ifort</env>
              <env name="I_MPI_F77">ifort</env>
              <env name="I_MPI_F90">ifort</env>
              <env name="I_MPI_CXX">icpc</env>
      </environment_variables>
      <resource_limits>
        <resource name="RLIMIT_STACK">300000000</resource>
      </resource_limits>
    </machine>
  </config_machines>

  ```

  **File :** ~/.cime/config\_machines.xml

  ```
  <?xml version="1.0"?>

  <config_machines version="2.0">
    <machine MACH="niagara">
      <DESC>https://docs.alliancecan.ca/wiki/Niagara</DESC>
      <NODENAME_REGEX>nia.*.scinet.local</NODENAME_REGEX>

      <OS>LINUX</OS>
      <COMPILERS>intel,gnu</COMPILERS>
      <MPILIBS>openmpi</MPILIBS>

      <PROJECT>def-EDIT_THIS</PROJECT>
      <CHARGE_ACCOUNT>def-EDIT_THIS</CHARGE_ACCOUNT>

      <CIME_OUTPUT_ROOT>/scratch/$USER/cesm/output</CIME_OUTPUT_ROOT>
      <DIN_LOC_ROOT>/scratch/$USER/cesm/inputdata</DIN_LOC_ROOT>
      <DIN_LOC_ROOT_CLMFORC>${DIN_LOC_ROOT}/atm/datm7</DIN_LOC_ROOT_CLMFORC>
      <DOUT_S_ROOT>$CIME_OUTPUT_ROOT/archive/case</DOUT_S_ROOT>
      <GMAKE>make</GMAKE>
      <GMAKE_J>8</GMAKE_J>
      <BATCH_SYSTEM>slurm</BATCH_SYSTEM>
      <SUPPORTED_BY>support@tech.alliancecan.ca</SUPPORTED_BY>
      <MAX_TASKS_PER_NODE>40</MAX_TASKS_PER_NODE>
      <MAX_MPITASKS_PER_NODE>40</MAX_MPITASKS_PER_NODE>
      <PROJECT_REQUIRED>TRUE</PROJECT_REQUIRED>

      <mpirun mpilib="openmpi">
        <executable>srun</executable>
      </mpirun>
      <module_system type="module" allow_error="true">
        <init_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/perl</init_path>
        <init_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/env_modules_python.py</init_path>
        <init_path lang="csh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/csh</init_path>
        <init_path lang="sh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/sh</init_path>
        <cmd_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod perl</cmd_path>
        <cmd_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod python</cmd_path>
        <cmd_path lang="csh">module</cmd_path>
        <cmd_path lang="sh">module</cmd_path>
        <modules>
        <command name="purge"/>
   	<command name="load">StdEnv/2023</command>
        </modules>
        <modules compiler="intel">
  	<command name="load">intel/2023.2.1</command>
  	<command name="load">git-annex/10.20231129</command>
  	<command name="load">cmake/3.27.7</command>
        </modules>
        <modules mpilib="openmpi">
          <command name="load">openmpi/4.1.5</command>
          <command name="load">hdf5-mpi/1.14.2</command>
          <command name="load">netcdf-c++4-mpi/4.3.1</command>
          <command name="load">netcdf-fortran-mpi/4.6.1</command>
          <command name="load">netcdf-mpi/4.9.2</command>
  	<command name="load">xml-libxml/2.0208</command>
  	<command name="load">flexiblas/3.3.1</command>
        </modules>
      </module_system>
      <environment_variables>
              <env name="NETCDF_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/pnetcdf/1.12.3</env>
              <env name="NETCDF_FORTRAN_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-fortran-mpi/4.6.1/</env>
              <env name="NETCDF_C_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-c++4-mpi/4.3.1/</env>
              <env name="NETLIB_LAPACK_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v3/Core/imkl/2023.2.0/mkl/2023.2.0/</env>
  	    <env name="OMP_STACKSIZE">256M</env>
              <env name="I_MPI_CC">icc</env>
              <env name="I_MPI_FC">ifort</env>
              <env name="I_MPI_F77">ifort</env>
              <env name="I_MPI_F90">ifort</env>
              <env name="I_MPI_CXX">icpc</env>
      </environment_variables>
      <resource_limits>
        <resource name="RLIMIT_STACK">300000000</resource>
      </resource_limits>
    </machine>
  </config_machines>

  ```

  Note: despite the Intel software dependencies, the below configuration works on Rorqual's AMD processors.

  **File :** ~/.cime/config\_machines.xml

  ```
  <?xml version="1.0"?>

  <config_machines version="2.0">
    <machine MACH="rorqual">
      <DESC>https://docs.alliancecan.ca/wiki/Rorqual/en</DESC>
      <NODENAME_REGEX>r.*\.rorqual\.calcul\.quebec</NODENAME_REGEX>

      <OS>LINUX</OS>
      <COMPILERS>intel,gnu</COMPILERS>
      <MPILIBS>openmpi</MPILIBS>

      <PROJECT>def-EDIT_THIS</PROJECT>
      <CHARGE_ACCOUNT>def-EDIT_THIS</CHARGE_ACCOUNT>

      <CIME_OUTPUT_ROOT>/scratch/$USER/cesm/output</CIME_OUTPUT_ROOT>
      <DIN_LOC_ROOT>/scratch/$USER/cesm/inputdata</DIN_LOC_ROOT>
      <DIN_LOC_ROOT_CLMFORC>${DIN_LOC_ROOT}/atm/datm7</DIN_LOC_ROOT_CLMFORC>
      <DOUT_S_ROOT>$CIME_OUTPUT_ROOT/archive/case</DOUT_S_ROOT>
      <GMAKE>make</GMAKE>
      <GMAKE_J>8</GMAKE_J>
      <BATCH_SYSTEM>slurm</BATCH_SYSTEM>
      <SUPPORTED_BY>support@tech.alliancecan.ca</SUPPORTED_BY>
      <MAX_TASKS_PER_NODE>192</MAX_TASKS_PER_NODE>
      <MAX_MPITASKS_PER_NODE>192</MAX_MPITASKS_PER_NODE>
      <PROJECT_REQUIRED>TRUE</PROJECT_REQUIRED>

      <mpirun mpilib="openmpi">
        <executable>srun</executable>
      </mpirun>
      <module_system type="module" allow_error="true">
        <init_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/perl</init_path>
        <init_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/env_modules_python.py</init_path>
        <init_path lang="csh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/csh</init_path>
        <init_path lang="sh">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/init/sh</init_path>
        <cmd_path lang="perl">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod perl</cmd_path>
        <cmd_path lang="python">/cvmfs/soft.computecanada.ca/custom/software/lmod/lmod/libexec/lmod python</cmd_path>
        <cmd_path lang="csh">module</cmd_path>
        <cmd_path lang="sh">module</cmd_path>
        <modules>
        <command name="purge"/>
   	<command name="load">StdEnv/2023</command>
        </modules>
        <modules compiler="intel">
  	<command name="load">intel/2023.2.1</command>
  	<command name="load">git-annex/10.20231129</command>
  	<command name="load">cmake/3.27.7</command>
        </modules>
        <modules mpilib="openmpi">
          <command name="load">openmpi/4.1.5</command>
          <command name="load">hdf5-mpi/1.14.2</command>
          <command name="load">netcdf-c++4-mpi/4.3.1</command>
          <command name="load">netcdf-fortran-mpi/4.6.1</command>
          <command name="load">netcdf-mpi/4.9.2</command>
  	<command name="load">xml-libxml/2.0208</command>
  	<command name="load">flexiblas/3.3.1</command>
        </modules>
      </module_system>
      <environment_variables>
              <env name="NETCDF_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/pnetcdf/1.12.3</env>
              <env name="NETCDF_FORTRAN_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-fortran-mpi/4.6.1/</env>
              <env name="NETCDF_C_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v4/MPI/intel2023/openmpi4/netcdf-c++4-mpi/4.3.1/</env>
              <env name="NETLIB_LAPACK_PATH">/cvmfs/soft.computecanada.ca/easybuild/software/2023/x86-64-v3/Core/imkl/2023.2.0/mkl/2023.2.0/</env>
  	    <env name="OMP_STACKSIZE">256M</env>
              <env name="I_MPI_CC">icc</env>
              <env name="I_MPI_FC">ifort</env>
              <env name="I_MPI_F77">ifort</env>
              <env name="I_MPI_F90">ifort</env>
              <env name="I_MPI_CXX">icpc</env>
      </environment_variables>
      <resource_limits>
        <resource name="RLIMIT_STACK">300000000</resource>
      </resource_limits>
    </machine>
  </config_machines>

  ```
- Validate your XML machine file with the following commands:

  ```
  [name@server ~]$ xmllint --noout --schema /path/to/CESM/cime/config/xml_schemas/config_machines.xsd ~/.cime/config_machines.xml
  /home/name/.cime/config_machines.xml validates

  ```

  ```
  [name@rorqual ~]$ /path/to/CESM/cime/scripts/query_config --machines current
  rorqual (current) : https://docs.alliancecan.ca/wiki/Rorqual/en
        os              LINUX
        compilers       intel,gnu
        pes/node        192
        max_tasks/node  192

  ```
- Check the official template for additional parameters:

  ```
  [name@server ~]$ less /path/to/CESM/cime/config/xml_schemas/config_machines_template.xml

  ```

## Local batch file

- Create and edit the file `~/.cime/config_batch.xml` from the following minimal content:

  FirNibiNarvalNiagaraRorqual

  **File :** ~/.cime/config\_batch.xml

  ```
  <?xml version="1.0"?>
  <file id="env_batch.xml" version="2.0">
    <header>
        These variables may be changed anytime during a run, they
        control arguments to the batch submit command.
    </header>
    <group id="config_batch">
      <entry id="BATCH_SYSTEM" value="slurm">
        <type>char</type>
        <valid_values>nersc_slurm,lc_slurm,moab,pbs,lsf,slurm,cobalt,cobalt_theta,sge,none</valid_values>
        <desc>The batch system type to use for this machine.</desc>
      </entry>
    </group>
    <group id="job_submission">
      <entry id="PROJECT_REQUIRED" value="TRUE">
        <type>logical</type>
        <valid_values>TRUE,FALSE</valid_values>
        <desc>whether the PROJECT value is required on this machine</desc>
      </entry>
    </group>
    <batch_system type="slurm" >
      <batch_submit>sbatch</batch_submit>
      <batch_cancel>scancel</batch_cancel>
      <batch_directive>#SBATCH</batch_directive>
      <jobid_pattern>(\d+)$</jobid_pattern>
      <depend_string> --dependency=afterok:jobid</depend_string>
      <depend_allow_string> --dependency=afterany:jobid</depend_allow_string>
      <depend_separator>,</depend_separator>
      <batch_mail_flag>--mail-user</batch_mail_flag>
      <batch_mail_type_flag>--mail-type</batch_mail_type_flag>
      <batch_mail_type>none, all, begin, end, fail</batch_mail_type>
      <submit_args>
        <arg flag="--time" name="$JOB_WALLCLOCK_TIME"/>
        <arg flag="--account" name="$CHARGE_ACCOUNT"/>
      </submit_args>
      <directives>
        <directive>--job-name={{ job_id }}</directive>
        <directive>--nodes={{ num_nodes }}</directive>
        <directive>--ntasks-per-node={{ tasks_per_node }}</directive>
        <directive>--output={{ job_id }}</directive>
        <directive>--exclusive</directive>
        <directive>--mem=0</directive>
      </directives>
     <unknown_queue_directives>regular</unknown_queue_directives>
      <queues>
       <queue walltimemax="12:00:00" nodemin="1" nodemax="864">fir</queue>
      </queues>
    </batch_system>
  </file>

  ```

  **File :** ~/.cime/config\_batch.xml

  ```
  <?xml version="1.0"?>
  <file id="env_batch.xml" version="2.0">
    <header>
        These variables may be changed anytime during a run, they
        control arguments to the batch submit command.
    </header>
    <group id="config_batch">
      <entry id="BATCH_SYSTEM" value="slurm">
        <type>char</type>
        <valid_values>nersc_slurm,lc_slurm,moab,pbs,lsf,slurm,cobalt,cobalt_theta,sge,none</valid_values>
        <desc>The batch system type to use for this machine.</desc>
      </entry>
    </group>
    <group id="job_submission">
      <entry id="PROJECT_REQUIRED" value="TRUE">
        <type>logical</type>
        <valid_values>TRUE,FALSE</valid_values>
        <desc>whether the PROJECT value is required on this machine</desc>
      </entry>
    </group>
    <batch_system type="slurm" >
      <batch_submit>sbatch</batch_submit>
      <batch_cancel>scancel</batch_cancel>
      <batch_directive>#SBATCH</batch_directive>
      <jobid_pattern>(\d+)$</jobid_pattern>
      <depend_string> --dependency=afterok:jobid</depend_string>
      <depend_allow_string> --dependency=afterany:jobid</depend_allow_string>
      <depend_separator>,</depend_separator>
      <batch_mail_flag>--mail-user</batch_mail_flag>
      <batch_mail_type_flag>--mail-type</batch_mail_type_flag>
      <batch_mail_type>none, all, begin, end, fail</batch_mail_type>
      <submit_args>
        <arg flag="--time" name="$JOB_WALLCLOCK_TIME"/>
        <arg flag="--account" name="$CHARGE_ACCOUNT"/>
      </submit_args>
      <directives>
        <directive>--job-name={{ job_id }}</directive>
        <directive>--nodes={{ num_nodes }}</directive>
        <directive>--ntasks-per-node={{ tasks_per_node }}</directive>
        <directive>--output={{ job_id }}</directive>
        <directive>--exclusive</directive>
        <directive>--mem=0</directive>
      </directives>
     <unknown_queue_directives>regular</unknown_queue_directives>
      <queues>
       <queue walltimemax="12:00:00" nodemin="1" nodemax="700">nibi</queue>
      </queues>
    </batch_system>
  </file>

  ```

  **File :** ~/.cime/config\_batch.xml

  ```
  <?xml version="1.0"?>
    <batch_system type="slurm" >
      <batch_submit>sbatch</batch_submit>
      <batch_cancel>scancel</batch_cancel>
      <batch_directive>#SBATCH</batch_directive>
      <jobid_pattern>(\d+)$</jobid_pattern>
      <depend_string> --dependency=afterok:jobid</depend_string>
      <depend_allow_string> --dependency=afterany:jobid</depend_allow_string>
      <depend_separator>,</depend_separator>
      <batch_mail_flag>--mail-user</batch_mail_flag>
      <batch_mail_type_flag>--mail-type</batch_mail_type_flag>
      <batch_mail_type>none, all, begin, end, fail</batch_mail_type>
      <submit_args>
        <arg flag="--time" name="$JOB_WALLCLOCK_TIME"/>
        <arg flag="--account" name="$CHARGE_ACCOUNT"/>
      </submit_args>
      <directives>
        <directive>--job-name={{ job_id }}</directive>
        <directive>--nodes={{ num_nodes }}</directive>
        <directive>--ntasks-per-node={{ tasks_per_node }}</directive>
        <directive>--output={{ job_id }}</directive>
        <directive>--exclusive</directive>
        <directive>--mem=0</directive>
      </directives>
      <unknown_queue_directives>regular</unknown_queue_directives>
      <queues>
        <queue walltimemax="12:00:00" nodemin="1" nodemax="1145">narval</queue>
      </queues>
    </batch_system>

  ```

  **File :** ~/.cime/config\_machines.xml

  ```
  <?xml version="1.0"?>
  <file id="env_batch.xml" version="2.0">
    <header>
        These variables may be changed anytime during a run, they
        control arguments to the batch submit command.
    </header>
    <group id="config_batch">
      <entry id="BATCH_SYSTEM" value="slurm">
        <type>char</type>
        <valid_values>nersc_slurm,lc_slurm,moab,pbs,lsf,slurm,cobalt,cobalt_theta,sge,none</valid_values>
        <desc>The batch system type to use for this machine.</desc>
      </entry>
    </group>
    <group id="job_submission">
      <entry id="PROJECT_REQUIRED" value="TRUE">
        <type>logical</type>
        <valid_values>TRUE,FALSE</valid_values>
        <desc>whether the PROJECT value is required on this machine</desc>
      </entry>
    </group>
    <batch_system type="slurm" >
      <batch_submit>sbatch</batch_submit>
      <batch_cancel>scancel</batch_cancel>
      <batch_directive>#SBATCH</batch_directive>
      <jobid_pattern>(\d+)$</jobid_pattern>
      <depend_string> --dependency=afterok:jobid</depend_string>
      <depend_allow_string> --dependency=afterany:jobid</depend_allow_string>
      <depend_separator>,</depend_separator>
      <submit_args>
        <arg flag="--time" name="$JOB_WALLCLOCK_TIME"/>
        <arg flag="--account" name="$CHARGE_ACCOUNT"/>
      </submit_args>
      <directives>
        <directive>--job-name={{ job_id }}</directive>
        <directive>--nodes={{ num_nodes }}</directive>
        <directive>--ntasks-per-node={{ tasks_per_node }}</directive>
        <directive>--output={{ job_id }}</directive>
        <directive>--exclusive</directive>
        <directive>--mem=0</directive>
        <directive>--constraint=[skylake|cascade]</directive>
      </directives>
     <unknown_queue_directives>regular</unknown_queue_directives>
      <queues>
       <queue walltimemax="12:00:00" nodemin="1" nodemax="2024">niagara</queue>
      </queues>
    </batch_system>
  </file>

  ```

  **File :** ~/.cime/config\_batch.xml

  ```
  <?xml version="1.0"?>
    <batch_system type="slurm" >
      <batch_submit>sbatch</batch_submit>
      <batch_cancel>scancel</batch_cancel>
      <batch_directive>#SBATCH</batch_directive>
      <jobid_pattern>(\d+)$</jobid_pattern>
      <depend_string> --dependency=afterok:jobid</depend_string>
      <depend_allow_string> --dependency=afterany:jobid</depend_allow_string>
      <depend_separator>,</depend_separator>
      <batch_mail_flag>--mail-user</batch_mail_flag>
      <batch_mail_type_flag>--mail-type</batch_mail_type_flag>
      <batch_mail_type>none, all, begin, end, fail</batch_mail_type>
      <submit_args>
        <arg flag="--time" name="$JOB_WALLCLOCK_TIME"/>
        <arg flag="--account" name="$CHARGE_ACCOUNT"/>
      </submit_args>
      <directives>
        <directive>--job-name={{ job_id }}</directive>
        <directive>--nodes={{ num_nodes }}</directive>
        <directive>--ntasks-per-node={{ tasks_per_node }}</directive>
        <directive>--output={{ job_id }}</directive>
        <directive>--exclusive</directive>
        <directive>--mem=0</directive>
      </directives>
      <unknown_queue_directives>regular</unknown_queue_directives>
      <queues>
        <queue walltimemax="12:00:00" nodemin="1" nodemax="670">rorqual</queue>
      </queues>
    </batch_system>

  ```
- Validate your XML batch file with the following commands:

  ```
  [name@server ~]$ xmllint --noout --schema /path/to/CESM/cime/config/xml_schemas/config_batch.xsd ~/.cime/config_batch.xml
  /home/name/.cime/config_batch.xml validates

  ```
- Check the documentation for additional **[configuration parameters and examples](https://esmci.github.io/cime/versions/maint-5.6/html/xml_files/cesm.html#cimeroot-config-cesm-machines)**.

## Local compilers file

- Create and edit the file `~/.cime/config_compilers.xml` from the following minimal content per cluster:

  FirNibiNarvalNiagaraRorqual

  **File :** ~/.cime/config\_compilers.xml

  ```
  <?xml version="1.0"?>

  	<compiler MACH="fir">
  	  <CPPDEFS>
  	    <append MODEL="gptl"> -DHAVE_NANOTIME -DBIT64 -DHAVE_VPRINTF -DHAVE_BACKTRACE -DHAVE_SLASHPROC -DHAVE_COMM_F2C -DHAVE_TIMES -DHAVE_GETTIMEOFDAY </append>
  	  </CPPDEFS>
  	  <NETCDF_PATH>$ENV{NETCDF_FORTRAN_ROOT}</NETCDF_PATH>
  	  <PIO_FILESYSTEM_HINTS>lustre</PIO_FILESYSTEM_HINTS>
  	  <PNETCDF_PATH>$ENV{PARALLEL_NETCDF_ROOT}</PNETCDF_PATH>
  	  <SLIBS>
  	    <append>-L$(NETCDF_PATH)/lib -lnetcdff -L$(NETCDF_C_ROOT)/lib -lnetcdf -L$(NETLIB_LAPACK_PATH)/lib/intel64 -lmkl -ldl </append>
  	  </SLIBS>
  	</compiler>

  ```

  **File :** ~/.cime/config\_compilers.xml

  ```
  <?xml version="1.0"?>

  	<compiler MACH="nibi">
  	  <CPPDEFS>
  	    <append MODEL="gptl"> -DHAVE_NANOTIME -DBIT64 -DHAVE_VPRINTF -DHAVE_BACKTRACE -DHAVE_SLASHPROC -DHAVE_COMM_F2C -DHAVE_TIMES -DHAVE_GETTIMEOFDAY </append>
  	  </CPPDEFS>
  	  <NETCDF_PATH>$ENV{NETCDF_FORTRAN_ROOT}</NETCDF_PATH>
  	  <PIO_FILESYSTEM_HINTS>lustre</PIO_FILESYSTEM_HINTS>
  	  <PNETCDF_PATH>$ENV{PARALLEL_NETCDF_ROOT}</PNETCDF_PATH>
  	  <SLIBS>
  	    <append>-L$(NETCDF_PATH)/lib -lnetcdff -L$(NETCDF_C_ROOT)/lib -lnetcdf -L$(NETLIB_LAPACK_PATH)/lib/intel64 -lmkl -ldl </append>
  	  </SLIBS>
  	</compiler>

  ```

  **File :** ~/.cime/config\_compilers.xml

  ```
  <?xml version="1.0"?>

  	<compiler MACH="narval">
  	  <CPPDEFS>
  	    <append MODEL="gptl"> -DHAVE_NANOTIME -DBIT64 -DHAVE_VPRINTF -DHAVE_BACKTRACE -DHAVE_SLASHPROC -DHAVE_COMM_F2C -DHAVE_TIMES -DHAVE_GETTIMEOFDAY </append>
  	  </CPPDEFS>
  	  <NETCDF_PATH>$ENV{NETCDF_FORTRAN_ROOT}</NETCDF_PATH>
  	  <PIO_FILESYSTEM_HINTS>lustre</PIO_FILESYSTEM_HINTS>
  	  <PNETCDF_PATH>$ENV{PARALLEL_NETCDF_ROOT}</PNETCDF_PATH>
  	  <SLIBS>
  	    <append>-L$(NETCDF_PATH)/lib -lnetcdff -L$(NETCDF_C_ROOT)/lib -lnetcdf -L$(NETLIB_LAPACK_PATH)/lib/intel64 -lmkl -ldl </append>
  	  </SLIBS>
  	</compiler>

  ```

  **File :** ~/.cime/config\_compilers.xml

  ```
  <?xml version="1.0"?>

  	<compiler MACH="niagara">
  	  <CPPDEFS>
  	    <append MODEL="gptl"> -DHAVE_NANOTIME -DBIT64 -DHAVE_VPRINTF -DHAVE_BACKTRACE -DHAVE_SLASHPROC -DHAVE_COMM_F2C -DHAVE_TIMES -DHAVE_GETTIMEOFDAY </append>
  	  </CPPDEFS>
  	  <NETCDF_PATH>$ENV{NETCDF_FORTRAN_ROOT}</NETCDF_PATH>
  	  <PIO_FILESYSTEM_HINTS>lustre</PIO_FILESYSTEM_HINTS>
  	  <PNETCDF_PATH>$ENV{PARALLEL_NETCDF_ROOT}</PNETCDF_PATH>
  	  <SLIBS>
  	    <append>-L$(NETCDF_PATH)/lib -lnetcdff -L$(NETCDF_C_ROOT)/lib -lnetcdf -L$(NETLIB_LAPACK_PATH)/lib/intel64 -lmkl -ldl </append>
  	  </SLIBS>
  	</compiler>

  ```

  **File :** ~/.cime/config\_compilers.xml

  ```
  <?xml version="1.0"?>

  	<compiler MACH="rorqual">
  	  <CPPDEFS>
  	    <append MODEL="gptl"> -DHAVE_NANOTIME -DBIT64 -DHAVE_VPRINTF -DHAVE_BACKTRACE -DHAVE_SLASHPROC -DHAVE_COMM_F2C -DHAVE_TIMES -DHAVE_GETTIMEOFDAY </append>
  	  </CPPDEFS>
  	  <NETCDF_PATH>$ENV{NETCDF_FORTRAN_ROOT}</NETCDF_PATH>
  	  <PIO_FILESYSTEM_HINTS>lustre</PIO_FILESYSTEM_HINTS>
  	  <PNETCDF_PATH>$ENV{PARALLEL_NETCDF_ROOT}</PNETCDF_PATH>
  	  <SLIBS>
  	    <append>-L$(NETCDF_PATH)/lib -lnetcdff -L$(NETCDF_C_ROOT)/lib -lnetcdf -L$(NETLIB_LAPACK_PATH)/lib/intel64 -lmkl -ldl </append>
  	  </SLIBS>
  	</compiler>

  ```
- Validate your XML compiler file with the following commands:

  ```
  [name@server ~]$ xmllint --noout --schema /path/to/CESM/cime/config/xml_schemas/config_compilers_v2.xsd ~/.cime/config_compilers.xml
  /home/name/.cime/config_compilers.xml validates

  ```

## Creating a test case

The following commands assume the default model `cesm` and the `current` machine:

```
[name@server ~]$ mkdir -p $SCRATCH/cesm/inputdata
[name@server ~]$ mkdir -p $SCRATCH/cesm/output
[name@server ~]$ /path/to/CESM/cime/scripts/create_newcase --case test_case --compset IHistClm50Bgc --res f19_g17
[name@server ~]$ cd test_case

```

```
[name@server test_case]$ ./case.setup
[name@server test_case]$ ./case.build
[name@server test_case]$ ./check_input_data --download

```

```
[name@server test_case]$ ./preview_run
[name@server test_case]$ ./case.submit

```

# Reference

- [Main website](https://www.cesm.ucar.edu/)
  - [CESM Quickstart Guide (CESM2.1)](https://escomp.github.io/CESM/versions/cesm2.1/html/)
  - [CESM Coupled Model XML Files](https://esmci.github.io/cime/versions/maint-5.6/html/xml_files/cesm.html)