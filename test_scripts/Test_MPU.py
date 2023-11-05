import time
from mpu9250_i2c import *
from imusensor.filters import kalman 

def start_sensorfusion():
    currTime = time.time()
    sensorfusion = kalman.Kalman()
    while True:
        ax, ay, az, wx, wy, wz = mpu6050_conv() # re ad and convert mpu6050 data
        mx, my, mz = AK8963_conv()
        newTime = time.time()
        dt = newTime - currTime
        currTime = newTime

        sensorfusion.computeAndUpdateRollPitchYaw(ax, ay, az, wx, wy, wz, mx, my, mz, dt)
        print("Roll: {0} ; Pitch: {1} ; Yaw: {2}".format(sensorfusion.roll, sensorfusion.pitch, sensorfusion.yaw))
        
        time.sleep(0.10)

start_sensorfusion()

