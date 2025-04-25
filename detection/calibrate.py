def estimate_size(bbox):
    x1, y1, x2, y2 = bbox
    width = x2 - x1
    height = y2 - y1
    # Fake calibration: 1 pixel = 0.5 cm (example)
    return (width * 0.5 + height * 0.5) / 2
