'''
Created on 23/03/2013

@author: Fernando Tarin Morales
'''

import random

# Given a chunk from the sudoku generates its permutations
# a chunk is a pice of three elements of a row or a column.
# From a given chunk there are only two permutations.
# The permutations come from the next matrix:
# v0 v1 v2 --> Given chunk
# v1 v2 v0
# v2 v0 v1
# As there are two possible matrices the rows are returned
# randomly. 
def generate_chunk_permutations(chunk):
    v0 = chunk[0]
    v1 = chunk[1]
    v2 = chunk[2]
    return ([v2, v0, v1], [v1, v2, v0]) if random.choice([True, False])\
        else ([v1, v2, v0], [v2, v0, v1])

# This function generates a partial sudoku with the following squares filled
# 0 x 2
# x x x
# 6 x 8
# It fills the central square and use the chunk permutations to fill the other
# squares randomly. If a seed is passed it will be used a seed for the random
# generator engine
def generate_partial_sudoku(seed=None):
    # Initialize the seed and the matrix that will hold the sudoku
    if seed: random.seed(seed)
    sudoku = [ [ 0 for _ in xrange(9) ] for _ in xrange(9) ]

    # seed first square
    row = range(1,10)
    random.shuffle(row)
    z = 0
    for i in xrange(3,6):
        for j in xrange(3,6):
            sudoku[i][j] = row[z]
            z += 1
            
    # central column
    chunks1 = generate_chunk_permutations(row[0:3])
    chunks2 = generate_chunk_permutations(row[3:6])
    chunks3 = generate_chunk_permutations(row[6:9])
    
    for i in [0,6]:
        if i == 0: index = 0
        else: index = 1
        for j in xrange(3):
            positions = [0,1,2]
            random.shuffle(positions)
            
            pos = positions.pop()
            element1 = chunks1[index][j]
            sudoku[i+pos][j+3] = element1
            
            pos = positions.pop()
            element2 = chunks2[index][j]
            sudoku[i+pos][j+3] = element2
            
            pos = positions.pop()
            element3 = chunks3[index][j]
            sudoku[i+pos][j+3] = element3
            
    # central row
    chunks1 = generate_chunk_permutations([sudoku[3][3], sudoku[4][3], sudoku[5][3]])
    chunks2 = generate_chunk_permutations([sudoku[3][4], sudoku[4][4], sudoku[5][4]])
    chunks3 = generate_chunk_permutations([sudoku[3][5], sudoku[4][5], sudoku[5][5]])
    
    for i in [0,6]:
        if i == 0: index = 0
        else: index = 1
        for j in xrange(3):
            positions = [0,1,2]
            random.shuffle(positions)
            
            pos = positions.pop()
            element1 = chunks1[index][j]
            sudoku[j+3][i+pos] = element1
            
            pos = positions.pop()
            element2 = chunks2[index][j]
            sudoku[j+3][i+pos] = element2
            
            pos = positions.pop()
            element3 = chunks3[index][j]
            sudoku[j+3][i+pos] = element3
            
            
    return sudoku

if __name__ == '__main__':
    print generate_partial_sudoku(1)