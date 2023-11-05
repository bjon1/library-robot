import Jetson.GPIO as GPIO
import time

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

    def in_range(distance):
        if(distance < 1):
            return True
        return False

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
                    if self.in_range(distance):
                        return True
                else:
                    print(f'{self.name} Falling edge timeout')
                    return True
                    
            else:
                print(f'{self.name} Rising edge timeout')
        except:
            GPIO.cleanup()
            return True
        

