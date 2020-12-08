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

while True:
    ret, frame = cam.read()
    cv2.imshow('cv2-webcam', frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) # https://stackoverflow.com/a/57421345
    fake1.schedule_frame(frame)
    if cv2.waitKey(1) == 27: 
        break  # esc to quit
    time.sleep(1/30.0)