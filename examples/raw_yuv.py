import pyfakewebcam

cam = pyfakewebcam.FakeWebcam('/dev/video1', 176, 144)

while 1:
	cam.schedule_yuv('akiyo_qcif.yuv', fps=15)
