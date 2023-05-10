import queue
import array

# object for x and y pair
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# object for the puzzle's problem (contains the inital and goal state, size of puzzle, and algorithm used to search it)
class Problem:
    # initialize the object
    def __init__(self, size, initial, goal, search):
        self.size = size
        self.initial = initial
        self.goal = goal
        self.search = ""

    # get the position of the blank node
    def getBlank(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.initial[i][j] == 0:
                     return Coord(i, j)

    # print the board's initial state
    def printInitial(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.initial[i][j], end=' ')
            print('')

    # get the size of the puzzle (dimension of the puzzle e.g 8 puzzle is 3x3 so returns 3)
    def getSize(self):
        return self.size