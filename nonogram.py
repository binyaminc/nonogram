

from enum import Enum
class state(Enum):
    Black = 1
    Unknown = 0
    White = -1
    
    
# this example creates אייל

ROWS = 15
COLUMNS = 15
Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]


#array that describes the rows of the matrix, up to down
values_rows_arr = [[2,2,2,1], [2,2,1,1,2,1], [4,1,1,2,1], [5,5], [2,5],[7], [1,1,5], [11], [12], [13],[8,5], [1,3,5], [5,5], [3,6], [6]]
#array that describes the columns of the matrix, left to right
values_columns_arr = [[2], [3,3], [2,2,2], [4,6], [5,7],[2,7], [3,1,4], [7], [2,4], [2,6,2],[12], [15], [4,10], [1,9], [4,8]]



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
        tmp_has_imp = update_1_row(values_rows_arr[i], i)
        if tmp_has_imp: 
            has_improvement = True

    #print("after rows iteration:")
    #print_nonogram()  # to debug purposes

    for i in range(0, COLUMNS):
        tmp_has_imp = update_1_column(values_columns_arr[i], i)
        if tmp_has_imp: 
            has_improvement = True
    
    #print("after columns iteration:")
    #print_nonogram()

    return has_improvement

def update_1_row(row_values, row_idx):
    # get all the possible permutations
    unknown_row = [state.Unknown for x in range(COLUMNS)]
    perms = rec_get_perms(unknown_row, row_values)  #  meanwhile_content starts "empty"
    
    # get valid permutations according to the current content of the matrix
    row_content = Matrix[row_idx][:]  # [:] to have a shallow copy
    con_filter = get_filter(row_content)  # contradiction filter - to delete all those who contradict the currently known values (row_content)
    valid_perms = list(filter(con_filter, perms))
    
    #find the 'agreed' values and update the matrix
    intersection = get_intersection(valid_perms)
    Matrix[row_idx] = intersection
    
    # return whether there was an improvement
    has_improvement = False
    if has_diff(row_content, intersection):
        has_improvement = True
    return has_improvement


def update_1_column(column_values, column_idx):
    # get all the possible permutations
    unknown_column = [state.Unknown for x in range(ROWS)]
    perms = rec_get_perms(unknown_column, column_values)  #  meanwhile_content starts "empty"

    # get valid permutations according to the current content of the matrix
    column_content = [line[column_idx] for line in Matrix][:]
    con_filter = get_filter(column_content)
    valid_perms = list(filter(con_filter, perms))

    #find the 'agreed' values and update the matrix
    intersection = get_intersection(valid_perms)
    enter_column_content(intersection, column_idx)

    # return whether there was an improvement
    has_improvement = False
    if has_diff(column_content, intersection):
        has_improvement = True
    return has_improvement


def enter_column_content(intersection, column_idx):
    for i in range(len(intersection)):
        Matrix[i][column_idx] = intersection[i]

def rec_get_perms(meanwhile_content, remaining_row):
    if remaining_row != [] and (not state.Unknown in meanwhile_content):  # not a possible permutation, not all values in the line
        return []
    elif remaining_row == [] and (not state.Unknown in meanwhile_content):  # all values in the line and finished - good
        return [meanwhile_content]
    elif remaining_row == [] and state.Unknown in meanwhile_content:  # all values in the line but yet there are unknown panels
        return [convert_unknown_to_white(meanwhile_content)]
    else:
        perms = []
        curr_to_add = remaining_row[0]
        first_index = find_first_unknown(meanwhile_content)
        for i in range(first_index, len(meanwhile_content)-curr_to_add+1):  # TODO: check if an 'if option is possible' should be added
            new_content = fill_curr_value(meanwhile_content, i, curr_to_add)
            perms += rec_get_perms(new_content, remaining_row[1:])
        return perms


def fill_curr_value(prev_content, first_index, curr_to_add):
    new_content = prev_content[:]
    for i in range(len(prev_content)):
        if i < first_index and prev_content[i] == state.Unknown:  # fill with whites until the first black
            new_content[i] = state.White
        elif first_index <= i and i < first_index + curr_to_add:  # the panels that should be black because of this sequence
            new_content[i] = state.Black
    if first_index + curr_to_add < len(prev_content):  # there are panels after this sequence- the next should be white
        new_content[first_index + curr_to_add] = state.White
    return new_content


def get_filter(line_content):
    def not_con(x): 
        for i in range(0, len(x)): 
            if (x[i] == state.Black and line_content[i] == state.White
                    or x[i] == state.White and line_content[i] == state.Black):
                return False
        return True
    return not_con

def find_first_unknown(line):
    for i in range(0, len(line)):
        if line[i] == state.Unknown:
            return i
    return -1  # Unknown not found

def convert_unknown_to_white(line):
    ret = line[:]  # in order not to change the source (line)
    for i in range(len(line)):
        if ret[i] == state.Unknown:
            ret[i] = state.White
    return ret


def has_diff(line1, line2):
    if len(line1) != len(line2):
        return True
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            return True
    return False


def get_intersection(perms):
    ret = [state.Unknown for x in range(len(perms[0]))]
    for i in range(len(perms[0])):
        curr = perms[0][i]
        same = True
        for perm in perms:
            if perm[i] != curr:
                same = False
        if same:
            ret[i] = curr
    return ret

def print_nonogram():
    for line in Matrix:
        for var in line:
            if var is state.Unknown:
                print('~~', end="")  # '-' another option
            elif var is state.White:
                print('  ', end="")  # '·' another option
            elif var is state.Black:
                print('██', end="")  # %
        print("")

        
def nonogram_was_solved():
    for line in Matrix:
        for var in line:
            if var is state.Unknown:
                return False
    return True


if __name__ == "__main__":
    main()


# TODO: using pyInstaller to convert to .exe
# The main issue to convert it to a single file
"""

# this example creates אייל

ROWS = 15
COLUMNS = 15
Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]


#array that describes the rows of the matrix, up to down
values_rows_arr = [[2,2,2,1], [2,2,1,1,2,1], [4,1,1,2,1], [5,5], [2,5],[7], [1,1,5], [11], [12], [13],[8,5], [1,3,5], [5,5], [3,6], [6]]
#array that describes the columns of the matrix, left to right
values_columns_arr = [[2], [3,3], [2,2,2], [4,6], [5,7],[2,7], [3,1,4], [7], [2,4], [2,6,2],[12], [15], [4,10], [1,9], [4,8]]




ROWS = 80
COLUMNS = 80
Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]

# in the middle of filling it in... 

#array that describes the rows of the matrix, up to down
values_rows_arr = [[2], [2,1,1], [1,2,3], [1,1,2,2], [1,4,1,2,1],
                   [1,2,4,1], [2,1,2,2,2,2], [3,1,2,2,1,2,1], [1,4,1,1,2,3,2], [1,2,2,2,1,2,3,2],
                   [1,3,2,3,3,1], [2,1,1,3,1,1,1,2,5], [2,2,3,3,1,4,1], [2,3,7,2,7,1], [5,1,1,2,3,3,5,1,2],
                   [2,2,3,4,6,7,1,1], [4,5,6,2,10,1,2,2], [2,2,7,6,1,7,1,2,2,3], [4,6,6,16,2,1,2,1], [2,2,1,5,9,3,2,3,2,3],
                   [3,3,9,4,4,3,2,3,1], [5,2,10,1,1,3,4,2,4,1], [3,3,5,3,4,1,1,3,4,3,5,3,1], [2,1,9,2,1,1,1,3,12,2,2], [1,2,1,7,2,3,1,3,9,2,1],
                   [2,1,3,1,3,4,1,3,4,1,2,2], [3,6,2,3,3,1,2,4,2,4,3], [3,2,3,9,2,4,8], [3,2,3,5,3,2,1,1,1,1,2], [3,2,10,2,1,2,1,1,1,1,1,2],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], []]
#array that describes the columns of the matrix, left to right
values_columns_arr = [[], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], []]


"""
