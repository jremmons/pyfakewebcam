# pyfakewebcam

An API for writing RGB frames to a fake webcam device on Linux!

## installation

```
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
apt-get install python-opencv # provides a big performance improvement if installed
apt-get install ffmpeg
```

## performance

When I run the `examples/example.py` script on an Intel i7-3520M (2.9
GHz, turbos to 3.6 GHz), the time to schedule a single frame is **~2.5
milliseconds** (with opencv installed). You can use this library
without installing opencv, but it is about 10x slower; time to
schedule a frame without opencv is **~25 milliseconds** (RGB to YUV
conversion done with numpy operations).

## usage 

Insert the v4l2loopback kernel module.

```
modprobe v4l2loopback devices=1
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
    time.sleep(1/1)

    camera.schedule_frame(blue)
    time.sleep(1/1)
```

Run the following command to see the output of the fake webcam.
```
ffplay /dev/video1
```
