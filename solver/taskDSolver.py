# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Greedy maze solver for all entrance, exit pairs
#
# __author__ = <student name here>
# __copyright__ = 'Copyright 2025, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze

from knapsack.knapsack import Knapsack
from itertools import permutations

from typing import List, Dict, Optional


class TaskDSolver:
    def __init__(self, knapsack:Knapsack):
        self.m_solverPath: List[Coordinates] = []
        self.m_cellsExplored = 0 # count of UNIQUE cells visited. i.e. final count should equal len(set(self.m_solverPath))
        self.m_entranceUsed = None
        self.m_exitUsed = None
        self.m_knapsack = knapsack
        self.m_value = 0
        self.m_reward = float('-inf') # initial reward should be terrible

        # you may which to add more parameters here, such as probabilities, etc
        # you may update these parameters using the Maze object in SolveMaze

    def reward(self):
        return self.m_knapsack.optimalValue - self.m_cellsExplored

    def solveMaze(self, maze: Maze, entrance: Coordinates, exit: Coordinates):

        from collections import deque

        visited = set()
        queue = deque()
        queue.append((entrance, []))  # (cell, path to cell)

        max_capacity = self.m_knapsack.capacity
        current_weight = 0
        current_value = 0
        collected_items = []

        while queue:
            current_cell, path = queue.popleft()

            if current_cell in visited:
                continue

            visited.add(current_cell)
            path = path + [current_cell]
            self.m_solverPath = path

            # Check for item at current cell
            if current_cell in maze.m_items:
                item_weight, item_value = maze.m_items[current_cell]
                if current_weight + item_weight <= max_capacity:
                    current_weight += item_weight
                    current_value += item_value
                    collected_items.append(current_cell)

            # Check if we're at the exit (early stopping if satisfied)
            if current_cell == exit:
                break

            # Expand neighbors
            neighbors = maze.getNeighbors(current_cell)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path))

        self.m_knapsack.optimalWeight = current_weight
        self.m_knapsack.optimalValue = current_value
        self.m_knapsack.optimalCells = collected_items
        self.m_cellsExplored = len(set(self.m_solverPath))
        self.m_reward = self.reward()

        """
        Solution for Task D goes here.

        Be sure to increase self.m_cellsExplored whenever you visit a NEW cell
        Be sure to increase the knapsack_value whenever you find an item and put it in your knapsack.
        You may use the maze object to check if a cell you visit has an item
        maze.m_itemParams can be used to calculate things like predicted reward, etc. But you can only use
        maze.m_items to check if your current cell contains an item (and if so, what is its weight and value)

        Code in this function will be rigorously tested. An honest but bad solution will still gain quite a few marks.
        A cheated solution will gain 0 marks for all of Task D.
        Args:
            maze: maze object
            entrance: initial entrance coord
            exit: exit coord

        Returns: Nothing, but updates variables
        """
        # set up initial condition for knapsack. It should be empty
        self.m_knapsack.optimalCells = []
        self.m_knapsack.optimalValue = 0
        self.m_knapsack.optimalWeight = 0

        # get intial knowledge base of the maze items. This is the only occasion we can use maze.m_items
        # get the number of items in the maze from the paramaters
        items_in_maze = maze.m_itemParams[0]
        # calculate total weight in maze form item list
        maze_item_weight = sum(weight_value[0] for weight_value in maze.m_items.values())
        # calculate total value in maze from item list
        maze_item_value = sum(weight_value[1] for weight_value in maze.m_items.values())

        # set up some intitial values for the TaskDSolver object. As you calculate a solution, you will need
        # to change the solver path and recalculate your reward.
        self.m_solverPath = []
        self.m_entranceUsed = entrance
        self.m_exitUsed = exit
        self.m_cellsExplored = len(set(self.m_solverPath))
        self.m_reward = self.reward()
