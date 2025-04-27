from ultralytics import YOLO

# Define dataset and model paths
dataset_path = "/Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/datasets/potholes.yaml"
pretrained_model = "runs/train/pothole_yolov912/weights/last.pt"  # yolov9s.pt or yolov9m.pt, yolov9l.pt depending on your compute power

# Load the model
model = YOLO(pretrained_model)

# Training configuration
train_params = {
    "data": dataset_path,
    "epochs": 100,               # Number of epochs
    "imgsz": 640,                # Image size
    "batch": 16,                 # Batch size
    "device": 'cpu',                 # Use GPU 0; set device="cpu" if you want CPU
    "optimizer": "auto",        # Optimizer: SGD or AdamW
    "project": "runs/train",     # Root folder for saving experiments
    "name": "pothole_yolov9",# Subfolder for this specific run
    "verbose": True,             # Detailed logs
    "cos_lr": True,              # Use cosine learning rate scheduler
    "patience": 15,              # Early stopping after 15 epochs without improvement
    "close_mosaic": 10,          # Close mosaic augmentation after 10 epochs
    "dropout": 0.1,              # Add dropout for regularization
    "multi_scale": True         # Train with multi-scale images
    #"resume": True              # Set to True if you want to resume from last checkpoint
}

# Start training
model.train(**train_params)

# Fine-tuning tip:
# After initial training, you can resume training with a lower learning rate
# Example:
# model.train(data=dataset_path, epochs=50, lr0=0.001, resume=True)
