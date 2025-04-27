import serial
import pynmea2

# Configuración del puerto serial
port = '/dev/ttyACM0'
baudrate = 9600  # normalmente los NEO-6M trabajan a 9600 baudios

def main():
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Escuchando GPS en {port}...")
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                    try:
                        msg = pynmea2.parse(line)
                        if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                            lat = msg.latitude
                            lon = msg.longitude
                            print(f"Latitud: {lat}, Longitud: {lon}")
                            print(f"Mapa: https://www.google.com/maps?q={lat},{lon}")
                            print("-" * 50)
                        if hasattr(msg, 'spd_over_grnd'):
                            print(f"Velocidad (nudos): {msg.spd_over_grnd}")
                    except pynmea2.ParseError:
                        continue
    except KeyboardInterrupt:
        print("\nCerrando programa.")
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")

if __name__ == '__main__':
    main()
