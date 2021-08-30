# # # # # # # # # # # # # # # # # # # # # # # # # # #
#			Genetic Algorithm Library
#
#				Written by David Franz
# # # # # # # # # # # # # # # # # # # # # # # # # # #

import time
import random
from functools import cmp_to_key

def identity(x):
	return 0

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

def get_number_best_instances(instances, number, fitness_function):
	def compare(item1, item2):
		return fitness_function(item2) - fitness_function(item1)
	instances.sort(key=cmp_to_key(compare))

	return instances[:number]

# roulette wheel selection
def get_percentage_best_instances(instances, percentage, fitness_function):
	number_of_best_instance = int(len(instances) * percentage)

	return get_number_best_instances(instances, number_of_best_instance, fitness_function)

def get_two_random_instances(instances):
	return instances[random.randint(0,len(instances)-1)], instances[random.randint(0,len(instances)-1)]

# we will use this as our timeout block for all code blocks that need it
def timeout(codeblock, threshold, default_value_list):
	# assert type of codeblock is function
	# assert type of threshold is number?
	# assert type of default_value_list is list
	# assert type of constraint_function is function

	result_list = list()
	loop_break = False

	t0 = time.time()
	while (not loop_break):
		result_list, loop_break = codeblock(default_value_list)

		if (time.time() - t0) > threshold:
			return default_value_list

def crossover(instance1, instance2, constraint_function=identity, constraint=0, max_time_per_instance=float('inf')):
	new_instance1 = generate_string_of_1s_of_length(len(instance1))
	new_instance2 = generate_string_of_1s_of_length(len(instance1))

	def codeblock(instances):
		crossover_point = random.randint(0, len(instance1))
		loop_break = False

		new_instance1 = instances[0][crossover_point:] + instances[1][:crossover_point]
		new_instance2 = instances[0][:crossover_point] + instances[1][crossover_point:]

		if (constraint_function(new_instance1) <= constraint) and (constraint_function(new_instance2) <= constraint):
			loop_break = True

		return [new_instance1, new_instance2], loop_break

	result = timeout(codeblock, max_time_per_instance, [instance1, instance2])

	return result[0], result[1]

def mutate_at_index(instance, index_of_mutation):
	# adding 1 mod 2 flips the bit
	return instance[:index_of_mutation] + str((int(instance[index_of_mutation]) + 1) % 2) + instance[index_of_mutation+1:]

# TODO: make this a timeout function
def mutation_with_probability(instance, probability_of_mutation, constraint_function=identity, constraint=0):
	if random.random() < probability_of_mutation:
		index_of_mutation = random.randint(0, len(instance)-1)

		new_instance = mutate_at_index(instance, index_of_mutation)
		
		if constraint_function(new_instance) <= constraint:
			return new_instance
	
	return instance

def mutation_local_search(instance, fitness_function, constraint_function=identity, constraint=0):
	def compare(item1, item2):
		return fitness_function(item2) - fitness_function(item1)

	new_instances = list()
	for index in range(len(instance)):
		new_instances.append(mutate_at_index(instance, index))
	new_instances.sort(key=cmp_to_key(compare))

	for new_instance in new_instances:
		if constraint_function(new_instance) <= constraint:
			return new_instance
	
	return instance

def find_best_instance(fitness_function, instances):
	best_instance, best_instance_fitness = instances[0], fitness_function(instances[0])

	for index, instance in enumerate(instances):
		if fitness_function(instance) > best_instance_fitness:
			best_instance, best_instance_fitness = instances[index], fitness_function(instances[index])

	return best_instance, best_instance_fitness