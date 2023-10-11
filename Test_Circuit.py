import RPi.GPIO as GPIO
import time

# Set output pins
output_pin1 = 32 #left
output_pin2 = 33 #right
digout_pin1 = 15 #left motor control
digout_pin2 = 16 #right motor control

# Define the pin numbers to BOARD mode
GPIO.setmode(GPIO.BOARD)

# Set the PWM pins to OUTPUT and HIGH
GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.LOW)

# Set the digital out pins to OUTPUT and LOW
GPIO.setup(digout_pin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(digout_pin2, GPIO.OUT, initial=GPIO.LOW)

def runTest():
    # Start both PWM outputs with duty cycle of 100%

    p1.start(100)
    p2.start(100)

    # Test forward for 5 seconds. User should be reading output of transistors 1 and 2 on the breadboard. 
    print("forward for 5 seconds...")
    GPIO.output(digout_pin1, GPIO.HIGH) # These values need to be checked
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

    GPIO.cleanup(15)
    GPIO.cleanup(16)


# Create PWM Objects with frequency 25kHz
p1 = GPIO.PWM(output_pin1, 25000)
p2 = GPIO.PWM(output_pin2, 25000)
runTest()




