'''
Created on 30/03/2013

@author: Fernando Tarin Morales
'''

import random

from PartialSudokuGenerator import generate_partial_sudoku
from PartialSudokuFiller import fill_partial_sudoku
from SudokuSolver import sudoku_solver
from SudokuTools import is_a_valid_sudoku

def get_sudoku_position(tile):
    return tile/9, tile%9

def print_sudoku(sudoku):
    for i in xrange(9):
        if i != 0: print
        for j in xrange(9):
            print sudoku[i][j],
    print '\n'

REPS = 50
EMPTY_TILES = 25

if __name__ == '__main__':
    for _ in xrange(REPS):
        empty_tiles = EMPTY_TILES
        tiles = [ x for x in xrange(81) ]
        random.shuffle(tiles)
        c = 0
        count, sudoku = fill_partial_sudoku(generate_partial_sudoku())
        original = [row[:] for row in sudoku]
        while empty_tiles > 0:
            tile = tiles.pop()
            i,j = get_sudoku_position(tile)
            value = sudoku[i][j]
            sudoku[i][j] = 'x'
            count = 0
            
            for _ in sudoku_solver(sudoku): count += 1
                
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
        
        e_t = 0
        for i in xrange(9):
            for j in xrange(9):
                if sudoku[i][j] == 'x':
                    e_t += 1
                    
        if e_t != EMPTY_TILES:
            raise ValueError("Expecting", EMPTY_TILES, "free tiles, got", e_t)
        
        for c, s in enumerate(sudoku_solver(sudoku)):
            if not is_a_valid_sudoku(s):
                raise ValueError("The solved sudoku is not valid")
            if c > 0:
                raise ValueError("The generated board has more than one solution")
                
    print REPS, "valid boards generated"
        
        
