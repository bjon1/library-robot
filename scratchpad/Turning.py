
import numpy as np
import time

def set_motor_speed(pin, speed):
    # Ensure the speed is within the valid range (0 to 100)
    speed = max(0, min(100, speed))
    # Convert the speed to a PWM value (0 to 4095)
    pwm_value = int(speed * 40.95)
    pca.channels[pin].duty_cycle = pwm_value * 0x10000 // 4096

def get_yaw():
    # Gets the yaw and returns it in degrees
    pass

def move_left(degrees):
    current_yaw = get_yaw() # Get the yaw in degrees
    yaw_to_be = current_yaw - degrees # Calculate what the yaw should be after turning
    yaw_left = degrees # Calculate how much yaw is left to turn
    error = 5 # Error in degrees
    while not yaw_to_be - error <= current_yaw <= yaw_to_be + error: # While the yaw is not within the error range
        current_yaw = get_yaw() # Get the current yaw
        yaw_left = current_yaw - yaw_to_be # Calculate how much yaw is left to turn
        turn_speed = 50 + 50*np.sin((np.pi*(yaw_left - 22.5))/45) # Calculate the speed to turn at
        move_counterclockwise(turn_speed)
        print("yaw_left: ", yaw_left)
        time.sleep(0.5)
    stop()

def move_counterclockwise(speed):
    set_motor_speed(left_forward_pin, 0)
    set_motor_speed(right_forward_pin, speed)
    set_motor_speed(left_reverse_pin, speed)
    set_motor_speed(right_reverse_pin, 0)
