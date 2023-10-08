import RPi.GPIO as GPIO
import time
import keyboard

output_pin1 = 32 
output_pin2 = 33
digOut_pin1 = 15
digOut_pin2 = 16

print("OUTPUT1", output_pin1)
print("OUTPUT2", output_pin2)

# Pin Setup:
# Board pin-numbering scheme
GPIO.setmode(GPIO.BOARD)
# set PWM as an output pin with optional initial state of HIGH
GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)
# set digitalOutput as an output pin with optional initial state of LOW
GPIO.setup(digOut_pin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(digOut_pin2, GPIO.OUT, initial=GPIO.LOW)
# create pwm objects
p1 = GPIO.PWM(output_pin1, 50)
p2 = GPIO.PWM(output_pin2, 50)


''' WARNING: Keyboard controls will not work. 
It is just a prototype of how it should look like. I will add an event listener, simple graphical user interface with buttons, or RTOS later using the tkinter module
'''

# Define the key you want to monitor  
forward = "w"
left = "a"
reverse = "s"
right = "d"
stop = "q"

directions = {
    forward: "forward",
    left: "left",
    reverse: "reverse",
    right: "right",
    quit: "quit"
}

while True:
    for key in directions.keys():
        if keyboard.is_pressed(key):
            direction = directions.getValue(key)
            move(direction)
            print("Moved", direction)
        elif keyboard.is_pressed(stop):
            print("Stopped")
            stop()


def move(direction):
    # determine the direction and move accordingly
    stop() # This may not be needed or may cause bugs
    match direction:
        case "forward":
            activate_pwm()
            GPIO.output(digOut_pin1, GPIO.LOW) # These values need to be checked
            GPIO.output(digOut_pin2, GPIO.LOW)
        case "left":
            activate_pwm()
            GPIO.output(digOut_pin1, GPIO.HIGH)
            GPIO.output(digOut_pin2, GPIO.LOW)
        case "reverse":
            activate_pwm()
            GPIO.output(digOut_pin1, GPIO.HIGH)
            GPIO.output(digOut_pin2, GPIO.HIGH)
        case "right":
            activate_pwm()
            GPIO.output(digOut_pin1, GPIO.LOW)
            GPIO.output(digOut_pin2, GPIO.HIGH)
        case _ :
            stop()
            raise ValueError("This movement does not exist")

def stop():
    p1.stop()
    p2.stop()
    
def activate_pwm():
    print("PWM running. Press CTRL+C to exit.")
    # set pwm values
    val = 25
    incr = 5
    # start pwm
    p1.start(val)
    p2.start(val)
    try:
        while True:
            time.sleep(0.05)
            if val >= 100:
                print(">=100")
                incr = -incr
            if val <= 0:
                print("<=0")
                incr = -incr
            val += incr
            p1.ChangeDutyCycle(val)
            p2.ChangeDutyCycle(val)
    finally:
        p1.stop()
        p2.stop()
        GPIO.cleanup(output_pin1)
        GPIO.cleanup(output_pin2)
        GPIO.cleanup(digOut_pin1)
        GPIO.cleanup(digOut_pin2)

        
        
                
