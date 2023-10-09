import RPi.GPIO as GPIO
import tkinter as tk
import time

output_pin1 = 32 #left
output_pin2 = 33 #right
digout_pin1 = 15 #left motor control
digout_pin2 = 16 #right motor control

GPIO.setmode(GPIO.BOARD)

GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)

GPIO.setup(digout_pin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(digout_pin2, GPIO.OUT, initial=GPIO.LOW)

p1 = GPIO.PWM(output_pin1, 25000)
p2 = GPIO.PWM(output_pin2, 25000)

def runTest():
    p1.start(75)
    p2.start(75)

    print("forward for 5 seconds...")
    GPIO.output(digout_pin1, GPIO.LOW) # These values need to be checked
    GPIO.output(digout_pin2, GPIO.LOW)
    time.sleep(5)

    print("left for 5 seconds...")
    GPIO.output(digout_pin1, GPIO.HIGH) # These values need to be checked
    GPIO.output(digout_pin2, GPIO.LOW)
    time.sleep(5)

    print("reverse for 5 seconds...")
    GPIO.output(digout_pin1, GPIO.HIGH) # These values need to be checked
    GPIO.output(digout_pin2, GPIO.HIGH)
    time.sleep(5)

    print("right for 5 seconds...")
    GPIO.output(digout_pin1, GPIO.LOW) # These values need to be checked
    GPIO.output(digout_pin2, GPIO.LOW)
    time.sleep(5)

    print("stop")
    p1.stop()
    p2.stop()


