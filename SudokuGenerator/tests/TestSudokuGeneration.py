'''
Created on 23/03/2013

@author: Fernando Tarin Morales
'''

import time

from PartialSudokuGenerator import generate_partial_sudoku
from PartialSudokuFiller import fill_partial_sudoku
from SudokuSolver import sudoku_solver
from SudokuTools import is_a_valid_sudoku

def generate_sudoku_board():
    return fill_partial_sudoku(generate_partial_sudoku())           
             
if __name__ == '__main__':
    # Using the custom algorithim
    reps = 7500;
    sudokus = []
    
    start = time.time()
    for v in xrange(reps):
        sudoku = None
        count, sudoku = generate_sudoku_board()

        if sudoku == None or not is_a_valid_sudoku(sudoku):
            print sudoku
            raise ValueError("Invalid sudoku generated")
        sudokus.append(sudoku)
    end = time.time()
    
    sudokus.sort()
    for x in xrange(reps-1):
        if sudokus[x] == sudokus[x+1]: 
            raise ValueError("Two equal sudokus generated")
    
    print reps, "valid and different sudokus generated in", end - start, "secs using the custom algorithm"
    
    # Using the solver to generate the sudokus
    sudoku = [ ['x' for _ in xrange(9)] for _ in xrange(9)]
    g = sudoku_solver(sudoku)
    start = time.time()
    reps = 50
    sudokus = []
    
    for _ in xrange(reps):
        sudoku = g.next()
        if not is_a_valid_sudoku(sudoku):
            print sudoku
            raise ValueError("Invalid sudoku generated")
        sudokus.append(sudoku)
    end = time.time()
    
    sudokus.sort()
    print reps, "valid sudokus generated in", end - start\
        ,"secs using the sudoku solver", "(", g.__name__, "version)"
    
    