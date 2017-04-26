#!/usr/bin/python

# Copyright 2017  Speech Lab, EE Dept., IITM (Author: Srinivas Venkattaramanujam)

import sys
from classes.word_time_entry import WordTimeEntry
# Inputs:
#	a file with lines for each word in the actual text
#	ctm file
#	segments file
#	ref_and_hyp_match
#	hyp_and_ref_match
# Logic:
#	assert number of lines in ref_hyp_match and hyp_ref_match are the same
#	for each line in ref_hyp_match and hyp_ref_match, get the words \
word_time_file=sys.argv[1]
ctm_file=sys.argv[2]
segments_file=sys.argv[3]
ref_and_hyp_match_file=sys.argv[4]
hyp_and_ref_match_file=sys.argv[5]
text_begin_offset=int(sys.argv[6])

with open(word_time_file) as f:
	word_time=f.readlines()

with open(ctm_file) as f:
	ctm=f.readlines()

with open(segments_file) as f:
        segments=f.readlines()

with open(ref_and_hyp_match_file) as f:
        ref_and_hyp_match=f.readlines()

with open(hyp_and_ref_match_file) as f:
        hyp_and_ref_match=f.readlines()

word_time_list=[]
segments_time_map=dict()

for w in word_time:
	word_time_list.append(WordTimeEntry(w))
for s in segments:
        s=s.strip().split(' ')
        segments_time_map[s[0]]=s[2]

assert len(ref_and_hyp_match)==len(hyp_and_ref_match)

for k,l in zip(ref_and_hyp_match, hyp_and_ref_match):
	text_start, text_end=map(int,k.split(' '))
	ctm_start, ctm_end=map(int, l.split(' '))
	try:
		assert ctm_end - ctm_start == text_end - text_start
	except AssertionError:
		print 'the number of words in the matched segments are not equal:', k,l
		exit(1)
	while text_start<=text_end:
		ctm_segment, _, ctm_begin_time, ctm_duration, word=ctm[ctm_start].strip().split()
		entry = word_time_list[text_start+text_begin_offset]
		try:
			assert word == entry.word
		except AssertionError:
			print 'words in correct segments are not matching', k, l
			print 'words ctm, text', word, entry.word
			print 'arguments:', sys.argv
			exit(1)
		entry.begin_time=float(segments_time_map[ctm_segment])+float(ctm_begin_time)
		entry.end_time=entry.begin_time+float(ctm_duration)
		text_start+=1
		ctm_start+=1
for e in word_time_list:
	e.print_entry()
