# pyfakewebcam

An API for writing RGB frames to a fake webcam device on Linux!

**Compatible with Python2.7 and Python3.x**

**Author:** John Emmons
**Email:** mail@johnemmons.com

**Disclaimer:** I wrote this project when I was a university
student. I now employed full time so I don't have time to keep things
update or add new features :(. Please feel free to fork!

## installation

```
# use pip to get the latest stable release
pip install pyfakewebcam

# use git to install the latest version
git clone https://github.com/jremmons/pyfakewebcam.git
cd pyfakewebcam
python setup.py install
```

## dependencies
```
# python
pip install numpy

# linux
apt-get install v4l2loopback-utils

# linux (optional)
apt-get install python-opencv # 10x performance improvement if installed (see below)
apt-get install ffmpeg # useful for debugging
```

## performance

When I run the `examples/example.py` script (640x360 resolution)
on an Intel i7-3520M (2.9GHz, turbos to 3.6 GHz), the time to
schedule a single frame is *~3 milliseconds* (with opencv
installed). **You can use this library without installing opencv**,
but it is almost 10x slower; time to schedule a frame without
opencv is *~26 milliseconds* (RGB to YUV conversion done with
numpy operations).

If your goal is to run at 30Hz (or slower) and ~26 milliseconds of
delay is acceptable in your application, then opencv may not be
necessary.

## usage

Insert the v4l2loopback kernel module.

```
modprobe v4l2loopback devices=2 # will create two fake webcam devices
```

Example code.

```python
# see red_blue.py in the examples dir
import time
import pyfakewebcam
import numpy as np

blue = np.zeros((480,640,3), dtype=np.uint8)
blue[:,:,2] = 255

red = np.zeros((480,640,3), dtype=np.uint8)
red[:,:,0] = 255

camera = pyfakewebcam.FakeWebcam('/dev/video1', 640, 480)

while True:

    camera.schedule_frame(red)
    time.sleep(1/30.0)

    camera.schedule_frame(blue)
    time.sleep(1/30.0)
```

Run the following command to see the output of the fake webcam.
```
ffplay /dev/video1
```
