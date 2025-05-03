#!/bin/bash

# Script para levantar el contenedor de Pothole Detection con GPU y 8GB de shared memory
echo "Levantando contenedor Docker..."
set -e  # Si hay un error, el script se detiene automáticamente

# Variables
PROJECT_DIR="/home/julio/Documents/Codigo IA/PotholeDetection"
CONTAINER_DIR="/workspace/PotholeDetection"

# Levantar contenedor
sudo docker run --runtime nvidia -it --rm --shm-size=8g \
  -v "$PROJECT_DIR":"$CONTAINER_DIR" \
  nvcr.io/nvidia/l4t-ml:r36.2.0-py3 bash -c "
    echo '🔵 Actualizando pip...'; 
    python3 -m pip install --upgrade pip --no-warn-script-location;
    
    echo '🔵 Instalando dependencias del proyecto...'; 
    if [ -f $CONTAINER_DIR/requirements.txt ]; then
        pip install --no-cache-dir -r $CONTAINER_DIR/requirements.txt;
    else
        echo '⚠️  Archivo requirements.txt no encontrado. Instalando paquetes individuales...'; 
        pip install --no-cache-dir py-cpuinfo tqdm opencv-python kiwisolver fonttools cycler contourpy matplotlib ultralytics-thop seaborn ultralytics;
        
    fi

    echo '🟢 Dependencias instaladas correctamente.';

    echo '🟣 Entrando a $CONTAINER_DIR...'; 
    cd $CONTAINER_DIR;

    echo '🔵 Instalando Ultralytics...'; 
    pip install ultralytics;

    echo '🚀 Iniciando entrenamiento...'; 
    python3 train_pro_template.py --epochs 100 --batch 16 --imgsz 640 --workers 0 --cache disk --device 0 --project runs/train --name pothole_yolov9_pro --optimizer auto --verbose
"
pip install --no-cache-dir pyserial py-cpuinfo tqdm opencv-python kiwisolver fonttools cycler contourpy matplotlib ultralytics-thop seaborn ultralytics;
