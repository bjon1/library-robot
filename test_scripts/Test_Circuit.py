import RPi.GPIO as GPIO
import time

# This script was written to test an intermediate circuit between the Jetson Nano and the H-Bridge.
# This intermediate circuit utilizes two NPN transistors and one PNP

# Set output pins
output_pin1 = 32 #left pwm
output_pin2 = 33 #right pwm
digout_pin1 = 18 #left motor control 
digout_pin2 = 16 #right motor control 

# Define the pin numbers to BOARD mode
GPIO.setmode(GPIO.BOARD)

# Set the PWM pins to OUTPUT and LOW
GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(digout_pin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(digout_pin2, GPIO.OUT, initial=GPIO.LOW)

def runTest():

    print("forward for 5 seconds...")
    GPIO.output(digout_pin1, GPIO.HIGH)
    GPIO.output(digout_pin2, GPIO.HIGH)
    time.sleep(5)

    print("left for 5 seconds...")
    GPIO.output(digout_pin1, GPIO.LOW) # These values need to be checked
    GPIO.output(digout_pin2, GPIO.HIGH)
    time.sleep(5)

    print("reverse for 5 seconds...")
    GPIO.output(digout_pin1, GPIO.LOW) # These values need to be checked
    GPIO.output(digout_pin2, GPIO.LOW)
    time.sleep(5)

    print("right for 5 seconds...")
    GPIO.output(digout_pin1, GPIO.HIGH) # These values need to be checked
    GPIO.output(digout_pin2, GPIO.LOW)
    time.sleep(5)

    print("stop")
    p1.stop()
    p2.stop()


# Create PWM Objects with frequency 25kHz
p1 = GPIO.PWM(output_pin1, 25000) 
p2 = GPIO.PWM(output_pin2, 25000)
p1.start(0)
p1.ChangeDutyCycle(100)
p2.start(0)
p2.ChangeDutyCycle(100)

runTest()




