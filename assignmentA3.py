#!/usr/bin/env python3 
from urllib import request	
from collections import Counter
import re
import argparse
import itertools

def counter_list(unigram, n):
	model = Counter(zip(*[unigram[i:] for i in range(n)]))
	return model

def split_into_array(string):
	words = re.split("\s+|><", string) #splits  words
	return words

# Add-one smoothing:
# P + 1 = (n-gram count + 1) / 
# 	(total number of tokens + total number of types)
def add_one_smoothing(model_n, unigram, n):

	v = len(unigram)

	print(Counter(model_n).most_common(10))	

	for i, j  in model_n.items():
		prop_n = model_n[i]
		prop_n_min_one = unigram[i[0:(n -1)]]
		if prop_n_min_one != 0:
			model_n[i] = (prop_n + 1) / (prop_n_min_one + v)
		else:
			model_n[i] = 0

	print(Counter(model_n).most_common(10))	
	return model_n

# Good-Turing smoothing:
# frequency of frequencies for k <= 5
def good_turing_smoothing(model_n):

	n_counts = [0,0,0,0,0,0,0]
	n_total = 0
	adj_counts = []

	for i, j in model_n.items():
		
		n_total += model_n[i]

		if model_n[i] <= 6:
			if model_n[i] == 1:
				n_counts[1] +=1
			if model_n[i] == 2:
				n_counts[2] +=1
			if model_n[i] == 3:
				n_counts[3] +=1
			if model_n[i] == 4:
				n_counts[4] +=1
			if model_n[i] == 5:
				n_counts[5] +=1
			if model_n[i] == 6:
				n_counts[6] +=1				

	uncounted = n_counts[1] / n_total	# zero frequency in training
	adj_counts.append(uncounted)		
	print(uncounted)			

	for i in range(1, 6):

		k = 5

		a = (i + 1) * (n_counts[i+1]) / (n_counts[i])
		b = (i * (k + 1) * n_counts[k+1]) / n_counts[1]
		c = (1 - (k + 1) * n_counts[k+1] / n_counts[1])

		c_star = a - b / c

		adj_counts.append(c_star)

	print(n_total)
	print(adj_counts)

	return adj_counts	

def read_file(train_file, n):
	train = open(train_file, 'r') 
	
	train_read = train.read().replace('\n\n', ' </s>'*(n-1) + '><'+ '<s> '*(n-1))

	file_array = split_into_array(train_read)

	return file_array

if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help = False)

	parser.add_argument("-train-corpus",  dest = 'train')
	parser.add_argument("-test-corpus", dest = 'test')
	parser.add_argument("-n", type = int)
	args = parser.parse_args()

	train_array = read_file(args.train, args.n)
	if args.test:
		test_array = read_file(args.test, args.n)
		test_model = counter_list(test_array, args.n)

	unigram = counter_list(train_array,args.n-1)
	train_model = counter_list(train_array, args.n)
	

	add_one_smoothing(train_model, unigram, args.n)	# run add-one

	# good_turing_smoothing(model_n)	# run good-turing

