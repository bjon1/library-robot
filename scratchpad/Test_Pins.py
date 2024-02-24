import Jetson.GPIO as GPIO
import time

test_pin = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(test_pin, GPIO.OUT, initial=GPIO.HIGH) #, initial=GPIO.HIGH


try:
    while True:
        GPIO.output(test_pin, GPIO.LOW)
        time.sleep(3)
        print("HIGH")
finally:
    GPIO.cleanup(test_pin)
    print("GPIO Cleaned Up")




        