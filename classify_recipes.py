import numpy as np
import json
import pprint
from Recipe import Recipe
import pandas as pd

"""
trin_tiny: 32
train_small: 332
train: 428275
"""

def recipe():

	json_file = "./train.json"
	json_data = open(json_file)

	data = json.load(json_data)
	json_data.close()

	recipe_list = []

	all_ingredients = []

	for i in xrange(0,np.size(data)):
		r = data[i]
		recipe = Recipe(r["cuisine"],r["id"],np.array(r["ingredients"]))
		recipe_list.append(recipe)

	ingredients_total = 0

	for i in xrange(0,np.size(data)):
		ingredients_total += np.size(recipe_list[i].ingredients)

	dt_str = np.dtype(('U',30))

	ingredients_numpy = np.zeros((ingredients_total,),dtype=dt_str)

	index = 0
	for i in xrange(0, np.size(data)):
		temp_array = np.array(data[i]["ingredients"])
		ingredients_numpy[index:(index+np.size(temp_array))] = temp_array
		index += np.size(temp_array)

	print np.shape(ingredients_numpy)


	# ingredients_pandas = pd.Series(np.array(all_ingredients))

	# print ingredients_pandas

	

def main():
	recipe()

if __name__ == '__main__':
  main()