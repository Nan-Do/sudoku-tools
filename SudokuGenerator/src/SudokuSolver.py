'''
Created on 24/03/2013

@author: Fernando Tarin Morales
'''

import itertools
from SudokuTools import is_a_valid_sudoku

def get_square_ranges_for_a_given_position(i, j):
    if i < 3: row_range = xrange(0,3)
    elif i < 6: row_range = xrange(3,6)
    else: row_range = xrange(6,9)
    
    if j < 3: column_range = xrange(0,3)
    elif j < 6: column_range = xrange(3,6)
    else: column_range = xrange(6,9)
    
    return row_range, column_range

def get_possible_values_for_a_given_position(sudoku, i, j):
    answer = set(xrange(1,10))
    row = [sudoku[i][x] for x in xrange(9) if sudoku[i][x] != 'x']
    column = [sudoku[x][j] for x in xrange(9) if sudoku[x][j] != 'x']
    row_range, column_range = get_square_ranges_for_a_given_position(i, j)
    
    square = [sudoku[r][c] for r in row_range for c in column_range
                if sudoku[r][c] != 'x']
    
    return answer.difference(row).difference(column).difference(square)

# This generator is used to compute all the possible answers for the given
# sudoku as input it will accept a partial filled sudoku.
# This version of the solver uses itertools.product to build every possible
# combination of values including invalid combinations. Easier to maintain
# and read but slower that the other one. Doesn't modify the given sudoku
# Returns:
# A possible solution for the given sudoku or raises StopIteration if there
# are no more answers
def _sudoku_solver_1(_sudoku):
    sudoku = [row[:] for row in _sudoku]
    
    # Get all the unknown tiles (positions with x)
    free_positions = []
    for i in xrange(9):
        for j in xrange(9):
            if sudoku[i][j] == 'x':
                free_positions.append((i,j))
    if len(free_positions) == 0:
        raise StopIteration
     
    # Build the list of generators to get all the possible
    # answers for the current sudoku           
    possible_values = []
    for pos in free_positions:
        possible_values.append(get_possible_values_for_a_given_position(
                                    sudoku, pos[0], pos[1]))
    
    # Create the generator
    answer_generator = itertools.product(*possible_values)
    
    # Check if the answer can be used to create a valid sudoku
    # and yield it
    for answer in answer_generator:
        for pos, value in enumerate(answer):
            i,j = free_positions[pos]
            sudoku[i][j] = value
        # Check if the given answer is valid           
        if is_a_valid_sudoku(sudoku):
            yield sudoku
                
    raise StopIteration

def is_a_valid_movement(sudoku, i, j, value, free_positions, last_position):
    not_check_positions = free_positions[last_position+1:]
    for x in xrange(9):
        if sudoku[i][x] == value and (i,x) not in not_check_positions:
            return False
        if sudoku[x][j] == value and (x,j) not in not_check_positions:
            return False
        
    row_range, column_range = get_square_ranges_for_a_given_position(i, j)
    for r in row_range:
        for c in column_range:
            if sudoku[r][c] == value and (r,c) not in not_check_positions:
                return False 
        
    return True
        
# This generator is used to compute all the possible answers for the given
# sudoku as input it will accept a partial filled sudoku.
# This version of builds manually every possible combination of values
# checking that every value is valid. Doesn't modify the given sudoku
# Returns:
# A possible solution for the given sudoku or raises StopIteration if there
# are no more answers
def _sudoku_solver_2(_sudoku):
    sudoku = [row[:] for row in _sudoku]
    
    # Get all the unknown tiles (positions with x)
    free_positions = []
    for i in xrange(9):
        for j in xrange(9):
            if sudoku[i][j] == 'x':
                free_positions.append((i,j))
    if len(free_positions) == 0:
        raise StopIteration     
      
    # Build the list of lists cotaining every possible value for every free
    # position. Change the set into a list as the set is not iterable
    possible_values = []
    for pos in free_positions:
        possible_values.append(list(get_possible_values_for_a_given_position(
                                    sudoku, pos[0], pos[1])))
     
    # Initialize the indexes that will be used to keep track of which element
    # will be used to build the answer   
    last_positions = [ 0 for _ in xrange(len(possible_values))]
    last_position = 0
    answer = []
    while 1:
        # Get a value and check if it is a valid movement in that case add it 
        # to the answer otherwise drop it and update the indexes 
        value = possible_values[last_position][last_positions[last_position]]
        i, j = free_positions[last_position]
        if is_a_valid_movement(sudoku, i, j, value, free_positions, last_position):
            answer.append(value)
            last_position += 1
            sudoku[i][j] = value
        else:
            last_positions[last_position] += 1
            while last_positions[last_position] == len(possible_values[last_position]):
                last_positions[last_position] = 0
                last_position -= 1
                if last_position == -1: break
                last_positions[last_position] += 1
            if last_position == -1: break
        
        # We have collected values to fill the sudoku update the indexes acordingly
        # and yield the solution
        if last_position == len(possible_values):
            last_position -= 1
            last_positions[last_position] += 1
            while last_positions[last_position] == len(possible_values[last_position]):
                last_positions[last_position] = 0
                last_position -= 1
                if last_position == -1: break
                last_positions[last_position] += 1
            yield sudoku            
            if last_position == -1: break
    
    raise StopIteration

# Wrapper to choose between the two versions of the solver
def sudoku_solver(sudoku):
    return _sudoku_solver_2(sudoku)
          
if __name__ == '__main__':
    sudoku = [[8, 1, 3, 4, 9, 2, 5, 6, 7],
              [5, 'x', 7, 1, 8, 6, 2, 3, 4],
              [4, 6, 2, 7, 5, 3, 8, 1, 9],
              [3, 8, 1, 'x', 7, 9, 4, 5, 2],
              [2, 5, 4, 8, 3, 1, 7, 9, 6],
              [9, 7, 6, 2, 4, 5, 1, 8, 3],
              [6, 2, 8, 3, 1, 4, 9, 7, 5],
              [7, 3, 5, 9, 2, 8, 6, 4, 1],
              [1, 4, 9, 5, 6, 7, 3, 2, 8]]
    
    g = sudoku_solver(sudoku)
    print g.next()
