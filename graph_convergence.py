import matplotlib.pyplot as plt

# this file graphs a list of lists, with each list representing the convergence data for each run of the algorithm
class GraphConvergence:

	# this will be our data for the x-axis for each graph

	# list of lists, representing the
	# this can be come from constructor argument
	# this will be our data for the y-axis for each graph
	#best_fitnesses_for_each_gen_for_each_run = list()

	def GraphConvergence():
		self.best_fitnesses_for_each_gen_for_each_run = best_fitnesses_for_each_gen_for_each_run

	def draw(self, title, best_fitnesses_for_each_gen_for_each_run):
		runs = [run for run in range(len(best_fitnesses_for_each_gen_for_each_run))]

		plt.plot(runs, best_fitnesses_for_each_gen_for_each_run)

		plt.title(title)
		plt.xlabel('gen #'), plt.ylabel('best fitness for gen') # naming the x and y axes
		plt.show()