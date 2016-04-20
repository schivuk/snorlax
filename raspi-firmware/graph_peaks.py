import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks_cwt
import random

peak_threshold = 4

def acc_algorithm(vals, threshold):
    num_vals = len(vals)
    peaks = set()

    for i in xrange(0, num_vals-10):
        next_ten_average = sum(vals[i:i+10])/10
        if next_ten_average > vals[i]+threshold:
            peaks.add(i)

    for i in xrange(0, num_vals-10):
        next_ten_average = sum(vals[i:i+10])/10
        if next_ten_average < vals[i]-threshold:
            peaks.add(i)

    for i in xrange(10, num_vals):
        prev_ten_average = sum(vals[i-10:i])/10
        if prev_ten_average < vals[i] - threshold:
            peaks.add(i)

    for i in xrange(10, num_vals):
        prev_ten_average = sum(vals[i-10:i])/10
        if prev_ten_average > vals[i] + threshold:
            peaks.add(i)

    return peaks

def mic_algorithm(vals, threshold):
    average = sum(vals)/len(vals)
    print average
    peaks = set()

    for i in xrange(len(vals)):
        val = vals[i]
        if abs(val-average) > threshold:
            peaks.add(i)

    return peaks

filename = 'accAndMicrophoneQuick.txt'

with open(filename) as f:
    mic_vals = []
    x_vals = []
    y_vals = []
    z_vals = []
    timestamps = []

    for line in f.readlines():

        mic,x,y,z,timestamp = line.strip('\n').split(',')
        mic = mic.lstrip('\x00')
        x = x.lstrip('\x00')
        y = y.lstrip('\x00')
        z = z.lstrip('\x00')

        mic_vals.append(int(mic))
        x_vals.append(int(x))
        y_vals.append(int(y))
        z_vals.append(int(z))
        timestamps.append(timestamp)

    timestamps = range(1,len(x_vals)+1)

    x_peaks = acc_algorithm(x_vals,4)
    y_peaks = acc_algorithm(y_vals,4)
    z_peaks = acc_algorithm(z_vals,4)
    mic_peaks = mic_algorithm(mic_vals,100)

    plt.subplot(4,1,1)
    plt.title('x vs. Time')
    for i in xrange(len(x_vals)):
        if i in x_peaks:
            plt.scatter(timestamps[i], x_vals[i], color='red')
        else:
            plt.scatter(timestamps[i], x_vals[i], color='green')

    plt.subplot(4,1,2)
    plt.title('y vs. Time')
    for i in xrange(len(y_vals)):
        if i in y_peaks:
            plt.scatter(timestamps[i], y_vals[i], color='red')
        else:
            plt.scatter(timestamps[i], y_vals[i], color='green')

    plt.subplot(4,1,3)
    plt.title('z vs. Time')
    for i in xrange(len(z_vals)):
        if i in z_peaks:
            plt.scatter(timestamps[i], z_vals[i], color='red')
        else:
            plt.scatter(timestamps[i], z_vals[i], color='green')

    plt.subplot(4,1,4)
    plt.title('Microhpone vs. Time')
    for i in xrange(len(mic_vals)):
        if i in mic_peaks:
            plt.scatter(timestamps[i], mic_vals[i], color='red')
        else:
            plt.scatter(timestamps[i], mic_vals[i], color='green')

    plt.show()
