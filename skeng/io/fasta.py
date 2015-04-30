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
	]
	
"""

class FastaHandlers:
	def __init__(self):
		self.fasta_dict = {}
		self.sorted_list = []

	def request_threshold(self):
		threshold = raw_input("Enter an integer value for the number of most" +
							 "frequently observed sequences you would like" +
							 "displayed (default is top 10) ")
		if threshold == '':
			threshold = 10
		else:
			threshold = int(threshold)
		return threshold

	def count_seqs(self, fasta_file):
		for line in open(fasta_file):
			if line.startswith('>'):
				pass
			elif line in self.fasta_dict:
				self.fasta_dict[line] += 1
			else:
				self.fasta_dict[line] = 1 
		return self.fasta_dict

	def get_top_seqs(self, fasta_dict, threshold):
		for seq in sorted(fasta_dict, key=fasta_dict.get, reverse=True):
			self.sorted_list.append([seq.strip('\n'), fasta_dict[seq]])
		return self.sorted_list[:threshold] #does not account for multiple seqs with same count

