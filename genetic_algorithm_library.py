# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#																		#
#	Genetic Algorithm Library											#
#		written in 2021 by David Franz									#
#																		#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import time
import random
from functools import cmp_to_key

class GeneticAlgoLib:
	def generate_random_binary_string_of_length_n(self, n):
		binary_string = ""

		for i in range(n):
			# adds 0 or 1 randomly to the end of the string
			# we do this n times
			binary_string += str(random.randint(0,1))

		return binary_string

	def generate_string_of_0s_length_n_with_1_at_index(self, n, index):
		binary_string = ""

		for i in range(n):
			if i == index:
				binary_string += '1'
				continue
			binary_string += '0'

		return binary_string

	# NOT YET WORKING
	def get_percentage_best_instances(self, instances, percentage):
		instances = instances.sort() # need to custom sort

		best_percentage_instances = list()
		for i in range(int(percentage * len(instances))):
			best_percentage_instances.append(instances[i])

		return best_percentage_instances

	def get_number_best_instances(self, instances, number, fitness_function):
		def compare(item1, item2):
			return fitness_function(item2) - fitness_function(item1)
		instances.sort(key=cmp_to_key(compare))

		return instances[:number]

	# test this function
	def crossover(self, instance1, instance2):
		assert len(instance1) == len(instance2)

		crossover_point = random.randint(0, len(instance1))
		new_instance1 = instance1[crossover_point:] + instance2[:crossover_point]
		new_instance2 = instance1[:crossover_point] + instance2[crossover_point:]

		return new_instance1, new_instance2

	def mutation_with_probability(self, instance, probability_of_mutation):
		new_instance = ""

		if random.random() < probability_of_mutation:
			index_of_mutation = random.randint(0, len(instance))

			for index, item in enumerate(instance):
				if index == index_of_mutation:
					item = (int(instance[index_of_mutation]) + 1) % 2 # adding 1 mod 2 flips the bit
				new_instance += str(item)
		else:
			return instance

		return new_instance

	def find_best_instance(self, fitness_function, instances):
		best_instance, best_instance_fitness = instances[0], fitness_function(instances[0])

		for index, instance in enumerate(instances):
			if fitness_function(instance) > best_instance_fitness:
				best_instance, best_instance_fitness = instances[index], fitness_function(instances[index])

		return best_instance, best_instance_fitness			