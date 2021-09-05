import pandas as pd

class DataLoader:

	@staticmethod
	def load_part1_data(filename): # command_line_argv0 is the filename
		
		# this will automatically close the file when we exit the block
		with open("knapsack-data/" + str(filename), "r") as f:
			return [line.split() for line in f.readlines()]

	@staticmethod
	def count_lines(filename):

		# this will automatically close the file when we exit the block
		with open("sonar-wbcd/" + str(filename), "r") as f:
			return len([line.split() for line in f.readlines()])

	@staticmethod
	def load_part2_data(filename):
		'''
			COMPLETELY REFACTOR THIS METHOD
		'''
		
		# this will automatically close the file when we exit the block
		with open("sonar-wbcd/" + str(filename), "r") as f:
			lines = [line.split() for line in f.readlines()]
			str_list = [list(line[0].split(',')) for line in lines]
			
			data_list = list()
			for l in str_list:
				data_entry = list()
				for feature in l:
					data_entry.append(float(feature))
				data_list.append(data_entry)
			
			data_dict = dict()
			for index, line in enumerate(data_list):
				data_dict[index] = line

			return pd.DataFrame(data_dict)