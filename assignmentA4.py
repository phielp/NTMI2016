
#!/usr/bin/env python3 
from urllib import request	
from collections import Counter
import re
import argparse
import itertools

def counter_list_t(unigram, n):
	model = Counter(zip(*[unigram[i:] for i in range(n)]))
	return model

def counter_list_wt(word_tag_array):
	word_tag_model = []
	for i in range(len(word_tag_array)):
		splitted = re.split('/', word_tag_array[i])
		word_tag_model.append((splitted[1], splitted[0]))
	word_tag_model = tuple(word_tag_model)
	return word_tag_model		

def door_de_kreng(word_tag_model):
	dic = {}
	for i in word_tag_model:
		if(dic.get(i[1]) == None):
			dic.update({i[1]: [i[0]]}) 
		else:
			if(i[0] not in dic[i[1]]):
				dic[i[1]].append(i[0])
	
	return dic

def whoooooooo(tag_array, word_tag_model):
	tag_counter = Counter(tag_array)
	word_tag_counter = Counter(word_tag_model)

	for key in word_tag_counter:
		tag_key = key[0]
		tag_value = tag_counter[tag_key] + 1
		word_tag_value = word_tag_counter[key]
		word_tag_counter[key] = word_tag_value/tag_value
	print(word_tag_counter)
		


def tag_file(file_handle, n):
	remove = ['#/#','--/:',';/:','-/:','!/.','2/,',"'/:",'non-``/``','Non-``/``',"underwriters/,",
	"an/,","section/,",'US$/$','NZ$/$','C$/$','A$/$','HK$/$','M$/$','S$/$','C/$',
	'``/``',"`/``",'`/`',',/,','(/(',')/)',"''/''","'/''","'/'",":/:","$/$",
	".../:","?/.",'[',']','{/(','}/)', './.']
	lines = file_handle.read()
	for t in remove:
		lines = lines.replace(t, "")
	# Set pointer to begin of file_handle.
	lines = re.sub(r'([^\s]|_)+/', '', lines)
	# print(lines)
	file_handle.seek(0)
	# Add initial START and END symbol to lines.
	lines = 'START ' + lines.strip() + ' END'
    # Add addition START and END symbols, by replacing two newlines by end,
    # newline en start. In this context paragraphs are considered sentences.
	lines = re.sub('======================================', ' END\nSTART ', lines)
	# print(lines)
    # Split text in lines by one or more occurrences of newline or space.
	words = re.split('[\n\s]+', lines)
    # Make n-grams from word list elements, by selecting range i to i+n, when a
    # n-gram can be made
	l = len(words)
	# print(words)
	return words

def word_tag_file(file_handle, n):
	remove = ['#/#','--/:',';/:','-/:','!/.','2/,',"'/:",'non-``/``','Non-``/``',"underwriters/,",
	"an/,","section/,",'US$/$','NZ$/$','C$/$','A$/$','HK$/$','M$/$','S$/$','C/$',
	'``/``',"`/``",'`/`',',/,','(/(',')/)',"''/''","'/''","'/'",":/:","$/$",
	".../:","?/.",'[',']','{/(','}/)', './.']
	lines = file_handle.read()
	for t in remove:
		lines = lines.replace(t, "")
	# Set pointer to begin of file_handle.
	# lines = re.split('/', lines)
	file_handle.seek(0)
	# Add initial START and END symbol to lines.
	lines = '<START>/START ' + lines.strip() + ' <END>/END'
    # Add addition START and END symbols, by replacing two newlines by end,
    # newline en start. In this context paragraphs are considered sentences.
	lines = re.sub('======================================', ' <END>/END\n<START>/START ', lines)
    # Split text in lines by one or more occurrences of newline or space.
	words = re.split('[\n\s]+', lines)
    # Make n-grams from word list elements, by selecting range i to i+n, when a
    # n-gram can be made
	l = len(words)
	# print(words[0:100])
	return words


if __name__ == '__main__':

	parser = argparse.ArgumentParser(add_help = False)

	parser.add_argument("-train-corpus",  dest = 'train')
	parser.add_argument("-test-corpus", dest = 'test')
	parser.add_argument("-n", type = int)
	parser.add_argument("-smoothing", dest = 'smoothing')
	args = parser.parse_args()

	train = open(args.train, 'r') 

	tag_array = tag_file(train, args.n)
	tag_model = counter_list_t(tag_array, args.n)
	# print(Counter(tag_model).most_common(10))
	
	word_tag_array = word_tag_file(train, args.n)
	print(Counter(tag_array).most_common(20))
	word_tag_model = counter_list_wt(word_tag_array)
	print(Counter(word_tag_model).most_common(20))
	dinges = door_de_kreng(word_tag_model)


	# woopwoop = whoooooooo(tag_array, word_tag_model)
	woop = whoooooooo(tag_array, tag_model)