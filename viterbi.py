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
	
# data
observations = ('x', 'z', 'y')
states = ('q_1', 'q_2')

start = {'q_1': 1, 'q_2': 0}

transition = {'q_1': {'q_1': 0.7, 'q_2': 0.3}, 
			  'q_2': {'q_1': 0.5, 'q_2': 0.5}}

emission = {'q_1': {'x': 0.6, 'y': 0.1, 'z': 0.3},
			'q_2': {'x': 0.1, 'y': 0.7, 'z': 0.2}}	

# run
viterbi(observations, states, start, transition, emission)	

		  