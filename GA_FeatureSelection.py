import sys
import math
import time
import random

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

import gal # genetic algorithm library
from dataloader import DataLoader
from graph_convergence import GraphConvergence

def probability_of_class(classname):
	count_of_class = 0

	index_of_class = df.shape[0]-1
	for key in df.keys():
		if df[key][index_of_class] == classname:
			count_of_class += 1

	return count_of_class / len(df.keys())

def calculate_entropy(probability):
	return -probability * math.log2(probability)	

def probability_of_feature_given_class(x, mean_class1, mean_class2):
	count_of_class = 0

	index_of_class = df.shape[0]-1
	for key in df.keys():
		if df[key][index_of_class] == classname:
			count_of_class += 1

# low entropy is better (expected value of surprise- we don't want surprise; we want to be able to make predictions)
# mutual information is:
# the difference in entropy between the class label not knowing any features, and the class label given the features
# meaning of this is:
# how much information this feature subset has to distinguish the class labels (larger is better)
# expect this to probably be worse than the wrapper based fitness function
#
# Because all features are chosen independently from each other, p(x_1, ..., x_n) = p(x_1) * ... * p(x_n) = (1/total_number_of_features)^n
# and p(y | x_1, ..., x_n) = p(y) because the specific features of each data point is independent from the amount of classlabels of a given kind # possibly this is wrong but at least if we get to this point, it might be the only thing that's wrong
# need to work out if a what values correspond to higher probability of each class
def filter_based_fitness_function(binary_string): # information gain
	p_class1 = probability_of_class(1.0)
	p_class2 = probability_of_class(2.0)
	entropy = calculate_entropy(p_class1) + calculate_entropy(p_class2)

	count_of_features_in_binary_string = sum([int(b) for b in binary_string])
	p_x_1tox_n = math.pow((1/total_number_of_features), count_of_features_in_binary_string)
	conditional_entropy = p_x_1tox_n * (calculate_entropy(p_class1) + calculate_entropy(p_class2)) # step I ran into trouble in

	# x_1, ..., x_n corresponds to the feature numbers
	# p(x_1 | y) means "what's the probability of choosing feature number x_1 given class y (1.0 or 2.0)?"
	#
	# possibly we can use Baye's therorem:
	# we have p(y|x_1, ..., x_n) = (p(x_1, ..., x_n | y) * p(y)) / p(x_1, ..., x_n) 
	#							 = (p(x_1 | y) * ... * p(x_n | y) * p(y)) / (p(x_1) * ... * p(x_n)) (by independence of each featyre selection)
	#							 = (p(x_1 | y) * ... * p(x_n | y) * p(y)) / (p(x_1) * ... * p(x_n))

	return entropy - conditional_entropy

def convert_df_to_list(data):
	data_as_list = list()
	for key in data.keys():
		vector = list()
		for feature in data[key]:
			vector.append(feature)
		data_as_list.append(vector)

	return data_as_list

# will need to provide training data
def wrapper_based_fitness_function(binary_string):
	if binary_string == ('0' * len(binary_string)):
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
	program_t0 = time.time()

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
	mutate_local_search = True
	mutate_local_search_skip_gens_number = 5
	max_time_per_instance = 0.00000001
	max_percentage_of_original_features_allowed = 0.3
	max_number_of_original_features_allowed = int(max_percentage_of_original_features_allowed * total_number_of_features)

	df = DataLoader.load_part2_data(datasource + ".data") # loads as a pandas dataframe
	print(df)
	
	seed = random.randint(0,100)
	print(f"seed = {seed}")

	training_data, testing_data = train_test_split(df.T, test_size=0.2, random_state=seed)
	training_data, testing_data = training_data.T, testing_data.T # transpose result

	#print(f"No. of training examples: {training_data.shape[0]}")
	#print(f"No. of testing examples: {testing_data.shape[]}")
	
	# the lambda condition is something that you want to satisfy
	# the condition here is that we can't take more features than max_number_of_original_features_allowed
	lambda_condition = (lambda instance: (sum([int(b) for b in instance]) <= max_number_of_original_features_allowed))

	# generating intial instances
	current_generation = [gal.generate_initial_instance(total_number_of_features, lambda_condition, 0) for i in range(population_size)]

	fitness_function = wrapper_based_fitness_function #filter_based_fitness_function

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
		
		current_generation = gal.generate_next_generation(current_generation, population_size, fitness_function, constraint=lambda_condition, probability_of_mutation=0.5, mutate_local_search_best=mutate_local_search_for_this_generation, mutate_local_search_all=False, max_time_per_instance=max_time_per_instance)

		best_instance = gal.get_number_best_instances(current_generation, 1, fitness_function)[0]
		best_instance_fitness = fitness_function(best_instance)
		best_instances.append(best_instance)
		best_instances_fitnesses.append(best_instance_fitness)
		print("best instance fitness: {}".format(best_instance_fitness))
	print("---------------------------------------------")
	final_solution = best_instances[-1]
	print("final solution = {}".format(final_solution))
	print("---------------------------------------------")
	
	print(f"program time = {time.time() - program_t0}")
	if fitness_function == filter_based_fitness_function:
		print(f"final classification accuracy = {wrapper_based_fitness_function(final_solution)}")

	gc = GraphConvergence()
	gc.draw(datasource, best_instances_fitnesses)