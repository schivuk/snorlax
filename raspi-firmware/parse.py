filename = 'accOutput.txt'

threshold = 60

outfile = open('accOutputSmall.txt', 'w')
with open(filename) as f:
	content = f.readlines()

    for i in xrange(len(content)):
        line = content[i]
		if not i % 150:
			x,y,z,time = line.strip('\n').split(',')
			if int(x) < threshold or int(y) < threshold or int(z) < threshold:
				continue
			new = "{0},{1},{2},{3}\n".format(x,y,z,time)

			outfile.write(new)

outfile.close()
