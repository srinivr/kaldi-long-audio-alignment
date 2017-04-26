#!/usr/bin/python

# Copyright 2017  Speech Lab, EE Dept., IITM (Author: Srinivas Venkattaramanujam)

import sys
import codecs
symtab=sys.argv[1]
input_file=sys.argv[2]

with codecs.open(symtab,'r', encoding='utf-8') as f:
	symtab_contents=f.readlines()

with codecs.open(input_file,'r', encoding='utf-8') as f:
	input_contents=f.readlines()

sym2int_dict=dict()
output_contents=[]
for line in symtab_contents:
	line=line.strip().split(' ')
	try:
		assert len(line) == 2
	except AssertionError:
		print 'number of words in line', unicode(line).encode('utf-8'), 'is not 2'
		exit(1)
	sym2int_dict[line[1]]=line[0]

for line in input_contents:
	line=line.strip().split(' ')
	out_str=u''
	for word in line:
		word=word.strip()
		if len(word) == 0:
			continue
		out_str=out_str+u' '+sym2int_dict[word]
	output_contents.append(out_str)

for line in output_contents:
	print unicode(line).encode('utf-8').strip()
