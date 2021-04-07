import time
import left_right
import perm
import tools
import data


def main():

    has_improvement = True

    begin = time.time()
    while not tools.nonogram_was_solved():
        #has_improvement = False

        ic = 0
        while (has_improvement):
            has_improvement = left_right.iteration()  # without recursion
            #print("after ", ic, "'th iteration:")
            #data.print_nonogram()
            ic+=1
            a = data.Matrix[:]

        has_improvement = False
        for i in range(data.ROWS):
            data.ROWS_HAS_CHANGE[i] = True  # is there a difference from the previous round
            data.COLUMNS_HAS_CHANGE[i] = True  # --"--

        if tools.nonogram_was_solved():
            break

        #print("after basic iteration (without recursion): ")
        #print_nonogram()
        ic = 0
        while not has_improvement: #  (has_improvement or (True in ROWS_HAS_CHANGE) or (True in COLUMNS_HAS_CHANGE)):
            rec_1_begin = time.time()
            has_improvement = perm.iteration()
            rec_1_end = time.time()
            """
            print("after ", ic, "'th iteration:")
            print("iteration ",ic , " took " + str(round(rec_1_end - rec_1_begin, 3)))
            print("has_improvement: ", has_improvement)
            #print("True in ROWS_HAS_CHANGE: ", (True in ROWS_HAS_CHANGE))
            #print("True in COLUMNS_HAS_CHANGE: ", (True in COLUMNS_HAS_CHANGE))
            print("ROWS_HAS_CHANGE: ", data.ROWS_HAS_CHANGE)
            print("COLUMNS_HAS_CHANGE: ", data.COLUMNS_HAS_CHANGE)
            data.print_nonogram()
            """
            ic+=1

    end = time.time()

    #check if the nonogram was finished:
    if (tools.nonogram_was_solved()):
        print("finished successfully!")
        data.print_nonogram()
        data.save_res_to_file()
    else:
        print("not succeeded finishing nonogram")
        data.print_nonogram()
    
    print("enters to rec: " + str(perm.REC_COUNTER[0]))
    print("total time took is: " + str(round(end - begin, 3)))



if __name__ == "__main__":
    main()


# TODO: using pyInstaller to convert to .exe
# The main issue to convert it to a single file
