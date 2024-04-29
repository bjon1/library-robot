import base64
import json
import torch
import cv2
from ultralytics import YOLO

class ObjectDetection:
    def __init__(self, capture_index):
        self.capture_index = capture_index
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)
        self.model = self.load_model()
        self.names = self.model.names
        self.cap = cv2.VideoCapture(self.capture_index)
        assert self.cap.isOpened(), "Error reading video file"
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def load_model(self):
        model = YOLO("yolov8n.pt")
        model.fuse()
        return model
    
    def predict(self, frame):
        results = self.model(frame)
        return results
    
    def plot_bboxes(self, results, frame):
        class_ids = []
        class_names = []

        #Extract detections for person class
        for result in results:
            boxes = result.boxes.cpu().numpy()
            class_ids.append(boxes.cls)
            for class_id in result.boxes.cls:
                class_name = self.names[int(class_id)]
                class_names.append(class_name)
        frame = results[0].plot()
        return frame, class_ids, class_names

    def __call__(self):
        ret, frame = self.cap.read()
        assert ret

        results = self.predict(frame)
        frame, class_ids, class_names = self.plot_bboxes(results, frame)
        _, jpeg = cv2.imencode('.jpg', frame)
        frame = base64.b64encode(jpeg.tobytes()).decode('utf-8')# Convert bytes to base64 encoded string
        frame_data = {
            'frame' : frame,
            'class_names':  class_names,
        }
        return json.dumps(frame_data) + '\n'