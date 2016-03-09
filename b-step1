#!/usr/bin/env python3 
from urllib import request
import re
import argparse
import itertools

# Creates a node which is used to indicate the previous siblings of the parent
class Node:
	def __init__(self, parent, children, tag):
		self.parent = parent
		self.children = children
		self.tag = tag
		


def bin(sentences, output):
	# Read all the lines of the input file
	for i in sentences.readlines():
		# Strips everything from the line to get the current sentence
		current_sentence = i.strip()
		rootNode = None
		currentNode = None
		previousNode = None
		# Splits the sentence on the spaces
		for state in current_sentence.split():			
			# If the state begins with a '(', you'll go to a child of the current node
			if(state.startswith('(')):

				currentNode = Node(previousNode, [], state.strip('('))
				# If there is a previous node, make this node a child of it
				if previousNode:
					previousNode.children.append(currentNode)
				# If there is no previous node, it means that the current node 
				# is the root node and will be the previous node of the next node
				else:
					rootNode = currentNode
				previousNode = currentNode

			# If the state ends with a ')', you'll go to the parent of the current node	
			elif(state.endswith(')')):
				# This node is a child of the previous node
				previousNode.children.append(state.strip(")"))
				# Go the amount of nodes up thats equal to the amount of closing brackets
				for _ in range(state.count(')')):
					previousNode = previousNode.parent
		# Make the output file with the created nodes of the input file		
		writeTree(rootNode, 0, output)
		# write \n\n to create an empty line in the output file 
		output.write("\n\n")


def writeTree(currentNode, nodeIndex, output):
	# If the current 'node' is a node, process the node 
	if isinstance(currentNode, Node):
		# Writes (ROOT if the current node is ROOT
		if currentNode.tag == "ROOT":
			output.write("(ROOT")
		# If the parent has no previous children, print the current node 
		elif currentNode.parent.children.index(currentNode) == 0:
			output.write(" (" + currentNode.tag)
		# If the parent has previous children, print the parent and 
		# all his children except the current node
		else:
			output.write(" (@" + currentNode.parent.tag + "->_" + 
				'_'.join([c.tag for c in currentNode.parent.children[:nodeIndex]]) 
				+ " (" + currentNode.tag)
		# Cycle to every child (depth first) to build the whole sentences the same way
		# as you took them apart
		for childIndex, childNode in enumerate(currentNode.children):
			writeTree(childNode, childIndex, output)
	
		output.write(")" * (len(currentNode.children)))
	# If the current 'node'	is a string, write it in the output file
	elif isinstance(currentNode, str):
		
		output.write(" " + currentNode)

if __name__ == '__main__':

	# Gets input arguments
	parser = argparse.ArgumentParser(add_help = False)

	parser.add_argument("-input",  dest = 'input')
	parser.add_argument("-output", dest = 'output')
	args = parser.parse_args()

	input_file = open(args.input, 'r+')
	# Creates the nodes needed for the binarization
	output = open(args.output, "w")

	bin(input_file, output )


				# print(niveau)	
					