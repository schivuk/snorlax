import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks_cwt
import random

peak_threshold = 4
deep_sleep_threshold = 550
rem_sleep_threshold = 1125

def set_to_list(vals):
    return sorted([val for val in vals])

def acc_algorithm(vals, timestamps):
    num_vals = len(vals)
    last_peak_time = timestamps[0];
    peaks = set()
    deep_sleep_indices = set()
    rem_sleep_indices = set()

    for i in xrange(10, num_vals-10):
        prev_ten_average = sum(vals[i-10:i])/10
        next_ten_average = sum(vals[i:i+10])/10
        if next_ten_average > vals[i]+peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        elif next_ten_average < vals[i]-peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        elif prev_ten_average < vals[i] - peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        elif prev_ten_average > vals[i] + peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        else:
            if timestamps[i] - last_peak_time > rem_sleep_threshold:
                rem_sleep_indices.add(i)
            elif timestamps[i] - last_peak_time > deep_sleep_threshold:
                deep_sleep_indices.add(i)

    return peaks, set_to_list(deep_sleep_indices), set_to_list(rem_sleep_indices)

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

    int_timestamps = range(0,len(x_vals))
    x_peaks, x_deep_indices, x_rem_indices = acc_algorithm(x_vals,timestamps)
    y_peaks, y_deep_times, y_rem_times = acc_algorithm(y_vals,timestamps)
    z_peaks, z_deep_times, z_rem_times = acc_algorithm(z_vals,timestamps)

    to_plot_x_rem_times = [timestamps[i] for i in x_rem_indices]
    to_plot_x_rem_vals = [x_vals[i] for i in x_rem_indices]

    to_plot_x_deep_times = [timestamps[i] for i in x_deep_indices]
    to_plot_x_deep_vals = [x_vals[i] for i in x_deep_indices]

    x_light_indices = set(int_timestamps).difference(x_deep_indices).difference(x_rem_indices)
    x_light_indices = set_to_list(x_light_indices)

    to_plot_x_light_times = [timestamps[i] for i in x_light_indices]
    to_plot_x_light_vals = [x_vals[i] for i in x_light_indices]

    light_to_deep_transitions = []
    light_to_rem_transitions = []
    deep_to_light_transitions = []
    deep_to_rem_transitions = []
    rem_to_light_transitions = []
    rem_to_deep_transitions = []

    x_deep_indices = set(x_deep_indices) # Set is faster
    x_rem_indices = set(x_rem_indices)
    x_light_indices = set(x_light_indices)

    for i in xrange(1,len(x_vals)):
        if i-1 in x_light_indices and i in x_deep_indices:
            light_to_deep_transitions.append(i)
        elif i-1 in x_light_indices and i in x_deep_indices:
            light_to_rem_transitions.append(i)
        elif i-1 in x_deep_indices and i in x_light_indices:
            deep_to_light_transitions.append(i)
        elif i-1 in x_deep_indices and i in x_rem_indices:
            deep_to_rem_transitions.append(i)
        elif i-1 in x_rem_indices and i in x_light_indices:
            rem_to_light_transitions.append(i)
        elif i-1 in x_rem_indices and i in x_deep_indices:
            rem_to_deep_transitions.append(i)


    print light_to_deep_transitions
    print light_to_rem_transitions
    print deep_to_light_transitions
    print deep_to_rem_transitions
    print rem_to_light_transitions
    print rem_to_deep_transitions

    print len(x_rem_indices), len(x_deep_indices), len(x_light_indices), len(timestamps)
    print len(x_rem_indices) + len(x_deep_indices) + len(x_light_indices), len(timestamps)
    foo = set()
    foo.update(x_rem_indices)
    foo.update(x_deep_indices)
    print len(foo)

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
    to_plot_z_light_times = set_to_list(to_plot_z_light_times)

    to_plot_z_light_vals = [z_vals[i] for i in to_plot_z_light_times]

    plt.subplot(3,1,3)
    plt.title('z vs. Time')
    plt.scatter(to_plot_z_rem_times, to_plot_z_rem_vals, color='blue', s=2)
    plt.scatter(to_plot_z_deep_times, to_plot_z_deep_vals, color='red', s=2)
    plt.scatter(to_plot_z_light_times, to_plot_z_light_vals, color='green', s=2)


    plt.show()
