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

class GTFHandlers:
	def __init__(self):
		self.chr_dict = {}

	def map_chr_dicts(self, gtf_file):
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
