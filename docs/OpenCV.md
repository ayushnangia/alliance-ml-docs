# OpenCV

Other languages:

- English
- [français](OpenCV_fr.md)

[OpenCV](https://opencv.org/) (Open Source Computer Vision Library) is a library of programming functions mainly aimed at real-time computer vision.

## CUDA

OpenCV is also available with CUDA.

```
[name@server ~]$ module load gcc cuda opencv/X.Y.Z

```

where X.Y.Z represent the desired version.

## Extra modules

The module also contains the [extra modules (contrib)](https://github.com/opencv/opencv_contrib/tree/4.x/modules#an-overview-of-the-opencv_contrib-modules).

## Python bindings

The module contains bindings for multiple Python versions.
To discover which are the compatible Python versions, run

```
[name@server ~]$ module spider opencv/X.Y.Z

```

Or search directly *opencv\_python*, by running

```
[name@server ~]$ module spider opencv_python/X.Y.Z

```

where X.Y.Z represent the desired version.

### Usage

1. Load the required modules.

```
[name@server ~]$ module load gcc opencv/X.Y.Z python scipy-stack

```

where X.Y.Z represent the desired version.

2. Import OpenCV.

```
[name@server ~]$ python -c "import cv2"

```

If the command displays nothing, the import was successful.

#### Available Python packages

Other Python packages depend on OpenCV bindings in order to be installed.
OpenCV provides four different packages:

- `opencv_python`
- `opencv_contrib_python`
- `opencv_python_headless`
- `opencv_contrib_python_headless`

```
[name@server ~]$ pip list | grep opencv
opencv-contrib-python              4.5.5                  
opencv-contrib-python-headless     4.5.5                  
opencv-python                      4.5.5                  
opencv-python-headless             4.5.5

```

With the `opencv` module loaded, your package dependency for one of the OpenCV named will be satisfied.

## Use with OpenEXR

In order to read EXR files with OpenCV, the module must be activated through an environment variable.

```
[name@server ~]$ OPENCV_IO_ENABLE_OPENEXR=1 python <file>

```