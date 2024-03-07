from ultralytics import YOLO

# Load a pretrained YOLO model (recommended for training)
model = YOLO('yolov8n.pt')

# Run Inference
results = model(source=0, show=True, conf=0.4, save=True)
print(results)