"""
[Ref]: https://pysource.com/2017/06/02/tutorial-remove-background-opencv-3-2-with-python-3/
"""
import cv2
import time
import pyfakewebcam
import numpy as np


class BackgroundRemover(object):
    def __init__(self, cam_num=0):
        self.webCam = cv2.VideoCapture(cam_num)
        self.backSub = cv2.bgsegm.createBackgroundSubtractorMOG()
        # backSub = cv2.createBackgroundSubtractorMOG2()
        # backSub = cv.createBackgroundSubtractorKNN()
        self.fakeCam = pyfakewebcam.FakeWebcam(
            '/dev/video2', int(self.webCam.get(3)), int(self.webCam.get(4)))

        self.panel_ = None
        ret, frame = self.webCam.read()
        prev_frame = frame

        self.create_panel()
        self.run()

    def create_panel(self):
        self.panel_ = np.zeros([100, 500], np.uint8)
        cv2.namedWindow('panel')

        def nothing(x):
            # print('help')
            pass

        cv2.createTrackbar('L – h', 'panel', 30, 179, nothing)
        cv2.createTrackbar('U – h', 'panel', 96, 179, nothing)
        cv2.createTrackbar('L – s', 'panel', 0, 255, nothing)
        cv2.createTrackbar('U – s', 'panel', 141, 255, nothing)
        cv2.createTrackbar('L – v', 'panel', 0, 255, nothing)
        cv2.createTrackbar('U – v', 'panel', 189, 255, nothing)

        # cv2.createTrackbar('S ROWS', 'panel', 0, 480, nothing)
        # cv2.createTrackbar('E ROWS', 'panel', 480, 480, nothing)
        # cv2.createTrackbar('S COL', 'panel', 0, 640, nothing)
        # cv2.createTrackbar('E COL', 'panel', 640, 640, nothing)

        self.s_r = 0 
        self.e_r = 480
        self.s_c = 0
        self.e_c = 640

    def panel(self):
        # self.s_r = cv2.getTrackbarPos('S ROWS', 'panel')
        # self.e_r = cv2.getTrackbarPos('E ROWS', 'panel')
        # self.s_c = cv2.getTrackbarPos('S COL', 'panel')
        # self.e_c = cv2.getTrackbarPos('E COL', 'panel')

        l_h = cv2.getTrackbarPos('L – h', 'panel')
        u_h = cv2.getTrackbarPos('U – h', 'panel')
        l_s = cv2.getTrackbarPos('L – s', 'panel')
        u_s = cv2.getTrackbarPos('U – s', 'panel')
        l_v = cv2.getTrackbarPos('L – v', 'panel')
        u_v = cv2.getTrackbarPos('U – v', 'panel')

        self.lower_green = np.array([l_h, l_s, l_v])
        self.upper_green = np.array([u_h, u_s, u_v])

    def run(self):
        while True:
            ret, frame = self.webCam.read()
            self.panel()
            # fgMask = self.backSub.apply(frame)
            # out_frame = fgMask

            roi = frame[self.s_r: self.e_r, self.s_c: self.e_c]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
            mask_inv = cv2.bitwise_not(mask)

            bg = cv2.bitwise_and(roi, roi, mask=mask)
            bg[:,:,0] = np.zeros(bg.shape[:2])
            bg[:,:,2] = np.zeros(bg.shape[:2])
            
            fg = cv2.bitwise_and(roi, roi, mask=mask_inv)
            out_frame = cv2.add(fg, bg)

            # outputing processed frame through the fake webcam
            out_frame = cv2.cvtColor(out_frame, cv2.COLOR_RGB2BGR)
            cv2.putText(out_frame, "prasanth kotaru", (25, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            self.fakeCam.schedule_frame(out_frame)
            time.sleep(1/30.0)

            cv2.imshow('panel', self.panel_)
            k = cv2.waitKey(30) & 0xFF
            if k == 27:
                break
        self.webCam.release()
        cv2.destroyAllWindows()






if __name__ == "__main__":
    bgrmvr = BackgroundRemover()
