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

@functools.lru_cache(maxsize=None)
def recursive_find_next_move1(matrix, depth):
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
                            score, next_move_list, _ = recursive_find_next_move1(next_matrix, depth-1)
                            if score[1] + rc > max_score[1]:
                                max_score = (rc, score[1] + rc)
                                max_score_move_list = (next_move,) + next_move_list
                                max_matrix = next_matrix
                                #print('new depth', depth, 'next_move_list', next_move_list, 'max_score', max_score)
                            break
    return (max_score, max_score_move_list, max_matrix)

def find_next_candidates_whwh(matrix, given_sum):
    sm = sum_matrix(matrix)
    candidates = list()
    for r1 in range(len(matrix)):
        for c1 in range(len(matrix[r1])):
            for r2 in range(r1, len(matrix)):
                for c2 in range(c1, len(matrix[r2])):
                    next_move = (r1, c1, r2, c2)
                    rs = range_sum(sm, next_move)
                    if rs == given_sum:
                        candidates.append(next_move)
                        break
    return candidates

def find_next_candidates(matrix, given_sum):
    candidates = list()

    def prefix_sum(l):
        ret = list(l)
        for i in range(1, len(l)):
            ret[i] += ret[i-1]
        return ret

    def check_and_add(r1, c1, r2, c2, r1_sum, r2_sum):
        if (r1_sum[c2] != (r1_sum[c1-1] if c1 > 0 else 0)) and (r2_sum[c2] != (r2_sum[c1-1] if c1 > 0 else 0)):
            next_move = (r1, c1, r2, c2)
            candidates.append(next_move)

    for r1 in range(len(matrix)):
        col_sum = [0] * len(matrix[r1])
        r1_sum = prefix_sum(matrix[r1])
        for r2 in range(r1, len(matrix)):
            for c in range(len(col_sum)):
                col_sum[c] += matrix[r2][c]
            r2_sum = prefix_sum(matrix[r2])
            c1 = 0
            c2 = 0
            c12_sum = 0
            nonzero_indice = tuple(i for i,v in enumerate(col_sum) if v > 0)
            while c1 < len(nonzero_indice):
                if c12_sum > given_sum:
                    c12_sum -= col_sum[nonzero_indice[c1]]
                    c1 += 1
                elif c12_sum < given_sum:
                    if c2 >= len(nonzero_indice):
                        break
                    c12_sum += col_sum[nonzero_indice[c2]]
                    c2 += 1
                else:
                    check_and_add(r1, nonzero_indice[c1], r2, nonzero_indice[c2-1], r1_sum, r2_sum)
                    c12_sum -= col_sum[nonzero_indice[c1]]
                    c1 += 1
    return candidates

@functools.lru_cache(maxsize=None)
def recursive_find_next_move(matrix, depth):
    max_score = None
    max_score_move_list = tuple()
    max_matrix = None
    if depth > 0:
        cm = sum_matrix(tuple(tuple(1 if v > 0 else 0 for v in r) for r in matrix))
        next_candidates = find_next_candidates(matrix, S)
        for next_move in next_candidates:
            rc = range_sum(cm, next_move)
            next_matrix = clear_range(matrix, next_move)
            score, next_move_list, _ = recursive_find_next_move(next_matrix, depth-1)
            #print('depth', depth, 'next_move', next_move, 'max_score', max_score, score, rc)
            #dump(next_matrix)
            if not max_score or score[1] + rc > max_score[1]:
                max_score = (rc, score[1] + rc)
                max_score_move_list = (next_move,) + next_move_list
                max_matrix = next_matrix
                #print('new depth', depth, 'next_move_list', next_move_list, 'max_score', max_score)
    if not max_score:
        max_score = (0,0)
    return (max_score, max_score_move_list, max_matrix)

def find_best_move(matrix, depth=3):
    score, move_list, next_matrix = recursive_find_next_move(matrix, depth)
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
