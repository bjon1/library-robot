import RPi.GPIO as GPIO
import time

def main():
    test_pin = 18
    output_pin = 33
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
    p = GPIO.PWM(output_pin, 50)
    p.start(0)
    p.ChangeDutyCycle(100)


    GPIO.setup(test_pin, GPIO.OUT, initial=GPIO.HIGH) #, initial=GPIO.HIGH
    GPIO.output(test_pin, GPIO.HIGH)




    print("PWM running. Press CTRL+C to exit.")
    try:
        while True:
            time.sleep(0.25)
    finally:
        p.stop()
        GPIO.cleanup(33)

if __name__ == '__main__':
    main()
