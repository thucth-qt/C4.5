import math
import numpy as np
import pandas as pd

class Node:
	def __init__(self,is_leaf=False, criterion=None, label="", threshold=None):
		self.criterion = criterion
		self.label = label
		self.threshold = threshold
		self.is_leaf = is_leaf
		self.children = []
class C45:
	"""Creates a bi-decision tree with C4.5 algorithm"""
	def __init__(self, pathToData):
		self.filePathToData = pathToData
		self.data = []
		self.classes = []
		self.numAttributes = -1 
		self.attributes = []
		self.tree = None

	def load_data(self, attributes:list, class_col):
		df = pd.read_excel(self.filePathToData, sheet_name=0, index_col=None, header=0, usecols=attributes+[class_col])  
		self.attributes = attributes
		self.data = df.values.tolist()
		self.classes = list(set(df.iloc[:,-1]))
		self.numAttributes = len(attributes)

	def printTree(self):
		self.printNode(self.tree)
	
	def printNode(self, node, indent=""):
		if node.is_leaf: return 

		leftChild = node.children[0]
		rightChild = node.children[1]
		print(indent+"|____" + node.criterion + " <= " + str(node.threshold) + " : " + leftChild.label)
		self.printNode(leftChild, indent + "|	")

		print(indent+"|____" + node.criterion + " > " + str(node.threshold) + " : " + rightChild.label)
		self.printNode(rightChild, indent + "	")
	
			

	def generateTree(self):
		self.tree = self.recursiveGenerateTree(self.data, self.attributes)

	def recursiveGenerateTree(self, curData, curAttributes, criterion=None):
		if len(curData) == 0:
			#No any data sample for this curAttributes. (only in decrete criterion)
			return None

		is_pure, class_ = self.allSameClass(curData)
		if is_pure:
			return Node(is_leaf=True,criterion=criterion, label = class_)
		elif len(curAttributes) == 0:
			main_class = self.get_main_class(curData)
			return Node(is_leaf = True, criterion=criterion, label = main_class)
		else:
			(best_attr, threshold, Sis) = self.split_data(curData, curAttributes)
			remainingAttributes = curAttributes[:]
			remainingAttributes.remove(best_attr)
			node = Node(is_leaf=False, criterion=best_attr, threshold=threshold)
			node.children = [self.recursiveGenerateTree(Si, remainingAttributes, criterion=best_attr) for Si in Sis]
			return node

	def get_main_class(self, S):
		labels = [row[-1] for row in S]
		classes, count = np.unique(labels, return_counts=True)
		max_idx = np.argmax(count)
		return classes[max_idx]

	def allSameClass(self, data):
		'''
			Check if all rows is the same class
			Return:
				False: different classes
				Class_name: if all rows are the same class
		'''
		for row in data:
			if row[-1] != data[0][-1]:
				return False, None
		return True, data[0][-1]

	def split_data(self, curData, curAttributes):
		splitted = []
		maxEnt = -1*float("inf")
		best_attribute = -1
		#None for discrete attributes, threshold value for continuous attributes
		best_threshold = None
		for attribute in curAttributes:
			indexOfAttribute = self.attributes.index(attribute)
	
			curData.sort(key = lambda x: x[indexOfAttribute])
			for j in range(0, len(curData) - 1):
				if curData[j][indexOfAttribute] != curData[j+1][indexOfAttribute]:
					threshold = (curData[j][indexOfAttribute] + curData[j+1][indexOfAttribute]) / 2
					less = []
					greater = []
					for row in curData:
						if(row[indexOfAttribute] > threshold):
							greater.append(row)
						else:
							less.append(row)
					e = self.gain(curData, [less, greater])
					if e >= maxEnt:
						splitted = [less, greater]
						maxEnt = e
						best_attribute = attribute
						best_threshold = threshold
		return (best_attribute,best_threshold,splitted)

	def gain(self,S, Sis):

		E_S = self.entropy(S)

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
