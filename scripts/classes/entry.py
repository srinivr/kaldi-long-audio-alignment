# Copyright 2017  Speech Lab, EE Dept., IITM (Author: Srinivas Venkattaramanujam)

class Entry:
	def __init__(self, begin_time, end_time, status, word_begin, word_end):
		self.begin_time=float(begin_time)
		self.end_time=float(end_time)
		self.status=status
		self.word_begin=int(word_begin)
		self.word_end=int(word_end)
	
	
