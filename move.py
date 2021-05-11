import tools
import data


def iteration():
    
    has_improvement = False
    
    # update rows
    for i in range(data.ROWS):
        row_content = data.get_row(i)
        updated = line_update(data.values_rows_arr[i], row_content)
        data.set_row(updated, i)
    
        data.ROWS_HAS_CHANGE[i] = False
        for idx in range(len(row_content)):
            if (row_content[idx] == data.state.Unknown and updated[idx] == data.state.Black) or (row_content[idx] == data.state.Unknown and updated[idx] == data.state.White):
                data.COLUMNS_HAS_CHANGE[idx] = True
                has_improvement = True

    # update columns
    for i in range(data.COLUMNS): 
        column_content = data.get_column(i)
        updated = line_update(data.values_columns_arr[i], column_content)
        data.set_column(updated, i)
        
        data.COLUMNS_HAS_CHANGE[i] = False
        for idx in range(len(column_content)):
            if (column_content[idx] == data.state.Unknown and updated[idx] == data.state.Black) or (column_content[idx] == data.state.Unknown and updated[idx] == data.state.White):
                data.ROWS_HAS_CHANGE[idx] = True
                has_improvement = True
    
    return has_improvement


def line_update(values, content):
    
    left = tools.move_to_left(values, content)

    
