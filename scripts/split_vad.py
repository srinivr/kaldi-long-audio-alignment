#!/usr/bin/python

# Copyright 2017  Speech Lab, EE Dept., IITM (Author: Srinivas Venkattaramanujam)

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
	begin_time=i/100.0
	end_time=(i+1000+k)/100.0
	if (end_time-begin_time) >= 0.1: # duration should be atleast 10ms for feature extraction in my setup.
		print "segment_"+str(segcount)+" key_1 "+str(i/100.0)+" "+str((i+1000+k)/100.0)
	framecount+=len(segment)
	i=i+1000+k
	segcount+=1

#print 'Framecount is',framecount

