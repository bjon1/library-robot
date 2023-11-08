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

plt_pts = 1000
mpu_array = np.zeros((plt_pts,9)) # pre-allocate the 9-DoF vector
mpu_array[mpu_array==0] = np.nan

ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
mx,my,mz = AK8963_conv() # read and convert AK8963 magnetometer data

mpu_array[0:-1] = mpu_array[1:] # get rid of last point
mpu_array[-1] = [ax,ay,az,wx,wy,wz,mx,my,mz] # update last point w/new data

ax = cal_offsets[0][0] * mpu_array[:, 0] + cal_offsets[0][1]
ay = cal_offsets[1][0] * mpu_array[:, 1] + cal_offsets[1][1]
az = cal_offsets[2][0] * mpu_array[:, 2] + cal_offsets[2][1]

wx = np.array(mpu_array[:, 3]) - cal_offsets[3]
wy = np.array(mpu_array[:, 4]) - cal_offsets[4]
wz = np.array(mpu_array[:, 5]) - cal_offsets[5]

cal_rot_indicies = [[6,7],[7,8],[6,8]]
mx = mpu_array[:, 6] - cal_offsets[cal_rot_indicies[0][0]]
my = mpu_array[:, 7] - cal_offsets[cal_rot_indicies[1][0]]
mz = mpu_array[:, 8] - cal_offsets[cal_rot_indicies[2][0]]