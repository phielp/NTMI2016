import re
import argparse
import itertools

# transitionMatrix = [[1, 0.7, 0.5], [0, 0.3, 0.5]]
# outputMatrix = [[0.6, 0.1], [0.1, 0.7], [0.3, 0.2]]
transitionMatrix = [[1, 0], [0.5, 0.5], [0.7, 0.3]]
outputMatrix = [[0.6, 0.3, 0.1], [0.1, 0.2, 0.7]]

n = 3
v = 2



# words
# O_1.....O_t
observations = []

# q_1.....q_n
states = []

def viterbi(transitionMatrix, outputMatrix):
	chart = []
	column = []
	viterbi = []

	# print(transitionMatrix[0][0])
	# print(outputMatrix[0][0])

	i = 0
	# initialization step (first column)
	for j in range(0, len(outputMatrix)):
		# print(transitionMatrix[i][j])
		# print(outputMatrix[i][j])
		multiple = transitionMatrix[i][j] * outputMatrix[i][j]
		column.append(multiple)	

	viterbi.append(column)
	

	for i in range(0, len(transitionMatrix)):
		print(viterbi[i])
		# for j in range(0, len(outputMatrix)):
		# 	result = viterbi[i][j] * transitionMatrix[i][j] * outputMatrix[i][j]





	# # recursion step (second...N columns)
	# for i in range (0, v-1):
	# 	for j in range(0, len(outputMatrix[0])-1):
	# 		transition = transitionMatrix[i][n]
	# 		n += 1
	# 		output = outputMatrix[len(outputMatrix)-1][0]
	# 		multiple = output * transition
	# 		print(multiple)
	# 		chart.append([chart[0][0] * output * transition])

	# print(chart)

viterbi(transitionMatrix,outputMatrix)	