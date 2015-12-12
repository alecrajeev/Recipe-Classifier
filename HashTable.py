import numpy as np

class HashTable(object):
	def __init__(self,table_size):
		self.size = table_size
		self.index_table = np.full(self.size, -1,dtype=np.int)
		self.key_table = np.full(self.size,"empty", dtype=np.dtype(('U',30)))

	def put(self,key,value):
		index_of_hash_table = self.hash_function(key)

		while (self.key_table[index_of_hash_table] != "empty"):
			index_of_hash_table = (index_of_hash_table + 1) % self.size

		# if there is a value already stored return -1
		if self.index_table[index_of_hash_table] != -1:
			return 1
		else: # without a value previously stored return 0
			self.index_table[index_of_hash_table] = value
			self.key_table[index_of_hash_table] = key
			return 0

	def get(self,key):
		index_of_hash_table = self.hash_function(key)

		return self.index_table[index_of_hash_table]

	def hash_function(self,key):
		key_sum = 0

		for i in xrange(0, len(key)):
			key_sum += ord(key[i])

		key_sum *= ord(key[0])
		key_sum *= ord(key[len(key)-1])
		key_sum /= ord(key[len(key)/2])

		key_sum = key_sum % self.size

		if key_sum < 0:
			print "less than zero"
			key_sum += self.size

		return key_sum