#!/bin/bash

# === Script para lanzar detección de baches en tiempo real con GPU ===
# Autor: Julio Gomez
# Fecha: $(date +%Y-%m-%d)

set -e

PROJECT_PATH="/home/julio/Documents/Codigo IA/PotholeDetection"
SCRIPT_PATH="/workspace/PotholeDetection/realtime/detect_realtime.py"

echo "🔧 Lanzando detección en tiempo real desde: $PROJECT_PATH"

sudo docker run --runtime nvidia -it --rm --shm-size=8g \
  -v "$PROJECT_PATH:/workspace/PotholeDetection" \
  nvcr.io/nvidia/l4t-ml:r36.2.0-py3 \
  bash -c 'pip install pyserial ultralytics && python3 /workspace/PotholeDetection/realtime/detect_realtime.py'