import RPi.GPIO as GPIO
import time

output_pins = {
    'JETSON_XAVIER': 18,
    'JETSON_NANO': 33,
    'JETSON_NX': 33,
    'CLARA_AGX_XAVIER': 18,
    'JETSON_TX2_NX': 32,
    'JETSON_ORIN': 18,
    'JETSON_ORIN_NX': 33,
    'JETSON_ORIN_NANO': 33
    'JETSON_DIGITALOUT1' : 15
    'JETSON_DIGITALOUT2' : 16
}

output_pin1 = 32 #output_pin1s.get(GPIO.model, None)
output_pin2 = 33
digOut_pin1 = 15
digOut_pin2 = 16
print(output_pin1)
print(output_pin2)
if output_pin1 is None:
    raise Exception('PWM not supported on this board')


def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin1, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(output_pin2, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(digOut_pin1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(digOut_pin2, GPIO.OUT, initial=GPIO.LOW)
    p1 = GPIO.PWM(output_pin1, 50)
    p2 = GPIO.PWM(output_pin2, 50)
    val = 25
    incr = 5
    p1.start(val)
    p2.start(val)

if __name__ == '__main__':
    main()
    
    
def move_foward():
    digOut_pin1 = False;
    digOut_pin2 = False;
    print("PWM running. Press CTRL+C to exit.")
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
        
def move_backward():
    digOut_pin1 = True;
    digOut_pin2 = True;
    print("PWM running. Press CTRL+C to exit.")
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
        
def move_right():
    digOut_pin1 = False;
    digOut_pin2 = True;
    print("PWM running. Press CTRL+C to exit.")
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
        
def move_left():
    digOut_pin1 = True;
    digOut_pin2 = False;
    print("PWM running. Press CTRL+C to exit.")
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
                