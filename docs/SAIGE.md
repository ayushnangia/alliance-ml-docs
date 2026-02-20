# SAIGE

Other languages:

- English
- [français](SAIGE_fr.md)

[SAIGE](https://saigegit.github.io/SAIGE-doc/)
is an R package developed with Rcpp for genome-wide association tests in large-scale data sets and biobanks.

The method

- accounts for sample relatedness based on the generalized mixed models;

- allows for model fitting with either full or sparse genetic relationship matrix (GRM);

- works for quantitative and binary traits;

- handles case-control imbalance of binary traits;

- computationally efficient for large data sets;

- performs single-variant association tests;

- provides effect size estimation through Firth’s Bias-Reduced Logistic Regression;

- performs conditional association analysis.

This page discusses how to install SAIGE package 1.0.0.

## Installing SAIGE under the environment StdEnv/2020

1. Load the appropriate modules.

```
[name@server ~]$ module load StdEnv/2020 gcc/9.3.0 r/4.2.2 savvy/2.1.0 superlu/5.2.1 flexiblas/3.0.4

```

2. Create the installation directory.

```
[name@server ~]$ mkdir -p ~/.local/R/$EBVERSIONR/
[name@server ~]$ export R_LIBS=~/.local/R/$EBVERSIONR/

```

3. Install the [R dependencies](R.md#Installing_R_packages). It is important to install these exact versions. During installation, if you are prompted to install the latest version of any dependency, simply press Enter to decline.

```
[name@server ~]$ R -e 'install.packages("remotes", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("Rcpp", version="1.0.10", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("RcppParallel", version="5.1.6", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("data.table", version="1.17.8", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("RcppArmadillo", version="14.0.2-1", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("SPAtest", version="3.1.2", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("RcppEigen", version="0.3.3.9.3", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("BH", version="1.81.0-1", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("optparse", version="1.7.3", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("SKAT", version="2.2.5", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("MetaSKAT", version="0.82", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("qlcMatrix", version="0.9.5", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("RhpcBLASctl", version="0.23-42", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("RSQLite", version="2.3.8", repos="https://cloud.r-project.org/")'
[name@server ~]$ R -e 'remotes::install_version("dplyr", version="1.1.0", repos="https://cloud.r-project.org/")'

```

4. Download SAIGE version 1.0.0.

```
[name@server ~]$ git clone --recursive https://github.com/saigegit/SAIGE.git -b 1.0.0
[name@server ~]$ cd SAIGE/

```

5. Patch the installation.

```
[name@server ~]$ rm configure
[name@server ~]$ sed -i 's/llapack/lflexiblas/' src/Makevars

```

First, remove the *configure* file to avoid installing already available dependencies. Then, change the library name to correctly link to the *Makevars* file to make sure that the linking options will use FlexiBLAS. Doing so will prevent the i>unable to find -llapack error message displayed at installation. Read more information on [FlexiBLAS, BLAS and LAPACK](BLAS_and_LAPACK.md).

6. Compile and install.

```
[name@server ~]$ R CMD INSTALL .

```

7. Test that it is available.

```
[name@server ~]$ R -e 'library(SAIGE)'

```