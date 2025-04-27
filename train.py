from ultralytics import YOLO

# Use absolute path to potholes.yaml (adjust if needed)
dataset_path = "/Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/datasets/potholes.yaml"


# Load YOLOv9 model (ensure yolov9s.pt is present)
model = YOLO("yolov9s.pt")

# Train the model
model.train(
    data=dataset_path,
    epochs=50,
    imgsz=640,
    project="runs/train",
    name="pothole_yolov9",
    verbose=True
)
