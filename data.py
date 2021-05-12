from enum import Enum
class state(Enum):
    Black = 1
    Unknown = 0
    White = -1
   

RES_PATH = r"D:\visual studio projects\nonogram\res_file.txt"

# ------------put rows and columns here------------

values_rows_arr = [[4],[3,2],[1],[3,5],[1,8],
                   [6,1,1],[1,5,5,1],[1,1,5,2],[2,5,7,2],[2,7,7,2],
                   [2,7,1,3],[3,1,1,9,3],[3,1,16,4],[3,2,16,4],[2,3,17,5],
                   [2,2,17,2],[3,1,1,3,1,7],[3,1,1,6],[11,1,7],[25],
                   [24],[21,1],[19,2],[9],[30],
                   [24],[25],[14],[16]]

values_columns_arr = [[1,1],[3,1],[2,2,2],[2,2,3],[3,2,3],
                   [3,3,2,4],[3,3,3,4],[2,3,3,4],[2,1,4,4],[1,2,5,3],
                   [1,2,4,5,3],[2,3,4,5,3],[1,2,3,4,5,3,1],[20,3,1],[1,2,3,4,5,3,1],
                   [2,3,4,4,5],[1,2,5,4,5],[1,6,4,5],[2,1,2,6,4,5],[1,2,4,5,4,5],
                   [2,2,4,5,4,5],[23,5],[2,4,5,4,5],[2,4,5,4,5],[1,2,5,5,5],
                   [1,12,5],[3,7,5],[16,1,3],[14,1,2],[5,5,1,1,1],
                   [3,3,2,1],[1,1,1]]

# ------------------until here------------------

ROWS = len(values_rows_arr)
COLUMNS = len(values_columns_arr)
Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]

ROWS_HAS_CHANGE = [True for x in range(ROWS)]  # is there a difference from the previous round
COLUMNS_HAS_CHANGE = [True for x in range(COLUMNS)]  # --"--

# getters
def get_row(row_idx):
    return Matrix[row_idx][:]  # [:] to have a shallow copy

def get_column(column_idx):
    return [row[column_idx] for row in Matrix][:]
# setters
def set_row(new_content, row_idx):
    Matrix[row_idx] = new_content

def set_column(new_content, column_idx):
    for i in range(len(new_content)):
        Matrix[i][column_idx] = new_content[i]

def print_nonogram():
    max_row_width = max([len(' '.join([str(i) for i in v])) for v in values_rows_arr]) 
    
    # print column numbers
    print(' '*max_row_width, end='    ')
    for col_num in range(COLUMNS):
        if col_num < 9:
            print(str(col_num).rjust(2), end="")
        elif col_num == 9:
            print("", end="  ")
        elif col_num%2 == 0:
            print(str(col_num).rjust(2), end="  ")
    print("")

    # print column values
    col_as_list = [list(reversed([str(v).rjust(2, ' ') for v in col])) for col in values_columns_arr]
    max_col_width = max([len(col) for col in col_as_list])
    
    to_print = ['' for i in range(max_col_width)]

    for depth in range(max_col_width):
        cur = ""
        for col in col_as_list:
            cur += (col[depth] if len(col) > depth else "  ")
        to_print[depth] = cur

    
    to_print = list(reversed(to_print))
    for i in to_print:
        print("    " + " "*max_row_width + i)

    # print Matrix content
    i = 0
    for line in Matrix:
        # print row number
        print(str(i).ljust(2), end= "")
        i = i + 1
        # print row values
        print(' ' + (' '.join([str(i) for i in values_rows_arr[i-1]])).rjust(max_row_width), end= " ")
        # row content
        for var in line:
            if var is state.Unknown:
                print(' -', end="")  # '-' another option
            elif var is state.White:
                print('██', end="")  # '·' another option
            elif var is state.Black:
                print('  ', end="")  # %
        print("")

def get_user_data():
    print("enter rows top to bottom, row after row \nwrite values and spaces between them, like 1 2 2 5 \nto finish- enter some non-digit characters")
    
    values_rows_arr.clear()
    values_columns_arr.clear()

    row = input()
    row_parts = row.split(' ')
    while all(d.isdigit() for d in row_parts):
        values_rows_arr.append([int(d) for d in row_parts])
        row = input()
        row_parts = row.split(' ')

    print("finished getting rows. result: ")
    for r in values_rows_arr:
        print(r)

    print("enter columns left to right. finish as before")

    column = input()
    column_parts = column.split(' ')
    while all(d.isdigit() for d in column_parts):
        values_columns_arr.append([int(d) for d in column_parts])
        column = input()
        column_parts = column.split(' ')

    print("finished getting columns. result: ")
    for r in values_columns_arr:
        print(r)

    global ROWS
    global COLUMNS
    global Matrix
    ROWS = len(values_rows_arr)
    COLUMNS = len(values_columns_arr)
    Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]


        
def save_res_to_file():
    res = ""
    for line in Matrix:
        res += " ".join(map(lambda var: str(var.value), line))
        res += '\n'
    with open(RES_PATH, 'w') as res_file:
        res_file.write(res)
   

"""
# some basic shape - 6*6

#array that describes the rows of the matrix, up to down
values_rows_arr = [[2,1],[1,3],[1,2],[3],[4],[1]]
#array that describes the columns of the matrix, left to right
values_columns_arr = [[1],[5],[2],[5],[2,1],[2]]


# fish? - 10*10

#array that describes the rows of the matrix, up to down
values_rows_arr = [[1,1], [2,2], [1,6], [1,3,1], [1,4,1],[1,7], [8], [4,1], [3,2], [4]]
#array that describes the columns of the matrix, left to right
values_columns_arr = [[3], [3], [2], [5], [8],[6,2], [7,1], [1,2,1], [2,2,1], [6,2]]


# this example creates deer - 15*15

values_rows_arr = [[2,2,2,1], [2,2,1,1,2,1], [4,1,1,2,1], [5,5], [2,5],
                    [7], [1,1,5], [11], [12], [13],
                    [8,5], [1,3,5], [5,5], [3,6], [6]]

values_columns_arr = [[2], [3,3], [2,2,2], [4,6], [5,7],
                     [2,7], [3,1,4], [7], [2,4], [2,6,2],
                     [12], [15], [4,10], [1,9], [4,8]]


# this example creates a bigger deer - 30*30

values_rows_arr = [[1], [1], [1,3,1], [1,2,1,2,1], [4,1,1,1,2],
                   [2,2,3,2], [2,2,1,2,2,4], [3,2,1,1,3,1], [3,5,1,3,1], [2,1,4,4,1,2],
                   [4,2,5,2], [4,2,5,5], [4,3,10], [12,3,3], [14],
                   [9], [12], [4,5,1], [7,2], [10],
                   [11], [13], [7,4], [7,2], [7],
                   [5,8], [18], [22], [23], [24]]

values_columns_arr = [[1], [2], [1,3], [2,3], [2,2,3],
                   [7,3], [4,4,4], [3,2,1,4], [5,4], [3,5],
                   [3,5], [3,5], [2,2,5], [3,2,1,5], [4,7,2,4],
                   [10,2,5], [1,1,2,6,9], [4,1,1,4,12], [5,17], [5,2,16],
                   [21], [22], [24], [7,3,3,4,4], [4,2,1,2,3],
                   [1,3,7], [5,6], [7,4], [2,2], [1]]


# ship - 29*32

values_rows_arr = [[4],[3,2],[1],[3,5],[1,8],
                   [6,1,1],[1,5,5,1],[1,1,5,2],[2,5,7,2],[2,7,7,2],
                   [2,7,1,3],[3,1,1,9,3],[3,1,16,4],[3,2,16,4],[2,3,17,5],
                   [2,2,17,2],[3,1,1,3,1,7],[3,1,1,6],[11,1,7],[25],
                   [24],[21,1],[19,2],[9],[30],
                   [24],[25],[14],[16]]

values_columns_arr = [[1,1],[3,1],[2,2,2],[2,2,3],[3,2,3],
                   [3,3,2,4],[3,3,3,4],[2,3,3,4],[2,1,4,4],[1,2,5,3],
                   [1,2,4,5,3],[2,3,4,5,3],[1,2,3,4,5,3,1],[20,3,1],[1,2,3,4,5,3,1],
                   [2,3,4,4,5],[1,2,5,4,5],[1,6,4,5],[2,1,2,6,4,5],[1,2,4,5,4,5],
                   [2,2,4,5,4,5],[23,5],[2,4,5,4,5],[2,4,5,4,5],[1,2,5,5,5],
                   [1,12,5],[3,7,5],[16,1,3],[14,1,2],[5,5,1,1,1],
                   [3,3,2,1],[1,1,1]]


# this example creates a huge deer - 80*80

#array that describes the rows of the matrix, up to down
values_rows_arr = [[2], [2,1,1], [1,2,3], [1,1,2,2], [1,4,1,2,1],
                   [1,2,4,1], [2,1,2,2,2,2], [3,1,2,2,1,2,1], [1,4,1,1,2,3,2], [1,2,2,2,1,2,3,2],
                   [1,3,2,3,3,1], [2,1,1,3,1,1,1,2,5], [2,2,3,3,1,4,1], [2,3,7,2,7,1], [5,1,1,2,3,3,5,1,2],
                   [2,2,3,4,6,7,1,1], [4,5,6,2,10,1,2,2], [2,2,7,6,1,7,1,2,2,3], [4,6,6,16,2,1,2,1], [2,2,1,5,9,3,2,3,2,3],
                   [3,3,9,4,4,3,2,3,1], [5,2,10,1,1,3,4,2,4,1], [3,3,5,3,4,1,1,3,4,3,5,3,1], [2,1,9,2,1,1,1,3,12,2,2], [1,2,1,7,2,3,1,3,9,2,1],
                   [2,1,3,1,3,4,1,3,4,1,2,2], [3,6,2,3,3,1,2,4,2,4,3], [3,2,3,9,2,4,8], [3,2,3,5,3,2,1,1,1,1,2], [3,2,10,2,1,2,1,1,1,1,1,2],
                   [1,2,12,2,2,2,1,2,2,2], [1,10,3,3,2,2,1,2,4,2], [1,1,6,4,3,1,1,2,1,6], [2,2,1,1,9,5,2,2,2,2,3], [3,1,1,2,2,8,4,3,5,1],
                   [3,5,3,8,5,6,7,2,1], [1,3,12,7,10,5,8,2,1], [4,5,3,1,6,2,7,3,7,1,2], [2,8,3,1,7,2,1,6,3,8,1,4,1], [5,2,7,1,6,2,1,1,3,3,3,5,1,3,1],
                   [4,1,1,3,2,6,2,1,3,5,5,1,3,1], [1,3,1,3,3,2,6,3,2,5,5,1,2,2], [6,11,1,7,3,2,4,6,1,7], [4,3,1,2,1,6,2,3,3,6,1,6], [2,2,4,2,1,1,5,2,2,3,6,2,7],
                   [2,2,2,2,2,1,5,3,1,2,9,2,4,1], [2,3,1,7,1,5,3,1,1,2,9,2,9], [3,5,3,4,2,5,3,1,1,2,2,5,3,8], [4,5,3,2,5,4,2,2,3,2,2,2,3,9], [8,4,1,6,5,4,3,1,1,2,3,9],
                   [2,9,2,2,3,13,1,1,2,2,1,2,10], [3,2,1,5,5,14,2,4,2,1,2,9], [5,2,1,1,3,2,13,3,1,1,4,1,1,3,10], [8,10,2,12,8,2,1,3,10], [9,3,6,2,11,9,3,1,2,8],
                   [21,9,4,9,3,2,1,2,9], [16,6,10,3,10,9,2,1,2], [25,10,3,2,3,4,2,6,2,2,3,1], [14,14,2,3,4,2,4,3,7], [8,9,5,9,2,3,4,7],
                   [1,8,1,6,5,2,8], [1,1,4,1,1,6,2,1,3,2,4], [1,2,1,3,1,1,1,3,2,1,4,1,4], [2,1,2,1,3,1,1,1,3,2,1,6,4], [3,7,1,5,1,3,2,1,4,2,2,2,2,4],
                   [4,6,3,3,1,3,2,1,1,2,5,2,2,4], [1,2,4,2,1,4,3,1,1,2,3,4,4], [1,1,4,1,4,3,1,1,1,3,2,5], [1,1,1,1,4,1,1,1,4,2,1,2,5,1,5], [1,1,3,2,3,1,2,2,4,2,1,1,4,2,4],
                   [3,2,1,4,2,4,1,3,2,2,1,2,4,1,1,3,1], [2,1,1,3,1,4,4,1,2,2,2,4,2,1,3,1,1], [3,3,1,6,2,10,4,1,4,2,1,5,2,2], [8,3,2,2,4,2,1,4,7,2,1,4,3,2], [2,1,1,1,3,8,1,9,11,3],
                   [1,1,2,1,2,1,4,1,2,1,1,6,2,6,2,9,3], [3,6,3,2,1,3,3,3,4,2,3,17,1], [3,9,2,4,2,7,6,24], [2,12,16,31], [6,12,21,20]]
#array that describes the columns of the matrix, left to right
values_columns_arr = [[1,1,2,1,2,2,1,1,4,4,2], [2,3,1,3,2,4,1,8,2,3,1,1,1], [2,3,2,2,3,4,2,2,9,3,1,1,4], [52,2,2,1,3], [4,6,4,1,1,1,1,19,3,3,1],
                   [2,1,2,1,2,1,1,1,2,2,3,7,2,1,1], [2,2,1,2,1,4,2,1,1,1,7,1,1,7,1], [2,1,2,1,2,1,1,4,16,3,2,4,1], [5,3,2,1,2,30,3,2,4], [31,4,3,2,1,4,2,2,1,5],
                   [2,2,4,3,34,3,1,2,3], [2,2,3,3,1,4,3,2,2,1,4,6,6,1,3], [1,2,3,2,4,2,2,3,1,3,6,3,10], [1,3,1,2,3,2,1,1,3,5,4,4,5], [2,9,5,2,1,4,2,5,2,7,4],
                   [4,2,1,6,8,3,2,5,14,3], [6,1,6,2,6,3,5,1,4,3,4], [5,1,6,1,2,2,1,1,4,1,2,4,1,2,2,1,2,2], [5,7,1,2,1,1,2,1,6,2,1,1,1,2], [4,6,1,1,1,1,5,2,2,2,1,1],
                   [11,7,1,1,3,2,1,1], [6,1,3,6,1,1,3,2,2,2], [2,1,5,2,3,2,1,5], [1,2,3,5,1,2,8,2,3], [1,2,5,20,2,4,1,2,1,2],
                   [1,3,22,2,4,2,2,2], [2,2,2,4,16,5,2,1,1,3], [4,3,4,17,8,7,6], [5,4,2,19,8,5,4], [7,4,2,19,5,4,9],
                   [5,4,28,5,3,2], [8,2,3,3,1,3,2,18,6,2], [5,4,1,1,22,4], [5,3,1,2,25,4], [4,2,2,2,2,13,6,2],
                   [5,12,14,1,3,2], [4,3,7,10,5,14], [9,2,1,6,15,1,11,4,1], [1,2,6,3,1,13,11,4,5,3], [3,6,5,1,3,4,14,10],
                   [6,3,2,2,12,5,3,4], [5,4,2,3,9,3,3,3,4], [4,1,2,4,3,7,1,4], [3,1,3,2,1,11,2,1,2,2], [4,4,3,7,8,2],
                   [5,15,2,3], [4,13,4,3], [1,2,7,3,10], [2,2,5,5,3,7], [2,3,13,8,3],
                   [1,2,10,16], [2,4,4,10,12,2], [3,9,4,16], [3,10,5,2,3], [5,13,3,6],
                   [5,6,16,9], [1,5,13,3,6,1,4], [1,6,10,4,1,1,4,1,4], [1,4,3,2,12,2,6], [2,1,2,2,10,7,5,9],
                   [2,1,3,8,4,3,1,3,6], [4,4,16,3,20], [4,2,21,2,21], [3,3,2,19,21], [5,2,12,10,7],
                   [4,2,1,1,6,6,2,5], [5,3,4,5,1,6], [5,3,3,9,2,3], [3,3,2,1,10,1,2,3], [3,2,5,6,3,1,2,1,3],
                   [2,2,10,1,2,1,1,4], [1,10,1,8,1,2,1], [1,4,1,1,10,1,2,2], [1,1,1,2,1,14,2,2,1], [5,1,23,2,2,1],
                   [5,2,18,3,1], [2,1,1,14,1,1], [3,2,4,12,1], [1,3,5,1,9,1,1], [6,1,10,1,1]]

"""
