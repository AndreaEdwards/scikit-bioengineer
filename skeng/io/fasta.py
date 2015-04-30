"""
I/O fasta (:mod:`skeng.io.fasta`)
================================

.. currentmodule:: skeng.io.fasta

This module provides utility functions to deal specifically with parsing
fasta files.

Functions
---------

class FastaHandlers
	methods = [
	request_threshold,
	count_seqs,
	get_top_seqs
	]
	
"""

class FastaHandlers:
	def __init__(self):
		self.fasta_dict = {}
		self.sorted_list = []

	def request_threshold(self):
		"""Prompt the user to enter a cutoff threshold for the number of
		top sequences counts they would like to return
		
		Useful for allowing the user to decide how many 'top' sequences to 
		view

		Parameters
		----------
		none

		Returns
		-------
		int
			Integer value for the number of 'top sequences' from a sorted 
			list of sequences and their corresponding counts the user would 
			like to view 

    	Examples
    	--------
    	>>> fasta_handlers = FastaHandlers()
    	>>> threshold = fasta_handlers.request_threshold()
	
		"""	
		threshold = raw_input("Enter an integer value for the number of most" +
							 "frequently observed sequences you would like" +
							 "displayed (default is top 10) ")
		if threshold == '':
			threshold = 10
		else:
			threshold = int(threshold)
		return threshold

	def count_seqs(self, fasta_file):
		"""Counts the number of each unique sequence found in a fasta file
		
		Useful for sorting a fasta file by the number of occurances of each 
		sequence

		Parameters
		----------
		fasta_file: string
			Input string corresponds to a file path pointing to a .fasta file

		Returns
		-------
		dict
			 Dictionary object in which keys are sequences and values are 
			 counts

    	Examples
    	--------
    	>>> fasta_handlers = FastaHandlers()
    	>>> fasta_dict = fasta_handlers.count_seqs('path/to/fasta_file')
	
		"""	
		for line in open(fasta_file):
			if line.startswith('>'):
				pass
			elif line in self.fasta_dict:
				self.fasta_dict[line] += 1
			else:
				self.fasta_dict[line] = 1 
		return self.fasta_dict

	def get_top_seqs(self, fasta_dict, threshold):
		"""Sorts a sequence(key): count(value) dictionary by the counts of
		each sequence
		
		Useful for calculating the frequency of each sequence found in a
		fasta file

		Parameters
		----------
		fasta_dict: dict
			Dictionary in which keys are unique sequences and values are the
			number of times each sequence was observed in a fasta file
		threshold: int
			Integer value of the number of 'top sequences' the user would like 
			displayed. If 10 is entered, then the top 10 sequnces will be
			output

		Returns
		-------
		list
			An ordered list of lists. The highest list contains a list at each
			index in a sorted order. List[0] corresponds to a list in which
			the first element List[0][0] is the sequence (originally the key
			from the input fasta_dict) and the second element List[0][1] is
			the count of that sequence (originally corresponding to the 
			value of the key in the input dictionary)  

    	Examples
    	--------
    	>>> fasta_handlers = FastaHandlers()
    	>>> fasta_dict = fasta_handlers.count_seqs('path/to/fasta_file')
    	>>> top_seqs = fasta_handlers.get_top_seqs(fasta_dict, 10)
	
		"""	
		for seq in sorted(fasta_dict, key=fasta_dict.get, reverse=True):
			self.sorted_list.append([seq.strip('\n'), fasta_dict[seq]])
		return self.sorted_list[:threshold] #does not account for multiple seqs with same count

