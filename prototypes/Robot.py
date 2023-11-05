import math
import time
import board
import busio
from adafruit_pca9685 import PCA9685
import numpy as np
import tkinter as tk
from imusensor.filters import kalman 
from mpu9250_i2c import *
from PIDController import PIDController
from enum import Enum
from threading import Thread

class States(Enum):
    IDLE = 0
    MOVING_FORWARD = 1
    MOVING_BACKWARD = 2
    TURNING_LEFT = 3
    TURNING_RIGHT = 4

class Robot:

    def __init__(self, pwm_frequency):

        # Initialize I2C
        i2c = busio.I2C(board.SCL_1, board.SDA_1) # Pin 27, 28
        # Initialize PCA9685 object and specify the PWM frequency
        self.pca = PCA9685(i2c) 
        self.pca.frequency = pwm_frequency  # Set PWM frequency to 50 Hz
        
        # Define the PWM channels for the robot's motors
        self.left_forward_pin = 0
        self.left_reverse_pin = 1
        self.right_forward_pin = 2
        self.right_reverse_pin = 3

        # Initialize the Kalman filter
        self.sensorfusion = kalman.Kalman()

        self.state = States.IDLE

    def get_yaw(self):
        if self.sensorfusion.yaw == 0 and self.sensorfusion.roll == 0 and self.sensorfusion.pitch == 0:
            raise Exception("Sensor fusion has not been started. Call start_sensorfusion() first.")
        print(self.sensorfusion.yaw)
        return self.sensorfusion.yaw
    
    def get_pitch(self):
        if self.sensorfusion.yaw == 0 and self.sensorfusion.roll == 0 and self.sensorfusion.pitch == 0:
            raise Exception("Sensor fusion has not been started. Call start_sensorfusion() first.")
        return self.sensorfusion.pitch

    def get_roll(self):
        if self.sensorfusion.yaw == 0 and self.sensorfusion.roll == 0 and self.sensorfusion.pitch == 0:
            raise Exception("Sensor fusion has not been started. Call start_sensorfusion() first.")
        return self.sensorfusion.roll

    def set_motor_speed(self, pin, speed):
        # Ensure the speed is within the valid range (0 to 100)
        speed = max(0, min(100, speed))
        # Convert the speed to a PWM value (0 to 4095)
        pwm_value = int(speed * 40.95)
        self.pca.channels[pin].duty_cycle = pwm_value * 0x10000 // 4096
        
    def move_forward(self, speed):
        self.set_motor_speed(self.left_reverse_pin, 0)
        self.set_motor_speed(self.right_reverse_pin, 0)
        self.set_motor_speed(self.left_forward_pin, speed)
        self.set_motor_speed(self.right_forward_pin, speed)
        print("Moving forward...")

    # This should replace the move_forward() once it has been tested
    def cruise_control(self): 
        time.sleep(5)
        self.set_motor_speed(self.left_reverse_pin, 0)
        self.set_motor_speed(self.right_reverse_pin, 0)
        target_yaw = self.get_yaw()  # capture the yaw at the moment the robot started moving forward
        pid_controller = PIDController(kp=1.0, ki=0.1, kd=0.01, max_out=50) # values of kp, ki, and kd will need tuning

        while True:
            current_yaw = self.get_yaw()
            error = target_yaw - current_yaw
            print("Target", target_yaw)
            print("Current", current_yaw)
            print("error", error)
            dt = 0.01  # time step in seconds
            time.sleep(dt)

            correction = pid_controller.update(error, dt)
            
            # 50 is the base speed, but it may need to be changed depending on the minimum duty cycle of the motors
            left_speed = 50 + correction 
            right_speed = 50 - correction

            left_forward_pin = 0 #placeholder
            right_forward_pin = 1 #placeholder

            #Testing Purposes
            print("Left Speed", left_speed)
            print("Right Speed", right_speed)
            #self.set_motor_speed(left_forward_pin, left_speed)
            #self.set_motor_speed(right_forward_pin, right_speed)
            time.sleep(1)

    def turn_left(self, degrees=90):
        time.sleep(5) # For testing purposes
        print("Turning left...")
        current_yaw = self.get_yaw() # Get the yaw in degrees
        yaw_to_be = current_yaw - degrees # Calculate what the yaw should be after turning
        yaw_left = degrees # Calculate how much yaw is left to turn
        error = 5 # Error in degrees
        while not yaw_to_be - error <= current_yaw <= yaw_to_be + error: # While the yaw is not within the error range
            current_yaw = self.get_yaw() # Get the current yaw
            yaw_left = current_yaw - yaw_to_be # Calculate how much yaw is left to turn
            turn_speed = 50 + 50*np.sin((np.pi*(yaw_left - 22.5))/45) # Calculate the speed to turn at
            print("turn_speed",turn_speed)
            self.move_counterclock(turn_speed)
            print("yaw_left: ", yaw_left)
            time.sleep(0.5)
        self.stop()

    # Function needs to be implemented later, after turn_left is tested
    def turn_right(self, speed):
        self.set_motor_speed(self.left_forward_pin, speed)
        self.set_motor_speed(self.right_forward_pin, 0)
        self.set_motor_speed(self.left_reverse_pin, 0)
        self.set_motor_speed(self.right_reverse_pin, speed)
        print("Turning right...")

    def move_reverse(self, speed):
        self.set_motor_speed(self.left_forward_pin, 0)
        self.set_motor_speed(self.right_forward_pin, 0)
        self.set_motor_speed(self.left_reverse_pin, speed)
        self.set_motor_speed(self.right_reverse_pin, speed)
        print("Moving in reverse...")

    def stop(self):
        self.set_motor_speed(self.left_forward_pin, 0)
        self.set_motor_speed(self.right_forward_pin, 0)
        self.set_motor_speed(self.left_reverse_pin, 0)
        self.set_motor_speed(self.right_reverse_pin, 0)
        print("stop")

    def move_counterclock(self, speed):
        self.set_motor_speed(self.left_forward_pin, 0)
        self.set_motor_speed(self.right_forward_pin, speed)
        self.set_motor_speed(self.left_reverse_pin, speed)
        self.set_motor_speed(self.right_reverse_pin, 0)
        print("Moving counter clockwise...")
    
    def move_clockwise(self, speed):
        self.set_motor_speed(self.left_forward_pin, speed)
        self.set_motor_speed(self.right_forward_pin, 0)
        self.set_motor_speed(self.left_reverse_pin, 0)
        self.set_motor_speed(self.right_reverse_pin, speed)
        print("Moving clockwise...")

    '''
        start_sensorfusion() is a function that takes the values of the accelerometer, gyroscope, and magnetometer 
        and uses them to calculate the roll, pitch, and yaw of the robot using the Kalman Filter.
        It should continuously run in the background and update the sensorfusion object as calculations and tasks are done.
    '''
    def start_sensorfusion(self):
        currTime = time.time()
        while True:
            ax, ay, az, wx, wy, wz = mpu6050_conv() # re ad and convert mpu6050 data
            mx, my, mz = AK8963_conv()
            newTime = time.time()
            dt = newTime - currTime
            currTime = newTime

            self.sensorfusion.computeAndUpdateRollPitchYaw(ax, ay, az, wx, wy, wz, mx, my, mz, dt)
            #print("Roll: {0} ; Pitch: {1} ; Yaw: {2}".format(self.sensorfusion.roll, self.sensorfusion.pitch, self.sensorfusion.yaw))
            
            time.sleep(0.05)

    def set_state(self, state):
        self.state = state

    def start_movement(self):
        current_state = self.state  # Get the initial state

        while True:
            if current_state != self.state:
                # State has changed, handle it here
                current_state = self.state  # Update the current state
                if self.state == States.MOVING_FORWARD:
                    self.move_forward(speed=50)
                elif self.state == States.MOVING_BACKWARD:
                    self.move_backward(speed=50)
                elif self.state == States.TURNING_LEFT:
                    self.turn_left(degrees=90)
                elif self.state == States.TURNING_RIGHT:
                    self.turn_right(degrees=90)
                elif self.state == States.IDLE:
                    self.stop()
                else:
                    raise Exception("Invalid state!")
                
    '''
        robot_controller_gui() is a function that utilizes the tkinter module to create a GUI that allows the user to control the robot.
    '''
    def robot_controller_gui(robot, speed):
        # Create the main window
        root = tk.Tk()
        root.title("Henry Control")

        # Create a frame to contain the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(padx=20, pady=20)

        # Create and configure buttons
        # Note: The lambda function is used to pass a parameter to the function called by the button
        # Note: IN THE FUTURE, the command parameters should call functions that change the robot's state
        button_forward = tk.Button(button_frame, text="Forward", command=lambda: robot.move_forward(speed))
        button_reverse = tk.Button(button_frame, text="Reverse", command=lambda: robot.move_reverse(speed))
        button_left = tk.Button(button_frame, text="Left", command=lambda: robot.move_counterclock(speed))
        button_right= tk.Button(button_frame, text="Right", command=lambda: robot.move_clockwise(speed))
        button_stop = tk.Button(button_frame, text="Stop", command=lambda: robot.stop(speed))

        # Pack the buttons
        button_forward.pack(side=tk.LEFT, padx=10)
        button_left.pack(side=tk.LEFT, padx=10)
        button_right.pack(side=tk.LEFT, padx=10)
        button_reverse.pack(side=tk.LEFT, padx=10)
        button_stop.pack(side=tk.LEFT, padx=10)

        # Start the Tkinter main loop
        root.mainloop()

if __name__ == "__main__":
    # Main logic for your script goes here
    robot = Robot(pwm_frequency=50)

    # Create threads to run processes simultaneously
    t1 = Thread(target=robot.start_sensorfusion)
    t2 = Thread(target=robot.turn_left)

    t1.start()
    t2.start()

    # robot.start_movement() T2
    # robot.start_ultrasound() T3
    # robot_controller_gui(robot, 50) T4

    # robot.start_object_detection() T5
    # robot.start_pathfinding() T6