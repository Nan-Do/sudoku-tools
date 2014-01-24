'''
Created on 23/03/2013

@author: Fernando Tarin Morales
'''

import random

from PartialSudokuGenerator import generate_partial_sudoku
from PartialSudokuFiller import fill_partial_sudoku
from SudokuSolver import sudoku_solver

# Values to determine the difficulty of the sudoku board
EASY = 0; MEDIUM = 1; HARD = 2
LEVEL = [20, 40, 60]

# This function returns the position (row and column) of a tile in 
# the sudoku numbered from 0 to 80 
def get_sudoku_position(tile):
    return tile/9, tile%9

# Pretty printer for the sudoku
def print_sudoku(sudoku):
    for i in xrange(9):
        if i != 0: print
        for j in xrange(9):
            print sudoku[i][j],
    print '\n'
    
# Pretty printer for all the sudoku boards
def print_sudokus(original, game_board, solved):
    for i in xrange(9):
        if i != 0: print
        for j in xrange(9):
            print original[i][j],
        print "\t",
        for j in xrange(9):
            print game_board[i][j],
        print "\t",
        for j in xrange(9):
            print solved[i][j],
 

# Generate the sudoku board
if __name__ == '__main__':
    # Select the difficulty  (EASY, MEDIUM, HARD)
    empty_tiles = LEVEL[HARD]
    difficulty = "HARD"
    
    # Generate a full board
    count, sudoku = fill_partial_sudoku(generate_partial_sudoku())
    original = [row[:] for row in sudoku]
    # Generate the list of tiles and shuffle it to remove them in a
    # random order
    tiles = [ x for x in xrange(81) ]
    random.shuffle(tiles)
    c = 0
    while empty_tiles > 0:
        # If the generated board removing one random tile has only one
        # possible solution keep removing tiles until we meet the requirements
        # otherwhise re-add the tile to the list of tiles and try with another one
        tile = tiles.pop()
        i,j = get_sudoku_position(tile)
        value = sudoku[i][j]
        sudoku[i][j] = 'x'
        count = 0
        for _ in sudoku_solver(sudoku):
            count += 1
        if count != 1:
            sudoku[i][j] = value
            tiles.append(tile)
            random.shuffle(tiles)
            c += 1
            if c == len(tiles):
                break
        else:
            #print "Remaining tiles: ", empty_tiles
            empty_tiles -= 1
            c = 0

    print "Difficulty:", difficulty
    g = sudoku_solver(sudoku)
    answer = g.next()
    print_sudokus(original, sudoku, answer)
