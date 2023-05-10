from problem import *
from node import *
import queue
import sys
import copy
import math

#Hardcoded initial and goal states
# initial = [ [1,2,3], [4,8,0], [7,6,5]]
initial = [ [1,2,3], [4,8,0], [7,6,5]]
# initial = [[5, 1, 3, 4], [2, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
goal = [ [1,2,3], [4,5,6], [7,8,0]]
# defaultSize = 3
puzzle_size= int(input("Welcome to puzzle solver. \nType the dimension of the puzzle you would like to solve (e.g. 8 puzzle dimension is 3).\n"))
if puzzle_size == 4:
    initial = [[5, 1, 3, 4], [2, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

expandedNodesCount = 0
maxQueue = 0
search = {
    "1": "Uniform",
    "2": "Misplaced",
    "3": "Euclidean"
}

def main():
    graph_search(print_interface())


def print_interface():
    # Create the default goal state based on the puzzle size
    goal = [[(i * puzzle_size) + j + 1 for j in range(puzzle_size)] for i in range(puzzle_size)]
    goal[-1][-1] = 0

    # Default problem (size of 3, hardcoded initial and goal states, NO Search choosen)
    problem = Problem(puzzle_size, initial, goal, "")
    problem.goal = goal
    problem.size = puzzle_size

    puzzle_choice = input("Welcome to 8 puzzle solver. \nType 1 to use a default puzzle, or 2 to enter your own puzzle.\n")
    if puzzle_choice == str(1): # Default puzzle is chosen
        # Print hardcoded initial state
        print("Default Puzzle:")
        problem.printInitial()
        print()
    elif puzzle_choice == str(2): # Custom puzzle is chosen
        customInitial = []
        for i in range(int(puzzle_size)):
            row = list(map(int, input("Enter the " + str(i+1) + "st row, use space or tabs between numbers: ").split()))
            customInitial.append(row)
        problem.initial = customInitial
        problem.printInitial()
        print()

    # Prompt user for what algorithm to use
    search_number = input("Enter your choice of algorithm\n(1) Uniform Cost Search\n(2) A* with the Misplaced Tile heuristic.\n(3) A* with the Euclidean distance heuristic.\n")
    print()

    # Use the users input to set the problem's search to the corresponding algorithm
    search_choice = search.get(search_number)
    problem.search = search_choice

    return problem

# Searches for solution given the problems parameters
def graph_search(prob):
    global expandedNodesCount
    global maxQueue

    # initialize frontier (PriorityQueue) and frontierList (contains the same board positions as the froniter, used to determine in node already in frontier)
    frontier = queue.PriorityQueue()
    frontierList = list()

    # initialize start Node, cost = 0, heuristic = 0
    start = Node(prob, prob.initial, prob.getBlank(), 0, None, 0)
    start.heuristic = getHeuristic(start, prob.search)

    # Add start node to the frontiers (PriorityQueue inserts a tuple of (node's total cost, node))
    frontier.put((0, start))
    frontierList.append(hash(start))

    # initialize explored list
    explored = list()

    # Check to see if this is the first time board is printed
    firstBoard = True

    # Checks if a goal has already been found
    goalFound = False
    goalCost = 0

    # iterate through frontier to check for goal states
    while not frontier.empty() and not (goalFound and frontier.queue[0][1].cost > goalCost) :
        if frontier.empty(): return "failure"
        if frontier.qsize() > maxQueue:
            maxQueue = frontier.qsize()

        # Pop the best node from the frontier
        leaf = frontier.get()[1]
        frontierList.remove(hash(leaf))

        # Set the leaf's h(n) to the corresponding algorithm's heuristic
        leaf.heuristic = getHeuristic(leaf, prob.search)

        # CODE TO PRINT OUT THE CORRECT SEQUENCE OF ACTIONS/OPERATORS
        # if firstBoard: # Print board for the first time
        #     print("Order of Expanded Nodes\nExpanding state")
        #     firstBoard = False
        #     leaf.printBoard()
        # else: # Print board subsequent times
        #     print("\nThe best state to expand with g(n) = " + str(leaf.cost) + " and h(n) = " + str(leaf.heuristic) + " is...\n")
        #     leaf.printBoard()
        #     print("Expanding this node...\n")

        #Check if the lead is the goal return the path from initial to this goal
        if leaf.isGoal():
            if goalFound: # compare which goal has a lower cost
                if goalNode.cost >= leaf.cost:
                    goalNode = leaf
            else:
                goalNode = leaf
            goalCost = leaf.cost
            goalFound = True

        # Add leaf to explored set
        explored.append(hash(leaf))

        # Expand the leaf node
        if not goalFound:
            frontier = expand(leaf, prob, frontier, frontierList, explored, leaf.heuristic)
            expandedNodesCount += 1

    print("Path to the Goal")
    goalNode.print_path()
    print("Goal!!!")
    print("Total # of Nodes Expanded: " + str(expandedNodesCount))
    print("Max # of Nodes in queue at one time: " + str(maxQueue))
    print("The depth of the goal node was: " + str(goalNode.cost))

# expands the leaf nodes possible moves
def expand(leaf, prob, frontier, frontierList, explored, heuristic):
    # Gets the possible moves
    neighbors = leaf.getBlankNeighbors()

    # iterates over all possible moves
    for i in neighbors:
        # Create new node from parent node leaf
        expandedNode = copy.deepcopy(leaf)

        # Update expandedNodes cost to be one greater and set its parent to the leaf node
        expandedNode.cost += 1
        expandedNode.heuristic = getHeuristic(expandedNode, prob.search)
        expandedNode.parent = leaf

        # Swap the blank position with the blank's neighbors
        expandedNode.swap(i)

        # Hashs the node to get the tuple of the current board positions and checks to see if its not in frontierList and explored
        # if hash(expandedNode) not in frontierList and hash(expandedNode) not in explored:
        if hash(expandedNode) not in explored:
            # Add node to the frontiers
            frontier.put((expandedNode.cost + getHeuristic(expandedNode, expandedNode.problem.search), copy.deepcopy(expandedNode)))
            frontierList.append(hash(expandedNode))

    return frontier

# Gets the corresponding h(n) for the 3 possible algorithms
def getHeuristic(leaf, choice):
    if choice == "Uniform": return 0
    if choice == "Misplaced": return misplacedHeuristic(leaf)
    if choice == "Euclidean": return euclideanHeuristic(leaf)

# Gets the corresponding h(n) for misplaced Heuristic
def misplacedHeuristic(leaf):
    count = 0
    for i in range(leaf.problem.size):
        for j in range(leaf.problem.size):
            if leaf.board[i][j] != 0 and leaf.board[i][j] != leaf.problem.goal[i][j]:
                count += 1
    return count

# Gets the corresponding h(n) for eucliedean Heuristic
def euclideanHeuristic(leaf):
    total_distance = 0
    for i in range(leaf.problem.size):
        for j in range(leaf.problem.size):
            target = leaf.problem.goal[i][j]
            if leaf.board[i][j] != 0 and leaf.board[i][j] != target:
                target_i = (leaf.board[i][j] - 1) // leaf.problem.size
                target_j = (leaf.board[i][j] - 1) % leaf.problem.size
                total_distance += math.ceil(((target_i - i) ** 2 + (target_j - j) ** 2) ** 0.5)
    return total_distance

main()