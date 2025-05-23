
# PotholeDetection
This project uses YOLOv9 for detecting potholes in real-time using a Jetson ReComputer J40. It also captures GPS data and estimates pothole size from video input.
=======
# Real-Time Pothole Detection with YOLOv9 and Jetson J40

Author: Julio Gomez

This project uses YOLOv9 for detecting potholes in real-time using a Jetson ReComputer J40. It also captures GPS data and estimates pothole size from video input.

## Features
- YOLOv9 object detection
- Real-time video processing
- GPS coordinates integration
- Pothole size estimation

## Requirements
Install dependencies:
```
pip install -r requirements.txt
```
##  Dataset

- **Name**: Pothole Detection  
- **Author**: Andrew Mvd  
- **Source**: [Kaggle - Pothole Detection](https://www.kaggle.com/datasets/andrewmvd/pothole-detection)  
- **License**: Publicly available for educational and research use

The dataset was restructured into the YOLO format with `train/` and `val/` image folders and corresponding annotation files.

##  Model

- **Base model**: `yolov9s.pt`
- **Framework**: [Ultralytics YOLO](https://docs.ultralytics.com/)
- **Training epochs**: 100
- **Image size**: 640×640
- **Batch size**: 16
- **Device**: CUDA (GPU)

##  Training Example

```python
from ultralytics import YOLO

model = YOLO('yolov9s.pt')
model.train(
    data='datasets/potholes.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='pothole_yolov9',
    exist_ok=True,
    device='cuda' 
)



```
##  Project Structure
```
PotholeDetection/
├── datasets/            # Dataset for training
├── detections/           # Images and detection data (generated in real-time)
├── models/               # Trained YOLOv9 models
├── notebooks/            # Experimentation notebooks
├── realtime/             # Real-time detection scripts
│   └── detect_realtime.py
├── requirements.txt      # Python dependencies
├── start_container.sh    # Training startup script
├── start_realtime.sh     # Real-time detection startup script
├── train_pro_template.py # Training template
```



##  Main Scripts
```
### 1. `start_container.sh`

- **What does it do?**
  - Launches a Docker container with GPU for **training tasks**.
  - Installs required dependencies.

- **How to use it?**

```bash
chmod +x start_container.sh
./start_container.sh
```

### 2. `start_realtime.sh`

- **What does it do?**
  - Launches a Docker container with GPU for **real-time pothole detection**.
  - Automatically runs the script `realtime/detect_realtime.py`.

- **How to use it?**

```bash
chmod +x start_realtime.sh
./start_realtime.sh
```

---


## Run
```
python main.py
```
