from imu.mpu9250 import MPU9250
import time

imu = MPU9250(bus=1, device_addr=0x68)
imu.mag.cal
imu.accel.cal
imu.gyro.cal


while True:
    time.sleep(0.5)
    #print("ACCEL", imu.accel.xyz)
    print("GYROSCOPE", imu.gyro.xyz)
    #print("MAGNOMETER", imu.mag.xyz)
    #print("TEMPERATURE", imu.temperature)
