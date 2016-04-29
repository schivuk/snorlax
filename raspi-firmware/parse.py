filename = 'accOutput04-28-2016.txt'

threshold = 60

outfile = open('accOutput04-28-2016Small.txt', 'w')
with open(filename) as f:
	content = f.readlines()

	for i in xrange(len(content)):
		line = content[i]
		if i % 3 == 0:
			# x,y,z,time = line.strip('\n').split(',')
			# if int(x) < threshold or int(y) < threshold or int(z) < threshold:
				# continue
			# new = "{0},{1},{2},{3}\n".format(x,y,z,time)

			outfile.write(line)

outfile.close()
