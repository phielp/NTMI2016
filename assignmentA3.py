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
def calc_prop(model_n, unigram, n):

	v = len(unigram)

	for i, j  in model_n.items():
		prop_n = model_n[i]
		prop_n_min_one = unigram[i[0:(n -1)]]
		if prop_n_min_one != 0:
			model_n[i] = (prop_n + 1) / (prop_n_min_one + v)
		else:
			model_n[i] = 0

	print(Counter(model_n).most_common(10))	
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

	unigram = counter_list(corpus_array,args.n-1)

	calc_prop(model_n, unigram, args.n)

