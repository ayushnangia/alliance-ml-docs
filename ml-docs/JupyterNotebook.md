# JupyterNotebook

Other languages:

- English
- [français](JupyterNotebook_fr.md)

Advanced material

This page is for advanced users. Please see [JupyterHub](JupyterHub.md) instead.

## Introduction

"Project Jupyter is a non-profit, open-source project, born out of the IPython Project in 2014 as it evolved to support interactive data science and scientific computing across all programming languages."[1]

"The Jupyter Notebook is an open-source web application that allows you to create and share documents that contain live code, equations, visualizations and narrative text."[2]

You can run Jupyter Notebook on a compute node or on a login node (not recommended). Note that login nodes impose various user- and process-based limits, so applications running there may be killed if they consume too much CPU time or memory. To use a compute node you will have to submit a job requesting the number of CPUs (and optionally GPUs), the amount of memory, and the run time. Here, we give instructions to submit a Jupyter Notebook job.

**Other information:**

- Since Jupyter Notebook is the older Jupyter interface, please consider installing **[JupyterLab](Advanced_Jupyter_configuration.md)** instead.
- If you are instead looking for a preconfigured Jupyter environment, please see the **[Jupyter](Jupyter.md)** page.

## Installing Jupyter Notebook

These instructions install Jupyter Notebook with the `pip` command in a [Python virtual environment](Python.md#Creating_and_using_a_virtual_environment) in your home directory. The following instructions are for Python 3.6, but you can also install the application for a different version by loading a different Python module.

1. Load the Python module.

   ```
   [name@server ~]$ module load python/3.7

   ```
2. Create a new Python virtual environment.

   ```
   [name@server ~]$ virtualenv $HOME/jupyter_py3

   ```
3. Activate your newly created Python virtual environment.

   ```
   [name@server ~]$ source $HOME/jupyter_py3/bin/activate

   ```
4. Install Jupyter Notebook in your new virtual environment.

   ```
   (jupyter_py3) [name@server ~]$ pip install --no-index --upgrade pip
   (jupyter_py3) [name@server ~]$ pip install --no-index jupyter

   ```
5. In the virtual environment, create a wrapper script that launches Jupyter Notebook.

   ```
   (jupyter_py3)_[name@server ~]$ echo -e '#!/bin/bash\nexport JUPYTER_RUNTIME_DIR=$SLURM_TMPDIR/jupyter\njupyter notebook --ip $(hostname -f) --no-browser' > $VIRTUAL_ENV/bin/notebook.sh

   ```
6. Finally, make the script executable.

   ```
   (jupyter_py3)_[name@server ~]$ chmod u+x $VIRTUAL_ENV/bin/notebook.sh

   ```

## Installing extensions

Extensions allow you to add functionalities and modify the application’s user interface.

### Jupyter Lmod

[Jupyter Lmod](https://github.com/cmd-ntrf/jupyter-lmod) is an extension that allows you to interact with environment modules before launching kernels. The extension uses the Lmod's Python interface to accomplish module-related tasks like loading, unloading, saving a collection, etc.

```
(jupyter_py3)_[name@server ~]$ pip install jupyterlmod
(jupyter_py3)_[name@server ~]$ jupyter nbextension install --py jupyterlmod --sys-prefix
(jupyter_py3)_[name@server ~]$ jupyter nbextension enable --py jupyterlmod --sys-prefix
(jupyter_py3)_[name@server ~]$ jupyter serverextension enable --py jupyterlmod --sys-prefix

```

### Proxy web services

[nbserverproxy](https://github.com/jupyterhub/nbserverproxy) enables users to reach arbitrary web services running within their spawned Jupyter server. This is useful to access web services that are listening only on a port of the localhost like [TensorBoard](https://www.tensorflow.org/programmers_guide/summaries_and_tensorboard).

```
(jupyter_py3)_[name@server ~]$ pip install nbserverproxy
(jupyter_py3)_[name@server ~]$ jupyter serverextension enable --py nbserverproxy --sys-prefix

```

#### Example

In Jupyter, a user starts a web service via 'Terminal' in the *New* dropdown list:

```
[name@server ~]$ tensorboard --port=8008

```

The service is proxied off of /proxy/ at [https://address.of.notebook.server/user/theuser/proxy/8008](https://address.of.notebook.server/user/theuser/proxy/8008).

### RStudio Launcher

Jupyter Notebook can start an RStudio session that uses Jupyter Notebook's token authentication system. RStudio Launcher adds an *RStudio Session* option to the Jupyter Notebook *New* dropdown list.

**Note:** the installation procedure below only works with the `StdEnv/2016.4` and `StdEnv/2018.3` software environments.

```
(jupyter_py3)_[name@server ~]$ pip install nbserverproxy
(jupyter_py3)_[name@server ~]$ pip install https://github.com/jupyterhub/nbrsessionproxy/archive/v0.8.0.zip
(jupyter_py3)_[name@server ~]$ jupyter serverextension enable --py nbserverproxy --sys-prefix
(jupyter_py3)_[name@server ~]$ jupyter nbextension install --py nbrsessionproxy --sys-prefix
(jupyter_py3)_[name@server ~]$ jupyter nbextension enable --py nbrsessionproxy --sys-prefix
(jupyter_py3)_[name@server ~]$ jupyter serverextension enable --py nbrsessionproxy --sys-prefix

```

## Activating the environment

Once you have installed Jupyter Notebook, you need only reload the Python module associated with your environment when you log into the cluster.

```
[name@server ~]$ module load python/3.7

```

Then, activate the virtual environment in which you have installed Jupyter Notebook.

```
[name@server ~]$ source $HOME/jupyter_py3/bin/activate

```

### RStudio Server (optional)

To use  RStudio Launcher, load the RStudio Server module.

```
(jupyter_py3)_[name@server ~]$ module load rstudio-server

```

## Starting Jupyter Notebook

To start the application, submit an interactive job. Adjust the parameters based on your needs. See [Running jobs](Scheduler.md) for more information.

```
(jupyter_py3)_[name@server ~]$ salloc --time=1:0:0 --ntasks=1 --cpus-per-task=2 --mem-per-cpu=1024M --account=def-yourpi srun $VIRTUAL_ENV/bin/notebook.sh
salloc: Granted job allocation 1422754
salloc: Waiting for resource configuration
salloc: Nodes cdr544 are ready for job
[I 14:07:08.661 NotebookApp] Serving notebooks from local directory: /home/fafor10
[I 14:07:08.662 NotebookApp] 0 active kernels
[I 14:07:08.662 NotebookApp] The Jupyter Notebook is running at:
[I 14:07:08.663 NotebookApp] http://cdr544.int.cedar.computecanada.ca:8888/?token=7ed7059fad64446f837567e32af8d20efa72e72476eb72ca
[I 14:07:08.663 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 14:07:08.669 NotebookApp]

Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://cdr544.int.cedar.computecanada.ca:8888/?token=7ed7059fad64446f837567e3

```

## Connecting to Jupyter Notebook

To access Jupyter Notebook running on a compute node from your web browser, you will need to create an [SSH tunnel](SSH_tunnelling.md) between the cluster and your computer since the compute nodes are not directly accessible from the Internet.

### From Linux or MacOS X

On a Linux or MacOS X system, we recommend using the [sshuttle](https://sshuttle.readthedocs.io) Python package.

On your computer, open a new terminal window and run the following `sshuttle` command to create the tunnel.

```
[name@my_computer ~]$ sshuttle --dns -Nr <username>@<cluster>.alliancecan.ca

```

In the preceding command substitute `<username>` by your username; and substitute `<cluster>` by the cluster you connected to launch your Jupyter Notebook.

Then, copy and paste the provided URL into your browser. In the above example, this would be

```
 http://cdr544.int.cedar.computecanada.ca:8888/?token=7ed7059fad64446f837567e3

```

### From Windows

An [SSH tunnel](SSH_tunnelling.md) can be created from Windows using [MobaXTerm](Connecting_with_MobaXTerm.md) as follows. This will also work from any Unix system (MacOS, Linux, etc).

1. Open a new Terminal tab in MobaXTerm (Session 1) and connect to a cluster. Then follow the instructions in section  Starting Jupyter Notebook. At this point, you should have on your screen an URL with the following form.
   ```
   http://cdr544.int.cedar.computecanada.ca:8888/?token=7ed7059fad64446f837567e3
          └────────────────┬───────────────────┘        └──────────┬───────────┘
                     hostname:port                               token

   ```
2. Open a second Terminal tab in MobaXTerm (Session 2). In the following command, substitute `<hostname:port>` by its corresponding value from the URL you obtained in Session 1 (refer to the previous figure); substitute `<username>` by your username; and substitute `<cluster>` by the cluster you connected to in Session 1. Run the command.

   ```
   [name@my_computer ~]$ ssh -L 8888:<hostname:port> <username>@<cluster>.alliancecan.ca

   ```
3. Open your browser and go to
   ```
    http://localhost:8888/?token=<token>

   ```

   Replace `<token>` with its value from Session 1.

## Shutting down Jupyter Notebook

You can shut down the Jupyter Notebook server before the walltime limit by pressing Ctrl-C twice in the terminal that launched the interactive job.

If you used MobaXterm to create a tunnel, press Ctrl-D in Session 2 to shut down the tunnel.

## Adding kernels

It is possible to add kernels for other programming languages or Python versions different than the one running the Jupyter Notebook. Refer to [Making kernels for Jupyter](http://jupyter-client.readthedocs.io/en/latest/kernels.html) to learn more.

The installation of a new kernel is done in two steps.

1. Installation of the packages that will allow the language interpreter to communicate with Jupyter Notebook.
2. Creation of a file that will indicate to Jupyter Notebook how to initiate a communication channel with the language interpreter. This file is called a *kernel spec file*.

Each kernel spec file has to be created in its own subfolder inside a folder in your home directory with the following path  `~/.local/share/jupyter/kernels`. Jupyter Notebook does not create this folder, so the first step in all cases is to create it. You can use the following command.

```
[name@server ~]$ mkdir -p  ~/.local/share/jupyter/kernels

```

In the following sections, we provide a few examples of the kernel installation procedure.

### Julia

1. Load the [Julia](Julia.md) module.

   ```
   [name@server ~]$ module load julia

   ```
2. Activate the Jupyter Notebook virtual environment.

   ```
   [name@server ~]$ source $HOME/jupyter_py3/bin/activate

   ```
3. Install IJulia.

   ```
   (jupyter_py3)_[name@server ~]$ echo 'Pkg.add("IJulia")' | julia

   ```

For more information, see the [IJulia documentation](https://github.com/JuliaLang/IJulia.jl).

### Python

1. Load the Python module.

   ```
   [name@server ~]$ module load python/3.5

   ```
2. Create a new Python virtual environment.

   ```
   [name@server ~]$ virtualenv $HOME/jupyter_py3.5

   ```
3. Activate your newly created Python virtual environment.

   ```
   [name@server ~]$ source $HOME/jupyter_py3.5/bin/activate

   ```
4. Install the `ipykernel` library.

   ```
   (jupyter_py3.5)_[name@server ~]$ pip install ipykernel

   ```
5. Generate the kernel spec file. Substitute `<unique_name>` by a name that will uniquely identify your kernel.

   ```
   (jupyter_py3.5)_[name@server ~]$ python -m ipykernel install --user --name <unique_name> --display-name "Python 3.5 Kernel"

   ```
6. Deactivate the virtual environment.

   ```
   (jupyter_py3.5)_[name@server ~]$ deactivate

   ```

For more information, see the [ipykernel documentation](http://ipython.readthedocs.io/en/stable/install/kernel_install.html).

### R

1. Load the R module.

   ```
   [name@server ~]$ module load r

   ```
2. Activate the Jupyter Notebook virtual environment.

   ```
   [name@server ~]$ source $HOME/jupyter_py3/bin/activate

   ```
3. Install the R kernel dependencies.

   ```
   (jupyter_py3)_[name@server ~]$ R -e "install.packages(c('crayon', 'pbdZMQ', 'devtools'), repos='http://cran.us.r-project.org')"

   ```
4. Install the R kernel.

   ```
   (jupyter_py3)_[name@server ~]$ R -e "devtools::install_github(paste0('IRkernel/', c('repr', 'IRdisplay', 'IRkernel')))"

   ```
5. Install the R kernel spec file.

   ```
   (jupyter_py3)_[name@server ~]$ R -e "IRkernel::installspec()"

   ```

For more information, see the [IRKernel documentation](https://irkernel.github.io/docs/).

## References

1. ↑ [http://jupyter.org/about.html](http://jupyter.org/about.html)
2. ↑ [http://www.jupyter.org/](http://www.jupyter.org/)