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
