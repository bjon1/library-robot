import RPi.GPIO as GPIO
import time

def stop_movement():
    print("Stopped Moving")

def check_distance(distance):
    if(distance < 1):
        #Stop all movement
        return False
    return True


# assign pins
GPIO_TRIGGER = 16
GPIO_ECHO = 18

# configure board and pins
GPIO.setmode(GPIO.BOARD) # GPIO Mode (BOARD / BCM)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# start sensor
GPIO.output(GPIO_TRIGGER, GPIO.LOW)
time.sleep(1)

while True:
    try:
        # send pulse
        GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, GPIO.LOW)

        # receive response and calculate distance
        if GPIO.wait_for_edge(GPIO_ECHO, GPIO.RISING, timeout=100):
            t_start = time.time()
            if GPIO.wait_for_edge(GPIO_ECHO, GPIO.FALLING, timeout=100):
                t_end = time.time()
                t = t_end - t_start
                distance = ((t * 34300) / 2)/100

                print(f"Distance: {distance} meters")

                if not check_distance(distance):
                    stop_movement()
            else:
                stop_movement()
                print('Falling edge timeout')
        else:
            print('Rising edge timeout')
    except:
        #Stop All Movement
        GPIO.cleanup()

    time.sleep(0.5)


    
