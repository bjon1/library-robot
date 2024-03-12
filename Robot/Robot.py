import math
import time
import board
import busio
import Jetson.GPIO as GPIO
from adafruit_pca9685 import PCA9685
from mpu9250_i2c import *
from SensorFusion import Orientation
from PIDController import PIDController
from USensor import USensor
from States import States
from threading import Thread
from multiprocessing import Process

class Robot:



    def __init__(self, pwm_frequency):



        # Initialize PCA9685 object with I2C
        self.pca = PCA9685(busio.I2C(board.SCL_1, board.SDA_1)) #28, 27
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
        self.orientation = Orientation()
        self.state = States.IDLE # This variable is only to be changed and accessed by set_state() 
        self.speed = 50 # This variable is only to be changed and accessed by set_speed() and handle_state_change()

        self.state_queue = []

    def get_yaw(self):
        if self.orientation.yaw == 0 and self.orientation.roll == 0 and self.orientation.pitch == 0:
            raise Exception("Sensor fusion has not been started. Call start_sensorfusion() first.")
        print(self.orientation.yaw)
        return self.orientation.yaw
    
    def get_pitch(self):
        if self.orientation.yaw == 0 and self.orientation.roll == 0 and self.orientation.pitch == 0:
            raise Exception("Sensor fusion has not been started. Call start_sensorfusion() first.")
        return self.orientation.pitch

    def get_roll(self):
        if self.orientation.yaw == 0 and self.orientation.roll == 0 and self.orientation.pitch == 0:
            raise Exception("Sensor fusion has not been started. Call start_sensorfusion() first.")
        return self.orientation.roll

    def set_motor_speed(self, pin, speed):
        # Ensure the speed is within the valid range (0 to 100)
        speed = max(0, min(100, speed))
        # Convert the speed to a PWM value (0 to 4095)
        pwm_value = int(speed * 40.95)
        self.pca.channels[pin].duty_cycle = pwm_value * 0x10000 // 4096

    # This should replace the move_forward() once it has been tested
    def cruise_control(self, speed): 
        time.sleep(1)
        target_yaw = self.get_yaw() # Get the current yaw
        speed = min(80, speed) # Ensure the speed is within the valid range (0 to 100)

        self.set_motor_speed(self.left_reverse_pin, 0)
        self.set_motor_speed(self.right_reverse_pin, 0)
        self.set_motor_speed(self.left_forward_pin, speed)
        self.set_motor_speed(self.right_forward_pin, speed)
        print("Moving forward...")

        pid_controller = PIDController(kp=10.0, ki=0.10, kd=0.10, max_out=100-speed) # values of kp, ki, and kd will need tuning

        while(self.state == States.CRUISE):
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
            time.sleep(0.2)

    def turn_left(self, degrees=90):
        current_yaw = self.get_yaw() # Get the yaw in degrees
        yaw_to_be = current_yaw - degrees # Calculate what the yaw should be after turning
        yaw_left = degrees # Calculate how much yaw is left to turn
        error = 0.2 # Error in degrees
        while (abs(yaw_left) > error or current_yaw >= yaw_to_be) and self.state == States.TURNING_LEFT:
            current_yaw = self.get_yaw() # Get the current yaw
            yaw_left = current_yaw - yaw_to_be # Calculate how much yaw is left to turn
            turn_speed = 65 + 35*np.sin((np.pi*(yaw_left - 22.5))/45) # Calculate the speed to turn at, assumes degrees is 90 and motors move the entire duty cycle range
            #print("turn_speed", turn_speed)
            self.counter_clockwise(turn_speed)
            print("yaw_left: ", yaw_left)
            time.sleep(0.1)
        self.set_state(States.IDLE)

    def turn_right(self, degrees=90):
        current_yaw = self.get_yaw() # Get the yaw in degrees
        yaw_to_be = current_yaw + degrees # Calculate what the yaw should be after turning
        yaw_left = degrees # Calculate how much yaw is left to turn
        error = 0.2
        while (abs(yaw_left) > error or current_yaw <= yaw_to_be) and self.state == States.TURNING_RIGHT:

            current_yaw = self.get_yaw() # Get the current yaw
            yaw_left = yaw_to_be - current_yaw # Calculate how much yaw is left to turn
            turn_speed = 65 + 35*np.sin((np.pi*(yaw_left - 22.5))/45) # Calculate the speed to turn at, assumes degrees is 90 and motors move the entire duty cycle range
            print("turn_speed", turn_speed)
            self.clockwise(turn_speed)
            print("yaw_left: ", yaw_left)
            time.sleep(0.1)
        self.set_state(States.IDLE)

    def move_forward(self, speed):
        if self.state == States.FORWARD:
            self.set_motor_speed(self.left_reverse_pin, 0)
            self.set_motor_speed(self.right_reverse_pin, 0)
            self.set_motor_speed(self.left_forward_pin, speed)
            self.set_motor_speed(self.right_forward_pin, speed)
            print("Moving forward")

    def move_reverse(self, speed):
        if self.state == States.REVERSE:
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
        if self.state == States.CLOCKWISE or self.state == States.TURNING_RIGHT:
            self.set_motor_speed(self.left_forward_pin, 0)
            self.set_motor_speed(self.right_forward_pin, speed)
            self.set_motor_speed(self.left_reverse_pin, speed)
            self.set_motor_speed(self.right_reverse_pin, 0)
            print("Moving clockwise...")

    def counter_clockwise(self, speed):
        if self.state == States.COUNTER_CLOCKWISE or self.state == States.TURNING_LEFT:
            self.set_motor_speed(self.left_forward_pin, speed)
            self.set_motor_speed(self.right_forward_pin, 0)
            self.set_motor_speed(self.left_reverse_pin, 0)
            self.set_motor_speed(self.right_reverse_pin, speed)
            print("Moving counter clockwise...")


    '''
        start_sensorfusion() is a function that takes the values of the accelerometer, gyroscope, and magnetometer 
        and uses them to calculate the roll, pitch, and yaw of the robot using the Kalman Filter.
        It should continuously run in the background and update the orientation object with yaw, roll, and pitch as calculations and tasks are done.
    '''
    def start_sensorfusion(self):

        # Calculate Error First. Make sure the robot is stationary
        ax_error, ay_error, az_error, gx_error, gy_error, gz_error = 0, 0, 0, 0, 0, 0

        for i in range(200):
            if self.state != States.IDLE:
                raise Exception("Robot is not stationary! Please ensure the robot is stationary before starting sensor fusion.")
            ax,ay,az,gx,gy,gz = mpu6050_conv()
            ax_error += (math.atan((ay) / math.sqrt(pow((ax), 2) + pow((az), 2))) * 180 / math.pi)
            ay_error += (math.atan(-1 * (ax) / math.sqrt(pow((ay), 2) + pow((az), 2))) * 180 / math.pi)
            gx_error += gx
            gy_error += gy
            gz_error += gz
        
        # Calculate the average error
        ax_error = ax_error/200
        ay_error = ay_error/200
        gx_error = gx_error/200
        gy_error = gy_error/200
        gz_error = gz_error/200

        g_roll = 0
        g_pitch = 0
        yaw = 0
    
        t_current = time.time()
        while True:
            
            ax,ay,az,gx,gy,gz = mpu6050_conv() # read and convert mpu6050 data
            #mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data

            a_roll = (math.atan(ay / math.sqrt(pow(ax, 2) + pow(az, 2))) * 180 / math.pi) - ax_error
            a_pitch = (math.atan(-1 * ax / math.sqrt(pow(ay, 2) + pow(az, 2))) * 180 / math.pi) - ay_error

            gx -= gx_error
            gy -= gy_error
            gz -= gz_error

            t_previous = t_current
            t_current = time.time()
            dt = t_current - t_previous # make sure this is in seconds

            g_roll += gx * dt
            g_pitch += gy * dt
            yaw += gz * dt

            # complementary filter
            self.orientation.roll = (0.96 * g_roll) + (0.04 * a_roll) 
            self.orientation.pitch = (0.96 * g_pitch) + (0.04 * a_pitch) 
            self.orientation.yaw = yaw

            print("Roll: {0} ; Pitch: {1} ; Yaw: {2}".format(self.orientation.roll, self.orientation.pitch, self.orientation.yaw))


            time.sleep(.1) #5Hz
            
    def set_state(self, new_state, speed=None):
        # Ensure the state is valid
        if new_state in States:
            if speed is not None:
                self.speed = max(0, min(100, speed))
            self.state = new_state
        else:
            raise Exception("Invalid state!")
            

    # start_movement_controller() is a function that handles incoming bluetooth requests, continuously checks the state of the robot, and performs the appropriate action based on the state.
    def start_movement_controller(self):
        current_state = self.state  # Get the initial state
        while True:
            if(current_state != self.state):
                self.stop()
                time.sleep(0.05)
                # State has changed, handle it here
                current_state = self.state  # Update the current state

                if self.state == States.FORWARD:
                    self.move_forward(speed=self.speed)
                elif self.state == States.REVERSE:
                    self.move_reverse(speed=self.speed)
                elif self.state == States.TURNING_LEFT:
                    self.turn_left(degrees=90)
                elif self.state == States.TURNING_RIGHT:
                    self.turn_right(degrees=90)
                elif self.state == States.IDLE:
                    self.stop()
                elif self.state == States.CLOCKWISE:
                    self.clockwise(speed=self.speed)
                elif self.state == States.COUNTER_CLOCKWISE:
                    self.counter_clockwise(speed=self.speed)
                elif self.state == States.CRUISE:
                    self.cruise_control(speed=self.speed)
                else:
                    raise Exception("Invalid state!")
                
    def start_ultrasound(self):

        try:

            usensor1 = USensor(name="front1", trig=16, echo=18) #The values of trig & echo will be converted from BOARD pin name to TEGRA_SOC name
            time.sleep(0.5)
            usensor2 = USensor(name="front2", trig=19, echo=21)
            #usensor3 = USensor(name="side1", trig=23, echo=24)
            #usensor4 = USensor(name="side2", trig=26, echo=22)

            
            if(usensor1.send_ultrasound()):
                self.set_state(States.IDLE) # Stop the robot if an object is within 1 meter       
                print("STOP") 

            

            if(usensor2.send_ultrasound()):
                self.set_state(States.IDLE)
                print("STOP")
        
        except Exception as e:
            GPIO.cleanup()
            print("Error:", e)
            

    def start_object_detection(self):
        #TODO: Implement object detection
        pass


    def handle_incoming_data(self):
        import serial
        port = '/dev/ttyTHS1' # Jetson Nano UART port 8 (TXD), 10 (RXD)
        baud = 9600

        ser = serial.Serial(port, baud, timeout=0.5)

        print("Connected to: " + ser.portstr)

        try:
            while True:
                data = None
                new_state = None
                new_speed = None

                # Check for incoming bluetooth requests
                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting).decode('utf-8')
                    print("Found New Data", data)

                if data and data.isdigit():
                    data = int(data)
                    if data > 0 and data < 10:
                        command_to_state = {
                            1: States.CRUISE,
                            2: States.FORWARD,
                            3: States.REVERSE,
                            4: States.TURNING_LEFT,
                            5: States.TURNING_RIGHT,
                            6: States.CLOCKWISE,
                            7: States.COUNTER_CLOCKWISE,
                            8: States.IDLE,
                            9: States.IDLE
                        }
                        new_state = command_to_state.get(data)
                    elif data >= 10 and data <= 100: 
                        new_speed = int(data)
                elif data == 'OK+LOST' or data == 'OK+CONN': # OK+CONN or OK+LOST
                    new_state = States.IDLE
                if new_state is None:
                    new_state = self.state
                if new_speed is None:
                    new_speed = self.speed
                self.set_state(new_state, new_speed)
                print("STATE", self.state)
                time.sleep(0.20)
        except KeyboardInterrupt:
            pass
        finally:
            ser.close()
                


if __name__ == "__main__":
    try:
        robot = Robot(pwm_frequency=50)
        
        t1 = Thread(target=robot.start_movement_controller)
        #t2 = Thread(target=robot.start_sensorfusion)
        t3 = Thread(target=robot.handle_incoming_data)
        t4 = Thread(target=robot.start_ultrasound)
        t1.start()
        print("got here")
        #t2.start()
        print("got here")
        t3.start()
        print("got here")
        t4.start()
    except Exception as e:
        print("Error", e)
        GPIO.cleanup()

    '''
    p1 = Process(target=robot.start_movement_controller)
    p2 = Process(target=robot.start_sensorfusion)
    p3 = Process(target=lambda: robot_controller_keyboard(robot)) #replace this process with keyboard arrow key controls
    p1.start()
    print("got here")
    p2.start()
    print("got here")
    p3.start()
    '''


    ''' Overall sequence; to be replaced by Process class
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
