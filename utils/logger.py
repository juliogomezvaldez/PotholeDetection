import datetime

def log_detection(data):
    with open("detections.log", "a") as f:
        f.write(f"{datetime.datetime.now()}: {data}\n")
