import RPi.GPIO as GPIO
import time
from threading import Thread

def stop_movement():
    print("Stopped Moving")

def check_distance(distance):
    if(distance < 1):

        return False
    return True

class USensor:
    def __init__(self, name, trig, echo):
        self.name = name
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

                        print(f"{self.name} Distance: {distance} meters")

                        if not check_distance(distance):
                            stop_movement()
                    else:
                        stop_movement()
                        print(f'{self.name} Falling edge timeout')
                else:
                    print(f'{self.name} Rising edge timeout')
            except:
                #Stop All Movement
                #GPIO.cleanup()
                pass

            time.sleep(0.5)

    def f1(self):
        while True:
            print("Hello1")

    def f2(self):
        while True:
            print("Hello2")



GPIO.setmode(GPIO.BOARD) #GPIO Mode BOARD
usensor1 = USensor(name="front1", trig=16, echo=18)
usensor2 = USensor(name="front2", trig=19, echo=21)
usensor3 = USensor(name="side1", trig=23, echo=24)
usensor4 = USensor(name="side2", trig=26, echo=22)