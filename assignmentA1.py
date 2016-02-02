#!/usr/bin/env python3 
from urllib import request	
from collections import Counter
import re
import argparse

def split_into_array(string):
	words = re.split("\W+", string)
	return words

def counter_list(list):
	model = Counter() #makes decitonaty 0, if not exists
	if args.n == 1:
		for i in list:
			model[i] += 1		
	elif args.n == 2:
		for i in range(0,len(list) -1):
			string = list[i] + " " + list[i+1]
			model[string] += 1
	elif args.n == 3:
		for i in range(0,len(list) - 2):
			string = list[i] + " " + list[i+1] + " " + list[i+2]
			model[string] += 1
	else:
		print("to much ngrams")
	return model



if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help=False)

	parser.add_argument("-corpus",  dest = 'file')
	parser.add_argument("-n",  type = int)
	parser.add_argument("-m", type = int)

	args = parser.parse_args()

	myfile = open(args.file, 'r') 
	text = myfile.read().replace('\n', ' ')

	list = split_into_array(text)

	model = counter_list(list)

	print(Counter(model).most_common(args.m))