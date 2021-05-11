import data

def move_to_left(values, content):
    
    # stick values to the left
    curr_idx = 0
    left = [data.state.Unknown for i in range(len(content))]
    for i in range(len(values)):
        left = fill_curr_value(left, curr_idx, values[i])
        curr_idx += values[i] + 1
    left = convert_unknown_to_white(left)
    
    not_cont = get_filter(content)
    not_con = not_cont(left)

    while(not not_con):  # left contradicts the content
        con_idx = find_first_con(left, content)
        if left[con_idx] == data.state.Black:  # and content[con_idx] == data.state.White
            beg_mov_idx = con_idx
            while(beg_mov_idx != 0 and left[beg_mov_idx - 1] == data.state.Black):
                beg_mov_idx = beg_mov_idx - 1

            move_size = 1 + con_idx - beg_mov_idx
            left = move(left, beg_mov_idx, move_size)

        elif left[con_idx] == data.state.White:
            beg_mov_idx = con_idx
            while(left[beg_mov_idx] == data.state.White):
                beg_mov_idx = beg_mov_idx - 1
            end_black_val = beg_mov_idx
            while(beg_mov_idx != 0 and left[beg_mov_idx - 1] == data.state.Black):
                beg_mov_idx = beg_mov_idx - 1

            move_size = con_idx - end_black_val
            left = move(left, beg_mov_idx, move_size)
        
        not_con = not_cont(left)
    return left

def move(line, beg_idx, move_size):
    # find end value idx
    end_idx = beg_idx
    while(line[end_idx + 1] == data.state.Black):  # to add 'end_idx != len(line)-1 and ' ?
        end_idx += 1

    # check if move possible
    if end_idx + 1 + move_size > len(line):
        return -1

    new_line = line[:]
    
    # make sure there is space for the move
    if data.state.Black in line[end_idx + 1:end_idx+1 + move_size + 1]:  #  the second +1 for the white after:
        #move the rest
        next_beg_idx = find_first_state(line, data.state.Black, end_idx+1)  #  TODO: should we check backwards?
        next_move_size = end_idx+1 + move_size + 1 - next_beg_idx
        new_line = move(line, next_beg_idx, next_move_size)
        # if next moves impossible- this one too
        if new_line == -1:
            return -1

    # after we cleared space, we move
    for i in range(beg_idx, end_idx + 1):
        new_line[i] = data.state.White
    for i in range(beg_idx+move_size, end_idx+move_size+1):
        new_line[i] = data.state.Black
    return new_line
    
def find_first_con(line1, line2):
    for i in range(len(line1)):
        if line1[i] == data.state.Black and line2[i] == data.state.White or line1[i] == data.state.White and line2[i] == data.state.Black:
            return i
    return -1

def merge_2_lines(line1, line2):
    merged = [data.state.Unknown for i in range(len(line1))]
    for i in range(len(merged)):
        if line1[i] != data.state.Unknown:
            merged[i] = line1[i]
        elif line2[i] != data.state.Unknown:
            merged[i] = line2[i]
    return merged

def fill_curr_value(prev_content, first_index, curr_to_add):
    new_content = prev_content[:]
    for i in range(len(prev_content)):
        if i < first_index and prev_content[i] == data.state.Unknown:  # fill with whites until the first black
            new_content[i] = data.state.White
        elif first_index <= i and i < first_index + curr_to_add:  # the panels that should be black because of this sequence
            new_content[i] = data.state.Black
    if first_index + curr_to_add < len(prev_content):  # there are panels after this sequence- the next should be white
        new_content[first_index + curr_to_add] = data.state.White
    return new_content

def get_filter(line_content):
    def not_con(x): 
        for i in range(0, len(x)): 
            if (x[i] == data.state.Black and line_content[i] == data.state.White
                    or x[i] == data.state.White and line_content[i] == data.state.Black):
                return False
        return True
    return not_con

def find_first_state(line, stat, from_idx = 0):
    for i in range(from_idx, len(line)):
        if line[i] == stat:
            return i
    return -1  # Unknown not found

def convert_unknown_to_white(line):
    ret = line[:]  # in order not to change the source (line)
    for i in range(len(line)):
        if ret[i] == data.state.Unknown:
            ret[i] = data.state.White
    return ret

def has_diff(line1, line2):
    if len(line1) != len(line2):
        return True
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            return True
    return False

def get_intersection(perms):
    if perms == [] or perms[0] in data.state:
        return perms

    ret = [data.state.Unknown for x in range(len(perms[0]))]
    for i in range(len(perms[0])):

        col = [row[i] for row in perms]
        if data.state.Black in col and not data.state.White in col and not data.state.Unknown in col:
            ret[i] = data.state.Black
        elif not data.state.Black in col and data.state.White in col and not data.state.Unknown in col:
            ret[i] = data.state.White
        # else stays Unknown
        """
        curr = perms[0][i]
        same = True
        for perm in perms:
            if perm[i] != curr:
                same = False
        if same:
            ret[i] = curr
        """
    return ret

def nonogram_was_solved():
    for line in data.Matrix:
        if data.state.Unknown in line:
            return False
    return True


# ----- select right order -----

def get_potential_filter(direction):
    def get_potential(idx):
        
        if direction == "rows":
            content = data.Matrix[idx]
            line = data.values_rows_arr[idx]
        else:
            content = [line[idx] for line in data.Matrix][:]
            line = data.values_columns_arr[idx]

        if data.state.White in content or data.state.Black in content:  # meanwhile, I don't have idea how to calc line with content
            return True
    
        biggest_value = max(line)
        min_content_size = sum(line) + len(line) - 1
        max_shift = len(content) - min_content_size 
        if max_shift >= biggest_value:
            return False
        return True
    return get_potential

def get_best_order(direction):
    if direction == 'rows':
        to_sort = data.values_rows_arr[:]
    else:
        to_sort = data.values_columns_arr[:]
    priority = [[i,0] for i in range(len(to_sort))]
    
    line_size = data.COLUMNS if direction == 'rows' else data.ROWS

    for i in range(len(to_sort)):  # filling priorities, rules of thumb
        priority[i][1] += max(to_sort[i]) * 2  # it's good to have a big number
        priority[i][1] -= line_size - (sum(to_sort[i]) + len(to_sort[i]) - 1)  # if the values are very close to the line size - it's better
        priority[i][1] -= len(to_sort[i]) # better computentially to have few values
        # TODO: take in account how much content of line has values different from Unknown - how much it is full?
        # TODO: prioritize lines that are in the edges

    return list(map(lambda x: x[0], sorted(priority, key = lambda x: x[1], reverse = True)))
 
