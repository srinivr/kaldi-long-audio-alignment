#!/usr/bin/python

# Copyright 2017  Speech Lab, EE Dept., IITM (Author: Srinivas Venkattaramanujam)

import sys
from classes.entry import Entry
from classes.entry_manager import EntryManager

status_file=sys.argv[1]
with open(status_file,'r') as f:
	status_file_contents=f.readlines()

em=EntryManager()
for l in status_file_contents:
	l=l.split()
	em.add_entry(Entry(l[0],l[1],l[2],l[3],l[4]))

em.print_entries()
