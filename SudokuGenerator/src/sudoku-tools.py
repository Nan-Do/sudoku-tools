#! /usr/bin/python
'''
Created on 23/03/2013

@author: Fernando Tarin Morales
'''

import sys
import random
import argparse

from PartialSudokuGenerator import generate_partial_sudoku
from PartialSudokuFiller import fill_partial_sudoku
from SudokuSolver import sudoku_solver

# Values to determine the difficulty of the sudoku board
EASY = 0; MEDIUM = 1; HARD = 2
level = [20, 40, 60]

# This function will read a sudoku from a given stream.
# The format is one row per line with spaces between
# values and and x when a value is unknown
def read_sudoku(stream):
    sudoku = []
    for i in xrange(9):
        line = stream.readline()
        if len(line.split()) != 9: return None, i
        row = []
        for p,c in enumerate(line.split()):
            if p > 9: return None
            if c == 'x':
                row.append(c)
            else:
                try: row.append(int(c))
                except ValueError: return None, i
        sudoku.append(row)

    return sudoku,i


# This function returns the position (row and column) of a tile in
# the sudoku numbered from 0 to 80
def get_sudoku_position(tile):
    return tile/9, tile%9


# Pretty printer for all the sudoku boards
def print_sudokus(original, game_board, print_only_gameboard=False):
    for i in xrange(9):
        if i != 0: print
        if not print_only_gameboard:
            for j in xrange(9):
                print original[i][j],
            print "    ",
        for j in xrange(9):
            print game_board[i][j],
    print '\n'

def generate_sudoku_table(board, empty_tiles):
    # Copy the given board
    sudoku = [ row[:] for row in  board ]

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
            empty_tiles -= 1
            c = 0

    return sudoku


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--difficulty", help="set the difficulty of the generated\
                                        sudoku can be easy, medium, hard. Medium by default",
                        type=str, choices=["easy", "medium", "hard"],)
    parser.add_argument("-e", "--empty-tiles", help="set the number of empty tiles in the\
                                        generated sudoku. Will override -d parameter.\
                                        Be careful a high value can take too much time",
                        type=int)
    parser.add_argument("-g", "--generate", help="generate as many sudokus as specified",
                        type=int)
    parser.add_argument("-s", "--solve", action="store_true",
                         help="In this mode the given sudoku will be solved. If an input file is\
                               not specified standard input will be used instead")
    parser.add_argument("-m", "--seed", help="use the specified seed to generate the sudoku board,\
                                        useless if -i option is specified",
                        type=int)
    parser.add_argument("-n", "--no-print-board", action="store_true",
                        help="don't print the sudoku board")
    parser.add_argument("-x", "--use-empty-board", action="store_true",
                        help="use an empty board to generate the sudokus. This is a special mode in which\
                              boards following an order will be generated. It is slower than the normal mode")
    parser.add_argument("-i", "--input-file", type=str,
                        help="get the sudoku from the input file. The sudoku can be used as a board to generate\
                              sudokus or to solve with the solver option. If used as boards and g option is used\
                              it will expect GENERATE sudokus in the file. If s option is used it will try to solve\
                              as many sudokus as there are in the file")

    args = parser.parse_args()

    input_file = None
    lines = 0
    if args.input_file != None:
        try:
            input_file = open(args.input_file, 'r')
        except IOError as e:
            sys.stderr.write("Error opening file " + str(args.input_file) + ": " + e.strerror + "\n")
            sys.exit(0)

    if args.solve:
        if input_file == None:
            input_file = sys.stdin

        while(1):
            sudoku, l = read_sudoku(input_file)
            lines += l
            if sudoku == None:
                sys.stderr.write("Error: File: ")
                if args.input_file != None:
                    sys.stderr.write(args.input_file + " at line " + str(lines))
                else:
                    sys.stderr.write("stdin at line " + str(lines))
                sys.stderr.write(": Problem reading the sudoku from file\n")
                sys.exit(0)

            #print sudoku
            try: answer = sudoku_solver(sudoku).next()
            except StopIteration:
                sys.stderr.write("Error: File: ")
                if args.input_file != None:
                    sys.stderr.write(args.input_file + " at line " + str(line))
                else:
                    sys.stderr.write("stdin at line " + str(line))
                sys.stderr.write(": The given sudoku has no answer\n")
                sys.exit(0)
            #print answer

            print_sudokus(sudoku, answer)
        sys.exit(0)


    if args.difficulty:
        if args.difficulty == 'easy': empty_tiles = level[EASY]
        elif args.difficulty == 'medium': empty_tiles = level[MEDIUM]
        elif args.difficulty == 'hard': empty_tiles = level[HARD]
    else:
        empty_tiles = level[MEDIUM]

    if args.empty_tiles != None:
        if (args.empty_tiles < 0 or args.empty_tiles > 81):
            sys.stderr.write("Warning empty_tiles: " + str(args.empty_tiles) + " is not valid\n")
            sys.stderr.write("         Only values between [0-81] are accepted\n")
            sys.stderr.write("         Backing to medium difficulty\n")
        else:
            empty_tiles = args.empty_tiles

    generate = 1
    if args.generate != None:
        if args.generate < 0:
            sys.stderr.write("Warning generate: " + str(args.generate) + " is not valid\n")
            sys.stderr.write("         Only values greater than 0 are accepted\n")
            sys.stderr.write("         Backing to 1\n")
        else:
            generate = args.generate

    seed = args.seed
    print_answer_only = args.no_print_board

    if args.use_empty_board:
        # generate the empty board
        empty_board = [['x' for _ in xrange(9) ] for _ in range(9)]
        g = sudoku_solver(empty_board)
        for _ in xrange(generate):
            board = g.next()
            sudoku = generate_sudoku_table(board, empty_tiles)
            print_sudokus(board, sudoku, print_answer_only)
        sys.exit(0)

    # Generate a full board
    for i in xrange(generate):
        if input_file:
            board, l = read_sudoku(input_file)
            if l == 0:
                if generate - i != 1:
                    sys.stderr.write("Expecting " + str(generate - i) + " more boards from file " + args.input_file + "\n")
                else:
                    sys.stderr.write("Expecting 1 more board from file " + args.input_file + "\n")
                sys.exit(0)
            lines += l
            if board == None:
                sys.stderr.write("Error reading the board from file: " + args.input_file + " Line: " + str(lines) + "\n")
                sys.exit(0)
            input_file.readline()
        else:
            count, board = fill_partial_sudoku(generate_partial_sudoku(seed))
        sudoku = generate_sudoku_table(board, empty_tiles)

        print_sudokus(board, sudoku, print_answer_only)



