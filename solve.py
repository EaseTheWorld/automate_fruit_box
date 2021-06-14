import sys
import time
import functools

S = 10

def clear_range(matrix, cur_range):
	r1, c1, r2, c2 = cur_range
	return tuple(
		tuple(0 if ci in range(c1,c2+1)
			else cv
			for ci,cv in enumerate(rv)) if ri in range(r1,r2+1)
		else rv
		for ri,rv in enumerate(matrix))

def sum_matrix(matrix):
	res = list(map(list, matrix))
	for r in range(len(res)):
		for c in range(1, len(res[r])):
			res[r][c] += res[r][c-1]
	for r in range(1, len(res)):
		for c in range(len(res[r])):
			res[r][c] += res[r-1][c]
	return res

def range_sum(sm, cur_range):
	r1, c1, r2, c2 = cur_range
	return (sm[r2][c2]
		- (sm[r1-1][c2] if r1 > 0 else 0)
		- (sm[r2][c1-1] if c1 > 0 else 0)
		+ (sm[r1-1][c1-1] if r1 > 0 and c1 > 0 else 0))

def dump(matrix):
	for r in matrix:
		print(' ', r)

funccount = 0

@functools.lru_cache(maxsize=None)
def recursive_find_next_move(matrix, depth):
    global funccount
    funccount += 1

    max_score = (0,0)
    max_score_move_list = tuple()
    max_matrix = None
    if depth > 0:
        sm = sum_matrix(matrix)
        cm = sum_matrix(tuple(tuple(1 if v > 0 else 0 for v in r) for r in matrix))
        for r1 in range(len(matrix)):
            for c1 in range(len(matrix[r1])):
                for r2 in range(r1, len(matrix)):
                    for c2 in range(c1, len(matrix[r2])):
                        next_move = (r1, c1, r2, c2)
                        rs = range_sum(sm, next_move)
                        if rs == S:
                            rc = range_sum(cm, next_move)
                            next_matrix = clear_range(matrix, next_move)
                            #print('depth', depth, 'next_move', next_move, 'max_score', max_score)
                            #dump(next_matrix)
                            score, next_move_list, _ = recursive_find_next_move(next_matrix, depth-1)
                            if score[1] + rc > max_score[1]:
                                max_score = (rc, score[1] + rc)
                                max_score_move_list = (next_move,) + next_move_list
                                max_matrix = next_matrix
                                #print('new depth', depth, 'next_move_list', next_move_list, 'max_score', max_score)
                            break
                        elif rs > S:
                            break
    return (max_score, max_score_move_list, max_matrix)

def find_best_move(matrix):
    score, move_list, next_matrix = recursive_find_next_move(matrix, 2)
    #print('return', score, move_list)
    next_move = move_list[0] if move_list else None
    return (score[0], next_move, next_matrix)

def solve(matrix, depth):
	score_sum = 0
	t1 = time.time()
	while True:
		score, next_move = find_best_move(matrix, depth)
		if not next_move:
			break
		score_sum += score[0]
		matrix = clear_range(matrix, next_move[0])
		#print(score, next_move[0])
		#dump(matrix)
	t2 = time.time()
	print('final score', score_sum, 'time', t2-t1)


'''

matrix = (
	(1, 9, 2, 8, 2, 7, 4, 2, 1, 9, 2, 8, 2, 7, 4, 2),
	(9, 3, 5, 2, 1, 3, 6, 3, 9, 3, 5, 2, 1, 3, 6, 3),
	(1, 7, 5, 5, 9, 1, 1, 5, 1, 7, 5, 5, 9, 1, 1, 5),
)
matrix = (
  (1, 9, 1, 8, 9, 1, 7, 4, 6, 6, 1, 7, 9, 4, 9, 9, 5) ,
  (3, 4, 8, 2, 7, 1, 5, 3, 4, 8, 2, 9, 8, 2, 5, 4, 8) ,
  (9, 2, 7, 9, 2, 5, 6, 6, 3, 6, 1, 7, 1, 2, 6, 8, 6) ,
  (2, 3, 7, 9, 5, 8, 4, 8, 5, 4, 8, 6, 5, 3, 6, 9, 5) ,
  (6, 6, 5, 1, 2, 7, 9, 8, 8, 7, 6, 9, 6, 8, 3, 3, 7) ,
  (2, 8, 9, 6, 1, 6, 1, 6, 4, 4, 8, 7, 3, 2, 5, 1, 5) ,
  (9, 7, 9, 2, 1, 2, 6, 2, 5, 7, 3, 4, 7, 4, 7, 1, 2) ,
  (1, 7, 1, 9, 3, 4, 1, 5, 3, 9, 1, 3, 8, 8, 1, 8, 3) ,
  (8, 8, 9, 9, 5, 9, 3, 2, 2, 8, 6, 6, 9, 3, 5, 9, 5) ,
  (9, 3, 2, 3, 3, 9, 7, 9, 7, 2, 8, 7, 9, 8, 5, 2, 7) ,
)




matrix3	 = (
	(1, 9, 2, 8, 2, 7, 4, 2),
	(9, 3, 5, 2, 1, 3, 6, 3),
	(1, 7, 5, 5, 9, 1, 1, 5),
	(1, 9, 2, 8, 2, 7, 4, 2),
	(9, 3, 5, 2, 1, 3, 6, 3),
	(1, 7, 5, 5, 9, 1, 1, 5),
)
matrix2 = (
	(1, 9, 2, 8),
	(9, 3, 5, 2),
	(1, 7, 5, 5)
)

# depth1:4, 2:6
matrix3 = (
	(5, 9, 4, 3, 1),
	(4, 1, 8, 3, 1),
	(2, 9, 1, 3, 4)
)


depth = int(sys.argv[1])

#print(matrix)
t1 = time.time()
score, next_move = find_best_move(matrix, depth)
t2 = time.time()
print('score', score, 'time', (t2-t1), 'funccount', funccount, 'cache', len(func_cache))
print('next_move', next_move)

solve(matrix, depth)
'''
