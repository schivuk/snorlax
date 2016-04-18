import numpy as np
import matplotlib.pyplot as plt

csvFile = open("accOutput.txt", 'r')
	
currLine = csvFile.readline()

xs = []
ys = []
zs = []

idx = 0

while(len(currLine) > 0):
	vals = currLine.split(',')
	try:
		xs.append(int(vals[0]))
		ys.append(int(vals[1]))
		zs.append(int(vals[2]))
	except ValueError:
		print "Idx:" + str(idx)
		print "x,y,z = " + vals[0] + ", " + vals[1] + ", " + vals[2] 
	
	currLine = csvFile.readline()
	idx+=1
	if(idx % 4000 == 0):
		print '.'

print "Size: " + str(len(xs))

x = np.array(xrange(len(xs)))
line, = plt.plot(x, np.array(xs), 'r-')
line, = plt.plot(x,np.array(ys), 'b-')
line, = plt.plot(x, np.array(zs), 'g-')
#, x, np.array(ys), 'b-', x, np.array(zs), 'g^'
#dashes = [10, 5, 100, 5]  # 10 points on, 5 off, 100 on, 5 off
#line.set_dashes(dashes)

plt.show()