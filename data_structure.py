import numpy as np

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