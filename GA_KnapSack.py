import random
import sys
import time

from dataloader import DataLoader

'''TODO:
# implement dataloader

# random generation of initial generation

- way of selecting individuals for next generation:
	– Construct an empty new population
	– Do elitism (copy 5% of top individuals)
	– Repeat until the new population is full:
		• Select two parents from the population by roulette wheel selection/k  tornament selection
			(the probability of selecting each individual is proportional with its fitness)
		• Apply one-point crossover to the two parents to generate two children
		• Each child has a probability (mutation rate) to undergo flip mutation
		• Put the two (mutated) children into the new population

- run for 5 generations and present results with matplotlib'
	- find good stopping criteria (or just after a certain number of generations)
	- download matplotlib
	- draw convergence curves

- abstract out code into libray for use in part 2'''

if len(sys.argv) != 2:
	print("Please enter the data filename as a command line argument.")
	sys.exit(1)

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

def get_percentage_best_instances(instances, percentage):
	instances = instances.sort() # need to custom sort

	best_percentage_instances = list()
	for i in range(int(percentage * len(instances))):
		best_percentage_instances.append(instances[i])

	return best_percentage_instances

def get_number_best_instances(instances, number):
	instances.sort() # need to custom sort

	best_percentage_instances = list()
	for i in range(number):
		best_percentage_instances.append(instances[i])

	return best_percentage_instances	

def crossover(instance1, instance2):
	assert len(instance1) == len(instance2)

	crossover_point = random.randint(0, len(instance1))

	new_instance1 = instance1[crossover_point:] + instance2[:crossover_point]
	new_instance2 = instance1[:crossover_point] + instance2[crossover_point:]

	return new_instance1, new_instance2

def mutation_with_probability(instance, probability_of_mutation):
	new_instance = ""

	if random.random() < probability_of_mutation:
		index_of_mutation = random.randint(0, len(instance))

		for index, item in enumerate(instance):
			if index == index_of_mutation:
				item = (int(instance[index_of_mutation]) + 1) % 2
			new_instance += str(item)
	else:
		return instance

	return new_instance

def generate_next_generation(instances):
	new_instances = list()

	new_instances.append(get_number_best_instances(instances, 5)) # change this to percentage when it works

	while len(new_instances) < bagsize:
		instance1, instance2 = tuple(get_number_best_instances(instances, 2)) # new function needed here
		new_instance1, new_instance2 = crossover(instance1, instance2)
		
		# experiment with the mutation probability
		new_instance1 = mutation_with_probability(new_instance1, 0.1)
		new_instance2 = mutation_with_probability(new_instance2, 0.1)
		
		new_instances.append(new_instance1)
		if len(new_instances) == bagsize: break
		
		new_instances.append(new_instance2)

	return new_instances

def find_best_instance(instances):
	best_instance, best_instance_fitness = instances[0], fitness_function(instances[0])

	for index, instance in enumerate(instances):
		if fitness_function(instance) > best_instance_fitness:
			best_instance, best_instance_fitness = instances[index], fitness_function(instances[index])

	return best_instance, best_instance_fitness

if __name__ == '__main__':

	# calculating the max allowed time to generate each instance in the intial generation
	# if this threshold is passed, a simpler generation technique is used
	max_allowed_runtime_for_initial_generation = 10 * (bagsize / capacity) # grows proportional to bagsize per unit capacity
	threshold_time = max_allowed_runtime_for_initial_generation / population_size

	# generating intial instances
	current_generation = [generate_initial_instance(threshold_time) for i in range(population_size)]
	print(current_generation)
	#print([calculate_weight_of_instance(instance) for instance in current_generation])
	#print([fitness_function(instance) for instance in current_generation])

	best_instance, best_instance_fitness = find_best_instance(current_generation)
	print("best instance = {}".format(best_instance))
	print("best instance fitness = {}".format(best_instance_fitness))

	current_generation = generate_next_generation(current_generation)
	print("current generation = {}".format(current_generation))

	best_instance, best_instance_fitness = find_best_instance(current_generation)
	print("best instance = {}".format(best_instance))
	print("best instance fitness = {}".format(best_instance_fitness))