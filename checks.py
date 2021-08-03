import time
import left_right
import perm
import tools
import data
import move


def main():
    
    print("Welcome to my nonogram solver program!")
    print("Use existant nonogram or type in new nonogram?\nexsistant: 'y', new: 'n', result from file: 'f'")
    choise = input()
    while choise not in ['y','n','f']:
        print("enter 'y', 'n' or 'f'")
        choise = input()

    if choise == 'n':
        data.get_user_data()
    elif choise == 'f':
        print("enter result file path: ")
        path = input()
        data.read_res_from_file(path)
        

    has_improvement = True

    while has_improvement: #  (has_improvement or (True in ROWS_HAS_CHANGE) or (True in COLUMNS_HAS_CHANGE)):
        has_improvement = move.iteration()
        print("\n\n\nafter iteration:\n")
        data.print_nonogram()
            
    #check if the nonogram was finished:
    if (tools.nonogram_was_solved()):
        print("finished successfully!")
        data.print_nonogram()
        data.save_res_to_file()
    else:
        print("not succeeded finishing nonogram")
        data.print_nonogram()
    
    


if __name__ == "__main__":
    main()


# TODO: using pyInstaller to convert to .exe
# The main issue to convert it to a single file



