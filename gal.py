# # # # # # # # # # # # # # # # # # # # # # # # # # #
#			Genetic Algorithm Library
#
#				Written by David Franz
# # # # # # # # # # # # # # # # # # # # # # # # # # #

import time
import random
from functools import cmp_to_key

# we will use this as our timeout block for all code blocks that need it
def timeout(codeblock, default, threshold=float('inf')):
	# assert type of codeblock is function
	# assert type of threshold is number?
	# assert type of default is list
	# assert type of constraint_function is function

	result_list = list()
	loop_break = False

	t0 = time.time()
	while (not loop_break):
		result, loop_break = codeblock(default)

		if (time.time() - t0) > threshold:
			return default

	return result

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

def generate_string_of_1s_of_length(length):
	new_instance = ""
	for i in range(length):
		new_instance += '1'
	return new_instance	

# WILL NEED TO THINK ABOUT THINK FUNCTION:
# HOW CAN I ABSTRACT FITNESS_FUNCTION ARGUMENTS?
def get_number_best_instances(instances, number, fitness_function):
	def compare(item1, item2):
		#print(f"fitness_function = {fitness_function}")
		#print(f"item1 = {item1}")
		#print(f"item2 = {item2}")

		return fitness_function(item2) - fitness_function(item1)
	instances.sort(key=cmp_to_key(compare))

	return instances[:number]

# roulette wheel selection
def get_percentage_best_instances(instances, percentage, fitness_function):
	number_of_best_instance = int(len(instances) * percentage)

	return get_number_best_instances(instances, number_of_best_instance, fitness_function)

def get_two_random_instances(instances):
	return instances[random.randint(0,len(instances)-1)], instances[random.randint(0,len(instances)-1)]

def crossover(instance1, instance2, constraint=(lambda x: True), max_time_per_instance=float('inf')):
	new_instance1 = generate_string_of_1s_of_length(len(instance1))
	new_instance2 = generate_string_of_1s_of_length(len(instance2))

	def codeblock(instances):
		crossover_point = random.randint(1, len(instance1)-1)

		new_instance1 = instance1[crossover_point:] + instance2[:crossover_point]
		new_instance2 = instance1[:crossover_point] + instance2[crossover_point:]

		loop_break = (constraint(new_instance1) and constraint(new_instance2))

		return [new_instance1, new_instance2], loop_break

	result = timeout(codeblock, [instance1, instance2], max_time_per_instance)

	return result[0], result[1]

def flip_bit(value):
	return (int(value) + 1) % 2

def mutate_at_index(instance, index_of_mutation):
	# adding 1 mod 2 flips the bit
	return instance[:index_of_mutation] + str((flip_bit(instance[index_of_mutation]))) + instance[index_of_mutation+1:]

# TODO: make this a timeout function
def mutation_with_probability(instance, probability_of_mutation, constraint=(lambda x: True)):
	if random.random() < probability_of_mutation:
		index_of_mutation = random.randint(0, len(instance)-1)

		new_instance = mutate_at_index(instance, index_of_mutation)
		
		if constraint(new_instance):
			return new_instance
	
	return instance

def mutation_local_search(instance, fitness_function, constraint=(lambda x: True)):
	def compare(item1, item2):
		return fitness_function(item2) - fitness_function(item1)

	new_instances = list()
	new_instances.append(instance)
	for index in range(len(instance)):
		new_instances.append(mutate_at_index(instance, index))
	new_instances.sort(key=cmp_to_key(compare))

	for new_instance in new_instances:
		if constraint(new_instance):
			return new_instance
	
	return instance

# this will return an initial instance below the weight capcity of the bag
# threshold...
# if no max_time_per_instance argument is given, the default argument is infinity (effectively turning off the system)
# the weight function should return a number type
def generate_initial_instance(binary_string_length, constraint=(lambda x: True), max_time_per_instance=float('inf')):
	initial_instance = generate_random_binary_string_of_length_n(binary_string_length)
	
	# we start at half instances with half capacity to give lots of chance for evolution
	t0 = time.time()
	while (not constraint(initial_instance)): # search until solution found that satisfies constraint or timeout
		initial_instance = generate_random_binary_string_of_length_n(binary_string_length)

		# this ensures that we only take a certain amount of time per instance generated (threshold)
		if (time.time() - t0) > max_time_per_instance:
			while (not constraint(initial_instance)):
				initial_instance = generate_string_of_0s_length_n_with_1_at_index(binary_string_length, random.randint(0, binary_string_length))

	return initial_instance		

# threshold is time allowed per instance generation before timeout (return original instance)
def generate_next_generation(instances, population_size, fitness_function, constraint=(lambda x: True), probability_of_mutation=0.0, mutate_local_search_best=False, mutate_local_search_all=False, max_time_per_instance=float('inf')):
	new_instances = list()
	new_instances.extend(get_percentage_best_instances(instances, 0.1, fitness_function)) # CHANGE 0.1 to variable

	# make this an internal function- two types of local search: best % or all
	if mutate_local_search_best:
		#new_instances = [mutation_local_search(instance, fitness_function, constraint) for instance in new_instances]
		new_instances_mutated = list()
		for instance in new_instances:
			result = mutation_local_search(instance, fitness_function, constraint)
			new_instances_mutated.append(result)
	
		new_instances = new_instances_mutated

	while len(new_instances) < population_size:
		instance1, instance2 = get_two_random_instances(instances)
		new_instance1, new_instance2 = crossover(instance1, instance2, constraint, max_time_per_instance)

		new_instance1 = mutation_with_probability(new_instance1, probability_of_mutation, constraint)
		new_instance2 = mutation_with_probability(new_instance2, probability_of_mutation, constraint)

		new_instances.append(new_instance1)
		new_instances.append(new_instance2)

	if mutate_local_search_all:
		#new_instances = [mutation_local_search(instance, fitness_function, constraint) for instance in new_instances]
		new_instances_mutated = list()
		for instance in new_instances:
			result = mutation_local_search(instance, fitness_function, constraint)
			new_instances_mutated.append(result)

	return new_instances