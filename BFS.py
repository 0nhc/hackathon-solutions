import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors

INIT = 0
WALL = 1
FREE = 2
START = 3
GOAL = 4
VISITING = 5
VISITED = 6
FINAL_PATH = 7

class Node:
    def __init__(self, position=[0,0], index=0, neighbours=[], state=-1, score=np.inf) -> None:
        self.position = position # 2D Position in a matrix
        self.index = index # Indenty ID
        self.neighbours = neighbours # Indices of beighbour Nodes
        self.state = state # Every node has a state for visualizing
        self.score = score # Every node has a state for finding the shortest path
        
    def set_neighbours(self, neighbours):
        self.neighbours = neighbours


class Stack:
    def __init__(self) -> None:
        self.data = []
        
    def push(self, push_data):
        self.data.append(push_data)
        
    def pop(self):
        return self.data.pop()
        
        
class Maze:
    def __init__(self, num_rows=1, num_columns=1) -> None:
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_nodes = self.num_rows * self.num_columns
        
        self.nodes = []
        self.position_to_node_index_table = {}
        self.init_node_to_be_wall_posibility = 0.35
        self.start_node_index = 0
        self.goal_node_index = 0
        
        # Initialize a 2D graph with Node data structure
        node_index = 0
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                p = [i,j]
                neighbours = [[p[0]-1,p[1]], [p[0],p[1]+1], [p[0]+1,p[1]], [p[0],p[1]-1]]
                neighbours = self._neighbours_filter(neighbours)
                new_node = Node(position=p, index=node_index, neighbours=neighbours, state=INIT)
                self.position_to_node_index_table[str(p)] = node_index
                self.nodes.append(new_node)
                node_index += 1
            
                
    def as_matrix(self):
        matrix = np.zeros((self.num_rows, self.num_columns), dtype=int)
        node_index = 0
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                matrix[i,j] = self.nodes[node_index].state
                node_index += 1
        return matrix
    
    
    def as_nodes(self):
        return self.nodes
    
    
    def init_random_maze_map(self):
        # Generate a random start node
        random_position = self._generate_random_position_within_matrix()
        start_node_index = self.position_to_node_index_table[str(random_position)]
        self.nodes[start_node_index].state = START
        self.start_node_index = start_node_index
        
        # Walk random steps and set FREE nodes
        num_steps = random.randint(1, self.num_rows*self.num_columns-1)
        current_node_index = self.nodes[start_node_index].index
        for i in range(num_steps):
            # Move to a random neighbour
            neighbour_positions = self.nodes[current_node_index].neighbours
            random_neighbour_choice_index = random.randint(0, len(neighbour_positions)-1)
            random_neighbour_position = neighbour_positions[random_neighbour_choice_index]
            random_neighbour_index = self.position_to_node_index_table[str(random_neighbour_position)]
            if(self.nodes[random_neighbour_index].state == INIT or self.nodes[random_neighbour_index].state == FREE):
                current_node_index = random_neighbour_index
                self.nodes[current_node_index].state = FREE
        
        # Set the end node
        self.nodes[current_node_index].state = GOAL
        self.goal_node_index = current_node_index
        
        # Set other nodes from INIT state to WALL and FREE randomly
        for i in range(self.num_nodes):
            if(self.nodes[i].state == INIT):
                choice = random.random()
                if(choice < self.init_node_to_be_wall_posibility): # Is wall
                    self.nodes[i].state = WALL
                else: # Is FREE
                    self.nodes[i].state = FREE
        
        
    def _neighbours_filter(self, position_list):
        # Remove positions out of the maze boundary
        valid_positions = []
        for position in position_list:
            if(position[0] < 0):
                continue
            if(position[0] >= self.num_rows):
                continue
            if(position[1] < 0):
                continue
            if(position[1] >= self.num_columns):
                continue
            valid_positions.append(position)
        return valid_positions
            
            
    def _generate_random_position_within_matrix(self):
        row_index = random.randint(0,self.num_rows-1)
        column_index = random.randint(0,self.num_columns-1)
        return [row_index, column_index]
    

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
            
    
class MazeVisualizer:
    def __init__(self):
        # Define a discrete colormap
        self._colors = ['black', 'white', 'purple', 'yellow', 'red', 'blue', 'gray', 'blue']
        self._cmap = mcolors.ListedColormap(self._colors)
        self._bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.6, 7.5]  # Define boundaries for each color
        self._norm = mcolors.BoundaryNorm(self._bounds, self._cmap.N)
        
        # Set matplotlib to full screen by default
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        
        # Lines cache
        self._lines_cache = [[], []]
        self._lines_cache_num = 0
        
        # Path cache
        self._path_cache = [[], []]
        self._path_cache_num = 0
    
        
    def play(self, mazes, interval=1.5):
        for maze in mazes:
            plt.imshow(maze, cmap=self._cmap, norm=self._norm, interpolation='nearest')
            plt.pause(interval) # seconds
            
    def display_single_state(self, maze, interval=1.0):
        plt.clf()
        plt.imshow(maze, cmap=self._cmap, norm=self._norm, interpolation='nearest')
        plt.pause(interval) # seconds
        
    def draw_line_between_two_points(self, p1, p2, color="orange"):
        self._lines_cache[0].append([p1[1], p2[1]])
        self._lines_cache[1].append([p1[0], p2[0]])
        self._lines_cache_num += 1
        
        plt.clf()
        for i in range(self._lines_cache_num):
            plt.plot(self._lines_cache[0][i], self._lines_cache[1][i], color=color, linewidth=2)
        plt.draw()  # Update the plot with the new line
        
    def draw_path_between_two_points(self, p1, p2, color="blue"):
        self._path_cache[0].append([p1[1], p2[1]])
        self._path_cache[1].append([p1[0], p2[0]])
        self._path_cache_num += 1
        
        for i in range(self._path_cache_num):
            plt.plot(self._path_cache[0][i], self._path_cache[1][i], color=color, linewidth=2)
        plt.draw()  # Update the plot with the new line
        
    def clear_visualizer_cache(self):
        plt.clf()
        self._lines_cache = [[], []]
        self._lines_cache_num = 0
        

maze = Maze(90,160)
maze.init_random_maze_map()

bfs_solver = BFSSolver(maze)
bfs_solver.find_the_goal()
bfs_solver.find_the_shortest_path()