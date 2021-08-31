import sys
import math
import time
import random

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

# this will return an initial instance below the weight capcity of the bag
# threshold...
# if no max_time_per_instance argument is given, the default argument is infinity (effectively turning off the system)
# the weight function should return a number type
def generate_initial_instance(capacity, max_time_per_instance=float('inf')):
	initial_instance = gal.generate_random_binary_string_of_length_n(bagsize)
	
	# we start at half instances with half capacity to give lots of chance for evolution
	t0 = time.time()
	while weight_function(initial_instance) > capacity:
		initial_instance = gal.generate_random_binary_string_of_length_n(bagsize)

		# this ensures that we only take a certain amount of time per instance generated (threshold)
		if (time.time() - t0) > max_time_per_instance:
			while weight_function(initial_instance) > capacity:
				initial_instance = gal.generate_string_of_0s_length_n_with_1_at_index(bagsize, random.randint(0, bagsize))

	return initial_instance	

# threshold is time allowed per instance generation before timeout (return original instance)
def generate_next_generation(instances, capacity, max_time_per_instance=float('inf')):
	new_instances = list()
	new_instances.extend(gal.get_percentage_best_instances(instances, 0.1, fitness_function)) 

	while len(new_instances) < population_size:
		instance1, instance2 = gal.get_two_random_instances(instances) # new function needed here
		new_instance1, new_instance2 = gal.crossover(instance1, instance2, weight_function, capacity, max_time_per_instance)

		new_instance1 = gal.mutation_with_probability(new_instance1, 0.1, weight_function, capacity)
		if mutate_local_search:
			new_instance2 = gal.mutation_local_search(new_instance2, fitness_function, weight_function, capacity)
		else:
			new_instance2 = gal.mutation_with_probability(new_instance2, 0.1, weight_function, capacity)

		new_instances.append(new_instance1)
		new_instances.append(new_instance2)

	return new_instances

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
	# use associativity later to make this one for loop (possibly)
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
	max_time_per_instance = (0.1 * (float(bagsize) / float(capacity))) / float(population_size) # threshold grows proportional to bagsize per unit capacity 

	# the file is loaded and returned as a list of lists of size 2
	# the first item of the internal lists is the value (index 0)
	# the second item of the internal lists is the weight (index 1)
	data = DataLoader.load_data(filename)

	# generating intial instances
	current_generation = [generate_initial_instance(capacity, max_time_per_instance) for i in range(population_size)]

	best_instances, best_instances_fitnesses = list(), list()
	for gen_number in range(number_of_generations):
		best_instance, best_instance_fitness = gal.find_best_instance(fitness_function, current_generation)
		best_instances.append(best_instance)
		best_instances_fitnesses.append(best_instance_fitness)

		print("---------------------------------------------")
		print("generation number: {}".format(gen_number + 1))
		print("best instance fitness: {}".format(best_instance_fitness))
		print("best instance weight:{}".format(weight_function(best_instance)))
		current_generation = generate_next_generation(current_generation, capacity, max_time_per_instance)
	print("---------------------------------------------")
	print("final solution = {}".format(best_instances[-1]))
	print("---------------------------------------------")

	gc = GraphConvergence()
	gc.draw(filename, best_instances_fitnesses)