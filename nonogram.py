import time

from enum import Enum
class state(Enum):
    Black = 1
    Unknown = 0
    White = -1
   
REC_COUNTER = [0]


# this example creates אייל

ROWS = 15
COLUMNS = 15
Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]


#array that describes the rows of the matrix, up to down
values_rows_arr = [[2,2,2,1], [2,2,1,1,2,1], [4,1,1,2,1], [5,5], [2,5],[7], [1,1,5], [11], [12], [13],[8,5], [1,3,5], [5,5], [3,6], [6]]
#array that describes the columns of the matrix, left to right
values_columns_arr = [[2], [3,3], [2,2,2], [4,6], [5,7],[2,7], [3,1,4], [7], [2,4], [2,6,2],[12], [15], [4,10], [1,9], [4,8]]


ROWS_CAN_IMPROVE = [True for x in range(ROWS)]  # is there a difference from the previous round
COLUMNS_CAN_IMPROVE = [True for x in range(COLUMNS)]  # --"--

ITER_AMOUNT = min(5, ROWS)  # we want to take the ITER_AMOUNT best iterations


def main():

    has_improvement = True

    begin = time.time()
    while (has_improvement or (True in ROWS_CAN_IMPROVE) or (True in COLUMNS_CAN_IMPROVE)):
        has_improvement = solve_1_iteration()
        
        #print("has_improvement: ", has_improvement)
        #print("True in ROWS_CAN_IMPROVE: ", (True in ROWS_CAN_IMPROVE))
        #print("True in COLUMNS_CAN_IMPROVE: ", (True in COLUMNS_CAN_IMPROVE))
        #print_nonogram()
        #print("")
        

    end = time.time()

    #check if the nonogram was finished:
    if (nonogram_was_solved()):
        print("finished successfully!")
        print_nonogram()
    else:
        print("not succeeded finishing nonogram")
        print_nonogram()
    print("enters to rec: " + str(REC_COUNTER[0]))
    print("time took is: " + str(round(end - begin, 3)))
     

    
def solve_1_iteration():
    has_improvement = False

    best_order_rows = get_best_order("rows")
    best_can_impr_rows = list(filter(lambda i: ROWS_CAN_IMPROVE[i] == True, best_order_rows))  # the best rows that can be improved

    for i in best_can_impr_rows[:ITER_AMOUNT]:
        tmp_has_imp = update_1_row(values_rows_arr[i], i)
        if tmp_has_imp: 
            has_improvement = True
        #print("after " + str(i) + "'th iteration:")
        #print_nonogram()
        #print("rec times: " + str(REC_COUNTER))

    #print("after rows iteration:")
    #print_nonogram()  # to debug purposes
    
    best_order_columns = get_best_order("columns")
    best_can_impr_columns = list(filter(lambda i: COLUMNS_CAN_IMPROVE[i] == True, best_order_columns))  # the best columns that can be improved

    for i in best_can_impr_columns[:ITER_AMOUNT]:
        tmp_has_imp = update_1_column(values_columns_arr[i], i)
        if tmp_has_imp: 
            has_improvement = True
    
    #print("after columns iteration:")
    #print_nonogram()

    return has_improvement

def update_1_row(row_values, row_idx):
    # get valid permutations according to the current content of the matrix
    row_content = Matrix[row_idx][:]  # [:] to have a shallow copy
    con_filter = get_filter(row_content)  # contradiction filter - to delete all those who contradict the currently known values (row_content)
    unknown_row = [state.Unknown for x in range(COLUMNS)]
    valid_perms = rec_get_perms(unknown_row, row_values, con_filter)  #  meanwhile_content starts "empty" - Unknown
    
    #find the 'agreed' values and update the matrix
    intersection = get_intersection(valid_perms)
    Matrix[row_idx] = intersection
    
    # update COLUMNS_CAN_IMPROVE and make false in this
    ROWS_CAN_IMPROVE[row_idx] = False
    for i in range(len(row_content)):
        if (row_content[i] == state.Unknown and intersection[i] == state.Black) or (row_content[i] == state.Unknown and intersection[i] == state.White):
            COLUMNS_CAN_IMPROVE[i] = True

    # return whether there was an improvement
    has_improvement = False
    if has_diff(row_content, intersection):
        has_improvement = True
    return has_improvement


def update_1_column(column_values, column_idx):
    # get valid permutations according to the current content of the matrix
    column_content = [line[column_idx] for line in Matrix][:]
    con_filter = get_filter(column_content)
    unknown_column = [state.Unknown for x in range(ROWS)]
    valid_perms = rec_get_perms(unknown_column, column_values, con_filter)  #  meanwhile_content starts "empty"

    #find the 'agreed' values and update the matrix
    intersection = get_intersection(valid_perms)
    enter_column_content(intersection, column_idx)

    # update ROWS_CAN_IMPROVE and make false in this
    COLUMNS_CAN_IMPROVE[column_idx] = False
    for i in range(len(column_content)):
        if (column_content[i] == state.Unknown and intersection[i] == state.Black) or (column_content[i] == state.Unknown and intersection[i] == state.White):
            ROWS_CAN_IMPROVE[i] = True

    # return whether there was an improvement
    has_improvement = False
    if has_diff(column_content, intersection):
        has_improvement = True
    return has_improvement


def rec_get_perms(meanwhile_content, remaining_row, con_filter):
    REC_COUNTER[0] = REC_COUNTER[0] + 1  # to inspect the improvemet - how many times we enter this function, since this is the most time consuming function.
    
    if remaining_row != [] and (not state.Unknown in meanwhile_content):  # not a possible permutation, not all values in the line
        return []
    elif remaining_row == [] and (not state.Unknown in meanwhile_content):  # all values in the line and finished - good
        return [meanwhile_content]
    elif remaining_row == [] and state.Unknown in meanwhile_content:  # all values in the line but yet there are unknown panels
        return [convert_unknown_to_white(meanwhile_content)]
    else:
        perms = []
        curr_to_add = remaining_row[0]
        
        first_beginning_index = find_first_unknown(meanwhile_content)
        min_place_for_remaining_row = max(sum(map(lambda x: x+1, remaining_row[1:])) - 1, 0)  # add 1 to each value for the space between each two. then sub 1 to the last one without space
        last_beginning_index = len(meanwhile_content) - curr_to_add + 1 - min_place_for_remaining_row # TODO: should subtract 1 because indexing starts from 0?
        
        for i in range(first_beginning_index, last_beginning_index):
            new_content = fill_curr_value(meanwhile_content, i, curr_to_add)
            if con_filter(new_content):  # the new content doesn't contradict the already-existant content
                perms += list(filter(con_filter, rec_get_perms(new_content, remaining_row[1:], con_filter)))
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


def enter_column_content(intersection, column_idx):
    for i in range(len(intersection)):
        Matrix[i][column_idx] = intersection[i]


def get_best_order(direction):
    if direction == 'rows':
        to_sort = values_rows_arr[:]
    else:
        to_sort = values_columns_arr[:]
    priority = [[i,0] for i in range(len(to_sort))]
    
    for i in range(len(to_sort)):  # filling priorities, rules of thumb
       priority[i][1] += max(to_sort[i]) * 2  # it's good to have a big number
       priority[i][1] -= COLUMNS - (sum(to_sort[i]) + len(to_sort[i]) - 1)  # if the values are very close to the line size - it's better
       priority[i][1] -= len(to_sort[i])  # better computentially to have few values
       # TODO: take in account how much content of line has values different from Unknown - how much it is full?
       # TODO: prioritize lines that are in the edges

    return list(map(lambda x: x[0], sorted(priority, key = lambda x: x[1], reverse = True)))


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
# some basic shape

ROWS = 6
COLUMNS = 6
Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]

#array that describes the rows of the matrix, up to down
values_rows_arr = [[2,1],[1,3],[1,2],[3],[4],[1]]
#array that describes the columns of the matrix, left to right
values_columns_arr = [[1],[5],[2],[5],[2,1],[2]]


# fish?

ROWS = 10
COLUMNS = 10
Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]

#array that describes the rows of the matrix, up to down
values_rows_arr = [[1,1], [2,2], [1,6], [1,3,1], [1,4,1],[1,7], [8], [4,1], [3,2], [4]]
#array that describes the columns of the matrix, left to right
values_columns_arr = [[3], [3], [2], [5], [8],[6,2], [7,1], [1,2,1], [2,2,1], [6,2]]


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
values_columns_arr = [[], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], [],
                   [], [], [], [], []]


"""


"""
#these functions are with the contradiction-checking outside of the rec_get_perms

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


def rec_get_perms(meanwhile_content, remaining_row):
    REC_COUNTER[0] = REC_COUNTER[0] + 1  # to inspect the improvemet - how many times we enter this function, since this is the most time consuming function.
    
    if remaining_row != [] and (not state.Unknown in meanwhile_content):  # not a possible permutation, not all values in the line
        return []
    elif remaining_row == [] and (not state.Unknown in meanwhile_content):  # all values in the line and finished - good
        return [meanwhile_content]
    elif remaining_row == [] and state.Unknown in meanwhile_content:  # all values in the line but yet there are unknown panels
        return [convert_unknown_to_white(meanwhile_content)]
    else:
        perms = []
        curr_to_add = remaining_row[0]
        
        first_beginning_index = find_first_unknown(meanwhile_content)
        #last_beginning_index = len(meanwhile_content) - curr_to_add + 1
        min_place_remaining_row = max(sum(map(lambda x: x+1, remaining_row[1:])) - 1, 0)  # add 1 to each value for the space between each two. then sub 1 to the last one without space
        last_beginning_index = len(meanwhile_content) - curr_to_add + 1 - min_place_remaining_row
        
        for i in range(first_beginning_index, last_beginning_index):
            new_content = fill_curr_value(meanwhile_content, i, curr_to_add)
            perms += rec_get_perms(new_content, remaining_row[1:])
        return perms


"""