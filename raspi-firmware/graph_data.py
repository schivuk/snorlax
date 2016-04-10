import time
import matplotlib.pyplot as plt

filename = 'accOutput.txt'

# y_min = 400
# y_max = 600

plt_start = 50000
plt_end = 55000

with open(filename) as f:
    x_vals = []
    y_vals = []
    z_vals = []
    timestamps = []

    start = time.time()

    counter = 0
    for line in f.readlines():
        # Only sample every 100 datapoints
        counter += 1
        if counter % 100 == 0:
            counter = 0

            x,y,z,timestamp = line.strip('\n').split(',')
            x_vals.append(x)
            y_vals.append(y)
            z_vals.append(z)
            timestamps.append(timestamp)

    read_end = time.time()
    print("Took {0} seconds to read data".format(read_end-start))

    # plt.plot(timestamps,x_vals)
    plt.subplot(3,1,1)
    plt.title('X vs. Time')
    plt.scatter(timestamps[plt_start:plt_end], x_vals[plt_start:plt_end])
    plt.subplot(3,1,2)
    plt.title('Y vs. Time')
    plt.scatter(timestamps[plt_start:plt_end], y_vals[plt_start:plt_end])
    plt.subplot(3,1,3)
    plt.title('Z vs. Time')
    plt.scatter(timestamps[plt_start:plt_end], z_vals[plt_start:plt_end])

    plot_end = time.time()
    print("Took {0} seconds to plot data".format(plot_end-read_end))

    # ax = plt.gca(); ax.set_ylim(y_min, y_max)
    plt.show()