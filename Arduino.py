from pylab import *

import numpy as np
import serial
import time
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=1)


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.1)
    data = arduino.readline()
    return data
    
# define some grids
def create_xy_raster(x1, y1, z1, x2, y2, z2, step):
    xgrid = linspace(x1, x2, step)
    ygrid = arange(y1, y2)
    zgrid = arange(z1, z2)
    xscan = []
    yscan = []
    zscan = []
    for j in zgrid:
        for i, yi in enumerate(ygrid):
            xscan.append(xgrid[::(-1)**i])
            yscan.append(ones_like(xgrid) * yi)
            zscan.append(ones_like(xgrid) * j)
            
    xscan = concatenate(xscan)
    yscan = concatenate(yscan)
    zscan = concatenate(zscan)
    cart_xyz = np.matrix([xscan, yscan, zscan])
    return cart_xyz

def cart2delta(cart_xyz, amp=500):
    mul = np.zeros((3, 3), int)
    np.fill_diagonal(mul, amp)
    rotation_matrix = np.matrix([[-0.8660, 0.8660, 0], [0.5, 0.5, -1], [1, 1, 1]])
    rotation_inv = np.linalg.inv(rotation_matrix)
    delta_abc = rotation_inv*cart_xyz
    delta_abc = mul*delta_abc
    return delta_abc


def write_delta(delta_abc, wait = 'false'):
    column = delta_abc.shape[1]
    a = [0, 0, 0]
    for i in range(column):
        if(wait == 'true'):
            input("Press Enter to continue")

            strings = "mr " + str(delta_abc[:, i].item(0) - a[0]) + " " + str(delta_abc[:, i].item(1) - a[1]) + " " + str(delta_abc[:, i].item(2) - a[2])
            print(strings)
            a = [(delta_abc[:, i].item(0)), (delta_abc[:, i].item(1)), (delta_abc[:, i].item(2))]


def goto_pos(x1, y1, z1):
    write_read("zero")
    cord_matrix = np.matrix([[0, x1], [0, y1], [0, z1]])
    delta_abc = cart2delta(cord_matrix)
    write_delta(delta_abc)

goto_pos(1, 1, 1)
goto_pos(2, 1, 1)

step = 5
cart_xyz = create_xy_raster(1, 0, 0, 8, 5, 1, step)
delta_abc = cart2delta(cart_xyz, 500)
write_delta(delta_abc, 'true')





