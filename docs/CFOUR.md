# CFOUR

Other languages:

- English
- [français](CFOUR_fr.md)

# Introduction

"**CFOUR** (Coupled-Cluster techniques for Computational Chemistry) is a program package for performing high-level quantum chemical calculations on atoms and molecules. The major strength of the program suite is its rather sophisticated arsenal of high-level *ab-initio* methods for the calculation of atomic and molecular properties. Virtually all approaches based on Møller-Plesset (MP) perturbation theory and the coupled-cluster approximation (CC) are available; most of these have complementary analytic derivative approaches within the package as well."

"**CFOUR** is not a commercial code. It is rather a program that is undergoing development; new techniques and improvements are constantly being made." See [the CFOUR web site](http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.HomePage) for more information.

# License limitations

The Alliance has signed a [license](http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.Download) agreement with [Prof. Dr. J. Gauss](https://www.tc.uni-mainz.de/prof-dr-juergen-gauss/) who acts for the developers of the CFOUR Software.

In order to use the current installed version on the Alliance systems, each user must agree to certain conditions. Please [contact support](Technical_Support.md) with a copy of the following statement:

1. I will use CFOUR only for academic research.
2. I will not copy the CFOUR software, nor make it available to anyone else.
3. I will properly acknowledge original papers related to CFOUR and to the Alliance in my publications (see the license form for more details).
4. I understand that the agreement for using CFOUR can be terminated by one of the parties: CFOUR developers or the Alliance.
5. I will notify the Alliance of any change in the above acknowledgement.

When your statement is received, we will allow you to access the program.

# Module

You can access the MPI version of CFOUR by loading a [module](Utiliser_des_modules.md).

```
module load intel/2023.2.1  openmpi/4.1.5 cfour-mpi/2.1

```

For the serial version, use:

```
module load intel/2023.2.1 cfour/2.1

```

There is a mailing list as a forum for user experiences with the CFOUR program system. For how to subscribe and other information, see [this page](http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.MailingList).

## Examples and job scripts

To run CFOUR, you need to have at least the input file [ZMAT](http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.InputFileZMAT) with all information concerning geometry, requested quantum-chemical method, basis set, etc. The second file is [GENBAS](http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.Basis-setFileGENBAS) that contains the required information for the basis sets available to the user. If GENBAS is not present in the directory from where you start your job, CFOUR will create a symlink and use the existing file provided by the module. The file is located at: `$EBROOTCFOUR/basis/GENBAS`.

INPUTSerial jobMPI job

**File :** ZMAT

```
Acetylene, CCSD/DZP excited-state geometry optimization
C                                                                              
C 1 RCC*
H 1 RCH* 2 A*
H 2 RCH* 1 A* 3 D180
                                                                               
RCC=1.36
RCH=1.08
A=124.
D180=180.
                                                                               
*ACES2(CALC=CCSD,BASIS=DZP,EXCITE=EOMEE                                     
ESTATE_CONV=10,CONV=10,SCF_CONV=10,CC_CONV=10,LINEQ_CONV=10,ZETA_CONV=10)                                      
                                                                               
%excite*                                                                       
1                                                                              
1                                                                              
1 7 0 8 0 1.0
```

**File :** run\_cfour\_serial.sh

```
#!/bin/bash
#SBATCH --account=def-someacct   # replace this with your own account
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2500M      # memory; default unit is megabytes.
#SBATCH --time=0-00:30           # time (DD-HH:MM).

# Load the module:

module load intel/2023.2.1 cfour/2.1

echo "Starting run at: `date`"

CFOUROUTPUT="cfour-output.txt"
export CFOUR_NUM_CORES=1

xcfour > ${CFOUROUTPUT} 

# Clean the symlink:
if [[ -L "GENBAS" ]]; then unlink GENBAS; fi

echo "Program finished with exit code $? at: `date`"

```

**File :** run-cfour-mpi.sh

```
#!/bin/bash
#SBATCH --account=def-someacct   # replace this with your own account
#SBATCH --ntasks-per-node=4
#SBATCH --mem-per-cpu=2500M      # memory; default unit is megabytes.
#SBATCH --time=0-00:30           # time (DD-HH:MM).

# Load the module:

module load intel/2023.2.1  openmpi/4.1.5 cfour-mpi/2.1

echo "Starting run at: `date`"

CFOUROUTPUT="cfour-output.txt"
export CFOUR_NUM_CORES=${SLURM_NTASKS}

xcfour > ${CFOUROUTPUT} 

# Clean the symlink:
if [[ -L "GENBAS" ]]; then unlink GENBAS; fi

echo "Program finished with exit code $? at: `date`"

```

# Related links

- [Manual](http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.Manual)
- [Features](http://slater.chemie.uni-mainz.de/cfour/index.php?n=Main.Features)