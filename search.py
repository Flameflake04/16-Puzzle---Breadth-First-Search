# CS 411 - Assignment 3 Starter Code
# Breadth First Search on 15 Puzzle
# Name: Duc Tran, UIN: 679876782
# Spring 2024

import random
import math
import time
import psutil
import os
from collections import deque
import sys


# This class defines the state of the problem in terms of board configuration
# This program used 2D array with size 4x4 to config the board
class Board:
    def __init__(self, tiles):
        board_config = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        for i in range(16):
            board_config[i//4][i%4] = tiles[i]
        self.tiles = board_config

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        for i in range(0,4):
            for j in range(0,4):
                if self.tiles[i][j] == 0:
                    xCordBlank = j
                    yCordBlank = i
        self.result = self.tiles
        if action == "D":
            temp = self.result[yCordBlank + 1][xCordBlank]
            self.result[yCordBlank + 1][xCordBlank] = 0
            self.result[yCordBlank][xCordBlank] = temp
        elif action == "U":
            temp = self.result[yCordBlank - 1][xCordBlank]
            self.result[yCordBlank - 1][xCordBlank] = 0
            self.result[yCordBlank][xCordBlank] = temp
        elif action == "R":
            temp = self.result[yCordBlank][xCordBlank + 1]
            self.result[yCordBlank][xCordBlank + 1] = 0
            self.result[yCordBlank][xCordBlank] = temp
        elif action == "L":
            temp = self.result[yCordBlank][xCordBlank - 1]
            self.result[yCordBlank][xCordBlank - 1] = 0
            self.result[yCordBlank][xCordBlank] = temp
        flattened_tiles = [int(tile) for row in self.result for tile in row] 
        new_board = Board(flattened_tiles)
        return new_board

# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
    # Returns string representation of the state
    def __repr__(self):
        string = ""
        for i in range (0,4):
            for j in range(0,4):
                string += str(((self.state.tiles)[i][j])) + " "
        string = string[:-1]
        return string

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    # Return hashing address of a node
    def __hash__(self):
        self.string = self.__repr__()
        return hash(tuple(self.string))

class Search:
    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        list_children = []
        list_possible_moves = ["R","L","U","D"]
        xCordBlankParent = 0
        yCordBlankParent = 0
        for i in range(0,4):
            for j in range(0,4):
                if int(parent_node.state.tiles[i][j]) == 0:
                    xCordBlankParent = j
                    yCordBlankParent = i
        if int(xCordBlankParent) == 0:
            list_possible_moves.remove("L")
        if int(xCordBlankParent) == 3:
            list_possible_moves.remove("R")
        if int(yCordBlankParent) == 0:
            list_possible_moves.remove("U")
        if int(yCordBlankParent) == 3:
            list_possible_moves.remove("D")
        for move in list_possible_moves:
            flattened_tiles = [int(tile) for row in parent_node.state.tiles for tile in row] 
            new_board = Board(flattened_tiles)
            new_state = new_board.execute_action(move)  
            new_child = Node(new_state, parent_node, move)  
            list_children.append(new_child)
        return list_children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        actions = []
        while node is not None:
            if node.parent is not None:
                actions.append(node.action)
            node = node.parent
        actions.reverse()
        string_action = ""
        for i in range(0, len(actions)):
            string_action += actions[i]
        return string_action


    # This function used Breadth-first search in order to searching for the goal node
    def run_bfs(self, root_node):
        start = time.time()
        process = psutil.Process()
        goal_states = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0"
        if root_node.__repr__() == goal_states:
            end = time.time()
            return "NoOps", 0, end - start, process.memory_info().rss
        frontier = deque()
        frontier.append(root_node)
        explore_set = set() # hashset
        node_explored = 1
        while len(frontier) != 0:
            current_node = frontier.popleft()
            explore_set.add(current_node.__hash__())
            for child in self.get_children(current_node): 
                if child.__repr__() == goal_states:
                    end = time.time()
                    return self.find_path(child), node_explored, end - start, process.memory_info().rss
                if (child.__hash__() not in explore_set): 
                    frontier.append(child)
                    node_explored += 1
 
    def solve(self, input):
        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        path, expanded_nodes, time_taken, memory_consumed = self.run_bfs(root)
        print("Moves: " + "".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)

# Testing the algorithm locally
if __name__ == '__main__':
    agent = Search()
    agent.solve("1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15")
    
    

    
    
    