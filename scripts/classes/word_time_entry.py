class WordTimeEntry:
	def __init__(self, entry_str):
		self.word, self.begin_time, self.end_time=entry_str.strip().split(' ')
	def print_entry(self):
		print self.word, self.begin_time, self.end_time
