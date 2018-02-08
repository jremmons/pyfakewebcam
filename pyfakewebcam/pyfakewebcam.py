
import os
import sys
import fcntl
import timeit
import time

import numpy as np
import pyfakewebcam.v4l2 as _v4l2
import scipy.misc as misc

class FakeWebcam:

    
    def __init__(self, video_device, width, height, channels=3, input_pixfmt='RGB'):
        
        if channels != 3:
            raise NotImplementedError('Code only supports inputs with 3 channels right now. You tried to intialize with {} channels'.format(channels))

        if input_pixfmt != 'RGB':
            raise NotImplementedError('Code only supports RGB pixfmt. You tried to intialize with {}'.format(input_pixfmt))
        
        if not os.path.exists(video_device):
            sys.stderr.write('\n--- Make sure the v4l2loopback kernel module is loaded ---\n')
            sys.stderr.write('sudo modprobe v4l2loopback devices=1\n\n')
            raise FileNotFoundError('device does not exist: {}'.format(video_device))

        self._video_device = os.open(video_device, os.O_WRONLY | os.O_SYNC)
                    
        self._settings = _v4l2.v4l2_format()
        self._settings.type = _v4l2.V4L2_BUF_TYPE_VIDEO_OUTPUT
        self._settings.fmt.pix.pixelformat = _v4l2.V4L2_PIX_FMT_YUYV
        self._settings.fmt.pix.width = width
        self._settings.fmt.pix.height = height
        self._settings.fmt.pix.field = _v4l2.V4L2_FIELD_NONE
        self._settings.fmt.pix.bytesperline = width * 2
        self._settings.fmt.pix.sizeimage = width * height * 2
        self._settings.fmt.pix.colorspace = _v4l2.V4L2_COLORSPACE_JPEG

        fcntl.ioctl(self._video_device, _v4l2.VIDIOC_S_FMT, self._settings)


    def print_capabilities(self):

        capability = _v4l2.v4l2_capability()
        print(("get capabilities result", (fcntl.ioctl(self._video_device, _v4l2.VIDIOC_QUERYCAP, capability))))
        print(("capabilities", hex(capability.capabilities)))
        print(("v4l2 driver: {}".format(capability.driver)))
        

    def schedule_frame(self, frame):

        sys.stderr.write('loading\n')
        im0 = misc.imread("doge1.jpg")

        sys.stderr.write('converting\n')
        buff0 = _convert2YUYV(self._settings.fmt.pix.sizeimage, self._settings.fmt.pix.bytesperline, im0)

        sys.stderr.write('loading\n')
        im1 = np.zeros((self._settings.fmt.pix.height, self._settings.fmt.pix.width, 3))
        sys.stderr.write('converting\n')
        t1 = timeit.default_timer()
        buff1 = _convert2YUYV(self._settings.fmt.pix.sizeimage, self._settings.fmt.pix.bytesperline, im1)
        t2 = timeit.default_timer()
        sys.stderr.write('conversion time: {}\n'.format(t2-t1))

        sys.stderr.write('looping\n')
        i = 0 
        while True:             
            t1 = timeit.default_timer()
            if i % 2 == 0:
                os.write(self._video_device, buff1)
            else:
                os.write(self._video_device, buff0)
                
            i += 1
            
            time.sleep(1/30.0)
            t2 = timeit.default_timer()
            sys.stderr.write('time: {}\n'.format(t2-t1))

def _convert2YUYV(sizeimage, bytesperline, im):
    '''
    This function is for debugging purposes only!
    It is too slow to be used for actually runs on the program (3 fps)
    '''
    
    sys.stderr.write('converting_internal\n')
    buff = np.zeros((sizeimage, ), dtype=np.uint8)
    imgrey = im[:,:,0] * 0.299 + im[:,:,1] * 0.587 + im[:,:,2] * 0.114
    Pb = im[:,:,0] * -0.168736 + im[:,:,1] * -0.331264 + im[:,:,2] * 0.5
    Pr = im[:,:,0] * 0.5 + im[:,:,1] * -0.418688 + im[:,:,2] * -0.081312
        
    sys.stderr.write('formating_internal\n')
    for y in range(imgrey.shape[0]):
        #Set lumenance
        cursor = y * bytesperline 
        for x in range(imgrey.shape[1]):
            try:
                buff[cursor] = imgrey[y, x]
            except IndexError:
                pass
            cursor += 2

        #Set color information for Cb
        cursor = y * bytesperline 
        for x in range(0, imgrey.shape[1], 2):
            try:
                buff[cursor+1] = 0.5 * (Pb[y, x] + Pb[y, x+1]) + 128
            except IndexError:
                pass
            cursor += 4

        #Set color information for Cr
        cursor = y * bytesperline 
        for x in range(0, imgrey.shape[1], 2):
            try:
                buff[cursor+3] = 0.5 * (Pr[y, x] + Pr[y, x+1]) + 128
            except IndexError:
                pass
            cursor += 4

    return buff.tostring()
        
