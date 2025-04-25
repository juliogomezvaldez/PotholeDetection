from ultralytics import YOLO

model = YOLO("weights/yolov9.pt")

def detect_potholes(frame):
    results = model(frame)
    detections = []
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:  # class 0 = pothole
                x1, y1, x2, y2 = box.xyxy[0]
                detections.append({'bbox': (x1.item(), y1.item(), x2.item(), y2.item())})
    return detections
