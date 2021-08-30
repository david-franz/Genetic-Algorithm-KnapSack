import sys
import math
import time
import random

# TODO:
# experiment with values
# clean up code
# combine with local search instead of just mutation

from dataloader import DataLoader
from genetic_algorithm_library import GeneticAlgoLib
from graph_convergence import GraphConvergence

# this will caculate the weight of an instance
def calculate_weight_of_instance(instance):
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
	initial_instance = ga.generate_random_binary_string_of_length_n(bagsize)
	
	# we start at half instances with half capacity to give lots of chance for evolution
	t0 = time.time()
	while calculate_weight_of_instance(initial_instance) > (capacity/2):
		initial_instance = ga.generate_random_binary_string_of_length_n(bagsize)

		# this ensures that we only take a certain amount of time per instance generated (threshold)
		if (time.time() - t0) > max_time_per_instance:
			while calculate_weight_of_instance(initial_instance) > (capacity/2):
				initial_instance = ga.generate_string_of_0s_length_n_with_1_at_index(bagsize, random.randint(0, bagsize))

	return initial_instance	

# threshold is time allowed per instance generation before timeout (return original instance)
def generate_next_generation(instances, capacity, max_time_per_instance=float('inf')):
	new_instances = list()
	number_of_best_instance = int(len(instances) * 0.1) # use this to build out library method properly
	new_instances.extend(ga.get_number_best_instances(instances, number_of_best_instance, fitness_function)) # change this to percentage when it works

	while len(new_instances) < bagsize:
		instance1, instance2 = ga.get_two_random_instances(instances) # new function needed here
		new_instance1, new_instance2 = ga.crossover(instance1, instance2, calculate_weight_of_instance, capacity, max_time_per_instance)
		
		# experiment with the mutation probability
		new_instance1 = ga.mutation_with_probability(new_instance1, 0.25, calculate_weight_of_instance, capacity)
		new_instance2 = ga.mutation_with_probability(new_instance2, 0.25, calculate_weight_of_instance, capacity)

		# shouldn't need these functions
		#if calculate_weight_of_instance(new_instance1) > capacity: # throw instance away if it is more weight than capacity
		#	continue
		new_instances.append(new_instance1)
		if len(new_instances) == bagsize: break
		
		#if calculate_weight_of_instance(new_instance2) > capacity: # throw instance away if it is more weight than capacity
		#	continue
		new_instances.append(new_instance2)

	return new_instances

# want to abstract this to take a lambda
# the fitness function is the sum of the values of the items
# probably will change to value per unit weight
# change to fitness function in notes
# 𝛼: very large value means you always ignore infeasible solutions
alpha = 10000 # large value to ignore infeasible solutions # change later?
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
	# Ensure that we 
	if len(sys.argv) < 2:
		print("Please enter the data filename as a command line argument.")
		sys.exit(1)

	# we use only the first command line argument
	filename = sys.argv[1]

	# filename is of form bagsize_capacity
	file_metadata = filename.split('_')
	bagsize = int(file_metadata[0])
	capacity = int(file_metadata[1])

	# PLACEHOLDER VALUE
	# make this some function of the bagsize
	# more local optima requires larger population_size
	# more resource can afford larger population
	population_size = 100

	# the file is loaded and returned as a list of lists of size 2
	# the first item in the list is the value (index 0)
	# the second item in the list is the weight (index 1)
	data = DataLoader.load_data(filename)

	print("bag size = {}".format(bagsize))
	print("capacity = {}".format(capacity))

	ga = GeneticAlgoLib()

	# calculating the max allowed time to generate each instance in the intial generation
	# if this threshold is passed, a simpler generation technique is used
	max_allowed_runtime_for_initial_generation = 10 * (bagsize / capacity) # grows proportional to bagsize per unit capacity
	threshold_time = max_allowed_runtime_for_initial_generation / population_size

	# generating intial instances
	current_generation = [generate_initial_instance(capacity, threshold_time) for i in range(population_size)]
	print(current_generation)
	#print([calculate_weight_of_instance(instance) for instance in current_generation])
	#print([fitness_function(instance) for instance in current_generation])

	# initially just going through 10 generations
	# will refine this with a while loop and stopping criteria later
	best_instances = list()
	best_instances_fitnesses = list()
	for gen_number in range(100): # number of generations
		best_instance, best_instance_fitness = ga.find_best_instance(fitness_function, current_generation)
		best_instances.append(best_instance)
		best_instances_fitnesses.append(best_instance_fitness)
		#print("best instance = {}".format(best_instance))
		print("--------------------------")
		print("generation number = {}".format(gen_number+1))
		print("best instance fitness = {}".format(best_instance_fitness))
		print("best instance weight = {}".format(calculate_weight_of_instance(best_instance)))
		current_generation = generate_next_generation(current_generation, capacity, 0.1)

	gc = GraphConvergence()
	gc.draw(best_instances_fitnesses)