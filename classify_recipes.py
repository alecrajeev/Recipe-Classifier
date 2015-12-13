import numpy as np
import json
import pprint
from TrainRecipe import TrainRecipe
from TestRecipe import TestRecipe
from HashTable import HashTable

def recipe():

	train_data = import_train_data()

	number_of_tuples = np.size(train_data)*1.0

	recipe_list, unique_cuisines = build_list_of_recipes(train_data)

	unique_ingredients = build_unique_ingredients(recipe_list)

	hash_table = build_hash_table(unique_ingredients)

	ingredients_count = build_ingredients_count(recipe_list,unique_cuisines, unique_ingredients, hash_table)

	test_data = import_test_data()

	test_recipe_list = build_test_recipe_list(test_data)

	bayes_classifier_algorith(test_recipe_list, hash_table, unique_cuisines, ingredients_count, number_of_tuples)

	print_classified_cuisines(test_recipe_list)

def get_cuisine_index(cuisine, unique_cuisines):
	return np.where(str(cuisine) == unique_cuisines[0])[0][0]

def find_count_of_cuisine(cuisine, unique_cuisines):
	index = get_cuisine_index(cuisine,unique_cuisines)

	return unique_cuisines[1][index]*1.0

def get_probability_of_ingredient(cuisine_index, ingredient_index, ingredients_count, unique_cuisines):
	ccount = unique_cuisines[1][cuisine_index]

	# the add one is the Laplacian correction
	icount = ingredients_count[cuisine_index][ingredient_index] + 1.0

	return icount/ccount

def get_probability_of_cuisine(cuisine_index, unique_cuisines, number_of_tuples):
	ccount = unique_cuisines[1][cuisine_index]*1.0

	return ccount/number_of_tuples

def print_classified_cuisines(test_recipe_list):
	print "id,cuisine"
	for i in xrange(0, np.size(test_recipe_list)):
		print str(test_recipe_list[i].id) + "," + str(test_recipe_list[i].cuisine)


def bayes_classifier_algorith(test_recipe_list, hash_table, unique_cuisines, ingredients_count, number_of_tuples):
	# cycle through every test tuple
	for i in xrange(0, np.size(test_recipe_list)):
		test_recipe = test_recipe_list[i]
		# cycle through every cuisine
		for cuisine_index in xrange(0, np.size(unique_cuisines[0])):
			prod = 1.0
			# cycle through every ingredient in tuple for every cuisine
			for k in xrange(0, np.size(test_recipe.ingredients)):
				ingredient_index = hash_table.get(test_recipe.ingredients[k])
				# if ingredient_index == -1 then the ingredient wasn't in the training data, so ignore
				if ingredient_index > -1:
					prod *= get_probability_of_ingredient(cuisine_index, ingredient_index, ingredients_count, unique_cuisines)

			test_recipe.cuisine_probabilities[cuisine_index] = prod*get_probability_of_cuisine(cuisine_index, unique_cuisines, number_of_tuples)

		cuisine_index_of_max = np.argmax(test_recipe.cuisine_probabilities)
		test_recipe.cuisine = unique_cuisines[0][cuisine_index_of_max]

def build_test_recipe_list(test_data):
	test_recipe_list = []

	for i in xrange(0, np.size(test_data)):
		test = test_data[i]
		recipe = TestRecipe(test_data[i]["id"],np.array(test_data[i]["ingredients"]))
		test_recipe_list.append(recipe)

	return test_recipe_list

def build_ingredients_count(recipe_list, unique_cuisines, unique_ingredients, hash_table):
	ingredients_count = np.zeros((np.size(unique_cuisines[0]),np.size(unique_ingredients)), dtype=np.int)

	for i in xrange(0, np.size(recipe_list)):
		recipe = recipe_list[i]
		cuisine_index = get_cuisine_index(recipe.cuisine, unique_cuisines)
		ingredients_array = np.array(recipe.ingredients)

		for j in xrange(0, np.size(ingredients_array)):
			ingredient_index = hash_table.get(ingredients_array[j])
			ingredients_count[cuisine_index][ingredient_index] += 1

	return ingredients_count

def build_hash_table(unique_ingredients):
	hash_table = HashTable(np.size(unique_ingredients))

	collision_count = 0
	A = []

	for i in xrange(0, np.size(unique_ingredients)):
		hash_table.put(unique_ingredients[i],i)

	# if collision_count > 0:
	# 	print "problem with collisions"

	return hash_table

def build_list_of_recipes(train_data):

	recipe_list = []

	dt_str = np.dtype(('U',30))

	cuisine_numpy = np.zeros((np.size(train_data),),dtype=dt_str)

	for i in xrange(0,np.size(train_data)):
		r = train_data[i]
		recipe = TrainRecipe(r["cuisine"],r["id"],np.array(r["ingredients"]))
		recipe_list.append(recipe)
		cuisine_numpy[i] = recipe.cuisine

	unique_cuisines = np.unique(cuisine_numpy)

	cuisine_count = np.zeros((np.size(unique_cuisines),),dtype=np.int)

	for i in xrange(0,np.size(train_data)):
		temp_cuisine = recipe_list[i].cuisine

		index = np.where(str(temp_cuisine) == unique_cuisines)[0][0]
		cuisine_count[index] +=1

	unique_cuisines = [unique_cuisines,cuisine_count]

	return recipe_list, unique_cuisines


def build_unique_ingredients(recipe_list):
	ingredients_total = 0

	for i in xrange(0,np.size(recipe_list)):
		ingredients_total += np.size(recipe_list[i].ingredients)

	dt_str = np.dtype(('U',75))

	ingredients_numpy = np.zeros((ingredients_total,),dtype=dt_str)

	index = 0
	for i in xrange(0, np.size(recipe_list)):
		temp_array = np.array(recipe_list[i].ingredients)
		ingredients_numpy[index:(index+np.size(temp_array))] = temp_array
		index += np.size(temp_array)

	unique_ingredients = np.unique(ingredients_numpy)

	return unique_ingredients

def import_test_data():
	json_file = "./test.json"
	json_data = open(json_file)

	test_data = json.load(json_data)
	json_data.close()

	return test_data

def import_train_data():
	json_file = "./train.json"
	json_data = open(json_file)

	train_data = json.load(json_data)
	json_data.close()

	return train_data

def main():
	recipe()

if __name__ == '__main__':
  main()