# Copyright 2017  Speech Lab, EE Dept., IITM (Author: Srinivas Venkattaramanujam)

from entry import Entry
class EntryManager:
	__statuses__ = ['PENDING','DONE']
	def __init__(self):
		self.entries=[]
	def add_entry(self,entry):
		# Problem:
		#	add new entries to the existing list such that:
		#		1) the start and end time of an entry is not the same
		#		2) All the words in the range are covered
		#		3) If two consecutive entries have the same status, merge
		# trivial cases:
		#	1) if list is empty, simply add to list
		# edge cases:
		#	1) While merging, if there is a status change, have to check previous entry, therefore don't do it inplace! remove the last entry, make changes and insert the entry 
		if(len(self.entries)==0):
			self.entries.append(entry)
		else:
			# assert (last word+1) of previous entry and the first word of current entry match
			try:
				assert (self.entries[-1].word_end+1)==entry.word_begin
			except AssertionError:
				print "Words are not continous in ",self.entries[-1]," and ", entry
				exit(1)
			# check if to be merged. if not, just insert.
			if(entry.begin_time!=entry.end_time and self.entries[-1].status!=entry.status and (entry.end_time-entry.begin_time)>=0.1):
				self.entries.append(entry)
			else:
				# merge case
				prev_entry=self.entries[-1]
				self.entries=self.entries[:-1]
				entry=self.__merge__(prev_entry, entry)
				return self.add_entry(entry)				
	def __min_status__(self, status1, status2):
#		_list=[EntryManager.__statuses__.index(status1), EntryManager.__statuses__.index(status2)]
#		print 'status 1,2', status1, status2
		_list=[EntryManager.__statuses__.index(status1), EntryManager.__statuses__.index(status2)]
		return EntryManager.__statuses__[min(_list)]

	def __merge__(self,prev_entry, entry):
#			print 'merge called'
			return Entry(prev_entry.begin_time, entry.end_time, self.__min_status__(prev_entry.status, entry.status), prev_entry.word_begin, entry.word_end)
	def print_entries(self):
		#print the entries
		for e in self.entries:
			print e.begin_time, e.end_time, e.status, e.word_begin, e.word_end
