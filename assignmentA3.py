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

	n_counts = [0,0,0,0,0,0]
	
	# count
	for i, j in model_n.items():
		
		if model_n[i] <= 5:
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

	# MLE count for Nc 
	print(n_counts)
	# print(model_n)
	# smoothed count c*
	for i, j in model_n.items():
		if model_n[i] <= 5:
			smoothed = (model_n[i] + 1) * ((n_counts[model_n[i]] + 1) / n_counts[model_n[i]])

		print(smoothed)
	return model_n	

if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help = False)

	parser.add_argument("-train-corpus",  dest = 'corpus')
	parser.add_argument("-n", type = int)
	args = parser.parse_args()

	corpus = open(args.corpus, 'r') 
	
	corpus_read = corpus.read().replace('\n\n', ' </s>'*(args.n-1) + '><'+ '<s> '*(args.n-1))

	corpus_array = split_into_array(corpus_read)

	model_n = counter_list(corpus_array,args.n)

	unigram = counter_list(corpus_array,args.n-1)

	# add_one_smoothing(model_n, unigram, args.n)	# run add-one

	good_turing_smoothing(model_n)	# run good-turing

