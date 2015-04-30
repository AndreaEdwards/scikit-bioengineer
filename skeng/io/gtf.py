"""
I/O gtf (:mod:`skeng.io.gtf`)
================================

.. currentmodule:: skeng.io.gtf

This module provides utility functions to deal specifically with parsing
gtf files.

Functions
---------

class GTFHandlers
	methods = [
	map_chr_dicts,
	reduce_chr_dicts,
	search_coordinates
	]
	
"""
import os
import util

class GTFHandlers:
	def __init__(self):
		self.chr_dict = {}

	def map_chr_dicts(self, gtf_file):
		"""Parses gene transfer format (gtf) file type. Returns a Dictionary
		of dictionaries. GTF file format consists of one line per feature, 
		each containing 9 columns of data, plus optional track definition lines

		Fields in GTF file must be tab-separated:
		1. seqname - name of the chromosome or scaffold; chromosome names can 
			be given with or without the 'chr' prefix. Important note: the 
			seqname must be one used within Ensembl, i.e. a standard chromosome
			name or an Ensembl identifier such as a scaffold ID, without any
			additional content such as species or assembly. See the example GFF
			output below.
		2. source - name of the program that generated this feature, or the 
			data source (database or project name)
		3. feature - feature type name, e.g. Gene, Variation, Similarity
		4. start - Start position of the feature, with sequence numbering 
			starting at 1.
		5. end - End position of the feature, with sequence numbering starting 
			at 1.
		6. score - A floating point value.
		7. strand - defined as + (forward) or - (reverse).
		8. frame - One of '0', '1' or '2'. '0' indicates that the first base of
			the feature is the first base of a codon, '1' that the second base 
			is the first base of a codon, and so on..
		9. attribute - A semicolon-separated list of tag-value pairs, providing
			additional information about each feature.
		
		Useful for building a mapping structure for gtf files in which seqname
		is a chromosome number and the attribute contains a gene name

		Parameters
		----------
		gtf_name: string
			input string corresponds to a file path pointing to a .gtf file

		Returns
		-------
		dict
			Dictionary of dictionaries. Highest-level dictionary has keys 
			corresponding to each seqname (for example chr1) and each value is
			a dictionary. The keys of each child dictionary are gene names
			listed as the first item in the attribute field. The values for
			each child dictionary have a list structure and contain all start
			and end positions associated with all instances of the key in the
			gtf file 

    	Examples
    	--------
    	>>> gtf_handlers = GTFHandlers()
    	>>> chr_dict = gtf_handlers.map_chr_dicts('path/to/gtf_file')
    	"""
	
		for line in open(gtf_file):
			fields = line.split()
			file_handlers = FileHandlers()
			cleaned = file_handlers.clean(fields)
			chr_id, coord1, coord2, gene_name = cleaned[0], int(cleaned[3]), int(cleaned[4]), cleaned[9]
			if chr_id in self.chr_dict:
				if gene_name in self.chr_dict[chr_id]:
					self.chr_dict[chr_id][gene_name].append(coord1)
					self.chr_dict[chr_id][gene_name].append(coord2)
				else:
					self.chr_dict[chr_id][gene_name] = [coord1, coord2]	
			else:
				self.chr_dict[chr_id] = {}
				if gene_name in self.chr_dict[chr_id]:
					self.chr_dict[chr_id][gene_name].append(coord1)
					self.chr_dict[chr_id][gene_name].append(coord2)
				else: 
					self.chr_dict[chr_id][gene_name] = [coord1, coord2]
		return self.chr_dict


	def reduce_chr_dicts(self, chr_dict):
		"""Filtering step for a dictionary of dictionaries. The child
		dict[key] == list with many integers. This method reduces a list of 
		many numbers to a list of two numbers that include only the minimum 
		and maximum values of the integers present in the original list.
		
		Useful for building a data structure that can be quickly searched for
		genes or features that fall within given start/end coordinates

		Parameters
		----------
		chr_dict: dict
			input dictionary of dictionaries with the following format:

		{KEY_1: {key_a: [item_1, item_2, item_3, ...., item_n],
				key_b: [item_1, item_2, item_3, ...., item_n],
				key_c: [item_1, item_2, item_3, ...., item_n],
				key_d: [item_1, item_2, item_3, ...., item_n],
				key_e: [item_1, item_2, item_3, ...., item_n]
				},
		KEY_2: {key_a: [item_1, item_2, item_3, ...., item_n],
				key_b: [item_1, item_2, item_3, ...., item_n],
				key_c: [item_1, item_2, item_3, ...., item_n],
				key_d: [item_1, item_2, item_3, ...., item_n],
				key_e: [item_1, item_2, item_3, ...., item_n]
				},
		KEY_3: {key_a: [item_1, item_2, item_3, ...., item_n],
				key_b: [item_1, item_2, item_3, ...., item_n],
				key_c: [item_1, item_2, item_3, ...., item_n],
				key_d: [item_1, item_2, item_3, ...., item_n],
				key_e: [item_1, item_2, item_3, ...., item_n]
				},
		}

		Returns
		-------
		dict
			Dictionary of dictionaries. Highest-level dictionary has keys 
			corresponding to each seqname (for example chr1) and each value is
			a dictionary. The keys of each child dictionary are gene names
			listed as the first item in the attribute field. The values for
			each child dictionary are a list with list[0] == start and 
			list[1] == end 

    	Examples
    	--------
    	>>> gtf_handlers = GTFHandlers()
    	>>> chr_dict = gtf_handlers.map_chr_dicts('path/to/gtf_file')
    	>>> red_chr_dicts = gtf_handlers.reduce_chr_dicts(chr_dict)
    	"""
		for chr_id in chr_dict:
			for gene_name in chr_dict[chr_id]:
				lower_bound = min(chr_dict[chr_id][gene_name])
				upper_bound = max(chr_dict[chr_id][gene_name])
				chr_dict[chr_id][gene_name] = [lower_bound, upper_bound]
		return chr_dict


	def search_coordinates(self, chr_dict, coord_file):
		output_file = os.getcwd() + os.sep + 'output.txt'
		output = open(output_file, "w")
		for line in open(coord_file):
			fields = line.split()
			file_handlers = FileHandlers()
			cleaned = file_handlers.clean(fields)
			chromosome, coordinate = cleaned[0], int(cleaned[1])
			if chromosome in chr_dict:
				coordinate_id = []
				for gene_name in chr_dict[chromosome]:
					if chr_dict[chromosome][gene_name][0] <= coordinate <= chr_dict[chromosome][gene_name][1]:
						found_coordinate = gene_name
						coordinate_id.append(found_coordinate.replace('"','').strip(';'))
					else:
						pass
				if coordinate_id == []:
					pass
				else:
					new_line = [chromosome, str(coordinate), "\t".join(coordinate_id), '\n']
					output.write("\t".join(new_line))
				print coordinate_id
			else:
				pass
		output.close()
