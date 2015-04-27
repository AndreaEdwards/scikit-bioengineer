"""
I/O utils (:mod:`skeng.io.util`)
================================

.. currentmodule:: skeng.io.util

This module provides utility functions to deal with files and I/O in
general.

Functions
---------

class FileHandlers
	methods = [
		search_directory,
		find_files,
		filter_files,
		clean,
		build_dict]
	
"""

import os


class FileHandlers:
	def __init__(self):
		self.directory = os.getcwd()
		self.file_paths = []
		self.new_file_list = []
		self.cleaned = []
		self.filtered_list = []


	def search_directory(self):
		for root, self.directory, file_list in os.walk(self.directory):
			for file_name in file_list:
				path = root + os.sep + file_name
				self.file_paths.append(path)
		return self.file_paths


	def find_files(self, file_list, extension):
		self.new_file_list = []
		for file_path in file_list:
			new_list = file_path.split('.')
			if new_list[1] == extension:
				self.new_file_list.append(file_path)
			else:
				pass
		return self.new_file_list


	def filter_files(self, file_list, character):
		for file in file_list:
			for line in open(file):
				if '\t' not in line:
					break
				else:
					self.filtered_list.append(file)
					break
		return self.filtered_list


	def clean(self, lines):
		#cleaned = []
		for field in lines:
			self.cleaned.append(field.strip()) 
		return(self.cleaned)