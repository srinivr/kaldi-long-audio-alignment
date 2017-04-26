#!/usr/bin/python

# Copyright 2017  Speech Lab, EE Dept., IITM (Author: Srinivas Venkattaramanujam)

# inputs:    res_ref_hyp, res_hyp_ref, actual_text, ctm
# outputs:   status to final_status_file
# caution: ensure ctm file is in the same order as the words in actual_text

import sys
from classes.entry import Entry
from classes.entry_manager import EntryManager
res_ref_hyp=sys.argv[1]
res_hyp_ref=sys.argv[2]
text_file=sys.argv[3]
ctm=sys.argv[4]
segments_file=sys.argv[5] # to get time offset for each segment
if(len(sys.argv)>6):
	text_initial_index=int(sys.argv[6])
	text_final_index=int(sys.argv[7]) # only in iteration 0
	audio_initial_time=sys.argv[8]
	audio_final_time=sys.argv[9] # only in iteration 0
	make_complete_status=True # only in iteration 0
else:
	make_complete_status=False # for any other iteration

segments_time_map=dict()

with open(res_ref_hyp,'r') as f:
	res_ref_hyp_contents=f.readlines()

with open(res_hyp_ref,'r') as f:
	res_hyp_ref_contents=f.readlines()

with open(text_file,'r') as f:
	text_contents=f.read().split(' ')
#	print "Length of text", len(text_contents)

with open(ctm,'r') as f:
	ctm_contents=f.readlines()

with open(segments_file,'r') as f:
	segments_contents=f.readlines()

for s in segments_contents:
	s=s.strip().split(' ')
	segments_time_map[s[0]]=s[2]

assert len(res_ref_hyp) == len(res_hyp_ref)
entryManager=EntryManager()
#status file format:
#	begin_time end_time status text_begin_index text_end_index
if len(res_ref_hyp_contents)==0:
	entryManager.add_entry(Entry(audio_initial_time, audio_final_time, 'PENDING', text_initial_index, text_final_index))
for k in range(len(res_ref_hyp_contents)):#,res_hyp_ref_contents):
	i,j=res_ref_hyp_contents[k],res_hyp_ref_contents[k]
	#print i.strip(),j.strip()
	text_start_index, text_end_index = map(int, i.split(' '))
	ctm_start_index, ctm_end_index = map(int, j.split(' '))
	ctm_begin_segment_id=ctm_contents[ctm_start_index].strip().split(' ')[0]
	ctm_end_segment_id=ctm_contents[ctm_end_index].strip().split(' ')[0]

	ctm_time_begin=float(ctm_contents[ctm_start_index].strip().split(' ')[2])+float(segments_time_map[ctm_begin_segment_id])
	ctm_time_end_temp=float(ctm_contents[ctm_end_index].strip().split(' ')[2])
	ctm_time_end_duration=float(ctm_contents[ctm_end_index].strip().split(' ')[3])
	ctm_time_end=ctm_time_end_temp+ctm_time_end_duration+float(segments_time_map[ctm_end_segment_id])
	ctm_word_begin=ctm_contents[ctm_start_index].strip().split(' ')[4]
	ctm_word_end=ctm_contents[ctm_end_index].strip().split(' ')[4]
	text_word_begin=text_contents[text_start_index]
	text_word_end=text_contents[text_end_index]

	# updating text_start_index to include text_initial_index
	text_start_index=text_start_index+text_initial_index
	text_end_index=text_end_index+text_initial_index
	try:
		assert ctm_word_begin.strip()==text_word_begin.strip()
	except AssertionError:
		print "Assertion Error in line:",(k+1)," begin word did not match"
		print "res_ref_hyp:", i
		print "res_hyp_ref:", j
		print "ctm_word: ", ctm_word_begin, "text_word: ", text_word_begin
		print sys.argv
		exit(1)
	try:
		assert ctm_word_end.strip() == text_word_end.strip()
	except AssertionError:
		print "Assertion Error in line:",(k+1)," end word did not match"
		print "ctm_word: ", ctm_word_end, "text_word: ", text_word_end
		print sys.argv
		exit(1)
	if(make_complete_status and k==0):
		# if first word has not been decoded
		if(text_start_index!=text_initial_index):
			entryManager.add_entry(Entry(audio_initial_time, ctm_time_begin, 'PENDING', text_initial_index, (text_start_index-1)))
	entryManager.add_entry(Entry(ctm_time_begin, ctm_time_end, 'DONE', text_start_index, text_end_index))
	if(make_complete_status and (k+1)<len(res_ref_hyp_contents)):
		next_text_start_index,_=map(int, res_ref_hyp_contents[k+1].split(' '))
		next_text_start_index=next_text_start_index+text_initial_index
		next_ctm_start_index,_=map(int, res_hyp_ref_contents[k+1].split(' '))
		next_ctm_begin_segment_id=ctm_contents[next_ctm_start_index].strip().split(' ')[0]
		ctm_next_begin_time=float(ctm_contents[next_ctm_start_index].strip().split(' ')[2])+float(segments_time_map[next_ctm_begin_segment_id])
		if((text_end_index+1)!=next_text_start_index):
			entryManager.add_entry(Entry(ctm_time_end,ctm_next_begin_time,'PENDING', (text_end_index+1), next_text_start_index-1))
	elif(make_complete_status and (k+1)==len(res_ref_hyp_contents) and text_end_index != text_final_index):
		entryManager.add_entry(Entry(ctm_time_end,audio_final_time,'PENDING',(text_end_index+1), text_final_index))


entryManager.print_entries()
