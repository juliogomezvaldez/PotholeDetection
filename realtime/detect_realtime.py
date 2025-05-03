import cv2                                                              
import os
import csv
import time
import datetime
import serial
import json
from ultralytics import YOLO  # Load YOLO model
import threading# ... (importaciones sin cambios)
import threading

# === CONFIGURATION ===
YOLO_MODEL_PATH = "runs/train/pothole_yolov916/weights/best.pt"
YOLO_CONFIDENCE_THRESHOLD = 0.5
DETECTIONS_FOLDER = "detection"
GPS_SERIAL_PORT = "/dev/ttyACM0"
GPS_BAUDRATE = 9600

# === FUNCTIONS ===
def crear_estructura_directorios(base_folder):
    # Create a directory for today's detections
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    day_path = os.path.join(base_folder, today)                                                                        
    os.makedirs(day_path, exist_ok=True)
    return day_path

def inicializar_geojson(day_path):
    # Create a GeoJSON file to store detection points
    geojson_path = os.path.join(day_path, f"detection_{datetime.datetime.now().strftime('%Y-%m-%d')}.geojson")
    if not os.path.exists(geojson_path):
        with open(geojson_path, 'w') as f:
            geojson = {
                "type": "FeatureCollection",
                "features": []
            }
            json.dump(geojson, f, indent=2)
    return geojson_path

def inicializar_csv(day_path):
    csv_path = os.path.join(day_path, f"detection_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv")
    if not os.path.exists(csv_path):
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp", "latitude", "longitude", "google_maps_link",
                "image_path", "confidence", "bbox_width", "bbox_height", "video_path"
            ])
    return csv_path

def guardar_deteccion(csv_path, geojson_path, timestamp, lat, lon, img_path, confidence, bbox_width, bbox_height, video_path):
    google_maps_link = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else ""
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, lat, lon, google_maps_link, img_path, confidence, bbox_width, bbox_height, video_path])

    if lat is not None and lon is not None:
        color = determinar_color_por_confianza(confidence)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "timestamp": timestamp,
                "image": img_path,
                "image_url": img_path,
                "video": video_path,
                "video_url": video_path,
                "confidence": confidence,
                "class": "pothole",
                "marker-color": color
            }
        }
        with open(geojson_path, 'r+') as f:
            data = json.load(f)
            data["features"].append(feature)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

def determinar_color_por_confianza(conf):
    if conf >= 0.9:
        return "#ff0000"  # red
    elif conf >= 0.7:
        return "#ffa500"  # orange
    else:
        return "#ffff00"  # yellow
    
def grabar_video(cap, video_path, duracion=5, fps=20):
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, fps, (ancho, alto))

    inicio = time.time()
    while time.time() - inicio < duracion:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    out.release()

# Read GPS data from serial port
def leer_gps():
    try:
        with serial.Serial(GPS_SERIAL_PORT, GPS_BAUDRATE, timeout=1) as ser:
            line = ser.readline().decode('ascii', errors='replace').strip()
            print(f"[GPS DEBUG] Raw NMEA: {line}")
            if line.startswith("$GPRMC"):
                data = line.split(",")
                if len(data) >= 7 and data[2] == "A":  # Valid fix
                    lat = data[3]
                    lat_dir = data[4]
                    lon = data[5]
                    lon_dir = data[6]
                    print(f"[GPS DEBUG] Lat: {lat} {lat_dir}, Lon: {lon} {lon_dir}")
                    return convertir_coordenadas(lat, lat_dir), convertir_coordenadas(lon, lon_dir)
    except Exception as e:
        print(f"GPS reading error: {e}")
    return None, None

def convertir_coordenadas(value, direction):
    # Convert NMEA coordinates to decimal format
    if not value:
        return None
    degrees = int(float(value) / 100)
    minutes = float(value) - degrees * 100
    decimal = degrees + minutes / 60
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def agregar_linestring(geojson_path):
    # Add LineString to GeoJSON by connecting all detection points
    with open(geojson_path, 'r+') as f:
        data = json.load(f)
        points = [feat["geometry"]["coordinates"] for feat in data["features"] if feat["geometry"]["type"] == "Point"]
        if len(points) >= 2:
            line = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": points
                },
                "properties": {
                    "type": "route",
                    "description": f"Route of pothole detections on {datetime.datetime.now().strftime('%Y-%m-%d')}"
                }
            }
            data["features"].append(line)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

def deteccion_baches():
    cap = cv2.VideoCapture(0)
    model = YOLO(YOLO_MODEL_PATH)

    day_path = crear_estructura_directorios(DETECTIONS_FOLDER)
    csv_path = inicializar_csv(day_path)
    geojson_path = inicializar_geojson(day_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading camera")
            break

        results = model.predict(source=frame, save=False, conf=YOLO_CONFIDENCE_THRESHOLD, verbose=False)
        detections = results[0].boxes

        if len(detections) > 0:
            for box in detections:
                confidence = box.conf.item()
                if confidence > YOLO_CONFIDENCE_THRESHOLD:
                    timestamp = datetime.datetime.now().isoformat()
                    lat, lon = leer_gps()

                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    bbox_width = int(x2 - x1)
                    bbox_height = int(y2 - y1)

                    # Dibujar bounding box
                    label = f"Pothole: {confidence:.2f}"
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                    # Guardar imagen
                    img_filename = f"pothole_{timestamp.replace(':', '-')}.jpg"
                    img_path = os.path.join(day_path, img_filename)
                    cv2.imwrite(img_path, frame)

                    # Guardar video
                    video_filename = f"pothole_{timestamp.replace(':', '-')}.mp4"
                    video_path = os.path.join(day_path, video_filename)
                    threading.Thread(target=grabar_video, args=(cap, video_path)).start()

                    # Guardar registro
                    guardar_deteccion(
                        csv_path, geojson_path, timestamp, lat, lon,
                        img_path, confidence, bbox_width, bbox_height, video_path
                    )
                    print(f" Pothole detected and saved: {img_filename}")

        cv2.imshow('Pothole Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🔚 Exiting and generating route LineString...")
            agregar_linestring(geojson_path)
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    deteccion_baches()
