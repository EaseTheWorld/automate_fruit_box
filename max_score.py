S = 10

def max_score(matrix):
	for c1 in range(len(matrix[0])):
		for c2 in range(c1, len(matrix[0])):
			print('col', c1, c2)
			r1 = -1
			r2 = -1
			row_sum = 0
			found = False
			while r2 < len(matrix):
				if row_sum < S:
					#print('inc [',r1,c1,']-[',r2,c2,']', row_sum)
					r2 += 1
					if r2 < len(matrix):
						row_sum += matrix[r2][c2] - (matrix[r2][c1-1] if c1 > 0 else 0)
					else:
						break
				elif row_sum > S:
					r1 += 1
					#print('dec [',r1,c1,']-[',r2,c2,']', row_sum)
					row_sum -= matrix[r1][c2] - (matrix[r1][c1-1] if c1 > 0 else 0)
				else:
					found = True
					print('*** [',r1,c1,']-[',r2,c2,']')
					r2 += 1
					if r2 < len(matrix):
						row_sum += matrix[r2][c2] - (matrix[r2][c1-1] if c1 > 0 else 0)
					else:
						break
			if not found:
				break

def prefix_sum_row(matrix):
	for r in range(len(matrix)):
		for c in range(1, len(matrix[r])):
			matrix[r][c] += matrix[r][c-1]
	return matrix


matrix = [
	[1,9,2,8],
	[9,3,5,2],
	[1,7,5,5]
]

print(matrix)
prefix_sum_row(matrix)
immutable_matrix = tuple(map(tuple, matrix))
print(immutable_matrix)
max_score(immutable_matrix)