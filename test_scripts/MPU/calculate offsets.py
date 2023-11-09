import numpy as np
import csv
from mpu9250_i2c import *


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

ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data

print(ax, ay, az)

ax = cal_offsets[0][0] * ax + cal_offsets[0][1]
ay = cal_offsets[1][0] * ay + cal_offsets[1][1]
az = cal_offsets[2][0] * az + cal_offsets[2][1]

wx = wx - cal_offsets[3]
wy = wy - cal_offsets[4]
wz = wy - cal_offsets[5]

cal_rot_indicies = [[6,7],[7,8],[6,8]]
mx = mx - cal_offsets[cal_rot_indicies[0][0]]
my = my - cal_offsets[cal_rot_indicies[1][0]]
mz = mz - cal_offsets[cal_rot_indicies[2][0]]

print(ax, ay, az)
