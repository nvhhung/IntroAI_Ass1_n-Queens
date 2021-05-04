import random as rd
import time


class SolveNQ:
    def __init__(self, nrange):
        self.range = nrange

    def byDFS(self, board):
        # Use recursive and for loop with a stack to implement Depth First Search, initalize board is []
        # With each row check all position of the next row. With the first satified position continue check all next row's position
        if (len(board) >= self.range):
            return True
        for i in range(self.range):
            # Put to stack the next row's position
            board.append(i)
            if (self.notConflict(board)):
                # If the next position is acceptable, pass this board to recursive function to check the next row
                if (self.byDFS(board) == True):
                    # If all next rows is satified, then return
                    return True
            # If next position is not satified, then pop it from stack
            board.pop()
        # There's no position is satified from the next row, backtrack (return false to pop this last element and go to the next value of the for loop)
        return False

    def byBFS(self, queue):
        # Use a queue saving states of the board, initalize queue is [[]] when the first board is empty
        # While the queue is not empty pop the first element and check if the board is final state, if not, put all the next states from poped board to the queue.
        while queue != []:
            board = queue.pop(0)
            # If last queen is acceptable, then check the lenght of the board.
            if (self.notConflict(board)):
                # If the board have enough row of queens, then return the board. This board is the final state.
                if (len(board) == self.range):
                    return board
                # Else append to the queue all possibly next state from the this board.
                for i in range(self.range):
                    nboard = board.copy()
                    nboard.append(i)
                    queue.append(nboard)
        # If queue is empty, there is no solution found
        return []

    # Use Hill Climbing algorithm
    def byHeur(self):
        if self.range <= 3 & self.range != 1:
            return[]
        # Initalize a random board with one queen a row, each queen is at a distinct column.
        initBoard = rd.sample(range(0, self.range), self.range)
        # If board is final state then return board.
        while (not self.finalState(initBoard)):
            # Mark that the board hasn't changed
            boardChanged = 0
            # Check all rows of the board
            for row in range(self.range):
                if (boardChanged == 1):
                    break
                # Check the conflict value of this row's position
                conflict = self.conflictValue(row, initBoard, initBoard[row])
                # If not conflict the go to the next row.
                if (conflict == 0):
                    continue
                # Else check the conflict value of all others position in this row
                for col in range(self.range):
                    if (col == initBoard[row]):
                        continue
                    nextConflict = self.conflictValue(row, initBoard, col)
                    # If there's one position has less conflict, then set it as new position of this row. Mark the board is changed
                    if (nextConflict < conflict):
                        initBoard[row] = col
                        conflict = nextConflict
                        boardChanged = 1
            # If after check all the rows and the board hasn't changed, then randomly changed value of one row's position
            if (boardChanged == 0):
                initBoard[rd.randint(0, self.range-1)] = rd.randint(
                    0, self.range-1)
        return initBoard

    def notConflict(self, board):
        # Use for DFS and BFS, check if the last queen's position in the board is conflict with others.
        for i in range(len(board)-1):
            lastIndex = len(board)-1
            if (abs(board[i]-board[-1]) == lastIndex - i) or board[i] == board[-1]:
                return False
        return True

    def conflictValue(self, queenIndex, board, checkValue):
        # Use for Heuristic search, return the times a queens see the others
        numOfConflict = 0
        for i in range(self.range):
            if (i == queenIndex):
                continue
            if (abs(board[i]-checkValue) == abs(i-queenIndex)):
                numOfConflict += 1
            if (board[i] == checkValue):
                numOfConflict += 1
        return numOfConflict

    def finalState(self, board):
        # Check if the board is at final state
        for i in range(self.range):
            for j in range(self.range):
                if (i == j):
                    continue
                if (abs(j-i) == abs(board[j]-board[i])) | (board[i] == board[j]):
                    return False
        return True

    def solve(self):
        case = int(
            input("Choose search algorithm:\n1.DFS\n2.BFS\n3.Heuristics\n"))
        start_time = time.time()
        if case == 1:
            print("Using DFS...", end=' ')
            board = []
            result = self.byDFS(board)
            result = board
        elif case == 2:
            print("Using BFS...", end=' ')
            board = [[]]
            result = self.byBFS(board)
        elif case == 3:
            print("Using Heuristics...", end=' ')
            result = self.byHeur()
        else:
            raise(SyntaxError)
        end_time = time.time()
        print("DONE")
        print("--- %s seconds ---" % (end_time - start_time))
        return result


def printBoard(board):
    print("\n")
    a = 0 if board == [] else max(board)+1
    for i in board:
        print("-"*(a*4+1))
        print("|"+"   |"*i+" Q |"+"   |"*(a-i-1))
    print("-"*(a*4+1))


if __name__ == "__main__":
    a = SolveNQ(int(input("Enter n:")))
    result = a.solve()
    print(result)
    # printBoard(result)
