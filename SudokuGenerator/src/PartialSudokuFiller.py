'''
Created on 23/03/2013

@author: Fernando Tarin Morales
'''

import itertools

def get_ranges_for_square(square):
    if square == 0:
        return xrange(0,3), xrange(0,3)
    if square == 2:
        return xrange(0,3), xrange(6,9)
    if square == 6:
        return xrange(6,9), xrange(0,3)
    if square == 8:
        return xrange(6,9), xrange(6,9) 

def get_valid_row_values(sudoku, i, row_range):
    values = [sudoku[i][j] for j in row_range if sudoku[i][j] != 0]
    return set(xrange(1,10)).symmetric_difference(values)

def get_valid_column_values(sudoku, column_range, j):
    values = [ sudoku[i][j] for i in column_range if sudoku[i][j] != 0]
    return set(xrange(1,10)).symmetric_difference(values)

def get_possible_matrix_values(sudoku, square):
    matrix_values = [ [] for _ in xrange(3)]
    i_range, j_range = get_ranges_for_square(square)
    
    if square == 0:
        row_range = column_range = [3,4,5]
    if square == 2:
        row_range, column_range  = [0,1,2,3,4,5], [3,4,5]
    if square == 6:
        row_range, column_range = [3,4,5], [0,1,2,3,4,5]
    if square == 8:
        row_range = column_range = [0,1,2,3,4,5]

    z = -1
    for i in i_range:
        row_values = get_valid_row_values(sudoku, i, row_range)
        z += 1
        for j in j_range:
            column_values = get_valid_column_values(sudoku, column_range, j)
            matrix_values[z].append(row_values.intersection(column_values))
            
    return matrix_values

def generate_possible_grid_squares(matrix):
    m = []
    for i in xrange(3):
        m.append([x for x in list(itertools.product(
                      matrix[i][0], matrix[i][1], matrix[i][2])) 
                      if len(x) == len(set(x))])
    
    valid = set([x for x in xrange(1,10)])
    for element in itertools.product(m[0], m[1], m[2]):
        answer = []
        for i in xrange(3):
            answer.extend(element[i])
        if valid != set(answer): continue
        yield answer
        
def fill_square(sudoku, grid, square):
    i_range, j_range = get_ranges_for_square(square)
    z = 0
    for i in i_range:
        for j in j_range:
            sudoku[i][j] = grid[z]
            z += 1   

# This function takes a partial filled sudoku as explained in the 
# PartialSudokuGenerator module and returns a complete and valid
# sudoku. The function works generating possible values for every 
# emtpy square and filling them. If a certaing combination leads
# to a non valid sudoku just try another one. On average it will
# only explore less than 10 different combinations/states 
def fill_partial_sudoku(sudoku):
    matrix_0 = get_possible_matrix_values(sudoku, 0)
    square0_gen = generate_possible_grid_squares(matrix_0)
    
    count = 0
    for grid_0 in square0_gen:
        fill_square(sudoku, grid_0, 0)
        matrix_2 = get_possible_matrix_values(sudoku, 2)
        square2_gen = generate_possible_grid_squares(matrix_2)
        for grid_2 in square2_gen:
            fill_square(sudoku, grid_2, 2)
            matrix_6 = get_possible_matrix_values(sudoku, 6)
            square6_gen = generate_possible_grid_squares(matrix_6)
            for grid_6 in square6_gen:
                fill_square(sudoku, grid_6, 6)
                matrix_8 = get_possible_matrix_values(sudoku, 8)
                try:
                    grid_8 = generate_possible_grid_squares(matrix_8).next()
                    fill_square(sudoku, grid_8, 8)
                    return count, sudoku
                except StopIteration:
                    count += 1 
                    continue                    

    return None

if __name__ == '__main__':
    pass