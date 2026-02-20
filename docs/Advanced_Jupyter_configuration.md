# Advanced Jupyter configuration

Other languages:

- English
- [français](Advanced_Jupyter_configuration_fr.md)

Not recommended

The content of this page is for advanced users only. It is seldom tested, and is not recommended. Consider using our preconfigured [JupyterLab](JupyterLab.md) instead.

# Introduction

Running notebooks

Jupyter Lab and notebooks are meant for **short** interactive tasks such as testing, debugging or quickly visualize data (few minutes). Running longer analysis must be done in an [non-interactive job (sbatch)](Scheduler.md#Use_sbatch_to_submit_jobs).
See also how to run notebooks as python scripts below.

- **Project Jupyter**: "a non-profit, open-source project, born out of the IPython Project in 2014 as it evolved to support interactive data science and scientific computing across all programming languages."[1]
- **JupyterLab**: "a web-based interactive development environment for notebooks, code, and data. Its flexible interface allows users to configure and arrange workflows in data science, scientific computing, computational journalism, and machine learning. A modular design allows for extensions that expand and enrich functionality."[2]

A JupyterLab server should only run on a compute node or on a cloud instance; cluster login nodes are not a good choice because they impose various limits which can stop applications if they consume too much CPU time or memory. In the case of using a compute node, users can reserve compute resources by [submitting a job](Scheduler.md) that requests a specific number of CPUs (and optionally GPUs), an amount of memory and the run time. **In this page, we give detailed instructions on how to configure and submit a JupyterLab job on any national cluster.**

If you are instead looking for a preconfigured Jupyter environment, please check the [Jupyter](Jupyter.md) page.

# Installing JupyterLab

These instructions install JupyterLab with the `pip` command in a
[Python virtual environment](Python.md#Creating_and_using_a_virtual_environment):

1. If you do not have an existing Python virtual environment, create one. Then, activate it:
   1. Load a Python module, either the default one (as shown below) or
      a specific version (see available versions with `module avail python`):

      ```
      [name@server ~]$ module load python

      ```

      **If you intend to use RStudio Server**, make sure to load `rstudio-server` first:

      ```
      [name@server ~]$ module load rstudio-server python

      ```
   2. Create a new Python virtual environment:

      ```
      [name@server ~]$ virtualenv --no-download $HOME/jupyter_py3

      ```
   3. Activate your newly created Python virtual environment:

      ```
      [name@server ~]$ source $HOME/jupyter_py3/bin/activate

      ```
2. Install JupyterLab in your new virtual environment (note: it takes a few minutes):

   ```
   (jupyter_py3) [name@server ~]$ pip install --no-index --upgrade pip
   (jupyter_py3) [name@server ~]$ pip install --no-index jupyterlab

   ```
3. In the virtual environment, create a wrapper script that launches JupyterLab:

   ```
   (jupyter_py3) [name@server ~]$ echo -e '#!/bin/bash\nunset XDG_RUNTIME_DIR\njupyter lab --ip $(hostname -f) --no-browser' > $VIRTUAL_ENV/bin/jupyterlab.sh

   ```
4. Finally, make the script executable:

   ```
   (jupyter_py3) [name@server ~]$ chmod u+x $VIRTUAL_ENV/bin/jupyterlab.sh

   ```

# Installing extensions

Extensions allow you to add functionalities and modify the JupyterLab’s user interface.

### Jupyter Lmod

[Jupyter Lmod](https://github.com/cmd-ntrf/jupyter-lmod) is an extension that allows you to interact with environment modules before launching kernels. The extension uses the Lmod's Python interface to accomplish module-related tasks like loading, unloading, saving a collection, etc.

The following commands will install and enable the Jupyter Lmod extension in your environment (note: the third command takes a few minutes to complete):

```
(jupyter_py3) [name@server ~]$ module load nodejs
(jupyter_py3) [name@server ~]$ pip install jupyterlmod
(jupyter_py3) [name@server ~]$ jupyter labextension install jupyterlab-lmod

```

Instructions on how to manage loaded *software* modules in the JupyterLab interface are provided in the [JupyterHub page](JupyterHub.md#JupyterLab).

### RStudio Server

The RStudio Server allows you to develop R codes in an RStudio environment that appears in your web browser in a separate tab. Based on the above Installing JupyterLab procedure, there are a few differences:

1. Load the `rstudio-server` module **before** the `python` module **and before creating a new virtual environment**:

   ```
   [name@server ~]$ module load rstudio-server python

   ```
2. Once Jupyter Lab is installed in the new virtual environment, install the Jupyter RSession proxy:

   ```
   (jupyter_py3) [name@server ~]$ pip install --no-index jupyter-rsession-proxy

   ```

All other configuration and usage steps are the same. In JupyterLab, you should see an RStudio application in the *Launcher* tab.

# Using your installation

## Activating the environment

Make sure the Python virtual environment in which you have installed JupyterLab is activated.

For example, when you log onto the cluster, you have to activate it again with:

```
[name@server ~]$ source $HOME/jupyter_py3/bin/activate

```

To verify that your environment is ready, you can get a list of installed `jupyter*` packages with the following command:

```
(jupyter_py3) [name@server ~]$ pip freeze | grep jupyter
jupyter-client==7.1.0+computecanada
jupyter-core==4.9.1+computecanada
jupyter-server==1.9.0+computecanada
jupyterlab==3.1.7+computecanada
jupyterlab-pygments==0.1.2+computecanada
jupyterlab-server==2.3.0+computecanada

```

## Starting JupyterLab

To start a JupyterLab server, submit an interactive job with `salloc`. Adjust the parameters based on your needs. See [Running jobs](Scheduler.md) for more information.

```
(jupyter_py3) [name@server ~]$ salloc --time=1:0:0 --ntasks=1 --cpus-per-task=2 --mem-per-cpu=1024M --account=def-yourpi srun $VIRTUAL_ENV/bin/jupyterlab.sh
...
[I 2021-12-06 10:37:14.262 ServerApp] jupyterlab | extension was successfully linked.
...
[I 2021-12-06 10:37:39.259 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2021-12-06 10:37:39.356 ServerApp]

    To access the server, open this file in a browser:
        file:///home/name/.local/share/jupyter/runtime/jpserver-198146-open.html
    Or copy and paste one of these URLs:
        http://node_name.int.cluster.computecanada.ca:8888/lab?token=101c3688298e78ab554ef86d93a196deaf5bcd2728fad4eb
     or http://127.0.0.1:8888/lab?token=101c3688298e78ab554ef86d93a196deaf5bcd2728fad4eb

```

## Connecting to JupyterLab

To access JupyterLab running on a compute node from your web browser, you will need to create an [SSH tunnel](SSH_tunnelling.md) from your computer through the cluster since the compute nodes are not directly accessible from the internet.

### From Linux or macOS

On a Linux or macOS system, we recommend using the [sshuttle](https://sshuttle.readthedocs.io) Python package.

On your computer, open a new terminal window and create the SSH tunnel with the following `sshuttle` command where `<username>` must be replaced with your Alliance account username, and `<cluster>` by the cluster on which you have launched JupyterLab:

```
[name@local ~]$ sshuttle --dns -Nr <username>@<cluster>.alliancecan.ca

```

Then, copy and paste the first provided HTTP address into your web browser. In the above `salloc` example, this would be:

```
http://node_name.int.cluster.alliancecan.ca:8888/lab?token=101c3688298e78ab554ef86d93a196deaf5bcd2728fad4eb

```

### From Windows

An [SSH tunnel](SSH_tunnelling.md) can be created from Windows using [MobaXTerm](Connecting_with_MobaXTerm.md) as follows. Note: this procedure also works from any terminal that supports the `ssh` command.

1. Once JupyterLab is launched on a compute node (see Starting JupyterLab), you can extract the `hostname:port` and the `token` from the first provided HTTP address. For example:
   ```
   http://node_name.int.cluster.alliancecan.ca:8888/lab?token=101c368829...2728fad4eb
          └────────────────────┬────────────────────┘           └──────────┬──────────┘
                         hostname:port                                   token

   ```
2. Open a new Terminal tab in MobaXTerm. In the following command, replace `<hostname:port>` with its corresponding value (refer to the above figure), replace `<username>` with your Alliance account username, and replace `<cluster>` with the cluster on which you have launched JupyterLab:

   ```
   [name@local ~]$ ssh -L 8888:<hostname:port> <username>@<cluster>.alliancecan.ca

   ```
3. Open your web browser and go to the following address where `<token>` must be replaced with the alphanumerical value extracted from the above figure:
   ```
   http://localhost:8888/?token=<token>

   ```

## Shutting down JupyterLab

You can shut down the JupyterLab server before the walltime limit by pressing **Ctrl-C twice** in the terminal that launched the interactive job.

If you have used MobaXterm to create an SSH tunnel, press **Ctrl-D** to shut down the tunnel.

# Adding kernels

It is possible to add kernels for other programming languages, for a different Python version or for a persistent virtual environment that has all required packages and libraries for your project. Refer to [Making kernels for Jupyter](http://jupyter-client.readthedocs.io/en/latest/kernels.html) to learn more.

The installation of a new kernel is done in two steps:

1. Installation of the packages that will allow the language interpreter to communicate with the Jupyter interface.
2. Creation of a file that will indicate to JupyterLab how to initiate a communication channel with the language interpreter. This file is called a *kernel spec file*, and it will be saved in a subfolder of `~/.local/share/jupyter/kernels`.

In the following sections, we provide a few examples of the kernel installation procedure.

## Julia Kernel

Prerequisites:

1. The configuration of a Julia kernel depends on a Python virtual environment and a `kernels` folder. If you do not have these dependencies, make sure to follow the first few instructions listed in **Python kernel** (note: no Python kernel required).
2. Since the installation of Julia packages requires an access to the internet, the configuration of a Julia kernel must be done in a **[remote shell session on a login node](SSH.md)**.

Once you have a Python virtual environment available and activated, you may configure the Julia kernel:

1. Load the **[Julia](Julia.md)** module:

   ```
   (jupyter_py3) [name@server ~]$ module load julia

   ```
2. Install IJulia:

   ```
   (jupyter_py3) [name@server ~]$ echo -e 'using Pkg\nPkg.add("IJulia")' | julia

   ```
3. **Important**: start or restart a new JupyterLab session before using the Julia kernel.

For more information, see the [IJulia documentation](https://github.com/JuliaLang/IJulia.jl).

### Installing more Julia packages

As in the above installation procedure, it is required to install Julia packages from a login node, but the Python virtual environment could be deactivated:

1. Make sure the same Julia module is loaded:

   ```
   [name@server ~]$ module load julia

   ```
2. Install any required package. For example with `Glob`:

   ```
   [name@server ~]$ echo -e 'using Pkg\nPkg.add("Glob")' | julia

   ```
3. The newly installed Julia packages should already be usable in a notebook executed by the Julia kernel.

## Python kernel

In a terminal with an active session on the remote server,
you may configure a [Python virtual environment](Python.md#Creating_and_using_a_virtual_environment) with all the required [Python modules](Wheels.md)
and a custom Python kernel for JupyterLab.
Here are the initial steps for the simplest Jupyter configuration
in a new Python virtual environment:

1. If you do not have a Python virtual environment, create one. Then, activate it:

1. Start from a clean Bash environment (this is only required if you are using the Jupyter *Terminal* via [JupyterHub](JupyterHub.md) for the creation and configuration of the Python kernel):

   ```
   [name@server ~]$ env -i HOME=$HOME bash -l

   ```
2. Load a Python module:

   ```
   [name@server ~]$ module load python

   ```
3. Create a new Python virtual environment:

   ```
   [name@server ~]$ virtualenv --no-download $HOME/jupyter_py3

   ```
4. Activate your newly created Python virtual environment:

   ```
   [name@server ~]$ source $HOME/jupyter_py3/bin/activate

   ```

2. Create the common `kernels` folder, which is used by all kernels you want to install:

   ```
   (jupyter_py3) [name@server ~]$ mkdir -p ~/.local/share/jupyter/kernels

   ```
3. Finally, install the Python kernel:
   1. Install the `ipykernel` library:

      ```
      (jupyter_py3) [name@server ~]$ pip install --no-index ipykernel

      ```
   2. Generate the kernel spec file. Replace `<unique_name>` with a name that will uniquely identify your kernel:

      ```
      (jupyter_py3) [name@server ~]$ python -m ipykernel install --user --name <unique_name> --display-name "Python 3.x Kernel"

      ```
4. **Important**: start or restart a new JupyterLab session before using the Python kernel.

For more information, see the [ipykernel documentation](http://ipython.readthedocs.io/en/stable/install/kernel_install.html).

### Installing more Python libraries

Based on the Python virtual environment configured in the previous section:

1. If you are using the Jupyter *Terminal* via [JupyterHub](JupyterHub.md), make sure the activated Python virtual environment is running in a clean Bash environment. See the above section for details.
2. Install any required library. For example, `numpy`:

   ```
   (jupyter_py3) [name@server ~]$ pip install --no-index numpy

   ```
3. The newly installed Python libraries can now be imported in any notebook using the `Python 3.x Kernel`.

## R Kernel

Prerequisites:

1. The configuration of an R kernel depends on a Python virtual environment and a `kernels` folder. If you do not have these dependencies, make sure to follow the first few instructions listed in **Python kernel** (note: no Python kernel required).
2. Since the installation of R packages requires an access to **[CRAN](https://cran.r-project.org/)**, the configuration of an R kernel must be done in a **[remote shell session on a login node](SSH.md)**.

Once you have a Python virtual environment available and activated, you may configure the R kernel:

1. Load an R module:

   ```
   (jupyter_py3) [name@server ~]$ module load r/4.1

   ```
2. Install the R kernel dependencies (`crayon`, `pbdZMQ`, `devtools`) - this will take up to 10 minutes, and packages should be installed in a local directory like `~/R/x86_64-pc-linux-gnu-library/4.1`:

   ```
   (jupyter_py3) [name@server ~]$ R --no-save
   > install.packages(c('crayon', 'pbdZMQ', 'devtools'), repos='http://cran.us.r-project.org')

   ```
3. Install the R kernel.

   ```
   > devtools::install_github(paste0('IRkernel/', c('repr', 'IRdisplay', 'IRkernel')))

   ```
4. Install the R kernel spec file.

   ```
   > IRkernel::installspec()

   ```
5. **Important**: Start or restart a new JupyterLab session before using the R kernel.

For more information, see the [IRkernel documentation](https://irkernel.github.io/docs/).

### Installing more R packages

The installation of R packages cannot be done from notebooks because there is no access to CRAN.
As in the above installation procedure, it is required to install R packages from a login node, but the Python virtual environment could be deactivated:

1. Make sure the same R module is loaded:

   ```
   [name@server ~]$ module load r/4.1

   ```
2. Start the R shell and install any required package. For example with `doParallel`:

   ```
   [name@server ~]$ R --no-save
   > install.packages('doParallel', repos='http://cran.us.r-project.org')

   ```
3. The newly installed R packages should already be usable in a notebook executed by the R kernel.

# Running notebooks as Python scripts

For longer run or analysis, we need to submit a [non-interactive job](Scheduler.md#Use_sbatch_to_submit_jobs). We then need to convert our notebook to a Python script, create a submission script and submit it.

1. From the login node, create and activate a [virtual environment](Python.md#Creating_and_using_a_virtual_environment), then install nbconvert if not already available.

```
(venv) [name@server ~]$ pip install --no-index nbconvert

```

2. Convert the notebook (or all notebooks) to Python scripts.

```
(venv) [name@server ~]$ jupyter nbconvert --to python mynotebook.ipynb

```

3. Create your submission script, and submit your job.

In your submission script, run your converted notebook with:

```
python mynotebook.py

```

and submit your non-interactive job:

```
[name@server ~]$ sbatch my-submit.sh

```

# References

1. ↑ [https://jupyter.org/about.html](https://jupyter.org/about.html)
2. ↑ [https://jupyter.org/](https://jupyter.org/)