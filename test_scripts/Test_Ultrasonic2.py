# Test_Ultrasonic2.py performs ultrasonic sensor tests without multithreading

import RPi.GPIO as GPIO
import time

def stop_movement():
    print("Stopped Moving")

def in_range(distance):
    if(distance < 1):

        return True
    return False

class USensor:
    def __init__(self, name, trig, echo):
        self.name = name
        self.trig = trig
        self.echo = echo
        self.configure()

    def configure(self):
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        # start sensor
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(1)

    def send_ultrasound(self):
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

                    print(f"{self.name} Distance: {distance} meters")
                    if in_range(distance):
                        return True
                else:
                    print(f'{self.name} Falling edge timeout')
                    return True
                    
            else:
                print(f'{self.name} Rising edge timeout')
        except:
            GPIO.cleanup()
            return True
        
def start_ultrasound(self):
    GPIO.setmode(GPIO.BOARD) #GPIO Mode BOARD
    usensor1 = USensor(name="front1", trig=16, echo=18)
    usensor2 = USensor(name="front2", trig=19, echo=21)
    usensor3 = USensor(name="side1", trig=23, echo=24)
    usensor4 = USensor(name="side2", trig=26, echo=22)

    while True:
        if(usensor1.send_ultrasound() or usensor2.send_ultrasound() or usensor3.send_ultrasound() or usensor4.send_ultrasound()):
            stop_movement()               
        time.sleep(0.5)