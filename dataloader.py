class DataLoader:

	@staticmethod
	def load_data(command_line_argv0):
		
		# this will automatically close the file when we exit the block
		with open("knapsack-data/" + str(command_line_argv0), "r") as f:
			return [line.split() for line in f.readlines()]