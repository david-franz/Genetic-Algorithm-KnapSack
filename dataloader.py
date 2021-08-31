class DataLoader:

	@staticmethod
	def load_data(filename): # command_line_argv0 is the filename
		
		# this will automatically close the file when we exit the block
		with open("knapsack-data/" + str(filename), "r") as f:
			return [line.split() for line in f.readlines()]