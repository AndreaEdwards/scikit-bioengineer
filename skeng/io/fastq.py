"""
I/O fastq (:mod:`skeng.io.fastq`)
================================

.. currentmodule:: skeng.io.fastq

This module provides utility functions to deal specifically with parsing
fastq files.

Functions
---------

class FastqHandlers
	methods = [
	parse_fastq,
	filter_by_length
	]
	
"""

class FastqHandlers:
	def __init__(self):
		self.fastq_dict = {}
		self.filtered_dict = {}

	def parse_fastq(self, file_name):
		"""Parses fastq file looking for first (identifier) and second
		(sequence) lines only. Outputs a dictionary in which the key is
		the identifies and the value is the sequence
		
		Useful for downstream processing such as finding all the sequences
		of a particular length or eliminating sequences with invalid characters

		Parameters
		----------
		file_name: string
			input string corresponds to a file path pointing to a .fastq file

		Returns
		-------
		dict
			Dictionary containing sequence ids (key) paired with sequences
			(values)  

    	Examples
    	--------
    	>>> fastq_handlers = FastqHandlers()
    	>>> fastq_dict = fastq_handlers.parse_fastq('path/to/fastq_file')
	
		"""	
		file = open(file_name)
		file_content = file.readlines()
		i = 0
		while i < len(file_content):
			if i % 4 == 0:
				self.fastq_dict[file_content[i].strip('\n')] = file_content[i+1].strip('\n')
				i += 1
			else:
				i += 1
		return self.fastq_dict


	def filter_by_length(self, fastq_dict, filter_length):
		"""Filters a dictionary (keys == sequence identifiers and values ==
		sequences) by value length.
		
		Useful for filtering out all sequences below a given length (such as
		less than 30 bp) from a parsed fastq file (dictionary of id/sequence 
		pairs).

		Parameters
		----------
		fastq_dict: dict
			Dictionary containing sequence ids as keys and sequences as values
		filter_length: int
			Integer value to use as a cutoff for the filtering length. This
			value is used to omit any dictionary key/value pairs that do not
			contain values with a length greater than or equal to the specified
			integer. 

		Returns
		-------
		dict
			Dictionary containing sequence ids (key) paired with sequences
			(values). This dictionary is a filtered form of the input
			dictionary that only contains key/value pairs with values greater
			than or equal to the filter_length value.

    	Examples
    	--------
    	>>> fastq_handlers = FastqHandlers()
    	>>> fastq_dict = fastq_handlers.parse_fastq('path/to/fastq_file')
    	>>> filtered_dict = fastq_handlers.filter_by_length(fastq_dict, 30)
	
		"""	
		for key in fastq_dict:
			if len(fastq_dict[key]) >= filter_length:
				self.filtered_dict[key] = fastq_dict[key]
		return self.filtered_dict 

