import math
from madgwickAHRS import MadgwickAHRS

def calculate_orientation(accel_data, gyro_data, mag_data):
    # Create an instance of the MadgwickAHRS class, with a sample period of 256 times per second
    madgwick_filter = MadgwickAHRS(sampleperiod=1/256)

    # Update the Madgwick filter with new sensor data
    madgwick_filter.update(gyro_data, accel_data, mag_data)

    # Get the current quaternion output from the filter
    # A quaternion is a complex number that can be used to represent orientation in 3D space
    q = madgwick_filter.quaternion

    # Convert quaternion to Euler angles
    roll, pitch, yaw = q.to_euler_angles_XYZ()

    # Convert to degrees
    yaw *= 180.0 / math.pi
    pitch *= 180.0 / math.pi
    roll *= 180.0 / math.pi

    return yaw, pitch, roll


