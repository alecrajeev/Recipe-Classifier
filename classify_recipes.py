import numpy as np
import json
import pprint
from Recipe import Recipe
from HashTable import HashTable

def recipe():

	json_file = "./train.json"
	json_data = open(json_file)

	rawData = json.load(json_data)
	json_data.close()

	number_of_tuples = np.size(rawData)*1.0

	recipe_list, unique_cuisines = build_list_of_recipes(rawData)

	unique_ingredients = build_unique_ingredients(recipe_list)

	H = HashTable(np.size(unique_ingredients))

	collision_count = 0
	A = []

	for i in xrange(0, np.size(unique_ingredients)):
		collision_count += H.put(unique_ingredients[i],i)

	if collision_count > 0:
		print "problem with collisions"

	ingredients_count = np.zeros((np.size(unique_cuisines[0]),np.size(unique_ingredients)), dtype=np.int)

	for i in xrange(0, np.size(recipe_list)):
		recipe = recipe_list[i]
		cuisine_index = get_cuisine_index(recipe.cuisine, unique_cuisines)
		ingredients_array = np.array(recipe.ingredients)

		for j in xrange(0, np.size(ingredients_array)):
			ingredient_index = H.get(ingredients_array[j])
			ingredients_count[cuisine_index][ingredient_index] += 1

def get_cuisine_index(cuisine, unique_cuisines):
	return np.where(str(cuisine) == unique_cuisines[0])[0][0]

def find_count_of_cuisine(cuisine, unique_cuisines):
	index = get_cuisine_index(cuisine,unique_cuisines)

	return unique_cuisines[1][index]*1.0

def build_list_of_recipes(rawData):

	recipe_list = []

	dt_str = np.dtype(('U',30))

	cuisine_numpy = np.zeros((np.size(rawData),),dtype=dt_str)

	for i in xrange(0,np.size(rawData)):
		r = rawData[i]
		recipe = Recipe(r["cuisine"],r["id"],np.array(r["ingredients"]))
		recipe_list.append(recipe)
		cuisine_numpy[i] = recipe.cuisine

	unique_cuisines = np.unique(cuisine_numpy)

	cuisine_count = np.zeros((np.size(unique_cuisines),),dtype=np.int)

	for i in xrange(0,np.size(rawData)):
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

def main():
	recipe()

if __name__ == '__main__':
  main()