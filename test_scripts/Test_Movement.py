import time
import board
import busio
from adafruit_pca9685 import PCA9685
import tkinter as tk

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

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

create_gui()