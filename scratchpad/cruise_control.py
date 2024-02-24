import time

class PIDController:
    def __init__(self, kp, ki, kd, max_out):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max_out = max_out
        self.error_sum = 0
        self.last_error = 0

    def update(self, error, dt):
        self.error_sum += error * dt
        derivative = (error - self.last_error) / dt
        output = (self.kp * error) + (self.ki * self.error_sum) + (self.kd * derivative)
        self.last_error = error
        return max(min(output, self.max_out), -self.max_out)

def cruise_control():
    target_yaw = get_yaw()  # capture the yaw at the moment the robot started moving forward
    pid_controller = PIDController(kp=1.0, ki=0.1, kd=0.01, max_out=50) # values of kp, ki, and kd will need tuning

    while True:
        current_yaw = get_yaw()
        error = target_yaw - current_yaw
        dt = 0.01  # time step in seconds
        time.sleep(dt)

        correction = pid_controller.update(error, dt)
        
        # 50 is the base speed, but it may need to be changed depending on the minimum duty cycle of the motors
        left_speed = 50 + correction 
        right_speed = 50 - correction

        left_forward_pin = 0 #placeholder
        right_forward_pin = 1 #placeholder

        set_motor_speed(left_forward_pin, left_speed)
        set_motor_speed(right_forward_pin, right_speed)

def get_yaw():
    pass

def set_motor_speed(pin, speed):
    pass



cruise_control()