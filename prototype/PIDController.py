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
    