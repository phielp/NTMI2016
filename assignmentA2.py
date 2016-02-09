#!/usr/bin/env python3 
from urllib import request	
from collections import Counter
import re
import argparse
import itertools

def split_into_array(string):
	words = re.split("\s+|><", string) #splits  words
	return words

def split_paragraphs(string):
	par = re.split ("\><", string)
	return par

def counter_list(unigram, n):
	model = Counter(zip(*[unigram[i:] for i in range(n)]))
	return model

def calc_prop(prop_array, model_n, model_n_min_one, n):
	

	prop_dict = {}

	for i in prop_array:
		prop_n = model_n[tuple(i)]
		prop_n_min_one = model_n_min_one[tuple(i[0:(n -1)])]
		if prop_n_min_one != 0:
			prop_w = prop_n/prop_n_min_one 
		else:
			prop_w = 0

		prop_dict[tuple(i)] = prop_w

	return prop_dict


if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help=False)

	parser.add_argument("-corpus",  dest = 'corpus')
	parser.add_argument("-n", type = int)
	parser.add_argument("-conditional-prob-file", dest = 'prop_file')
	parser.add_argument("-sequence-prob-file", dest = 'seq_file')
	parser.add_argument("-scored-permutations", dest = 'perm_file')
	args = parser.parse_args()


	corpus = open(args.corpus, 'r') 
	
	corpus_read = corpus.read().replace('\n\n', ' </s>'*(args.n-1) + '><'+ '<s> '*(args.n-1))

	prop_file = open(args.prop_file, 'r') 
	
	prop_read = prop_file.read().replace('\n', ' </s>'*(args.n-1) + '><'+ '<s> '*(args.n-1))
	
	corpus_array = split_into_array(corpus_read)

	model_n = counter_list(corpus_array,args.n)

	model_n_min_one = counter_list(corpus_array,(args.n-1))

	prop_array = split_into_array(prop_read) 

	del prop_array[0:(args.n)]
	del prop_array[(len(prop_array)-args.n):len(prop_array)]
	# TODO: Make list in list split on <s>
	
	prop_array = [prop_array[i:args.n+i] for i in range(len(prop_array)-(args.n))]

	# print(prop_array)

	# prop_array = [prop_array[i*n: (i*n)+n] for i in range(n - 1)] 
	# makes lists with lists of length n part 2

	prop_dict = calc_prop(prop_array, model_n, model_n_min_one, args.n)
	
	# print(prop_dict)

	perm_array = ['I', 'do', 'not', 'know']

	perms = tuple(itertools.permutations(perm_array)) #permutatie functie voor opdracht 4

	start = tuple(['<s>'])
	end = tuple(['</s>'])

	perm_sen = [start*(args.n-1) + perms[i] + end*(args.n-1) for i in range(len(perms))]

	print(perm_sen)
	print(len(per_sen))

	# # print(Counter(model_n).most_common(10)) 
	#For part 1

	# print(Counter(model_n_min_one).most_common(10)) 
	#For part 1