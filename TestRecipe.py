import numpy as np


class TestRecipe(object):
    def __init__(self, id, ingredients):
        self.cuisine = None
        self.id = id
        self.ingredients = ingredients
        self.cuisine_probabilities = np.zeros((20,), dtype=np.float)
