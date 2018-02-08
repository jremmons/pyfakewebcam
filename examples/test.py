import pyfakewebcam

cam = pyfakewebcam.FakeWebcam('/dev/video1', 640, 480)

cam.print_capabilities()
cam.schedule_frame(None)
