import cv2

def draw_boxes(frame, bbox, size_cm, gps_coords):
    x1, y1, x2, y2 = map(int, bbox)
    label = f"{size_cm:.1f} cm - {gps_coords}"
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
