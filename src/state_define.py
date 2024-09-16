"""
Pre-defined different states in every maze node.

This script includes every possible state for a maze node. 
These states are both used for path planning and visualizing.
"""

INIT = 0 # The node has not been processed yet.

WALL = 1 # The node is a wall and cannot be traversed.

FREE = 2 # The node is a free space and can be traversed

START = 3 # The node is the starting point of the maze.

GOAL = 4 # The node is the goal point of the maze.

VISITING = 5 # The node is currently being visited.

VISITED = 6 # The node has been visited and processed.

FINAL_PATH = 7 # The node is part of the final path from start to goal.
