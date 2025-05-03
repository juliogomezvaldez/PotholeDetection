from ultralytics import YOLO

# Define dataset and model paths
dataset_path = "/workspace/PotholeDetection/datasets/potholes.yaml"
pretrained_model = "yolov9s.pt"  # Puedes elegir entre yolov9s, yolov9m o yolov9l dependiendo de la capacidad de tu GPU

# Load the model
model = YOLO(pretrained_model)

# Training configuration
train_params = {
    "data": dataset_path,
    "epochs": 100,               # Número de épocas
    "imgsz": 640,                # Tamaño de imagen
    "batch": 16,                 # Tamaño de lote (cambio de batch_size a batch)
    "device": 0,                 # Utilizar GPU 0; cambia a "cpu" si deseas usar la CPU
    "optimizer": "auto",         # Optimizador: SGD o AdamW
    "project": "runs/train",     # Carpeta principal para guardar experimentos
    "name": "pothole_yolov9",    # Subcarpeta para esta ejecución específica
    "verbose": True,             # Logs detallados
    "cos_lr": True,              # Usar un programador de tasa de aprendizaje coseno
    "patience": 15,              # Early stopping después de 15 épocas sin mejora
    "close_mosaic": 10,          # Cerrar la mejora de mosaico después de 10 épocas
    "dropout": 0.1,              # Regularización por dropout
    "multi_scale": True,         # Entrenamiento con imágenes de múltiples escalas
    "workers": 0,                # Número de trabajadores para cargar datos
}

# Start training
model.train(**train_params)