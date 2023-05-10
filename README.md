# 8-Puzzle Solver

This program is an 8-puzzle solver that uses Uniform Cost Search, A* with the Misplaced Tile heuristic, and A* with the Euclidean distance heuristic to find the solution to a given 8-puzzle.

## How it works

The program takes the input puzzle size and a user-defined puzzle or a default puzzle. The user is prompted to choose an algorithm to solve the puzzle. The program then outputs the solution path, the number of expanded nodes, the maximum number of nodes in the queue, and the depth of the goal node.

## Files

- `main.py`: The main file that includes the primary functions for solving the 8-puzzle.
- `problem.py`: Contains the `Problem` class that represents the 8-puzzle problem with its initial and goal states.
- `node.py`: Contains the `Node` class that represents the nodes in the search tree.

## Running the program

1. Make sure you have Python installed on your system.
2. Open a terminal and navigate to the folder containing the program files.
3. Run the following command: `python main.py`
4. Follow the prompts to enter the puzzle size and algorithm choice.

