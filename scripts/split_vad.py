#!/usr/bin/python
# TODO add offset argument to account to adjust the duration for iterations > 0
import sys

arkFilePath=sys.argv[1]
audioDurationRange=10 # in seconds

with open(arkFilePath) as f:
	contents=f.read()
#print contents
i=0
segcount=0
framecount=0
#print 'length: ',len(contents)
while i < len(contents):
	try:
		k=contents[i+1000:].index('0')
		segment=contents[i:i+1000+k]
	except ValueError:	
		segment=contents[i:]
		k=len(segment)-1000
#	print "k is ",k
	print "segment_"+str(segcount)+" key_1 "+str(i/100.0)+" "+str((i+1000+k)/100.0)
	framecount+=len(segment)
	i=i+1000+k
	segcount+=1

#print 'Framecount is',framecount

