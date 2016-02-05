"""
Made by:	Philip Bouman, 10668667
		Danny Dijkzeul, 10554386
		Kaj Meijer, 10509534

test git

This program takes a corpus, splits the words and proccesses them. Given the input (corpus, n and m) it makes
an n-gram model of the corpus and shows the m number of sequences with the highest frequencies. This program
also shows the sum of the frequencies of the sequences. 

Run the program with the following lines:

For unigrams: python3 assignment1.py -corpus [CORPUS] -n 1 -m 10 
For bigrams: python3 assignment1.py -corpus [CORPUS] -n 2 -m 10 	
For trigrams: python3 assignment1.py -corpus [CORPUS] -n 3 -m 10 

NOTE: [CORPUS] is the name of the corpus-file

""" 
#!/usr/bin/env python3 
from urllib import request	
from collections import Counter
import re
import argparse

def split_into_array(string):
	words = re.split("\W+", string) #splits  words
	return words

def counter_list(list):
	model = Counter() #makes decitonaty 0, if not exists
	sumOfFreq = 0
	if args.n == 1:
		for i in list: # makes unigram
			model[i] += 1
			sumOfFreq += 1		
	elif args.n == 2: # makes bigram 
		for i in range(0,len(list) -1): # -1 to prevent index out of range
			string = list[i] + " " + list[i+1]
			model[string] += 1
			sumOfFreq += 1
	elif args.n == 3: # makes trigram
		for i in range(0,len(list) - 2): # -2 to prevent index out of range 
			string = list[i] + " " + list[i+1] + " " + list[i+2] 
			model[string] += 1
			sumOfFreq += 1
	else:
		print("to much ngrams")
	print("Sum of frequencies of sequences: " + str(sumOfFreq))
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
	
