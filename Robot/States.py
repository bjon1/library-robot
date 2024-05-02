from enum import Enum
import time 
class States(Enum):
    CRUISE = 1
    FORWARD = 2
    REVERSE = 3
    TURNING_LEFT = 4
    TURNING_RIGHT = 5
    CLOCKWISE = 6
    COUNTER_CLOCKWISE = 7
    IDLE = 8

    

def handle_serial_ports():
        
        
        import serial
        port_bluetooth = 'COM9' 
        baud_bluetooth = 9600


        ser_bluetooth = serial.Serial(port_bluetooth, baud_bluetooth, timeout=0.5) 

        print("Connected to: " + ser_bluetooth.portstr)

        
        while True:
            try:
                data = None
                new_state = 0
                new_speed = 0

                # Check for incoming bluetooth requests
                if ser_bluetooth.in_waiting > 0:
                    print(type(ser_bluetooth.in_waiting))
                    data = ser_bluetooth.read(ser_bluetooth.in_waiting).decode('utf-8')
                    print("Found new Data (Bluetooth):", data)

                if data and data.isdigit():
                    data = int(data)
                    if data > 0 and data < 10:
                        command_to_state = {
                            1: States.CRUISE,
                            2: States.FORWARD,
                            3: States.REVERSE,
                            4: States.TURNING_LEFT,
                            5: States.TURNING_RIGHT,
                            6: States.CLOCKWISE,
                            7: States.COUNTER_CLOCKWISE,
                            8: States.IDLE,
                            9: States.IDLE
                        }
                        new_state = command_to_state.get(data)
                    elif data >= 10 and data <= 90: 
                        new_speed = int(data)
                        print(new_speed)
                elif data == 'OK+LOST' or data == 'OK+CONN': # OK+CONN or OK+LOST
                    new_state = States.IDLE

                print("STATE, SPEED (Bluetooth)", new_state)


                time.sleep(0.4)

            except KeyboardInterrupt:
                pass
            except Exception as e:
                print("Error:", e)
                continue
            finally:
                ser_bluetooth.close()

