#!/usr/bin/python

# Copyright 2017  Speech Lab, EE Dept., IITM (Author: Srinivas Venkattaramanujam)

import sys
import codecs

word_timing_path=sys.argv[1]
key_name=sys.argv[2]
segment_file_write_path=sys.argv[3]
text_file_write_path=sys.argv[4]
audio_end_time=sys.argv[5]
num_words=10
with codecs.open(word_timing_path,'r') as f:
	word_timing_contents=f.readlines()

idx=0
cntr=0
segment_contents=[]
text_contents=[]

for k in word_timing_contents:
	# cntr=9 is we've seen 10 words
	if cntr >= (num_words-1) or (idx+cntr+1) == len(word_timing_contents):
		end_time = k.split(' ')[2]
		if float(end_time) == -1.0 and (idx+cntr+1) == len(word_timing_contents):
			end_time=audio_end_time
		if(float(end_time) != -1.0):
			begin_time = word_timing_contents[idx].split(' ')[1]
			tmp_str=key_name
			tmp_str+="_" + "segment_" + str(idx)
			tmp_str+=" " + key_name
			if(float(begin_time) == -1.0):
				if(len(segment_contents)<1):
					begin_time="0.0"
				else:
					begin_time=segment_contents[-1].split(' ')[-1]
			tmp_str+=" " + begin_time
			tmp_str+=" " + end_time
			segment_contents.append(tmp_str)
			tmp_text=key_name + "_" + "segment_" + str(idx) +" " 
			tmp_text+=" ".join([x.split(' ')[0] for x in word_timing_contents[idx:idx+cntr+1]])
			text_contents.append(tmp_text)
			idx=idx+cntr+1
			cntr=-1
	cntr+=1
with codecs.open(segment_file_write_path,'w') as seg_f, codecs.open(text_file_write_path,'w') as text_f:
	for s,t in zip(segment_contents, text_contents):
		seg_f.write("%s\n" % s)
		text_f.write("%s\n" % t)
