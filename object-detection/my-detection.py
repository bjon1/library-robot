from jetson_utils import videoSource, videoOutput
from ultralytics import YOLO

net = YOLO('yolov8n.pt')
camera = videoSource("/dev/video0")
display = videoOutput("display://0")

while display.IsStreaming():
	img = camera.Capture()
	
	if img is None:
		continue

	detections = net.Detect(img)

	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
