import math
import time
import board
import busio
import Jetson.GPIO as GPIO
from adafruit_pca9685 import PCA9685
import numpy as np
import tkinter as tk
from imusensor.filters import kalman 
from mpu9250_i2c import *
from PIDController import PIDController
from USensor import USensor
from States import States
from threading import Thread
import csv

class Robot:



    def __init__(self, pwm_frequency):



        # Initialize PCA9685 object with I2C
        self.pca = PCA9685(busio.I2C(board.SCL_1, board.SDA_1)) 
        self.pca.frequency = pwm_frequency  # Set PWM frequency to 50 Hz
        
        # Define the PWM channels for the robot's motors      
        pins = {
            "left_forward": 0,
            "left_reverse": 1,
            "right_forward": 2,
            "right_reverse": 3
        }
          
        self.left_forward_pin = pins.get("left_forward")
        self.left_reverse_pin = pins.get("left_reverse")
        self.right_forward_pin = pins.get("right_forward")
        self.right_reverse_pin = pins.get("right_reverse")

        # Initialize the Kalman filter
        self.sensorfusion = kalman.Kalman()
        self.state = States.IDLE

        self.state_queue = []

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

    # This should replace the move_forward() once it has been tested
    def cruise_control(self, speed): 
        time.sleep(5)
        target_yaw = self.get_yaw()  # capture the yaw at the moment the robot started moving forward

        self.set_motor_speed(self.left_reverse_pin, 0)
        self.set_motor_speed(self.right_reverse_pin, 0)
        self.set_motor_speed(self.left_forward_pin, speed)
        self.set_motor_speed(self.right_forward_pin, speed)
        print("Moving forward...")

        pid_controller = PIDController(kp=1.0, ki=0.1, kd=0.01, max_out=100-speed) # values of kp, ki, and kd will need tuning

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
            left_speed = speed + correction 
            right_speed = speed - correction

            print("Left Speed", left_speed)
            print("Right Speed", right_speed)
            self.set_motor_speed(self.left_forward_pin, left_speed)
            self.set_motor_speed(self.right_forward_pin, right_speed)
            time.sleep(1)

    def turn_left(self, degrees=90):
        current_yaw = self.get_yaw() # Get the yaw in degrees
        yaw_to_be = current_yaw - degrees # Calculate what the yaw should be after turning
        yaw_left = degrees # Calculate how much yaw is left to turn
        error = 5 # Error in degrees
        while not yaw_to_be - error <= current_yaw <= yaw_to_be + error: # While the yaw is not within the error range
            current_yaw = self.get_yaw() # Get the current yaw
            yaw_left = current_yaw - yaw_to_be # Calculate how much yaw is left to turn
            turn_speed = 50 + 50*np.sin((np.pi*(yaw_left - 22.5))/45) # Calculate the speed to turn at, assumes degrees is 90 and motors move the entire duty cycle range
            #print("turn_speed", turn_speed)
            self.counter_clockwise(turn_speed)
            print("yaw_left: ", yaw_left)
            time.sleep(0.5)
        self.set_state(States.IDLE)

    def turn_right(self, degrees=90):
        current_yaw = self.get_yaw() # Get the yaw in degrees
        yaw_to_be = current_yaw + degrees # Calculate what the yaw should be after turning
        yaw_left = degrees # Calculate how much yaw is left to turn
        error = 5 # Error in degrees
        while not yaw_to_be - error <= current_yaw <= yaw_to_be + error: # While the yaw is not within the error range
            current_yaw = self.get_yaw() # Get the current yaw
            yaw_left = yaw_to_be - current_yaw # Calculate how much yaw is left to turn
            turn_speed = 50 + 50*np.sin((np.pi*(yaw_left - 22.5))/45) # Calculate the speed to turn at, assumes degrees is 90 and motors move the entire duty cycle range
            print("turn_speed", turn_speed)
            self.clockwise(turn_speed)
            print("yaw_left: ", yaw_left)
            time.sleep(0.5)
        self.set_state(States.IDLE)

    def move_forward(self, speed):
        self.set_motor_speed(self.left_reverse_pin, 0)
        self.set_motor_speed(self.right_reverse_pin, 0)
        self.set_motor_speed(self.left_forward_pin, speed)
        self.set_motor_speed(self.right_forward_pin, speed)
        print("Moving forward")

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

    def clockwise(self, speed):
        self.set_motor_speed(self.left_forward_pin, speed)
        self.set_motor_speed(self.right_forward_pin, 0)
        self.set_motor_speed(self.left_reverse_pin, 0)
        self.set_motor_speed(self.right_reverse_pin, speed)
        print("Moving clockwise...")

    def counter_clockwise(self, speed):
        self.set_motor_speed(self.left_forward_pin, 0)
        self.set_motor_speed(self.right_forward_pin, speed)
        self.set_motor_speed(self.left_reverse_pin, speed)
        self.set_motor_speed(self.right_reverse_pin, 0)
        print("Moving counter clockwise...")

    '''
        start_sensorfusion() is a function that takes the values of the accelerometer, gyroscope, and magnetometer 
        and uses them to calculate the roll, pitch, and yaw of the robot using the Kalman Filter.
        It should continuously run in the background and update the sensorfusion object with yaw, roll, and pitch as calculations and tasks are done.
    '''
    def start_sensorfusion(self):

        cal_filename = 'mpu9250_cal_params.csv'

        # Open the calibration file and store the offsets into cal_offsets
        cal_offsets = np.array([[],[],[],0.0,0.0,0.0,[],[],[]]) # cal vector
        with open(cal_filename,'r',newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            iter_ii = 0
            for row in reader:
                if len(row)>2:
                    row_vals = [float(ii) for ii in row[int((len(row)/2)+1):]]
                    cal_offsets[iter_ii] = row_vals
                else:
                    cal_offsets[iter_ii] = float(row[1])
                iter_ii+=1

        currTime = time.time()
        while True:
            ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
            mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data

            mx = mx - cal_offsets[6]
            my = my - cal_offsets[7]
            mz = mz - cal_offsets[8]
            #print(ax)
            newTime = time.time()
            dt = newTime - currTime
            currTime = newTime

            self.sensorfusion.computeAndUpdateRollPitchYaw(ax, ay, az, wx, wy, wz, mx, my, mz, dt)
            print("Roll: {0} ; Pitch: {1} ; Yaw: {2}".format(self.sensorfusion.roll, self.sensorfusion.pitch, self.sensorfusion.yaw))
            
            time.sleep(0.5)
           

    # set_state() should be the only way to change the direction of the robot.
    # Later, have it update the state_queue instead of just setting the state
    def set_state(self, state):
        # Ensure the state is valid
        if state in States:
            self.state = state
        else:
            raise Exception("Invalid state!")

    '''
        start_movement_controller() is a function that should continuously run in the background and check the state of the robot.
        It should call the appropriate function to move the robot based on the state. Later, it will also manage state_queue    
    '''
    def start_movement_controller(self):
        current_state = self.state  # Get the initial state

        while True:
            if current_state != self.state:
                # State has changed, handle it here
                current_state = self.state  # Update the current state
                if self.state == States.MOVING_FORWARD:
                    self.move_forward(speed=50) #self.cruise_control(speed=50)
                elif self.state == States.MOVING_BACKWARD:
                    self.move_reverse(speed=50)
                elif self.state == States.TURNING_LEFT:
                    self.turn_left(degrees=90)
                elif self.state == States.TURNING_RIGHT:
                    self.turn_right(degrees=90)
                elif self.state == States.IDLE:
                    self.stop()
                elif self.state == States.CLOCKWISE:
                    self.clockwise(speed=50)
                elif self.state == States.COUNTER_CLOCKWISE:
                    self.counter_clockwise(speed=50)
                else:
                    raise Exception("Invalid state!")
                
    def start_ultrasound(self):
        GPIO.setmode(GPIO.BOARD)

        usensor1 = USensor(name="front1", trig=16, echo=18)
        usensor2 = USensor(name="front2", trig=19, echo=21)
        usensor3 = USensor(name="side1", trig=23, echo=24)
        usensor4 = USensor(name="side2", trig=26, echo=22)

        while True:
            if(usensor1.send_ultrasound() or usensor2.send_ultrasound() or usensor3.send_ultrasound() or usensor4.send_ultrasound()):
                self.set_state(States.IDLE) # Stop the robot if an object is within 1 meter        
            time.sleep(0.5)

    def start_object_detection(self):
        #TODO: Implement object detection
        pass
                
'''
    robot_controller_gui() is a function that utilizes the tkinter module to create a GUI that allows the user to control the robot.
'''
def robot_controller_gui(robot):
    # Create the main window
    root = tk.Tk()
    root.title("Henry Control")

    # Create a frame to contain the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(padx=20, pady=20)

    # Create and configure buttons
    # Note: The lambda function is used to pass a parameter to the function called by the button
    button_forward = tk.Button(button_frame, text="Forward", command=lambda: robot.set_state(States.MOVING_FORWARD))
    button_reverse = tk.Button(button_frame, text="Reverse", command=lambda: robot.set_state(States.MOVING_BACKWARD))
    button_left = tk.Button(button_frame, text="Left", command=lambda: robot.set_state(States.TURNING_LEFT))
    button_right= tk.Button(button_frame, text="Right", command=lambda: robot.set_state(States.TURNING_RIGHT))
    button_stop = tk.Button(button_frame, text="Stop", command=lambda: robot.set_state(States.IDLE))

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

    t1 = Thread(target=robot.start_movement_controller)
    t2 = Thread(target=robot.start_sensorfusion)
    t3 = Thread(target=lambda: robot_controller_gui(robot))
    t1.start()
    print("got here")
    t2.start()
    print("got here")
    t3.start()

    #robot.set_state(States.MOVING_FORWARD)
    print("got here2")


    ''' replace this with multiprocessing
    # Create threads to run processes simultaneously
    t1 = Thread(target=robot.start_sensorfusion)
    t1.start()
    time.sleep(4) # Wait for the sensor fusion to start & initialize for accurate readings
    t2 = Thread(target=robot.start_ultrasound)
    t3 = Thread(target=robot.start_movement_controller)
    t2.start()
    t3.start()

    # robot.start_object_detection() T4
    # robot.start_pathfinding() T5
    '''
