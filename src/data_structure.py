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
    """
    Pre-defined Stack data structure.
    """
    def __init__(self) -> None:
        self.data = []
        
    def push(self, push_data):
        """
        Push a new element to the top of the stack.
        
        Input: New element
        Return: None
        """
        self.data.append(push_data)
        
    def pop(self):
        """
        Pop the element on the top of the stack.
        
        Input: None
        Return: The poped element on the top of the stack
        """
        return self.data.pop()
    
class Queue:
    """
    Pre-defined Queue data structure.
    """
    def __init__(self) -> None:
        self.data = []
        
    def push(self, push_data):
        """
        Push a new element to the end of the queue.
        
        Input: New element
        Return: None
        """
        self.data.append(push_data)
        
    def pop(self):
        """
        Pop the element on the front of the queue.
        
        Input: None
        Return: The poped element on the front of the queue
        """
        return self.data.pop(0)