# Tensorboard

Other languages:

- English
- [français](Tensorboard_fr.md)

TensorBoard is a suite of web applications for inspecting and understanding your AI and Machine Learning runs. It includes visual tools to track performance and evaluation metrics, profile code, explore intermediate layers inside models, visualize embeddings and more. Originally built for [TensorFlow](https://www.tensorflow.org/tensorboard/get_started), it also supports other frameworks such as [PyTorch](https://docs.pytorch.org/tutorials/intermediate/tensorboard_tutorial.html) and [Jax](https://docs.jaxstack.ai/en/latest/JAX_visualizing_models_metrics.html).

## On JupyterHub

On clusters where [JupyterHub](JupyterHub.md) is available, you can launch Tensorboard by clicking on the following icon on an active launcher tab:

[![](/mediawiki/images/thumb/d/d7/Tensorboard.png/300px-Tensorboard.png)](FileTensorboardpng.md)

This will open the application on a new tab on your web browser. Switch to that tab to start using Tensorboard.

Upon launching Tensorboard on JupyterHub, a directory $HOME/tensorboard\_logs will be created. This is the location where Tensorboard will look for data to display on your web browser, so you must make sure any calls to Tensorboard in your code write data to this directory. Failing to do so will result in no data being displayed on the Tensorboard tab on your browser. You can change the location of this directory by adding export TENSORBOARD\_LOGDIR=/some/other/path in your .bashrc.

For detailed examples on the many uses of Tensorboard, see the official documentation for your preferred AI framework:

- [PyTorch](https://docs.pytorch.org/tutorials/intermediate/tensorboard_tutorial.html)
- [TensorFlow](https://www.tensorflow.org/tensorboard/get_started)
- [Jax](https://docs.jaxstack.ai/en/latest/JAX_visualizing_models_metrics.html)