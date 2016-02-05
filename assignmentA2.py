#!/usr/bin/env python3 
from urllib import request	
from collections import Counter
import re
import argparse

def split_into_array(string):
	words = re.split("\W+ ", string) #splits  words
	return words


if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help=False)

	parser.add_argument("-corpus",  dest = 'file')
	args = parser.parse_args()

	myfile = open(args.file, 'r') 
	text = myfile.read().replace('\n\n', '</S>  <S>')

	array = split_into_array(text)	

	print(array[1:100])