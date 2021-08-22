import random
import sys

from fileloader import FileLoader

'''
need to program:

- random generation of initial generation
	choose: size of generation

- way of selecting individuals for next generation: _describe_method_

- run for 5 generations
'''

# we use only the first command line argument
filename = sys.argv[1]

# the file is loaded and returned as a dictionary data structure
FileLoader.load_file(filename)

# placeholder values
# should change dependent on sys.argv[1]
capacity = 20
bag_size = 12

# maximum value
# possibly dictionaries will be not efficient- consider later
def fitness_function(dict_of_chosen_items_to_values):
	pass

def generate_binary_string_of_length_n(n):
	binary_string = ""

	for i in range(n):
		# adds 0 or 1 randomly to the end of the string
		# we do this n times
		binary_string += str(random.randint(0,1))

	return binary_string

def generate_initial_population():
	weight_of_chosen_population = float('inf')

	while weight_of_chosen_population > capcity:
		chosen_population = generate_binary_string_of_length_n(bag_size)