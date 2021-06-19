#https://stackoverflow.com/questions/24657384/plotting-a-decision-tree-with-pydot
import math
import numpy as np
import pandas as pd
from draw import plot_tree

class Node:
	'''
	Data structure is to store nodes of tree.
	'''
	def __init__(self, is_leaf=False, criterion=None, label="", threshold=None, pure_degree="", correct_wrong=None, children=[]):
		self.criterion = criterion
		self.label = label
		self.threshold = threshold
		self.is_leaf = is_leaf
		self.children = children
		self.pure_degree = pure_degree
		self.correct_wrong = correct_wrong
class C45:
	"""Creates a bi-decision tree with C4.5 algorithm"""

	def __init__(self):
		self.data = None
		self.classes = None
		self.numAttributes = None
		self.attributes = None
		self.tree = None
		self.tree_dict={}

	def load_data(self, attributes, data, classes):
		self.data = data
		self.classes = classes
		self.numAttributes = len(attributes)
		self.attributes = attributes

	def printTree(self):
		'''
		Visualize on console
		'''
		self.__printNode(self.tree)
	
	def __printNode(self, node, indent=""):
		if node.is_leaf: 
			return 
		
		leftChild = node.children[0]
		rightChild = node.children[1]
		if leftChild.is_leaf:
			print(indent+"|____" + node.criterion + " <= " + str(node.threshold) + " : " + leftChild.label + " (" +str(leftChild.pure_degree)+ ")")
		else:
			print(indent+"|____" + node.criterion + " <= " + str(node.threshold))
		self.__printNode(leftChild, indent + "|	")
		
		if rightChild.is_leaf:
			print(indent+"|____" + node.criterion + " > " + str(node.threshold) + " : " + rightChild.label+ " (" + str(rightChild.pure_degree) + ")")
			print(indent)
		else:
			print(indent+"|____" + node.criterion + " > " + str(node.threshold))
		self.__printNode(rightChild, indent + "	")
	
	def __generate_tree_dict(self):
		'''
		Generate dictionary for visualizing in image
		'''
		self.tree_dict[self.tree.criterion] = self.__recursive_generate_tree_dict(self.tree)
	
	def __recursive_generate_tree_dict(self, node:Node):
		if node.is_leaf:
			return 

		leftChild:Node = node.children[0]
		rightChild:Node = node.children[1]

		branch ={}
		if leftChild.is_leaf:
			branch["<="+str(node.threshold)] = leftChild.label + "\n"+str(leftChild.pure_degree) + "\n" +str(leftChild.correct_wrong)
		else:
			branch["<="+str(node.threshold)] = {leftChild.criterion: self.__recursive_generate_tree_dict(leftChild)}
		
		if rightChild.is_leaf:
			branch[">"+str(node.threshold)] = rightChild.label+ "\n"+str(rightChild.pure_degree)+ "\n" +str(rightChild.correct_wrong)
		else:
			branch[">"+str(node.threshold)] = {rightChild.criterion: self.__recursive_generate_tree_dict(rightChild)}

		return branch
	
	def draw_tree(self, name):
		'''
		input: 
			name: name of image of tree 
		visualize tree with image named "name"
		'''
		self.__generate_tree_dict()
		plot_tree(self.tree_dict, name)

	def generate_tree(self, is_prune=False):
		'''
		run generating tree from data.
		Input:
			is_prune: prune the leaf if two branches are the same label
		'''
		self.tree = self.__recursiveGenerateTree(curData=self.data, curAttributes=self.attributes,  is_prune=is_prune)

	def __recursiveGenerateTree(self, curData=None, curAttributes=None, criterion=None, threshold=None, is_prune=False):
		if len(curData) == 0:
			#No any data sample for this curAttributes. (only in decrete criterion)
			return None

		is_pure, class_ = self.__allSameClass(curData)
		if is_pure:
			return Node(is_leaf=True, criterion=criterion, label=class_, pure_degree=100.0, correct_wrong=(len(curData), len(curData)-len(curData)))
		elif len(curAttributes) == 0:
			main_class, pure_degree, true_class_num = self.get_main_class(curData)
			return Node(is_leaf=True, criterion=criterion, label=main_class, pure_degree=pure_degree, correct_wrong=(true_class_num, len(curData) - true_class_num))
		else:
			(best_attr, threshold_, Sis) = self.__split_data(curData, curAttributes)
			remainingAttributes = curAttributes[:]
			remainingAttributes.remove(best_attr)
			children = [self.__recursiveGenerateTree(Si, remainingAttributes, criterion=best_attr, threshold=threshold_, is_prune=is_prune) for Si in Sis]
			if len(children)==1:
				node=children[0]
				node.criterion=criterion
				node.threshold = threshold
				
			elif (is_prune and children[0].is_leaf==True 
				and children[1].is_leaf==True 
				and children[0].label==children[1].label):

				correct_wrong = (children[0].correct_wrong[0] + children[1].correct_wrong[0], children[0].correct_wrong[1]+children[1].correct_wrong[1])
				node = Node(is_leaf=True, criterion=None,
							label=children[0].label,
				            children=[], pure_degree=correct_wrong[0]/(correct_wrong[0]+correct_wrong[1]),
                            correct_wrong=correct_wrong)
			else:
				node = Node(is_leaf=False, criterion=best_attr, threshold=threshold_, children=children)
			return node

	def get_main_class(self, S):
		'''
			There is no attribute left. So vote the main label for current data set.
			Input: 
				S: current data set.
			
		'''
		labels = [row[-1] for row in S]
		classes, count = np.unique(labels, return_counts=True)
		max_idx = np.argmax(count)
		pure_degree = round(count[max_idx]/sum(count)*100, ndigits=2)
		return classes[max_idx], pure_degree, np.max(count)

	def __allSameClass(self, data):
		'''
			Check if all rows is the same class
			Input:
				data: current data
			Return:
				False: different classes
				Class_name: if all rows are the same class
		'''
		for row in data:
			if row[-1] != data[0][-1]:
				return False, None
		return True, data[0][-1]

	def __split_data(self, data, attributes):
		'''
			use decision tree algorithm to create tree.
			Input:
				curData: remain data set.
				curAtt
		'''
		#initialize		
		maxEnt = -1*float("inf")
		best_attribute = attributes[0]
		indexOfAttribute = self.attributes.index(best_attribute)
		best_threshold = data[0][indexOfAttribute]
		splitted = [data]

		for attribute in attributes:
			indexOfAttribute = self.attributes.index(attribute)
	
			data.sort(key = lambda x: x[indexOfAttribute])
			for j in range(0, len(data) - 1):
				if data[j][indexOfAttribute] != data[j+1][indexOfAttribute]:
					threshold = data[j][indexOfAttribute]
					less = []
					greater = []
					for row in data:
						if(row[indexOfAttribute] > threshold):
							greater.append(row)
						else:
							less.append(row)
					e = self.gain(data, [less, greater])
					if e >= maxEnt:
						splitted = [less, greater]
						maxEnt = e
						best_attribute = attribute
						best_threshold = threshold
		return (best_attribute,best_threshold,splitted)

	def gain(self,S, Sis):
		E_S = self.entropy(S)
		
		if len(Sis[0])==0 or len(Sis[1])==0:
			return E_S-0

		total_E_Si = sum([len(Si)/len(S)*self.entropy(Si)  for Si in Sis])

		Gain = E_S - total_E_Si
		return Gain

	def entropy(self, S):
		labels = [row[-1] for row in S]
		S = len(labels)

		_,Si = np.unique(labels, return_counts=True)
		Si = list(Si)
		entropy = -sum([si_/S * math.log(si_/S,2) for si_ in Si])
		
		return entropy

	def fit(self, data):
		'''
		this function is to predict with given data.
		
		Input:
			data: one sample, example: [10,20,16,5,51]
		Return: 
			label of this sample. Example: "Yes"
		'''
		node: Node = self.tree
		considered_attr = 0
		while (considered_attr < self.numAttributes):
			if len(node.children) == 0:
				return node.label
			considered_attr += 1
			idx_attr = self.attributes.index(node.criterion)
			if (data[idx_attr] <= node.threshold):
				node = node.children[0]
			else:
				node = node.children[1]
		return node.label
