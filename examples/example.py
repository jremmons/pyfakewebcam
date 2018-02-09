import pyfakewebcam
import scipy.misc as misc
import numpy as np
import time
import timeit

cam = pyfakewebcam.FakeWebcam('/dev/video1', 640, 512)

cam.print_capabilities()

im0 = misc.imread("doge1.jpg")
im1 = np.zeros((512,640,3), dtype=np.uint8)

while True:

    t1 = timeit.default_timer() 
    cam.schedule_frame(im0)
    t2 = timeit.default_timer() 
    print('write time:{}'.format(t2-t1))

    time.sleep(1/60)

    t1 = timeit.default_timer() 
    cam.schedule_frame(im1)
    t2 = timeit.default_timer() 
    print('write time:{}'.format(t2-t1))
    time.sleep(1/60)
