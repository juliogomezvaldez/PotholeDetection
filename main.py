from detection.yolov9_detector import detect_potholes
from gps.gps_reader import get_gps
from detection.calibrate import estimate_size
from detection.draw import draw_boxes
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = detect_potholes(frame)
    gps_coords = get_gps()

    for det in detections:
        bbox = det['bbox']
        size_cm = estimate_size(bbox)
        draw_boxes(frame, bbox, size_cm, gps_coords)

    cv2.imshow("Pothole Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
