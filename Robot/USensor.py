import RPi.GPIO as GPIO
import time

def is_close(distance):
    if(distance < 0.3):
        return True
    return False

class USensor:
    def __init__(self, name, trig, echo):

        '''
        BCM_to_TEGRA_SOC = {
            k: list(GPIO.gpio_pin_data.get_data()[-1]['TEGRA_SOC'].keys())[i] for i, k in enumerate(GPIO.gpio_pin_data.get_data()[-1]['BOARD'])
        }     
        
        

        if(isinstance(trig, int)):
            trig = BCM_to_TEGRA_SOC.get(trig, None)

        if(isinstance(echo, int)):
            echo = BCM_to_TEGRA_SOC.get(echo, None)
        '''

        self.name = name
        self.trig = trig
        self.echo = echo
        
        

    def configure(self):
        
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        # start sensor
        GPIO.output(self.trig, False)
        print("Waiting for Ultrasound Sensor to Settle...")
        time.sleep(2)

    def send_ultrasound(self):
        GPIO.setmode(GPIO.BCM)
        try:
            # send pulse
            GPIO.output(self.trig, True)
            time.sleep(0.00001)
            GPIO.output(self.trig, False)

            # receive response and calculate distance
            while GPIO.input(self.echo) == 0:
                t_start = time.time() 
            while GPIO.input(self.echo) == 1:
                t_end = time.time()
            t = t_end - t_start
            distance = (t * 17150) 
            distance = round(distance, 2)

            print(f"{self.name} Distance: {distance} centimeters")

            return distance

        except Exception as e:
            #Stop All Movement
            print("error", e)
        finally:
            GPIO.cleanup()

        
