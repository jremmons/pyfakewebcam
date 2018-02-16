import pyfakewebcam
import numpy as np
import time
import timeit

from PIL import Image

cam = pyfakewebcam.FakeWebcam('/dev/video1', 1280, 720)

cam.print_capabilities()

im0 = np.array( Image.open("doge1.jpg") )
im1 = np.zeros((720,1280,3), dtype=np.uint8)

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
