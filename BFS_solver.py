from data_structure import Node, Stack
from maze import Maze
from state_define import *
from maze_visualizer import MazeVisualizer
import numpy as np

class BFSSolver:
    def __init__(self, maze=Maze()) -> None:
        self.maze = maze
        self.visiting_stack = Stack()
        self.visited_node_indices = []
        self.visualizer = MazeVisualizer()
        
    def find_the_goal(self):
        # Display first
        self.visualizer.display_single_state(self.maze.as_matrix(), interval=2.0)
        
        # Main loop
        self.visiting_stack.push(self.maze.start_node_index)
        found_the_goal = False
        score = 0
        while(found_the_goal == False):
        # for i in range(2):
            # Change all visiting nodes'state to VISITING for visualizing
            for visiting_node_index in self.visiting_stack.data:
                visiting_node = self.maze.nodes[visiting_node_index]
                if(visiting_node.state == FREE):
                    self.maze.nodes[visiting_node.index].state = VISITING
            self.visualizer.display_single_state(self.maze.as_matrix(), interval=0.01)
            
            # Check if current stack has nodes adjacent to the goal
            for visiting_node_index in self.visiting_stack.data:
                visiting_node = self.maze.nodes[visiting_node_index]
                neighbours = visiting_node.neighbours
                for neighbour_position in neighbours:
                    neighbour_index = self.maze.position_to_node_index_table[str(neighbour_position)]
                    if(neighbour_index == self.maze.goal_node_index):
                        # Change al VISITING nodes' state to VISITED and exit the for loop
                        # for visiting_node_index in self.visiting_stack.data:
                        #     self.maze.nodes[visiting_node_index].state = VISITED
                        # self.visualizer.display_single_state(self.maze.as_matrix(), interval=3.0)
                        found_the_goal = True
                
            # Get all neighbours of current visiting nodes
            neighbour_indices = []
            for visiting_node_index in self.visiting_stack.data:
                visiting_node = self.maze.nodes[visiting_node_index]
                neighbours = visiting_node.neighbours
                for neighbour_position in neighbours:
                    neighbour_index = self.maze.position_to_node_index_table[str(neighbour_position)]
                    if neighbour_index not in self.visited_node_indices:
                        if(self.maze.nodes[neighbour_index].state == FREE):
                            neighbour_indices.append(neighbour_index)
                            self.visited_node_indices.append(neighbour_index)
            
            # Update visiting nodes
            # Changing visiting nodes' states and turn them to VISITED
            while(len(self.visiting_stack.data) != 0):
                visited_node_index = self.visiting_stack.pop()
                self.maze.nodes[visited_node_index].score = score
                if(self.maze.nodes[visited_node_index].state != START):
                    self.maze.nodes[visited_node_index].state = VISITED
            # Change neighbours as visiting nodes
            for index in neighbour_indices:
                self.visiting_stack.push(index)
            self.visualizer.display_single_state(self.maze.as_matrix(), interval=0.01)
            
            # Update score
            score += 1
            
    
    def find_the_shortest_path(self):
        path_node_indices = []
        current_index = self.maze.goal_node_index
        reached_start = False
        while(reached_start == False):
            # Find the neighbour of current node with lowest score
            minimum_score = np.inf
            minimum_index = 0
            neighbours = self.maze.nodes[current_index].neighbours
            for neighbour_position in neighbours:
                neighbour_index = self.maze.position_to_node_index_table[str(neighbour_position)]
                if(self.maze.nodes[neighbour_index].state == VISITED):
                    neighbour_score = self.maze.nodes[neighbour_index].score
                    if(neighbour_score < minimum_score):
                        minimum_index = neighbour_index
                        # print(neighbour_index, minimum_index)
                        minimum_score = neighbour_score
            
            path_node_indices.append(minimum_index)
            self.maze.nodes[minimum_index].state = FINAL_PATH
            current_index = minimum_index
            self.visualizer.display_single_state(self.maze.as_matrix(), interval=0.01)
            
            # Check if current node has reached the start node
            neighbours = self.maze.nodes[current_index].neighbours
            for neighbour_position in neighbours:
                neighbour_index = self.maze.position_to_node_index_table[str(neighbour_position)]
                if(neighbour_index == self.maze.start_node_index):
                    reached_start = True
            
        self.visualizer.display_single_state(self.maze.as_matrix(), interval=3.0)