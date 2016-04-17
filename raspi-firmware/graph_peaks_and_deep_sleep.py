import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks_cwt
import random

peak_threshold = 2
deep_sleep_threshold = 3000
rem_sleep_threshold = 6400

def set_to_list(vals):
    return sorted([val for val in vals])

def acc_algorithm(vals, timestamps):
    num_vals = len(vals)
    last_peak_time = timestamps[0];
    peaks = set()
    deep_sleep_times = set()
    rem_sleep_times = set()

    for i in xrange(0, num_vals-10):
        next_ten_average = sum(vals[i:i+10])/10
        if next_ten_average > vals[i]+peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        else:
            if timestamps[i] - last_peak_time > rem_sleep_threshold:
                rem_sleep_times.add(i)
            elif timestamps[i] - last_peak_time > deep_sleep_threshold:
                deep_sleep_times.add(i)

    for i in xrange(0, num_vals-10):
        next_ten_average = sum(vals[i:i+10])/10
        if next_ten_average < vals[i]-peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        else:
            if timestamps[i] - last_peak_time > rem_sleep_threshold:
                rem_sleep_times.add(i)
            elif timestamps[i] - last_peak_time > deep_sleep_threshold:
                deep_sleep_times.add(i)

    for i in xrange(10, num_vals):
        prev_ten_average = sum(vals[i-10:i])/10
        if prev_ten_average < vals[i] - peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        else:
            if timestamps[i] - last_peak_time > deep_sleep_threshold:
                rem_sleep_times.add(i)
            elif timestamps[i] - last_peak_time > deep_sleep_threshold:
                deep_sleep_times.add(i)

    for i in xrange(10, num_vals):
        prev_ten_average = sum(vals[i-10:i])/10
        if prev_ten_average > vals[i] + peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        else:
            if timestamps[i] - last_peak_time > deep_sleep_threshold:
                rem_sleep_times.add(i)
            elif timestamps[i] - last_peak_time > deep_sleep_threshold:
                deep_sleep_times.add(i)

    return peaks, deep_sleep_times, rem_sleep_times

filename = 'accOutputSmall.txt'

with open(filename) as f:
    # mic_vals = []
    x_vals = []
    y_vals = []
    z_vals = []
    timestamps = []

    for line in f.readlines():

        x,y,z,timestamp = line.strip('\n').split(',')
        # mic = mic.lstrip('\x00')
        x = x.lstrip('\x00')
        y = y.lstrip('\x00')
        z = z.lstrip('\x00')

        # mic_vals.append(int(mic))
        x_vals.append(int(x))
        y_vals.append(int(y))
        z_vals.append(int(z))
        timestamps.append(float(timestamp))

    int_timestamps = range(1,len(x_vals)+1)
    x_peaks, x_deep_times, x_rem_times = acc_algorithm(x_vals,int_timestamps)
    y_peaks, y_deep_times, y_rem_times = acc_algorithm(y_vals,int_timestamps)
    z_peaks, z_deep_times, z_rem_times = acc_algorithm(z_vals,int_timestamps)


    to_plot_x_rem_times = set_to_list(x_rem_times)
    to_plot_x_rem_vals = [x_vals[i] for i in to_plot_x_rem_times]

    to_plot_x_deep_times = set_to_list(x_deep_times)
    to_plot_x_deep_vals = [x_vals[i] for i in to_plot_x_deep_times]

    to_plot_x_light_times = set(int_timestamps).difference(x_deep_times).difference(x_rem_times)
    to_plot_x_light_times.remove(len(x_vals))
    to_plot_x_light_times = set_to_list(to_plot_x_light_times)

    to_plot_x_light_vals = [x_vals[i] for i in to_plot_x_light_times]

    light_to_deep_transitions = []
    deep_to_light_transitions = []
    for i in xrange(1,len(x_vals)):
        if i in x_deep_times and not i-1 in x_deep_times:
            light_to_deep_transitions.append(i)
        elif i-1 in x_deep_times and not i in x_deep_times:
            deep_to_light_transitions.append(i)

    plt.subplot(3,1,1)
    plt.title('x vs. Time')
    plt.scatter(to_plot_x_rem_times, to_plot_x_rem_vals, color='blue', s=2)
    plt.scatter(to_plot_x_deep_times, to_plot_x_deep_vals, color='red', s=2)
    plt.scatter(to_plot_x_light_times, to_plot_x_light_vals, color='green', s=2)



    to_plot_y_rem_times = set_to_list(y_rem_times)
    to_plot_y_rem_vals = [y_vals[i] for i in to_plot_y_rem_times]

    to_plot_y_deep_times = set_to_list(y_deep_times)
    to_plot_y_deep_vals = [y_vals[i] for i in to_plot_y_deep_times]

    to_plot_y_light_times = set(int_timestamps).difference(y_deep_times).difference(y_rem_times)
    to_plot_y_light_times.remove(len(y_vals))
    to_plot_y_light_times = set_to_list(to_plot_y_light_times)

    to_plot_y_light_vals = [y_vals[i] for i in to_plot_y_light_times]

    plt.subplot(3,1,2)
    plt.title('y vs. Time')
    plt.scatter(to_plot_y_rem_times, to_plot_y_rem_vals, color='blue', s=2)
    plt.scatter(to_plot_y_deep_times, to_plot_y_deep_vals, color='red', s=2)
    plt.scatter(to_plot_y_light_times, to_plot_y_light_vals, color='green', s=2)





    to_plot_z_rem_times = set_to_list(z_rem_times)
    to_plot_z_rem_vals = [z_vals[i] for i in to_plot_z_rem_times]

    to_plot_z_deep_times = set_to_list(z_deep_times)
    to_plot_z_deep_vals = [z_vals[i] for i in to_plot_z_deep_times]

    to_plot_z_light_times = set(int_timestamps).difference(z_deep_times).difference(z_rem_times)
    to_plot_z_light_times.remove(len(z_vals))
    to_plot_z_light_times = set_to_list(to_plot_z_light_times)

    to_plot_z_light_vals = [z_vals[i] for i in to_plot_z_light_times]

    plt.subplot(3,1,3)
    plt.title('z vs. Time')
    plt.scatter(to_plot_z_rem_times, to_plot_z_rem_vals, color='blue', s=2)
    plt.scatter(to_plot_z_deep_times, to_plot_z_deep_vals, color='red', s=2)
    plt.scatter(to_plot_z_light_times, to_plot_z_light_vals, color='green', s=2)


    plt.show()
