import Jetson.GPIO as GPIO
import time
from threading import Thread

def stop_movement():
    print("Stopped Moving")

def check_distance(distance):
    if(distance < 0.3):

        return False
    return True

class USensor:
    def __init__(self, name, trig, echo):

        BCM_to_TEGRA_SOC = {
            k: list(GPIO.gpio_pin_data.get_data()[-1]['TEGRA_SOC'].keys())[i] for i, k in enumerate(GPIO.gpio_pin_data.get_data()[-1]['BOARD'])
        }     

        if(isinstance(trig, int)):
            trig = BCM_to_TEGRA_SOC.get(trig, None)

        if(isinstance(echo, int)):
            echo = BCM_to_TEGRA_SOC.get(echo, None)

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
                if GPIO.wait_for_edge(self.echo, GPIO.RISING, timeout=1):
                    t_start = time.time()
                    if GPIO.wait_for_edge(self.echo, GPIO.FALLING, timeout=1):
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
                GPIO.cleanup()
                pass

            time.sleep(0.5)

    def f1(self):
        while True:
            print("Hello1")

    def f2(self):
        while True:
            print("Hello2")




GPIO.setmode(GPIO.TEGRA_SOC) #GPIO Mode BOARD
usensor1 = USensor(name="front1", trig=16, echo=18)
usensor2 = USensor(name="front2", trig=19, echo=21)
usensor1.start_ultrasound()

#usensor2 = USensor(name="front2", trig=19, echo=21)
#usensor3 = USensor(name="side1", trig=23, echo=24)
#usensor4 = USensor(name="side2", trig=26, echo=22)