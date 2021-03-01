

from enum import Enum
class state(Enum):
    Black = 1
    Unknown = 0
    White = -1
    

ROWS = 6
COLUMNS = 6
Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]

#array that describes the rows of the matrix, up to down
rows_arr = ["2 1", "1 3", "1 2", "3", "4", "1"]
#array that describes the columns of the matrix, left to right
columns_arr = ["1", "5", "2", "5", "2 1", "2"]

"""
Matrix[0][3] = state.White
Matrix[0][4] = state.White
Matrix[2][4] = state.Black
Matrix[2][5] = state.Black
"""


def main():

    has_improvement = True

    while has_improvement:
        has_improvement = solve_1_iteration()

    #check if the nonogram was finished:
    if (nonogram_was_solved()):
        print("finished successfully!")
        print_nonogram()
    else:
        print("not succeeded finishing nonogram")
        print_nonogram()
        
    
def solve_1_iteration():
    has_improvement = False

    for i in range(0, ROWS):
        tmp_has_imp = update_1_row(rows_arr[i], i)
        if tmp_has_imp: 
            has_improvement = True

    for i in range(0, COLUMNS):
        tmp_has_imp = update_1_column(columns_arr[i], i)
        if tmp_has_imp: 
            has_improvement = True

    return has_improvement

def update_1_row(row, row_idx):
    x=1

def update_1_column(column, column_idx):
    x=1

def print_nonogram():
    for line in Matrix:
        for var in line:
            if var is state.Unknown:
                print('-', end=" ")
            elif var is state.White:
                print('~', end=" ")
            elif var is state.Black:
                print('%', end=" ")
        print("")

        
def nonogram_was_solved():
    for line in Matrix:
        for var in line:
            if var is state.Unknown:
                return False
    return True


if __name__ == "__main__":
    main()
