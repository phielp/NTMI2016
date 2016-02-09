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

def get_prop_array(prop_file,n):
	prop_file = open(prop_file, 'r') 
	
	prop_read = prop_file.read().replace('\n', ' </s>'*(n-1) + '><'+ '<s> '*(n-1))
		
	prop_array = split_into_array(prop_read) 

	if prop_array[1] == '</s>': 
		del prop_array[0:(n)]
	if prop_array[len(prop_array)-2] == '<s>':
		del prop_array[(len(prop_array)-n)+1:len(prop_array)]
		
	prop_array = [prop_array[i:n+i] for i in range(len(prop_array)-(n))]

	return prop_array


def calc_prop(prop_array, model_n, model_n_min_one, n):
	

	prop_value = 1
	prop_value_array = []

	for i in prop_array:
		prop_n = model_n[tuple(i)]
		prop_n_min_one = model_n_min_one[tuple(i[0:(n -1)])]
		if prop_n_min_one != 0:
			prop_w = prop_n/prop_n_min_one 
		else:
			prop_w = 0
		if i[0:2] == ["</s>","<s>"]:
			
			prop_value_array.append(prop_value)
			prop_value = 1
			prop_w = 1
		prop_value *= prop_w

	prop_value_array.append(prop_value)	
	return prop_value_array


if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help = False)

	parser.add_argument("-corpus",  dest = 'corpus')
	parser.add_argument("-n", type = int)
	parser.add_argument("-conditional-prob-file", dest = 'prop_file')
	parser.add_argument("-sequence-prob-file", dest = 'seq_file')
	parser.add_argument("-scored-permutations", dest = 'perm_file')
	args = parser.parse_args()

	corpus = open(args.corpus, 'r') 
	
	corpus_read = corpus.read().replace('\n\n', ' </s>'*(args.n-1) + '><'+ '<s> '*(args.n-1))

	corpus_array = split_into_array(corpus_read)

	model_n = counter_list(corpus_array,args.n)

	model_n_min_one = counter_list(corpus_array,(args.n-1))

	if args.prop_file:
		prop_array = get_prop_array(args.prop_file, args.n)
		print(calc_prop(prop_array[args.n-1:args.n], model_n, model_n_min_one, args.n))
	elif args.seq_file:
		prop_array = get_prop_array(args.seq_file, args.n)
		print(calc_prop(prop_array, model_n, model_n_min_one, args.n))
	elif args.perm_file:
		print("niks")
	else:
		print(Counter(model_n).most_common(10)) 
		print(Counter(model_n_min_one).most_common(10)) 
	


	# print(prop_array)

	# prop_array = [prop_array[i*n: (i*n)+n] for i in range(n - 1)] 
	# makes lists with lists of length n part 2	
	# print(prop_dict)

	perm_array = ['I', 'do', 'not', 'know']

	perms = tuple(itertools.permutations(perm_array)) #permutatie functie voor opdracht 4

	start = tuple(['<s>'])
	end = tuple(['</s>'])

	perm_sen = [start*(args.n-1) + perms[i] + end*(args.n-1) for i in range(len(perms))]

	print(perm_sen)
	print(len(perm_sen))

	