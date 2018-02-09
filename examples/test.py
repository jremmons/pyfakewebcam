import pyfakewebcam
import scipy.misc as misc
import numpy as np
import time 

cam = pyfakewebcam.FakeWebcam('/dev/video1', 640, 512)

cam.print_capabilities()

im0 = misc.imread("examples/doge1.jpg")
im1 = np.zeros((512,640,3), dtype=np.uint8)

while True:
    cam.schedule_frame(im0)
    time.sleep(1/60)

    cam.schedule_frame(im1)
    time.sleep(1/60)
