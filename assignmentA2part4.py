#!/usr/bin/env python3 
from urllib import request 
from collections import Counter
import re
import argparse
import itertools

def split_into_array(string):
	#splits words in array 
	words = re.split("\s+|><", string) 
	return words

def counter_list(unigram, n):
	# makes a n gram model using the unigram model given n
	model = Counter(zip(*[unigram[i:] for i in range(n)])) 
	return model

def get_prop_array(prop_file,n):
	# opens propfile
	prop_file = open(prop_file, 'r') 
	# replaces every /n with n - 1 times <s> in the begin and </s> in the end
	prop_read = prop_file.read().replace('\n', ' </s>'*(n-1) + '><'+ '<s> '*(n-1))
	# splits file into an array
	prop_array = split_into_array(prop_read) 

	# deletes </s> if it is the first element, same for <s> if it is the last
	if prop_array[0] == '</s>':
		del prop_array[0:(n)]
	if prop_array[n] == '<s>':
		del prop_array[(len(prop_array)-n):len(prop_array)]

	# creates a list containing lists of with length n 
	prop_array = [prop_array[i:n+i] for i in range(len(prop_array)-(n))]
	close(prop_file)
	return prop_array

def get_perm_sens(perm_file, n):
	# opens perm_file
	perm_array = open(perm_file, 'r')
	# read perm_file
	perm_read = perm_array.read()
	# splits file into array
	perm_array = split_into_array(perm_read)
	# generates permutations of the elements of perm_array
	perms = tuple(itertools.permutations(perm_array)) 
	start = tuple(['<s>'])
	end = tuple(['</s>'])
	# makes lists of perms and adds start and end symbols to the sentences
	perm_sens = [start*(args.n-1) + perms[i] + end*(args.n-1) for i in range(len(perms))]
	close(perm_file)
	return perm_sens


def calc_prop(prop_array, model_n, model_n_min_one, n):
	
	# set default value
	prop_value = 1
	prop_value_array = []

	# takes every n gram form prop_array
	for i in prop_array:
		prop_n = model_n[tuple(i)]
		prop_n_min_one = model_n_min_one[tuple(i[0:(n -1)])]
		# checks for empty propabilty 
		if prop_n_min_one != 0:
			# calculates propabilty of i
			prop_w = prop_n/prop_n_min_one 
		else:
			prop_w = 0
		# checks for new sentence start and resets propabilty of the new sentence
		if i[0:2] == ["</s>","<s>"]:
			
			prop_value_array.append(prop_value)
			prop_value = 1
			prop_w = 1
		prop_value *= prop_w

	prop_value_array.append(prop_value)	
	return prop_value_array


if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help = False)

	parser.add_argument("-corpus", dest = 'corpus')
	parser.add_argument("-n", type = int)
	parser.add_argument("-conditional-prob-file", dest = 'prop_file')
	parser.add_argument("-sequence-prob-file", dest = 'seq_file')
	parser.add_argument("-scored-permutations", dest = 'perm_file')
	args = parser.parse_args()

	# opens corpus
	corpus = open(args.corpus, 'r') 
	# replaces every \n\n with n - 1 times <s> in the begin and </s> in the end
	corpus_read = corpus.read().replace('\n\n', ' </s>'*(args.n-1) + '><'+ '<s> '*(args.n-1))
	# puts file into array
	corpus_array = split_into_array(corpus_read)
	# makes n gram for given n
	model_n = counter_list(corpus_array,args.n)
	# makes n - 1 gram for given n
	model_n_min_one = counter_list(corpus_array,(args.n-1))

	if args.prop_file:
		prop_array = get_prop_array(args.prop_file, args.n)
	elif args.seq_file:
		print("bla")
	elif args.perm_file:
		perm_sens = get_perm_sens(args.perm_file, args.n)
		# print(perm_sens)

		total_ngrams = [x[i:args.n+i] for x in perm_sens for i in range(len(perm_sens[0])-1)] # added -1 at the end
		# print(total_ngrams, '\n')
		
		# convert list of tuples to list of lists
		# dat had ik begrepen dat nodig was
		perm_array = []
		for i in range(0,len(total_ngrams)):
			list_in_list = list(total_ngrams[i])
			perm_array.append(list_in_list)
			print(perm_array)

			# calc_prop met de array van permutation bigrams
			# niet zeker of dit klopt
			# print(calc_prop(perm_array, model_n, model_n_min_one, args.n))

		# print(perm_array)

		#perm_sens = [perm_sens[i:args.n+i] for i in range(len(perm_sens)-(args.n))]
		#print(perm_sens)

	else:
		print(Counter(model_n).most_common(10)) 
		print(Counter(model_n_min_one).most_common(10)) 



	# print(prop_array)

	# prop_array = [prop_array[i*n: (i*n)+n] for i in range(n - 1)] 
	# makes lists with lists of length n part 2

	# prop_dict = calc_prop(prop_array, model_n, model_n_min_one, args.n)

	# print(prop_dict)

	
