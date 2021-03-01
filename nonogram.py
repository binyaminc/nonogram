

from enum import Enum
class state(Enum):
    Black = 1
    Unknown = 0
    White = -1
    

ROWS = 6
COLUMNS = 6
Matrix = [[state.Unknown for x in range(COLUMNS)] for y in range(ROWS)]

Matrix[0][3] = state.White
Matrix[0][4] = state.White
Matrix[2][4] = state.Black
Matrix[2][5] = state.Black


def main():

    

    #array that describes the rows of the matrix, up to down
    rowsArr = ["2 1", "1 3", "1 2", "3", "4", "1"]
    #array that describes the columns of the matrix, left to right
    columnsArr = ["1", "5", "2", "5", "2 1", "2"]

    printNonogram(Matrix)
    solve1Iteration(Matrix, rowsArr, columnsArr)
    printNonogram(Matrix)

    hasImprovement = True

    while hasImprovement:
        hasImprovement = solve1Iteration(Matrix, rowsArr, columnsArr)

    #check if the nonogram was finished:
    if (nonogramWasSolved(Matrix)):
        print("finished successfully!")
        printNonogram(Matrix)
    else:
        print("not succeeded finishing nonogram")
        printNonogram(Matrix)
        
    
def solve1Iteration(Matrix, rowsArr, columnsArr):
    # Matrix[5][5] = state.White
    hasImprovement = False

    for i in range(0, ROWS):
        tmp_HasImp = update1Row(Matrix, rowsArr[i])
        if tmp_HasImp: 
            hasImprovement = True

    for i in range(0, COLUMNS):
        tmp_HasImp = update1Column(Matrix, columnsArr[i])
        if tmp_HasImp: 
            hasImprovement = True

    return hasImprovement

def update1Row(Matrix, row):
    x=1

def update1Column(Matrix, column):
    x=1

def printNonogram(Matrix):
    for line in Matrix:
        for var in line:
            if var is state.Unknown:
                print('-', end=" ")
            elif var is state.White:
                print('~', end=" ")
            elif var is state.Black:
                print('%', end=" ")
        print("")


def nonogramWasSolved(Matrix):
    for line in Matrix:
        for var in line:
            if var is state.Unknown:
                return False
    return True

#TODO: check if the matrix changes in function's call

if __name__ == "__main__":
    main()
