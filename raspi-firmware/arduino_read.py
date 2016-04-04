""" this is reallllly reallllllllly terrible code """

import serial
import sys
import time
import matplotlib.pyplot as plt

x_min = 0
x_max = 8
y_min = 200
y_max = 600

try:
    y_min = int(sys.argv[1])
    y_max = int(sys.argv[2])
except:
    pass

try:
    ser = serial.Serial('/dev/tty.usbmodem1421', 9600, timeout=1)
except:
    ser = serial.Serial('/dev/tty.usbmodem1411', 9600, timeout=1)

plt.subplot(3,1,1)
plt.axis([0, x_max, y_min, y_max])
# plt.ion()
plt.title('X-Direction')

plt.subplot(3,1,2)
plt.axis([0, x_max, y_min, y_max])
# plt.ion()
plt.title('Y-Direction')

plt.subplot(3,1,3)
plt.axis([0, x_max, y_min, y_max])
plt.title('Z-Direction')

plt.ion()
plt.show()

num_datapoints = 0

out_file = open('accOutput.txt', 'w')

prev_x = 0
prev_y = 0
prev_z = 0

while True:
    try:
        value = ser.readline().split(',')
        if value == []:
            continue
        x_val = value[0]
        y_val = value[1]
        z_val = value[2].strip('\r\n')

        num_datapoints += 1
        if num_datapoints > x_max:
            x_max *= 2
            for i in xrange(1,4):
                plt.subplot(3,1,i)
                plt.axis([0, x_max, y_min, y_max])

        plt.subplot(3,1,1)
        plt.scatter(num_datapoints, x_val)
        plt.subplot(3,1,2)
        plt.scatter(num_datapoints, y_val)
        plt.subplot(3,1,3)
        plt.scatter(num_datapoints, z_val)
        # if (num_datapoints % 7 == 0):
        plt.draw()

        print x_val, y_val, z_val, time.time()

        prev_x = x_val
        prev_y = y_val
        prev_z = z_val

        out_data = '{x},{y},{z},{time}\n'.format(x=x_val, y=y_val, z=z_val, time=time.time())
        out_file.write(out_data)
        if num_datapoints % 50 == 0: # Update text file every 50 reads
            out_file.close()
            out_file = open('accOutput.txt', 'a')
    except:
        continue # lol
