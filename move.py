import tools
import data

"""
principle: pushing the left-most moveable seq the minimum distance.
"""

def iteration():
    
    has_improvement = False
    
    # update rows
    for i in range(data.ROWS):
        if i == 10:
            x=0
        row_content = data.get_row(i)
        updated = line_update(data.values_rows_arr[i], row_content)
        data.set_row(updated, i)
        #print("update of ", data.values_rows_arr[i])
        #data.print_nonogram()

        data.ROWS_HAS_CHANGE[i] = False
        for idx in range(len(row_content)):
            if (row_content[idx] == data.state.Unknown and updated[idx] == data.state.Black) or (row_content[idx] == data.state.Unknown and updated[idx] == data.state.White):
                data.COLUMNS_HAS_CHANGE[idx] = True
                has_improvement = True

    # update columns
    for i in range(data.COLUMNS): 
        column_content = data.get_column(i)
        if i == 18: #the second iteration locates '5' in wrong place. to inspect
            x=0
        updated = line_update(data.values_columns_arr[i], column_content)
        data.set_column(updated, i)
        #print("update of ", data.values_columns_arr[i])
        #data.print_nonogram()

        data.COLUMNS_HAS_CHANGE[i] = False
        for idx in range(len(column_content)):
            if (column_content[idx] == data.state.Unknown and updated[idx] == data.state.Black) or (column_content[idx] == data.state.Unknown and updated[idx] == data.state.White):
                data.ROWS_HAS_CHANGE[idx] = True
                has_improvement = True
    
    return has_improvement


def line_update(values, content):
    
    # if line is finished - no reason to work on it
    if not data.state.Unknown in content:
        return content

    # first option - most left
    tmp_perm = tools.move_to_left(values, content)
    #tmp_perm = stay_unknown_of_orig(tmp_perm, content)

    beginning_indexes = tools.get_beginning_indexes(tmp_perm)  # given content · · █ █ · · █ will give [2, 6]

    perms = [tmp_perm]

    for i in range(len(beginning_indexes)):

        tmp_perm = tools.move_to_left(values, content) # start anew, all values to the left
        beginning_indexes = tools.get_beginning_indexes(tmp_perm)

        for j in range(i, len(beginning_indexes)):
            move_size = 1
            while beginning_indexes[j] < len(content) - move_size: # there is still possibility to move this one
            
                new_move = tools.move(tmp_perm, beginning_indexes[j], move_size)
                if new_move == -1: # this move wasn't successful
                    move_size += 1 # try bigger move
                    continue
                new_move = tools.solve_contradiction_to_right(new_move, content)
                if new_move == -1: # this move wasn't successful
                    move_size += 1 # try bigger move
                else:
                    tmp_perm = new_move
                    move_size = 1
                    perms += [new_move]
                    beginning_indexes = tools.get_beginning_indexes(new_move)

    return tools.get_intersection(perms)

