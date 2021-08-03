import tools
import data



def iteration():
    
    has_improvement = False

    # update rows
    for i in range(data.ROWS):
        #print("row ", i)
        row_content = data.get_row(i)
        updated = line_update(data.values_rows_arr[i], row_content)
        data.set_row(updated, i)
    
        # data.ROWS_HAS_CHANGE[i] = False
        for idx in range(len(row_content)):
            if (row_content[idx] == data.state.Unknown and updated[idx] == data.state.Black) or (row_content[idx] == data.state.Unknown and updated[idx] == data.state.White):
                data.COLUMNS_HAS_CHANGE[idx] = True
                has_improvement = True
    #print("after rows: ")
    #print_nonogram()
 
    # update columns
    for i in range(data.COLUMNS): 
        #print("column ", i)
        column_content = data.get_column(i)
        updated = line_update(data.values_columns_arr[i], column_content)
        data.set_column(updated, i)
        #print_nonogram()
        
        #data.COLUMNS_HAS_CHANGE[i] = False
        for idx in range(len(column_content)):
            if (column_content[idx] == data.state.Unknown and updated[idx] == data.state.Black) or (column_content[idx] == data.state.Unknown and updated[idx] == data.state.White):
                data.ROWS_HAS_CHANGE[idx] = True
                has_improvement = True
    #print("after columns: ")
    #print_nonogram()

    return has_improvement

def line_update(values, content):

    left = tools.move_to_left(values, content)
    
    rev_val = list(reversed(values))
    rev_con = list(reversed(content)) 
    rev_right = tools.move_to_left(rev_val, rev_con)
    right = list(reversed(rev_right))

    val_begin_end_l_r = [[0,0,0,0] for i in range(len(values))]  # [0] = begin left
                                                                      # [1] = end left
                                                                      # [2] = begin right
                                                                      # [3] = end right
    
    # loop over left to find begin-end for each val
    begin_end_l = get_begin_end(values, left)
    
    # loop over right to find begin-end for each val
    begin_end_r = get_begin_end(values, right)

    # enter to val_begin_end_l_r
    for i in range(len(values)):
        val_begin_end_l_r[i][0] = begin_end_l[i][0]
        val_begin_end_l_r[i][1] = begin_end_l[i][1]
        val_begin_end_l_r[i][2] = begin_end_r[i][0]
        val_begin_end_l_r[i][3] = begin_end_r[i][1]
    
    # find must-be blacks
    updated = content[:]  # [data.state.Unknown for i in range(len(content))]
    for val in val_begin_end_l_r:
        if val[2] <= val[1]:  # begin right <= end left
            for i in range(val[2], val[1] + 1): 
                updated[i] = data.state.Black

    # find panels that no one can reach, and mark as white
    can_reach = [False for i in range(len(content))]  
    for val in val_begin_end_l_r:
        for i in range(val[0], val[3] + 1): 
                can_reach[i] = True
    for i in range(len(content)):
        if not can_reach[i]:
            updated[i] = data.state.White
    
    return updated

def get_begin_end(values, content):
    beg_end = [[0,0] for i in range(len(values))]
    con_idx = 0
    val_idx = 0
    all_in = False
    while(not all_in):
        if content[con_idx] == data.state.White:
            con_idx += 1
        else:
            beg_end[val_idx][0] = con_idx  # begin
            val_len = values[val_idx]
            beg_end[val_idx][1] = con_idx + val_len - 1 # end
            
            con_idx += val_len
            val_idx += 1
            if val_idx == len(values):
                all_in = True
    return beg_end
 