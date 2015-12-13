import numpy as np
from Node import Node

class HashTable(object):
	def __init__(self,table_size):
		self.size = table_size
		self.table = [None]*table_size

	def put(self,key,value):
		index_of_hash_table = self.hash_function(key)

		node = Node(key,index_of_hash_table,value)

		temp = self.table[index_of_hash_table]
		if temp == None:
			self.table[index_of_hash_table] = node
		else:
			temp.add_node(node)

	def get(self,key):
		index_of_hash_table = self.hash_function(key)

		if self.table[index_of_hash_table] == None:
			return -1

		# handles collisions with separate chaining
		node = self.table[index_of_hash_table]
		if node.key == key:
			return node.value

		while node.key != key:
			node = node.next
			if node == None:
				return -1

		if node.key == key:
			return node.value

		print "problem"
		return -1

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