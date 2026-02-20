# Keras

Other languages:

- English
- [français](Keras_fr.md)

"Keras is a high-level neural networks API, written in Python and capable of running on top of TensorFlow, CNTK, or Theano."[1]

If you are porting a Keras program to one of our clusters, you should follow [our tutorial on the subject](Tutoriel_Apprentissage_machine.md).

## Installing

1. Install [TensorFlow](TensorFlow.md), CNTK, or Theano in a Python [virtual environment](Python.md#Creating_and_using_a_virtual_environment).
2. Activate the Python virtual environment (named $HOME/tensorflow in our example).

   :   ```
       [name@server ~]$ source $HOME/tensorflow/bin/activate

       ```
3. Install Keras in your virtual environment.

   :   ```
       (tensorflow)_[name@server ~]$ pip install keras

       ```

### R package

This section details how to install Keras for R and use TensorFlow as the backend.

1. Install TensorFlow for R by following [these instructions](TensorFlow.md#R_package).
2. Follow the instructions from the parent section.
3. Load the required modules.

   :   ```
       [name@server ~]$ module load gcc/7.3.0 r/3.5.2

       ```
4. Launch R.

   :   ```
       [name@server ~]$ R

       ```
5. In R, install the Keras package with `devtools`.

   :   ```
       devtools::install_github('rstudio/keras')

       ```

You are then good to go. Do not call `install_keras()` in R, as Keras and TensorFlow have already been installed in your virtual environment with `pip`. To use the Keras package installed in your virtual environment, enter the following commands in R after the environment has been activated.

```
library(keras)
use_virtualenv(Sys.getenv('VIRTUAL_ENV'))

```

## References

1. ↑ [https://keras.io/](https://keras.io/)