import serial
import time

port = "/dev/ttyTHS1"
baud = 9600

ser = serial.Serial(port, baud, timeout=0.5)
data = []
command_number = ''


print("Connected to: " + ser.portstr)

try:
    while True:
        if ser.in_waiting > 0:
            # Read the available bytes from the serial port
            data = ser.read(ser.in_waiting)
            print(data)
except KeyboardInterrupt:
    pass
finally:
    # Close the serial port
    ser.close()
