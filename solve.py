import sys
import time
import functools

S = 10

class Move:

    def __init__(self, score, rect):
        self.score = score
        self.r1 = rect[0]
        self.c1 = rect[1]
        self.r2 = rect[2]
        self.c2 = rect[3]

    def rect(self):
        return (self.r1, self.c1, self.r2, self.c2)

    def __str__(self):
        return f'score={self.score} ({self.r1},{self.c1})-({self.r2},{self.c2})'

def dump(matrix):
	for r in matrix:
		print(' '.join(map(lambda x : ' ' if x == 0 else str(x), r)))

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
    final_score = 0
    final_move_list = ()

    if depth > 0:
        cm = sum_matrix(tuple(tuple(1 if v > 0 else 0 for v in r) for r in matrix))
        next_candidates = find_next_candidates(matrix, S)
        for next_move in next_candidates:
            rc = range_sum(cm, next_move)
            next_matrix = clear_range(matrix, next_move)
            score, move_list = recursive_find_next_move(next_matrix, depth-1)
            #print('depth', depth, 'next_move', next_move, 'final_score', final_score, score, rc)
            #dump(next_matrix)
            if not final_score or score + rc < final_score:
                final_score = score + rc
                final_move_list = (Move(rc, next_move),) + move_list
                #print('new depth', depth, str(final_move_list[0]), 'final_score', final_score)
    return final_score, final_move_list

def find_move_list(matrix):
    total_move_list = []
    dump(matrix)
    while True:
        score, move_list = recursive_find_next_move(matrix, 2)
        for move in move_list:
            matrix = clear_range(matrix, move.rect())
            total_move_list.append(move)
            break
        if not move_list:
            break
    return total_move_list
