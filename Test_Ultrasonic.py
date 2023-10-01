import RPi.GPIO as GPIO
import time

def stop_movement():
    print("Stopped Moving")

def check_distance(distance):
    if(distance < 1):

        return False
    return True

class USensor:
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo

    def configure(self):
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        # start sensor
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(1)

    def start_ultrasound(self):
        self.configure()

        while True:
            try:
                # send pulse
                GPIO.output(self.trig, GPIO.HIGH)
                time.sleep(0.00001)
                GPIO.output(self.trig, GPIO.LOW)

                # receive response and calculate distance
                if GPIO.wait_for_edge(self.echo, GPIO.RISING, timeout=100):
                    t_start = time.time()
                    if GPIO.wait_for_edge(self.echo, GPIO.FALLING, timeout=100):
                        t_end = time.time()
                        t = t_end - t_start
                        distance = ((t * 34300) / 2)/100

                        print(f"Sensor1 Distance: {distance} meters")

                        if not check_distance(distance):
                            stop_movement()
                    else:
                        stop_movement()
                        print('Sensor1 Falling edge timeout')
                else:
                    print('Sensor1 Rising edge timeout')
            except:
                #Stop All Movement
                GPIO.cleanup()

            time.sleep(0.5)


GPIO.setmode(GPIO.BOARD) #GPIO Mode BOARD
usensor1 = USensor(trig=16, echo=18)
usensor2 = USensor(trig=19, echo=21)
usensor1.start_ultrasound()
usensor2.start_ultraasound()






    
