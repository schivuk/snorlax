peak_threshold = 4
deep_sleep_threshold = 7200

def set_to_list(vals):
    return sorted([val for val in vals])

# def acc_algorithm(vals, threshold):
#     num_vals = len(vals)
#     peaks = set()

#     for i in xrange(0, num_vals-10):
#         next_ten_average = sum(vals[i:i+10])/10
#         if next_ten_average > vals[i]+peak_threshold:
#             peaks.add(i)

#     for i in xrange(0, num_vals-10):
#         next_ten_average = sum(vals[i:i+10])/10
#         if next_ten_average < vals[i]-peak_threshold:
#             peaks.add(i)

#     for i in xrange(10, num_vals):
#         prev_ten_average = sum(vals[i-10:i])/10
#         if prev_ten_average < vals[i] - peak_threshold:
#             peaks.add(i)

#     for i in xrange(10, num_vals):
#         prev_ten_average = sum(vals[i-10:i])/10
#         if prev_ten_average > vals[i] + peak_threshold:
#             peaks.add(i)

#     return peaks

def acc_algorithm(vals, timestamps):
    num_vals = len(vals)
    last_peak_time = timestamps[0];
    peaks = set()
    deep_sleep_times = set()

    for i in xrange(0, num_vals-10):
        next_ten_average = sum(vals[i:i+10])/10
        if next_ten_average > vals[i]+peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        else:
            if timestamps[i] - last_peak_time > deep_sleep_threshold:
                deep_sleep_times.add(i)

    for i in xrange(0, num_vals-10):
        next_ten_average = sum(vals[i:i+10])/10
        if next_ten_average < vals[i]-peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        else:
            if timestamps[i] - last_peak_time > deep_sleep_threshold:
                deep_sleep_times.add(i)

    for i in xrange(10, num_vals):
        prev_ten_average = sum(vals[i-10:i])/10
        if prev_ten_average < vals[i] - peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        else:
            if timestamps[i] - last_peak_time > deep_sleep_threshold:
                deep_sleep_times.add(i)

    for i in xrange(10, num_vals):
        prev_ten_average = sum(vals[i-10:i])/10
        if prev_ten_average > vals[i] + peak_threshold:
            peaks.add(i)
            last_peak_time = timestamps[i]
        else:
            if timestamps[i] - last_peak_time > deep_sleep_threshold:
                deep_sleep_times.add(i)

    return peaks, deep_sleep_times
