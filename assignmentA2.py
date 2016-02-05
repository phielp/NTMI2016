#!/usr/bin/env python3 
from urllib import request	
from collections import Counter
import re
import argparse


if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help=False)

	parser.add_argument("-corpus",  dest = 'file')
	args = parser.parse_args()

	myfile = open(args.file, 'r') 
	text = myfile.read().replace('\n\n', '</S> \n <S>')

	text.write()

	print(text)