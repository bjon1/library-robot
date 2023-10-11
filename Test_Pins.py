import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH)


try:
    while True:
        GPIO.output(15, GPIO.HIGH)
        time.sleep(3)
        print("HIGH")
        GPIO.output(15, GPIO.LOW)
        time.sleep(3)
        print("LOW")
finally:
    GPIO.cleanup(15)
    print("GPIO Cleaned Up")



