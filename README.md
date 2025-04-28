
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
## Project Structure
Project Structure:
```
PotholeDetection/
├── datasets/                # Training datasets and annotations
├── runs/                    # Training and inference results
├── models/                  # Trained YOLOv9s models (.pt files)
├── inference/               # Inference scripts for videos, images, etc.
│   └── detect_potholes_video_yolov9s.py
├── utils/                   # Helper scripts (optional)
├── train_pro_template.py    # Training script
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

## Run
```
python main.py
```
