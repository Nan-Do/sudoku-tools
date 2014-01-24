'''
Created on 30/03/2013

@author: Fernando Tarin Morales
'''

# This function checks that a given sudoku (as a list of lists)
# is complete and valid. 
# Returns:
# True if the given sudoku is complete and valid
# False otherwise
def is_a_valid_sudoku(sudoku):
    # build the answer to compare with
    answer = set([ x for x in xrange(1, 10)])
    squares = [ [] for _ in xrange(9) ]
    # check rows, columns and build the squares
    for i in xrange(9):
        if answer != set(sudoku[i]): return False
        column = []
        for j in xrange(9):
            column.append(sudoku[j][i])
        
            if i < 3:
                if j < 3:
                    squares[0].append(sudoku[i][j])
                elif j < 6:
                    squares[1].append(sudoku[i][j])
                elif j < 9:
                    squares[2].append(sudoku[i][j])
            elif i < 6:
                if j < 3:
                    squares[3].append(sudoku[i][j])
                elif j < 6:
                    squares[4].append(sudoku[i][j])
                if j < 9:
                    squares[5].append(sudoku[i][j])
            elif i < 9:
                if j < 3:
                    squares[6].append(sudoku[i][j])
                elif j < 6:
                    squares[7].append(sudoku[i][j])
                elif j < 9:
                    squares[8].append(sudoku[i][j])
                    
        if answer != set(column): return False
                    
    # check the squares
    for i in xrange(9):
        if set(squares[i]) != answer: return False
        
    return True