import cv2
import os
import csv
import time
import datetime
import serial
from ultralytics import YOLO  # Importa el modelo YOLO

# === CONFIGURACIONES ===
YOLO_MODEL_PATH = "runs/train/pothole_yolov9s/weights/best.pt"  # Ajusta tu ruta del modelo
YOLO_CONFIDENCE_THRESHOLD = 0.5
DETECTIONS_FOLDER = "detections"
GPS_SERIAL_PORT = "/dev/ttyUSB0"  # Ajusta el puerto GPS
GPS_BAUDRATE = 9600

# === FUNCIONES ===
def crear_estructura_directorios(base_folder):
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    ruta_dia = os.path.join(base_folder, fecha_hoy)
    os.makedirs(ruta_dia, exist_ok=True)
    return ruta_dia

def inicializar_csv(ruta_dia):
    csv_path = os.path.join(ruta_dia, f"detections_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv")
    if not os.path.exists(csv_path):
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "latitude", "longitude", "image_path", "confidence", "bbox_width", "bbox_height"])
    return csv_path

def guardar_deteccion(csv_path, timestamp, lat, lon, img_path, confidence, bbox_width, bbox_height):
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, lat, lon, img_path, confidence, bbox_width, bbox_height])

def leer_gps():
    try:
        with serial.Serial(GPS_SERIAL_PORT, GPS_BAUDRATE, timeout=1) as ser:
            line = ser.readline().decode('ascii', errors='replace')
            if line.startswith("$GPGGA"):
                datos = line.split(",")
                lat = datos[2]
                lon = datos[4]
                return convertir_coordenadas(lat, datos[3]), convertir_coordenadas(lon, datos[5])
    except Exception as e:
        print(f"Error leyendo GPS: {e}")
    return None, None

def convertir_coordenadas(valor, direccion):
    if not valor:
        return None
    grados = int(float(valor) / 100)
    minutos = float(valor) - grados * 100
    decimal = grados + minutos / 60
    if direccion in ['S', 'W']:
        decimal = -decimal
    return decimal

def deteccion_baches():
    cap = cv2.VideoCapture(0)  # Usa la camara por defecto
    model = YOLO(YOLO_MODEL_PATH)  # Carga el modelo

    ruta_dia = crear_estructura_directorios(DETECTIONS_FOLDER)
    csv_path = inicializar_csv(ruta_dia)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error leyendo la cámara")
            break

        results = model.predict(source=frame, save=False, conf=YOLO_CONFIDENCE_THRESHOLD, verbose=False)
        detecciones = results[0].boxes

        if len(detecciones) > 0:
            for box in detecciones:
                confidence = box.conf.item()
                if confidence > YOLO_CONFIDENCE_THRESHOLD:
                    timestamp = datetime.datetime.now().isoformat()
                    lat, lon = leer_gps()

                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    bbox_width = int(x2 - x1)
                    bbox_height = int(y2 - y1)

                    img_filename = f"pothole_{timestamp.replace(':', '-')}.jpg"
                    img_path = os.path.join(ruta_dia, img_filename)
                    cv2.imwrite(img_path, frame)

                    guardar_deteccion(csv_path, timestamp, lat, lon, img_path, confidence, bbox_width, bbox_height)
                    print(f"✅ Bache detectado y guardado: {img_filename}")

        # Mostrar el video en una ventana
        cv2.imshow('Deteccion de Baches', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    deteccion_baches()
