import random
import sys
import time

from dataloader import DataLoader

'''TODO:
# implement dataloader

# random generation of initial generation

- way of selecting individuals for next generation:
	– Construct an empty new population
	– Do elitism (copy top individuals) <- experiment with fraction of individuals
	– Repeat until the new population is full:
		• Select two parents from the population by roulette wheel selection
			(the probability of selecting each individual is proportional with its fitness)
		• Apply one-point crossover to the two parents to generate two children
		• Each child has a probability (mutation rate) to undergo flip mutation
		• Put the two (mutated) children into the new population

- run for 5 generations and present results with matplotlib'
	- find good stopping criteria (or just after a certain number of generations)
	- download matplotlib
	- draw convergence curves

- abstract out code into libray for use in part 2'''

# we use only the first command line argument
filename = sys.argv[1]

# filename is of form bagsize_capacity
file_metadata = filename.split('_')
bagsize = int(file_metadata[0])
capacity = int(file_metadata[1])

# placeholder value
# make this some function of the bagsize
# more local optima requires larger population_size
# more resource can afford larger population
population_size = 30

# the file is loaded and returned as a list of lists of size 2
# the first item in the list is the value (index 0)
# the second item in the list is the weight (index 1)
data = DataLoader.load_data(filename)

print("bag size = {}".format(bagsize))
print("capacity = {}".format(capacity))

def generate_random_binary_string_of_length_n(n):
	binary_string = ""

	for i in range(n):
		# adds 0 or 1 randomly to the end of the string
		# we do this n times
		binary_string += str(random.randint(0,1))

	return binary_string

def generate_string_of_0s_length_n_with_1_at_index(n, index):
	binary_string = ""

	for i in range(n):
		if i == index:
			binary_string += '1'
			continue
		binary_string += '0'

	return binary_string

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
def generate_initial_instance(max_time_per_instance):
	initial_instance = generate_random_binary_string_of_length_n(bagsize)
	
	t0 = time.time()
	while calculate_weight_of_instance(initial_instance) > capacity:
		initial_instance = generate_random_binary_string_of_length_n(bagsize)

		# this ensures that we only take a certain amount of time per instance generated (threshold)
		if (time.time() - t0) > max_time_per_instance:
			initial_instance = generate_string_of_0s_length_n_with_1_at_index(bagsize, random.randint(0, bagsize))

	return initial_instance

# the fitness function is the sum of the values of the items
# probably will change to value per unit weight
# change to fitness function in notes
# 𝛼: very large value means you always ignore infeasible solutions
def fitness_function(instance):
	value = 0

	# note that activation_function range is {0,1} because instance in a binary string
	# data[index][0] refers to the value of the item at index in the data list
	for index, character in enumerate(instance):
		activation_function = int(character)
		value += (activation_function * int(data[index][0]))

	return value

if __name__ == '__main__':
	max_allowed_runtime_for_initial_generation = 10 * (bagsize / capacity)
	threshold_time = max_allowed_runtime_for_initial_generation / population_size
	initial_instances = [generate_initial_instance(threshold_time) for i in range(population_size)]
	print(initial_instances)
	print([calculate_weight_of_instance(instance) for instance in initial_instances])
	print([fitness_function(instance) for instance in initial_instances])