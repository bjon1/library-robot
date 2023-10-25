# This script is the same as the Test_Movement.py script, except that it regulates the robot's turns

import time
import math
import board
import busio
from adafruit_pca9685 import PCA9685
import tkinter as tk
from madgwickAHRS import MadgwickAHRS
from imusensor.filters import madgwick
from imusensor.filters import kalman 
from mpu9250_i2c import *

# Initialize I2C
i2c = busio.I2C(board.SCL_1, board.SDA_1)

# Initialize PCA9685 and specify the PWM frequency
pca = PCA9685(i2c)
pca.frequency = 50  # Set PWM frequency to 50 Hz

# Define the PWM channels for your robot's motors
left_forward_pin = 0
left_reverse_pin = 1
right_forward_pin = 2
right_reverse_pin = 3

# Set initial motor speeds (0 to 100)
left_motor_speed = 0
right_motor_speed = 0

speed = 100 # Duty Cycle

def set_motor_speed(pin, speed):
    # Ensure the speed is within the valid range (0 to 100)
    speed = max(0, min(100, speed))
    # Convert the speed to a PWM value (0 to 4095)
    pwm_value = int(speed * 40.95)
    pca.channels[pin].duty_cycle = pwm_value * 0x10000 // 4096

# Function to move the robot forward
def move_forward():
    set_motor_speed(left_reverse_pin, 0)
    set_motor_speed(right_reverse_pin, 0)
    set_motor_speed(left_forward_pin, speed)
    set_motor_speed(right_forward_pin, speed)
    print("forward")

# Function to move the robot left
def move_left():
    set_motor_speed(left_forward_pin, 0)
    set_motor_speed(right_forward_pin, speed)
    set_motor_speed(left_reverse_pin, speed)
    set_motor_speed(right_reverse_pin, 0)
    print("left")

# Function to move the robot right
def move_right():
    set_motor_speed(left_forward_pin, speed)
    set_motor_speed(right_forward_pin, 0)
    set_motor_speed(left_reverse_pin, 0)
    set_motor_speed(right_reverse_pin, speed)
    print("right")

# Function to move the robot backward
def move_reverse():
    set_motor_speed(left_forward_pin, 0)
    set_motor_speed(right_forward_pin, 0)
    set_motor_speed(left_reverse_pin, speed)
    set_motor_speed(right_reverse_pin, speed)
    print("reverse")

# Function to stop the robot
def stop():
    set_motor_speed(left_forward_pin, 0)
    set_motor_speed(right_forward_pin, 0)
    set_motor_speed(left_reverse_pin, 0)
    set_motor_speed(right_reverse_pin, 0)
    print("stop")

'''

def calculate_orientation(accel_data, gyro_data, mag_data):
    # Create an instance of the MadgwickAHRS class, with a sample period of 256 times per second
    madgwick_filter = MadgwickAHRS(sampleperiod=1/256)

    # Update the Madgwick filter with new sensor data
    madgwick_filter.update(gyro_data, accel_data, mag_data)

    # Get the current quaternion output from the filter
    # A quaternion is a complex number that can be used to represent orientation in 3D space
    q = madgwick_filter.quaternion

    # Convert quaternion to Euler angles
    roll, pitch, yaw = q.to_euler_angles()

    # Convert to degrees
    yaw *= 180.0 / math.pi
    pitch *= 180.0 / math.pi
    roll *= 180.0 / math.pi

    return yaw, pitch, roll
'''

# Use Tkinter for UI
def create_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Henry Control")

    # Create a frame to contain the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(padx=20, pady=20)

    # Create and configure buttons
    button_forward = tk.Button(button_frame, text="Forward", command=move_forward)
    button_reverse = tk.Button(button_frame, text="Reverse", command=move_reverse)
    button_left = tk.Button(button_frame, text="Left", command=move_left)
    button_right= tk.Button(button_frame, text="Right", command=move_right)
    button_stop = tk.Button(button_frame, text="Stop", command=stop)

    # Pack the buttons
    button_forward.pack(side=tk.LEFT, padx=10)
    button_left.pack(side=tk.LEFT, padx=10)
    button_right.pack(side=tk.LEFT, padx=10)
    button_reverse.pack(side=tk.LEFT, padx=10)
    button_stop.pack(side=tk.LEFT, padx=10)

    # Start the Tkinter main loop
    root.mainloop()

#create_gui()

sensorfusion = kalman.Kalman()
count = 0
currTime = time.time()
while True:
    ax, ay, az, wx, wy, wz = mpu6050_conv() # read and convert mpu6050 data
    mx, my, mz = AK8963_conv()
    newTime = time.time()
    dt = newTime - currTime
    currTime = newTime

    sensorfusion.computeAndUpdateRollPitchYaw(ax, ay, az, wx, wy, wz, mx, my, mz, dt)
    print("Roll: {0} ; Pitch: {1} ; Yaw: {2}".format(sensorfusion.roll, sensorfusion.pitch, sensorfusion.yaw))
	
    time.sleep(0.01)

'''
sensorfusion = madgwick.Madgwick(0.5)
currTime = time.time()
print_count = 0
while True:
    ax, ay, az, wx, wy, wz = mpu6050_conv() # read and convert mpu6050 data
    mx, my, mz = AK8963_conv()

    for i in range(10):
        newTime = time.time()
        dt = newTime - currTime
        currTime = newTime
        
        sensorfusion.updateRollPitchYaw(ax, ay, az, wx, wy, wz, mx, my, mz, dt)

    if print_count == 2:
        print("Roll: {0} ; Pitch: {1} ; Yaw: {2}".format(sensorfusion.roll, sensorfusion.pitch, sensorfusion.yaw))
        print_count = 0
    print_count += 1
    time.sleep(0.1)
'''


'''while True:
    # Calculate the orientation
    ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
    mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data

    # Store variables in tuples
    accel_data = [ax, ay, az]
    gyro_data = [wx, wy, wz]
    mag_data = [mx, my, mz]

    yaw, pitch, roll = calculate_orientation(accel_data, gyro_data, mag_data)
    print("YAW", yaw)
    print("PITCH", pitch)
    print("ROLL", roll)
    
    time.sleep(0.2)'''