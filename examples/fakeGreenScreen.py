"""
- python script to create a fake green screen 
- reads the webcam input and outputs the new image 
   to a fake camera device
- uses background subtractor to identify the foreground and 
   turns the background to green color

TODO: add argument parser

related work: 
[1] https://www.learnopencv.com/applications-of-foreground-background-separation-with-semantic-segmentation/
[2] https://medium.com/@chris.s.park/image-background-removal-using-opencv-part-1-da3695ac66b6
"""
import cv2
import time
import pyfakewebcam
import numpy as np

IMG_W = 1280
IMG_H = 720

def main():
   backSub = cv2.bgsegm.createBackgroundSubtractorMOG()
   # backSub = cv2.createBackgroundSubtractorMOG2()
   # backSub = cv.createBackgroundSubtractorKNN()

   cam = cv2.VideoCapture(0)
   fake1 = pyfakewebcam.FakeWebcam('/dev/video2', int(cam.get(3)), int(cam.get(4)))

   ret, frame = cam.read()
   prev_frame = frame

   while True:
      ret, frame = cam.read()
      # fgMask = backSub.apply(frame)

      # mask = np.mean(frame-prev_frame, axis=2)
      # rows, cols = np.where(mask < 1*np.ones(mask.shape[:2]))
      # frame[rows, cols, 0] = 0
      # frame[rows, cols, 1] = 255
      # frame[rows, cols, 2] = 0

      # hardcoded for now  TODO: obviously identify the face region
      frame[0:90, :, 0] = 0
      frame[0:90, :, 1] = 255
      frame[0:90, :, 2] = 0

      frame[:, 0:50, 0] = 0
      frame[:, 0:50, 1] = 255
      frame[:, 0:50, 2] = 0
      frame[:, 590:640, 0] = 0
      frame[:, 590:640, 1] = 255
      frame[:, 590:640, 2] = 0

      frame[0:430, 0:100, 0] = 0
      frame[0:430, 0:100, 1] = 255
      frame[0:430, 0:100, 2] = 0
      frame[0:430, 540:640, 0] = 0
      frame[0:430, 540:640, 1] = 255
      frame[0:430, 540:640, 2] = 0

      frame[0:380, 0:150, 0] = 0
      frame[0:380, 0:150, 1] = 255
      frame[0:380, 0:150, 2] = 0
      frame[0:380, 490:640, 0] = 0
      frame[0:380, 490:640, 1] = 255
      frame[0:380, 490:640, 2] = 0

      # cv2.imshow("frame", frame)
      # key = cv2.waitKey(1)
      # if key == 27: 
      #    break  # esc to quit

      # outputing processed frame through the fake webcam
      frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 
      cv2.putText(frame, "prasanth kotaru", (25, 25),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8 , (255,0,0), 2)
      fake1.schedule_frame(frame)
      time.sleep(1/30.0)

if __name__ == "__main__":
    main()

