from machine import UART

bluetooth_module = UART(channel=0, baudrate=9600)
while True:
    if bluetooth_module.any():
        data = bluetooth_module.read()
        #data = str(data)
        print(data)

        
