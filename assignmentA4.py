
#!/usr/bin/env python3 
from urllib import request	
from collections import Counter
import re
import argparse
import itertools

# Get the dictionary for tag bigrams
def counter_list_t(unigram, n):
	model = Counter(zip(*[unigram[i:] for i in range(n)]))
	return model

# Get the dictionary for the tag then word combinations
def counter_list_wt(word_tag_array):
	word_tag_model = []
	# Use word/tag, split them and put them together in a tuple
	for i in range(len(word_tag_array)):
		splitted = re.split('/', word_tag_array[i])
		word_tag_model.append((splitted[1], splitted[0]))
	word_tag_model = tuple(word_tag_model)
	return word_tag_model		

# Assigns a word as key to a tag
def word_tag_dictionary(word_tag_model):
	dic = {}
	for i in word_tag_model:
		if(dic.get(i[1]) == None):
			dic.update({i[1]: [i[0]]}) 
		else:
			if(i[0] not in dic[i[1]]):
				dic[i[1]].append(i[0])
	return dic

# Calculates the probability between the tags and a dictionary
def get_probablities(tag_array, word_tag_model):
	tag_counter = Counter(tag_array)
	word_tag_counter = Counter(word_tag_model)

	for key in word_tag_counter:
		# The key for the dictionary
		tag_key = key[0]
		# The value that comes with the key (add-one smoothing)
		tag_value = tag_counter[tag_key] + 1
		# The value of the word and tag combination
		word_tag_value = word_tag_counter[key]
		# The probability
		word_tag_counter[key] = word_tag_value/(tag_value + len(tag_counter))
	return word_tag_counter
		


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
	file_handle.seek(0)
	# Add initial START and END symbol to lines.
	lines = 'START ' + lines.strip() + ' END'
    # Add addition START and END symbols, by replacing two newlines by end,
    # newline en start. In this context paragraphs are considered sentences.
	lines = re.sub('======================================', ' END\nSTART ', lines)
    # Split text in lines by one or more occurrences of newline or space.
	words = re.split('[\n\s]+', lines)
    # Make n-grams from word list elements, by selecting range i to i+n, when a
    # n-gram can be made
	l = len(words)
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

def viterbi(observations, states, start, transition, emission):
	# Vocabulary
	V = [{}]

	# initialization step, first column
	for i in states:
		V[0][i] = start[i] * emission[i][observations[0]]	

	for words in range(1, len(observations)):
		# extend Vocabulary with new column
		V.append({})

		# calculate next step values
		for j in states:
			
			# tuple containing all values
			probabilities = ()

			# generate all possible probabilities
			for k in states:
				(probability, state) = (V[words-1][k] * transition[k][j] 
					* emission[j][observations[words]], k)
				probabilities = (probability, ) + probabilities

			# choose highest and add to Vocabulary
			V[words][j] = max(probabilities)

		# probability of best path
		max_prob = max(V[-1].values())

		# states of best path
		path = []
		for step in V:
			for state, prob in step.items():
				if (step[state] == max(step.values())):
					path.append(state)

	# show results
	print('vocabulary: ', V)	
	print('path: ', path)
	print('prob: ', max_prob)
	

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
	
	word_tag_array = word_tag_file(train, args.n)
	word_tag_model = counter_list_wt(word_tag_array)
	word_keys = word_tag_dictionary(word_tag_model)

	# The probability of a tag given a word
	word_tag_prob = get_probablities(tag_array, word_tag_model)
	# The probability of a tag given the previous tag
	tag_prob = get_probablities(tag_array, tag_model)

	# Makes empty tag array
	Tags = []

	# Provides test sentences
	sentence_array = ["Just",'as', 'you', 'can', 'yell', "the"]


	# Makes an tuple of all the tags that a word can have
	for j in sentence_array:
		
		new_Tags = word_keys[j]

		for i in new_Tags:
			if i not in Tags:
				Tags.append(i)
		
	# These are all the tags	
	states = tuple(Tags)

	# Puts all words from the sentence in observations
	observations = tuple(sentence_array)


	# Makes an array containg the first column of V
	start_probability = {}

	for i in states:
		prob = tag_prob["START",i] * word_tag_prob[i, observations[0]]
		start_probability.update({i: prob})


	#Makes the first part of the dict using Start
	transition_probability = {}

	dict = {}		
	j = 0
	while(j < len(states) ):
		dict.update({states[j]: tag_prob["START",states[j]] } )
		j += 1
	transition_probability.update({"START": dict})

	# Sets all probabilities for the transition model in a dict
	for i in range(0, len(states)):

		dict = {}		
		j = 0
		while(j < len(states) ):
			dict.update({states[j]: tag_prob[states[i],states[j]] } )
			j += 1
			
		transition_probability.update({states[i]: dict})

	# Sets all probabilities for the Emission model in a dict	
	emission_probability = {}
		
	for i in states:
		dict = {} 
		for j in observations:
			dict.update({j: word_tag_prob[i,j]})
		emission_probability.update({i: dict})	
	

# run
viterbi(observations, states, start_probability, transition_probability, emission_probability)	