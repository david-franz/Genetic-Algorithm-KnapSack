import sys
import time
import math
import random

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

import gal # genetic algorithm library
from dataloader import DataLoader
from graph_convergence import GraphConvergence

# low entropy is better
# mutual information is:
# the difference in entropy between the class label not knowing any features, and the class label given the features
# meaning of this is:
# how much information this feature subset has to distinguish the class labels (larger is better)
# expect this to probably be worse than the wrapper based fitness function
def filter_based_fitness_function(binary_string): # information gain
	pass

	# step 1: calculate the entropy of the class

	# first we calculate the probability of winning

def convert_df_to_list(data):
	data_as_list = list()
	for key in data.keys():
		vector = list()
		for feature in data[key]:
			vector.append(feature)
		data_as_list.append(vector)

	return data_as_list

# will need to provide training data
def wrapper_based_fitness_function(binary_string): # KNN try DBScan later maybe
	if binary_string == ('0' * len(binary_string)): # change later
		return 0

	# process this as a list here to ensure we remove the class label
	training_data_filtered, class_labels = filter_rows_with_binary_string(training_data, binary_string, True)
	df_as_list = convert_df_to_list(training_data_filtered)

	knn = KNeighborsClassifier(n_neighbors=10)

	knn.fit(df_as_list, class_labels)

	testing_data_filtered, testing_data_class_labels = filter_rows_with_binary_string(testing_data, binary_string, True)
	testing_data_filtered_as_list = convert_df_to_list(testing_data_filtered)

	predicted_class_labels = knn.predict(testing_data_filtered_as_list)

	count_correct = 0
	for i in range(len(predicted_class_labels)):
		if predicted_class_labels[i] == testing_data_class_labels[i]:
			count_correct += 1

	return float(count_correct) / len(predicted_class_labels)

def filter_row_with_binary_string(vector, binary_string, vector_includes_class_label=False):
	filtered_row = list()

	for index, feature in enumerate(vector):
		if index == len(binary_string): # COMMENT ON THIS
			break
		if bool(int(binary_string[index])):
			filtered_row.append(feature)

	if vector_includes_class_label:
		filtered_row.append(vector[len(binary_string)])

	return filtered_row

def filter_rows_with_binary_string(data, binary_string, get_class_labels=False):
	filtered_data = dict()

	data_keys = data.keys().sort_values()

	data.sort_values(by=data_keys[0], ascending=True)

	for key in data_keys:
		filtered_data[key] = filter_row_with_binary_string(data[key], binary_string) # we add one to the the end to include the class label

	if get_class_labels:
		class_labels = list()
		for key in data.keys():
			class_labels.append(data[key][data.shape[0]-1])
		return (pd.DataFrame(filtered_data), class_labels)

	return pd.DataFrame(filtered_data)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Please enter the data source (sonar or wbcd) as a command line argument.")
		sys.exit(1)

	# we use only the first command line argument
	datasource = sys.argv[1]

	if ('.' in datasource):
		datasource = str(datasource.split('.')[0]) # 'sonar' or 'wbcd'

	# __datasource__.names has a line for each feature (+ an initial line)
	total_number_of_features = DataLoader.count_lines(datasource + ".names") - 1

	print("number of features = {}".format(total_number_of_features))

	# THESE ARE OUR MAIN VALUES FOR TWEAKING THE ALGORITHM
	population_size = 25 # More local optima requires larger population_size. More resource can afford larger population.
	number_of_generations = 25
	mutate_local_search = True # PLACEHOLDER VALUE # try later
	mutate_local_search_skip_gens_number = 5
	max_time_per_instance = 0.00000001 # PLACEHOLDER VALUE
	max_percentage_of_original_features_allowed = 0.35 # BETTER NAME THAN AIMED?
	max_number_of_original_features_allowed = int(max_percentage_of_original_features_allowed * total_number_of_features)

	df = DataLoader.load_part2_data(datasource + ".data") # loads as a pandas dataframe
	print(df)
	
	#seed = random.randint(0,100)
	seed = 34
	print(f"seed = {seed}")

	training_data, testing_data = train_test_split(df.T, test_size=0.2, random_state=seed)
	training_data, testing_data = training_data.T, testing_data.T # transpose result

	#print(f"No. of training examples: {training_data.shape[0]}")
	#print(f"No. of testing examples: {testing_data.shape[]}")

	# the condition here is that we can't take more features than the 
	# the lambda condition is something that you want to satisfy
	# may need to change code in gal.py so that it means "while condition is not satisfied: run this while loop"
	lambda_condition = (lambda instance: (sum([int(b) for b in instance]) <= max_number_of_original_features_allowed))

	# generating intial instances
	current_generation = [gal.generate_initial_instance(total_number_of_features, lambda_condition, 0) for i in range(population_size)]

	fitness_function = wrapper_based_fitness_function

	best_instances, best_instances_fitnesses = list(), list()
	for gen_number in range(number_of_generations):
		print("---------------------------------------------")
		print("generation number: {}".format(gen_number+1))

		# this ensures that we only do local search every mutate_local_search_skip_gens_number generations
		mutate_local_search_for_this_generation = bool(int(mutate_local_search) * (1 if ((gen_number+1)%mutate_local_search_skip_gens_number==0) else 0))
		if mutate_local_search_for_this_generation:
			print("[doing local search this generation]")

		# this ensures that we only do local search every mutate_local_search_skip_gens_number generations
		mutate_local_search_for_this_generation = bool(int(mutate_local_search) * (1 if ((gen_number+1)%mutate_local_search_skip_gens_number==0) else 0))
		
		current_generation = gal.generate_next_generation(current_generation,
															population_size, 
															fitness_function, # CHANGE THIS
															constraint=lambda_condition,
															probability_of_mutation=0.5,
															mutate_local_search_best=mutate_local_search_for_this_generation,
															mutate_local_search_all=False,
															max_time_per_instance=max_time_per_instance)

		# BE SURE TO CHANGE THE PASSED IN FITNESS FUNCTION HERE
		best_instance = gal.get_number_best_instances(current_generation, 1, fitness_function)[0]
		best_instance_fitness = fitness_function(best_instance) # CHANGE THIS
		best_instances.append(best_instance)
		best_instances_fitnesses.append(best_instance_fitness)

		print(best_instance)
		print("best instance fitness: {}".format(best_instance_fitness))
	print("---------------------------------------------")
	print("final solution = {}".format(best_instances[-1]))
	print("---------------------------------------------")

	gc = GraphConvergence()
	gc.draw(datasource, best_instances_fitnesses)