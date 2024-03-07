import Jetson.GPIO as GPIO
import time

class USensor:

    def __init__(self, name, trig, echo):

        BCM_to_TEGRA_SOC = {
            k: list(GPIO.gpio_pin_data.get_data()[-1]['TEGRA_SOC'].keys())[i] for i, k in enumerate(GPIO.gpio_pin_data.get_data()[-1]['BOARD'])
        }      

        if(isinstance(trig, int)):
            trig = BCM_to_TEGRA_SOC.get(trig, None)

        if(isinstance(echo, int)):
            echo = BCM_to_TEGRA_SOC.get(echo, None)

        print(BCM_to_TEGRA_SOC)

        self.name = name
        self.trig = trig
        self.echo = echo
        self.configure()

    def configure(self):
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        # start sensor
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(3)

        print(self.name, self.trig)
        print(self.name, self.echo)

    def in_range(self, distance):
        if(distance < 1):
            return True
        return False

    def send_ultrasound(self):

        # send pulse
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(2)

        # receive response and calculate distance
        if GPIO.wait_for_edge(self.echo, GPIO.RISING, timeout=10):
            t_start = time.time()
            if GPIO.wait_for_edge(self.echo, GPIO.FALLING, timeout=10):
                t_end = time.time()
                t = t_end - t_start
                distance = ((t * 343) / 2)

                print(f"{self.name} Distance: {distance} meters")
                if self.in_range(distance):
                    print(f'{self.name} In Distance')
                    return True
            else:
                print(f'{self.name} Falling edge timeout')
                return True
                
        else:
            print(f'{self.name} Rising edge timeout')
            return True

        
