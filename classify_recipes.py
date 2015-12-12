import numpy as np
import json
import pprint
from Recipe import Recipe

def recipe():

	json_file = "./train.json"
	json_data = open(json_file)

	rawData = json.load(json_data)
	json_data.close()

	recipe_list, unique_cuisines = build_list_of_recipes(rawData)

	unique_ingredients = build_unique_ingredients(recipe_list)

def build_list_of_recipes(rawData):

	recipe_list = []

	dt_str = np.dtype(('U',15))

	cuisine_numpy = np.zeros((np.size(rawData),),dtype=dt_str)

	for i in xrange(0,np.size(rawData)):
		r = rawData[i]
		recipe = Recipe(r["cuisine"],r["id"],np.array(r["ingredients"]))
		recipe_list.append(recipe)
		cuisine_numpy[i] = recipe.cuisine

	unique_cuisines = np.unique(cuisine_numpy)

	return recipe_list, unique_cuisines


def build_unique_ingredients(recipe_list):
	ingredients_total = 0

	for i in xrange(0,np.size(recipe_list)):
		ingredients_total += np.size(recipe_list[i].ingredients)

	dt_str = np.dtype(('U',30))

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