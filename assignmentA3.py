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


# P + 1 = (n-gram count + 1) / 
# 	(total number of tokens + total number of types)
def add_one_smoothing(model_n):
	for i, j in model_n.items():
		j = j + 1

	return model_n	




if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help = False)

	parser.add_argument("-corpus",  dest = 'corpus')
	parser.add_argument("-n", type = int)
	args = parser.parse_args()

	corpus = open(args.corpus, 'r') 
	
	corpus_read = corpus.read().replace('\n\n', ' </s>'*(args.n-1) + '><'+ '<s> '*(args.n-1))

	corpus_array = split_into_array(corpus_read)

	model_n = counter_list(corpus_array,args.n)

	model_one = add_one_smoothing(model_n)

	print(model_one)

