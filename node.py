from problem import *
import copy

class Node:
    # initialize the node with it's parameters
    def __init__(self, problem, board, blank, cost, parent, heuristic):
        self.problem = problem
        self.board = board
        self.blank = blank
        self.cost = cost
        self.parent = parent
        self.heuristic = heuristic

    # override less than function so that priorityqueue can compare which nodes are best
    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
    
    # override equal to function so that priorityqueue can compare which nodes are best
    def __eq__(self, other):
        return (self.cost + self.heuristic) == (other.cost + other.heuristic)
    
    # override copy function so that you can make copies of node that don't affect the original
    def __copy__(self):
        return type(self)(self.problem, self.board, self.blank, self.cost, self.parent, self.heuristic)
    
    # creates a tuple of the current board's position so that lists can check if the position has already been calculated before
    def __hash__(self):
        order = list()
        for items in self.board:
            for i in range(self.problem.getSize()):
                order.append(items[i])
        return hash(tuple(order))

    # returns the value of the board at specified position
    def getPos(self, x, y):
        return self.board[x][y]
    
    # print the current board 
    def printBoard(self):
        for i in range(self.problem.getSize()):
            for j in range(self.problem.getSize()):
                print(self.getPos(i, j), end=' ')
            print('')

    def print_path(self):
        path = []
        node = self
        while node:
            path.append(node)
            node = node.parent
        path.reverse()
        for p in path:
            print("The best state to expand with g(n) = {} and h(n)= {} is:".format(p.cost, p.heuristic))
            for i in range(p.problem.getSize()):
                print(p.board[i])
            print()
    
    # swap the value at the coord with the current blank position
    def swap(self, coord):
        self.board[self.blank.x][self.blank.y], self.board[coord.x][coord.y] = self.board[coord.x][coord.y], self.board[self.blank.x][self.blank.y]
        self.blank = Coord(coord.x, coord.y)
        
        return self

    # check if the current board is the goal state
    def isGoal(self):
        for i in range(self.problem.getSize()):
            for j in range(self.problem.getSize()):
                if self.board[i][j] != self.problem.goal[i][j]:
                    return False
        return True
    
    # get all the possible positions that the blank position can swap with
    def getBlankNeighbors(self):
        neighbors = []
        blankX = copy.deepcopy(self.blank.x)
        blankY = copy.deepcopy(self.blank.y)

        if blankX > 0: neighbors.append(Coord(blankX - 1, blankY))
        if blankX < self.problem.getSize() - 1: neighbors.append(Coord(blankX + 1, blankY))
        if blankY > 0: neighbors.append(Coord(blankX, blankY - 1))
        if blankY < self.problem.getSize() - 1: neighbors.append(Coord(blankX, blankY + 1))

        return neighbors