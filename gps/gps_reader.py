import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def get_gps():
    while True:
        line = ser.readline().decode('utf-8', errors='ignore')
        if line.startswith('$GPGGA'):
            parts = line.split(',')
            try:
                lat = float(parts[2]) / 100.0
                lon = float(parts[4]) / 100.0
                return lat, lon
            except:
                continue
