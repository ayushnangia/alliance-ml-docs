# Symbolic algebra software

Other languages:

- English
- [français](Symbolic_algebra_software_fr.md)

Symbolic algebra software is a program, often accessible as an interactive environment, that is able to work directly with symbolic expressions (derivatives, integrals and so forth) and permits exact arithmetic (e.g. exp(-i\*pi/2) = -i) as well as other formal operations that arise in domains like number theory, group theory, differential geometry, commutative algebra and so forth. Most such programs also permit the use of approximate numerical calculations using floating point numbers for handling problems that are analytically intractable. Some well-known symbolic algebra software packages are the commercial products [Mathematica](http://www.wolfram.com/mathematica/) and [Maple](http://www.maplesoft.com/), neither of which is available on our clusters but which you can install in your home directory if your license for the software allows this. An open source alternative, [SageMath](https://www.sagemath.org/), can however be used by loading the appropriate module:

```
[name@server ~]$ module load sagemath/9.3

```

Afterwards you can then run the software interactively, e.g.

```
[name@server ~]$ sage
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 9.3, Release Date: 2021-05-09                     │
│ Using Python 3.8.10. Type "help()" for help.                       │
└────────────────────────────────────────────────────────────────────┘
sage:

```

Additional open source software that may be of interest and which is available on the clusters as a [module](Utiliser_des_modules.md) includes the [Number Theory Library (NTL)](https://www.shoup.net/ntl/) (`ntl`), [SINGULAR](https://www.singular.uni-kl.de/) (`singular`), [Macaulay2](https://faculty.math.illinois.edu/Macaulay2/) (`m2`) and [PARI/GP](http://pari.math.u-bordeaux.fr/) (`pari-gp`).