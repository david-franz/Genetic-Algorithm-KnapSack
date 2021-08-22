# not actually loading the data yet

class FileLoader:
	
	@staticmethod
	def load_file(command_line_argv0):
		# this method will automatically close the file when we exit the block
		with open("knapsack-data/" + str(command_line_argv0), "r") as f:
			for line in f.readlines():
				print(line)