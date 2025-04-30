import cv2
import os
import csv
import time
import datetime
import serial
import json
from ultralytics import YOLO  # Load YOLO model

# === CONFIGURATION ===
YOLO_MODEL_PATH = "Users/julio.c.gomez.valdez/Documents/CodigoIA/PotholeDetection/runs/train/pothole_yolov913/weights/best.pt"  # Example: "runs/train/pothole_yolov9/weights/best.pt"
YOLO_CONFIDENCE_THRESHOLD = 0.5
DETECTIONS_FOLDER = "detection"
GPS_SERIAL_PORT = "/dev/ttyUSB0"  # Adjust according to your GPS port
GPS_BAUDRATE = 9600

# === FUNCTIONS ===
def crear_estructura_directorios(base_folder):
    # Create a directory for today's detections
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    day_path = os.path.join(base_folder, today)
    os.makedirs(day_path, exist_ok=True)
    return day_path

def inicializar_csv(day_path):
    # Create or open CSV file to log detections
    csv_path = os.path.join(day_path, f"detection_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv")
    if not os.path.exists(csv_path):
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "latitude", "longitude", "google_maps_link", "image_path", "confidence", "bbox_width", "bbox_height"])
    return csv_path

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

def determinar_color_por_confianza(conf):
    if conf >= 0.9:
        return "#ff0000"  # red
    elif conf >= 0.7:
        return "#ffa500"  # orange
    else:
        return "#ffff00"  # yellow

def guardar_deteccion(csv_path, geojson_path, timestamp, lat, lon, img_path, confidence, bbox_width, bbox_height):
    # Save detection to CSV
    google_maps_link = f"https://www.google.com/maps?q={lat},{lon}" if lat and lon else ""
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, lat, lon, google_maps_link, img_path, confidence, bbox_width, bbox_height])

    # Save detection to GeoJSON
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
                "image_url": img_path,  # adjust to cloud URL if needed
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

def leer_gps():
    # Read GPS data from serial port
    try:
        with serial.Serial(GPS_SERIAL_PORT, GPS_BAUDRATE, timeout=1) as ser:
            line = ser.readline().decode('ascii', errors='replace')
            if line.startswith("$GPGGA"):
                data = line.split(",")
                lat = data[2]
                lon = data[4]
                return convertir_coordenadas(lat, data[3]), convertir_coordenadas(lon, data[5])
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

def deteccion_baches():
    cap = cv2.VideoCapture(0)  # Open default camera
    model = YOLO(YOLO_MODEL_PATH)  # Load trained model

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

                    # Draw bounding box on frame
                    label = f"Pothole: {confidence:.2f}"
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                    # Save image
                    img_filename = f"pothole_{timestamp.replace(':', '-')}.jpg"
                    img_path = os.path.join(day_path, img_filename)
                    cv2.imwrite(img_path, frame)

                    guardar_deteccion(csv_path, geojson_path, timestamp, lat, lon, img_path, confidence, bbox_width, bbox_height)
                    print(f" Pothole detected and saved: {img_filename}")

        # Show video in a window
        cv2.imshow('Pothole Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🔚 Exiting and generating route LineString...")
            agregar_linestring(geojson_path)
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    deteccion_baches()
