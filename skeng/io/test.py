from util import *


def main():
	#instantiate FileHandlers
	file_handlers = FileHandlers()
	
	#locate files
	file_paths = file_handlers.search_directory()
	fastq_files = file_handlers.find_files(file_paths, 'fastq')

	test_file = os.getcwd() + os.sep + 'test.txt'
	for line in open(test_file):
		fields = line.split()
		file_handlers = FileHandlers()
		cleaned = file_handlers.clean(fields)
		print cleaned


main()