import cv2
import os
from datetime import datetime
from ultralytics import YOLO

# Ruta de tu modelo entrenado
model_path = "/Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/runs/train/pothole_yolov913/weights/best.pt"  # Ejemplo: "runs/train/pothole_yolov9/weights/best.pt"

# Ruta al video de prueba
video_path = "runs/detect/input_videos/bache1.mp4"


# Crear carpeta de salida si no existe
output_dir = "runs/detect/output_videos/"
os.makedirs(output_dir, exist_ok=True)

# Nombre del archivo de salida con timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"detected_potholes_{timestamp}.mp4"
output_path = os.path.join(output_dir, output_filename)

# Cargar el modelo
model = YOLO(model_path)

# Abrir el video
cap = cv2.VideoCapture(video_path)

# Verificar que el video abrió correctamente
if not cap.isOpened():
    print(" Error: No se pudo abrir el video.")
    exit()

# Obtener propiedades del video
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Configurar el video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec mp4
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Crear una ventana para mostrar el video
cv2.namedWindow("Pothole Detection", cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Realizar la detección
    results = model.predict(frame, imgsz=640, conf=0.3)

    # Dibujar las predicciones en el frame
    annotated_frame = results[0].plot()

    # Escribir el frame procesado en el video de salida
    out.write(annotated_frame)

    # Mostrar el frame
    cv2.imshow("Pothole Detection", annotated_frame)

    # Salir si presionas 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
out.release()
cv2.destroyAllWindows()

print(f" Process completed. Processed video saved at: {output_path}")
