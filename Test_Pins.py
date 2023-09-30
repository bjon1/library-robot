import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)


try:
    while True:
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        print("HIGH")
        GPIO.output(18, GPIO.LOW)
        time.sleep(1)
        print("LOW")
finally:
    GPIO.cleanup(18)
    print("GPIO Cleaned Up")



