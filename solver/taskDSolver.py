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
        """
        Task D: Exploration under partial observability.
        The agent explores the maze incrementally, discovering new cells and items.
        It re-evaluates its knapsack contents dynamically as new treasures appear.
        """

        from collections import deque

        # Initialise tracking variables
        self.m_solverPath = []
        self.m_entranceUsed = entrance
        self.m_exitUsed = exit
        self.m_cellsExplored = 0
        self.m_knapsack.optimalCells = []
        self.m_knapsack.optimalWeight = 0
        self.m_knapsack.optimalValue = 0

        # Parameters
        max_capacity = self.m_knapsack.capacity
        known_items = []  # discovered items
        visited = set()
        frontier = deque()
        frontier.append(entrance)

    while frontier:
        current = frontier.popleft()

        if current in visited:
            continue

        visited.add(current)
        self.m_solverPath.append(current)
        self.m_cellsExplored = len(visited)

        # --- Perception: discover new info around current cell ---
        for neighbor in maze.getNeighbors(current):
            if neighbor not in visited and neighbor not in frontier:
                frontier.append(neighbor)

        # --- Check if current cell contains an item ---
        if current in maze.m_items:
            item_weight, item_value = maze.m_items[current]

            # Add newly discovered item to known list (if not already)
            if current not in [i[0] for i in known_items]:
                known_items.append((current, item_weight, item_value))

            # Re-run knapsack solver dynamically to decide what to keep
            selected, total_wt, total_val = self.m_knapsack.dynamicKnapsack(
                known_items, max_capacity, len(known_items), "testing"
            )

            self.m_knapsack.optimalCells = selected
            self.m_knapsack.optimalWeight = total_wt
            self.m_knapsack.optimalValue = total_val

        # --- Check termination condition ---
        # Exit if the knapsack is full or exit reached
        if current == exit or self.m_knapsack.optimalWeight >= max_capacity:
            break

    # Update reward: total value minus cells explored
    self.m_reward = self.reward()

