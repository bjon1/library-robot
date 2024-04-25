import Jetson.GPIO as GPIO
import time

def is_close(distance):
    if(distance < 0.3):
        return True
    return False

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

    def send_ultrasound(self):
        self.configure()
        
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

                    return is_close(distance)
                else:
                    print(f'{self.name} Falling edge timeout')
                    return True
            else:
                print(f'{self.name} Rising edge timeout')
                return True
        except:
            #Stop All Movement
            GPIO.cleanup()
            pass

        
