# GDAL

Other languages:

- English
- [français](GDAL_fr.md)

[GDAL](https://www.gdal.org/) is an open source translator library for raster geospatial data formats.
It can be used as a a library, as which presents a single abstract data model to the calling application for all supported formats.
It also comes with a variety of useful command line utilities for data translation and processing.

GDAL is used by a [long list of software packages](https://gdal.org/software_using_gdal.html#software-using-gdal)
and its functionality can be used in scripts written in [Python](Python.md) or [R](R.md).

## Using GDAL from Python

GDAL functionality can be used via the [osgeo](https://gdal.org/api/python/osgeo.html) package,
which we install as an extension to the GDAL module. In order to use it, you need to load
a compatible Python module alongside the GDAL module.

### Using osgeo under StdEnv/2020

Check which Python modules are compatible with e.g. `gdal/3.5.1`:

```
[name@server ~]$  module whatis gdal/3.5.1
gdal/3.5.1          : Description: GDAL is a translator library for raster geospatial data formats...
gdal/3.5.1          : Homepage: https://www.gdal.org/
gdal/3.5.1          : URL: https://www.gdal.org/
gdal/3.5.1          : Compatible modules: python/3.8, python/3.9, python/3.10

```

We have the choice between Python 3.8, 3.9 and 3.10. Let's choose `python/3.10` for this.

```
[name@server ~]$  module load StdEnv/2020 gcc/9.3.0 python/3.10 gdal/3.5.1

```

**File :** osgeo\_gdal.py

```
#!/usr/bin/env python3
from osgeo import gdal

print("osgeo.gdal version:", gdal.__version__)
# osgeo.gdal version: 3.5.1

```

### Using osgeo under StdEnv/2023

Check which Python modules are compatible with e.g. `gdal/3.7.2`:

```
[name@server ~]$  module whatis gdal/3.7.2 
gdal/3.7.2          : Description: GDAL is a translator library for raster geospatial data formats...
 data translation and processing.
gdal/3.7.2          : Homepage: https://www.gdal.org/
gdal/3.7.2          : URL: https://www.gdal.org/
gdal/3.7.2          : Compatible modules: python/3.10, python/3.11
gdal/3.7.2          : Extensions: osgeo-3.7.2

```

We have the choice between Python 3.10 and 3.11. Let's choose `python/3.11` for this.

```
[name@server ~]$  module load StdEnv/2023 gcc/12.3 python/3.11 gdal/3.7.2

```

**File :** osgeo\_gdal.py

```
#!/usr/bin/env python3
from osgeo import gdal

print("osgeo.gdal version:", gdal.__version__)
# osgeo.gdal version: 3.7.2

```

## Using GDAL from R

Several [R-packages for Analysis of Spatial Data](https://cran.r-project.org/web/views/Spatial.html) directly depend on GDAL
as a System dependency. For example:

- [sf](https://CRAN.R-project.org/package=sf): Simple Features for R
- [terra](https://CRAN.R-project.org/package=terra): Spatial Data Analysis

The older package [rgdal](https://CRAN.R-project.org/package=rgdal) has been discontinued in favor of sf and terra.

### Installing `sf` and `terra` under StdEnv/2020

Installing these packages not only requires loading a `gdal` module, but also `udunits`
which is required by [units](https://CRAN.R-project.org/package=units).

**File :** install\_sf\_terra\_StdEnv2020.sh

```
# load required modules:
module load  StdEnv/2020  gcc/9.3.0  udunits/2.2.28  gdal/3.5.1  r/4.2.2

# create a local R library in $HOME:
mkdir -p $HOME/R/x86_64-pc-linux-gnu-library/4.2
export R_LIBS="$HOME/R/x86_64-pc-linux-gnu-library/4.2:$R_LIBS"

# install sf and terra from a Canadian CRAN mirror:
R -e "install.packages(c('sf', 'terra'), repos='https://mirror.csclub.uwaterloo.ca/CRAN/', dep=TRUE)"

```

### Installing `sf` and `terra` under StdEnv/2023

Note that under StdEnv/2023, in addition to modules `gdal` and `udunits`
also `hdf/4.3.1` is required.

**File :** install\_sf\_terra\_StdEnv2020.sh

```
# load required modules:
module load  StdEnv/2023  gcc/12.3  udunits/2.2.28  hdf/4.2.16  gdal/3.7.2  r/4.4.0

# create a local R library in $HOME:
mkdir -p $HOME/R/x86_64-pc-linux-gnu-library/4.4
export R_LIBS="$HOME/R/x86_64-pc-linux-gnu-library/4.4:$R_LIBS"

# install sf and terra from a Canadian CRAN mirror:
R -e "install.packages(c('sf', 'terra'), repos='https://mirror.csclub.uwaterloo.ca/CRAN/', dep=TRUE)"

```