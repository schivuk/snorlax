import numpy as np
import matplotlib.pyplot as plt

filename = '4velostatsMarch30.txt'


with open(filename) as f:
    
    v0s, v1s, v2s, v3s = [],[],[],[]

    timestamps = []

    i=0
    for line in f.readlines():
        i+=1
        #print "strip: " + str(line.strip().split(',')) 
        arr = line.strip().split(',')
        v0,v1,v2,v3 = arr[0], arr[1], arr[2], arr[3] 
        #print "v0 strip: " + v0.strip()
        v0s.append(int(v0.lstrip('\x00')))
        v1s.append(int(v1.lstrip('\x00')))
        v2s.append(int(v2.lstrip('\x00')))
        v3s.append(int(v3.lstrip('\x00')))
        if i%10000 == 0:
            print i
        


    print "len v0s:" + str(len(v0s))
    print "vos[1000000:1000020]:" + str(v0s[1000000:1000020])


    v0s = np.array(v0s)
    v1s = np.array(v1s)
    v2s = np.array(v2s)
    v3s = np.array(v3s)

    numChunks = 100
    chunkSize = len(v0s) / numChunks

    chunkMeans = []
    chunkStds = []
    sleepStages = []

    for i in xrange(numChunks):
        thisChunk = v0s[chunkSize*i : chunkSize*i + chunkSize]
        thisMean = thisChunk.mean()
        thisStd = thisChunk.std()
        chunkMeans.append(thisMean)
        chunkStds.append(thisStd)

        if thisStd < 10:
            sleepStages.append('deep sleep')
        elif thisStd < 20:
            sleepStages.append('mid-disturbed sleep')
        else:
            sleepStages.append('very mild / disturbed sleep')
        print '.'

    print sleepStages

    xs = np.array(xrange(numChunks)) 
    plt.scatter(xs, np.array(chunkMeans),color='blue')
    plt.scatter(xs, np.array(chunkStds),color='green')
    plt.show()

