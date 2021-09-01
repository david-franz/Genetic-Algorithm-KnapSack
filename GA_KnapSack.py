import sys

import gal # genetic algorithm library
from dataloader import DataLoader
from graph_convergence import GraphConvergence

# this will caculate the weight of an instance
def weight_function(instance):
	weight = 0

	# note that activation_function range is {0,1} because it is a character in a binary string
	# data[index][1] refers to the weight of the item at index in the data list
	for index, character in enumerate(instance):
		activation_function = int(character)
		weight += (activation_function * int(data[index][1]))

	return weight

# want to abstract this to take a lambda
# the fitness function is the sum of the values of the items
# probably will change to value per unit weight
# change to fitness function in notes
# alpha: very large value means you always ignore infeasible solutions
alpha = 10000 # large value to ignore infeasible solutions
def fitness_function(instance):
	fitness = 0

	# note that activation_function range is {0,1} because instance in a binary string
	# data[index][0] refers to the value of the item at index in the data list
	for index, character in enumerate(instance):
		activation_function = int(character)
		fitness += activation_function * int(data[index][0])

	for index, character in enumerate(instance):
		fitness -= alpha * max(0, (activation_function * int(data[index][1]) - capacity))

	return fitness

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Please enter the data filename as a command line argument.")
		sys.exit(1)

	# we use only the first command line argument
	filename = sys.argv[1]

	# filename is of form bagsize_capacity
	file_metadata = filename.split('_')
	bagsize = int(file_metadata[0])
	capacity = int(file_metadata[1])

	print("bag size = {}".format(bagsize))
	print("capacity = {}".format(capacity))

	# THESE ARE OUR MAIN VALUES FOR TWEAKING THE ALGORITHM
	population_size = 100 # More local optima requires larger population_size. More resource can afford larger population.
	number_of_generations = 100
	mutate_local_search = True
	mutate_local_search_skip_gens_number = 10
	max_time_per_instance = (1.0 * (float(bagsize) / float(capacity))) / float(population_size) # threshold grows proportional to bagsize per unit capacity 

	# the file is loaded and returned as a list of lists of size 2
	# the first item of the internal lists is the value (index 0)
	# the second item of the internal lists is the weight (index 1)
	data = DataLoader.load_data(filename)

	# generating intial instances
	current_generation = [gal.generate_initial_instance(bagsize, (lambda instance : weight_function(instance) > capacity), max_time_per_instance) for i in range(population_size)]

	best_instances, best_instances_fitnesses = list(), list()
	for gen_number in range(number_of_generations):
		print("---------------------------------------------")
		print("generation number: {}".format(gen_number+1))

		# this ensures that we only do local search every mutate_local_search_skip_gens_number generations
		mutate_local_search_for_this_generation = bool(int(mutate_local_search) * (1 if ((gen_number+1)%mutate_local_search_skip_gens_number==0) else 0))
		if mutate_local_search_for_this_generation:
			print("[doing local search this generation]")
			
		current_generation = gal.generate_next_generation(current_generation,
															population_size, 
															capacity, 
															fitness_function, 
															(lambda instance : weight_function(instance) <= capacity), 
															mutate_local_search_for_this_generation,
															max_time_per_instance)

		best_instance = gal.get_number_best_instances(current_generation, 1, fitness_function)[0]
		best_instance_fitness = fitness_function(best_instance)
		best_instances.append(best_instance)
		best_instances_fitnesses.append(best_instance_fitness)

		print("best instance fitness: {}".format(best_instance_fitness))
		print("best instance weight:{}".format(weight_function(best_instance)))
	print("---------------------------------------------")
	print("final solution = {}".format(best_instances[-1]))
	print("---------------------------------------------")

	gc = GraphConvergence()
	gc.draw(filename, best_instances_fitnesses)