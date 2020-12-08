"""
https://stackoverflow.com/questions/21446292/using-opencv-output-as-webcam
https://stackoverflow.com/a/61394280
"""
import cv2
import time
import pyfakewebcam
import numpy as np

IMG_W = 1280
IMG_H = 720

cam = cv2.VideoCapture(0)
fake1 = pyfakewebcam.FakeWebcam('/dev/video2', int(cam.get(3)), int(cam.get(4)))

iter = 0
while True:
    ret, frame_ = cam.read()
    cv2.imshow('cv2-webcam', frame_)

    frame = cv2.cvtColor(frame_, cv2.COLOR_RGB2BGR) # https://stackoverflow.com/a/57421345
    fake1.schedule_frame(frame)
    
    key = cv2.waitKey(1)
    if key == 27: 
        break  # esc to quit
    elif key == 115 or key == 83:
        cv2.imwrite('image'+str(iter)+'.jpg', frame_)
        iter += 1
    time.sleep(1/30.0)