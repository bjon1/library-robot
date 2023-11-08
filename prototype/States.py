from enum import Enum

class States(Enum):
    IDLE = 0
    MOVING_FORWARD = 1
    MOVING_BACKWARD = 2
    TURNING_LEFT = 3
    TURNING_RIGHT = 4
    CLOCKWISE = 5
    COUNTER_CLOCKWISE = 6
    
