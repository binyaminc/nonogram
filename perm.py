import tools
import data

REC_COUNTER = [0]
ITER_AMOUNT = min(5, data.ROWS)  # we want to take the ITER_AMOUNT best iterations

def iteration():
    has_improvement = False

    # get best rows to work on
    best_order_rows = tools.get_best_order("rows")
    best_has_change_rows = list(filter(lambda i: data.ROWS_HAS_CHANGE[i] == True, best_order_rows))  # the best rows that changes from last time
    get_potential = tools.get_potential_filter("rows")
    best_has_change_potential_rows = list(filter(get_potential, best_has_change_rows))  # the rows that will make result

    print("rows that I work on:", best_has_change_potential_rows[:ITER_AMOUNT])
    for i in best_has_change_potential_rows[:ITER_AMOUNT]:  
        #print("calc " + str(i) + "'th row: " + str(values_rows_arr[i]))
        tmp_has_imp = update_1_row(data.values_rows_arr[i], i)
        if tmp_has_imp: 
            has_improvement = True
        #print("after " + str(i) + "'th row:")
        #print_nonogram()
        #print("rec times: " + str(REC_COUNTER))

    #print("after rows iteration:")
    #print_nonogram()  # to debug purposes
    

    # get best columns to work on
    best_order_columns = tools.get_best_order("columns")
    best_has_change_columns = list(filter(lambda i: data.COLUMNS_HAS_CHANGE[i] == True, best_order_columns))  # the best columns that changes from last time
    get_potential = tools.get_potential_filter("columns")
    best_has_change_potential_columns = list(filter(get_potential, best_has_change_columns))  # the columns that will make result
    
    print("columns that I work on:", best_has_change_potential_columns[:ITER_AMOUNT])
    for i in best_has_change_potential_columns[:ITER_AMOUNT]:
        #print("calc " + str(i) + "'th column: " + str(data.values_columns_arr[i]))
        tmp_has_imp = update_1_column(data.values_columns_arr[i], i)
        if tmp_has_imp: 
            has_improvement = True
        #print("after " + str(i) + "'th row:")
        #print_nonogram()
        
    #print("after columns iteration:")
    #print_nonogram()


    return has_improvement

def update_1_row(row_values, row_idx):
    # get valid permutations according to the current content of the matrix
    row_content = data.get_row(row_idx)
    con_filter = tools.get_filter(row_content)  # contradiction filter - to delete all those who contradict the currently known values (row_content)
    unknown_row = [data.state.Unknown for x in range(data.COLUMNS)]
    valid_perms = get_perms(unknown_row, row_values, con_filter)  #  meanwhile_content starts "empty" - Unknown
    
    #find the 'agreed' values and update the matrix
    intersection = tools.get_intersection(valid_perms)
    data.set_row(intersection, row_idx)

    # update COLUMNS_CAN_IMPROVE and make false in this
    data.ROWS_HAS_CHANGE[row_idx] = False
    for i in range(len(row_content)):
        if (row_content[i] == data.state.Unknown and intersection[i] == data.state.Black) or (row_content[i] == data.state.Unknown and intersection[i] == data.state.White):
            data.COLUMNS_HAS_CHANGE[i] = True

    # return whether there was an improvement
    has_improvement = False
    if tools.has_diff(row_content, intersection):
        has_improvement = True
    return has_improvement

def update_1_column(column_values, column_idx):
    
    # get valid permutations according to the current content of the matrix
    column_content = data.get_column(column_idx)
    con_filter = tools.get_filter(column_content)
    unknown_column = [data.state.Unknown for x in range(data.ROWS)]
    valid_perms = get_perms(unknown_column, column_values, con_filter)  #  meanwhile_content starts "empty"

    #find the 'agreed' values and update the matrix
    intersection = tools.get_intersection(valid_perms)
    data.set_column(intersection, column_idx)

    # update ROWS_CAN_IMPROVE and make false in this
    data.COLUMNS_HAS_CHANGE[column_idx] = False
    for i in range(len(column_content)):
        if (column_content[i] == data.state.Unknown and intersection[i] == data.state.Black) or (column_content[i] == data.state.Unknown and intersection[i] == data.state.White):
            data.ROWS_HAS_CHANGE[i] = True

    # return whether there was an improvement
    has_improvement = False
    if tools.has_diff(column_content, intersection):
        has_improvement = True
    return has_improvement

def get_perms(meanwhile_content, remaining_row, con_filter):
    REC_COUNTER[0] = REC_COUNTER[0] + 1  # to inspect the improvemet - how many times we enter this function, since this is the most time consuming function.
    
    if remaining_row != [] and (not data.state.Unknown in meanwhile_content):  # not a possible permutation, not all values in the line
        return []
    elif remaining_row == [] and (not data.state.Unknown in meanwhile_content):  # all values in the line and finished - good
        return [meanwhile_content]
    elif remaining_row == [] and data.state.Unknown in meanwhile_content:  # all values in the line but yet there are unknown panels
        return [tools.convert_unknown_to_white(meanwhile_content)]
    else:
        perms = []
        curr_to_add = remaining_row[0]
        
        first_beginning_index = tools.find_first_state(meanwhile_content, data.state.Unknown)
        min_place_for_remaining_row = max(sum(map(lambda x: x+1, remaining_row[1:])) - 1, 0)  # add 1 to each value for the space between each two. then sub 1 to the last one without space
        last_beginning_index = len(meanwhile_content) - curr_to_add + 1 - min_place_for_remaining_row # TODO: should subtract 1 because indexing starts from 0?
        
        for i in range(first_beginning_index, last_beginning_index):
            new_content = tools.fill_curr_value(meanwhile_content, i, curr_to_add)
            if len(remaining_row) == 1:  # another change
                new_content = tools.convert_unknown_to_white(new_content)
            if con_filter(new_content):  # the new content doesn't contradict the already-existant content
                
                deeper_perms = get_perms(new_content, remaining_row[1:], con_filter)  # --------------changes from here
                if len(deeper_perms) == 0:
                    pass
                elif len(deeper_perms) == 1 and con_filter(deeper_perms[0]):
                    perms += deeper_perms
                elif con_filter(deeper_perms):
                    perms += [deeper_perms]

        return tools.get_intersection(perms)  # --------------until here
        
                #perms += list(filter(con_filter, get_perms(new_content, remaining_row[1:], con_filter)))
        #return perms

