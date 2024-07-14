from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: "up", 1: "left", 2: "down", 3: "right"}
MAX_PLAYER, CHANCE_PLAYER = 0, 1


# Tree node. To be used to construct a game tree.
class Node:
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        # state[0] is the current board layout
        # state[1] is the current score
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return len(self.children) == 0


# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions:
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node=None, depth=0):
        """
        Build a tree that switches between MAX_PLAYER and CHANCE_PLAYER
        - The MAX_PLAYER, at each state, should consider all valid moves
        - The CHANCE_PLAYER, at each state, should consider all possible tiles to set to 2
        """

        # base case for when max depth has been reached
        if not node or not depth:
            return

        currLayout = node.state[0]
        currScore = node.state[1]
        player = node.player_type
        children = node.children

        if player == MAX_PLAYER:
            for move in MOVES:
                # create deep copy of the current board state
                self.simulator.set_state(currLayout, currScore)

                # if a valid move, add a chance player node and update the current state of the board
                if self.simulator.move(move):
                    childNode = Node(self.simulator.current_state(), CHANCE_PLAYER)
                    children.append((move, childNode))
                    self.build_tree(childNode, depth - 1)

        else:
            for row, col in self.simulator.get_open_tiles():
                # create deep copy of the current board state
                self.simulator.set_state(currLayout, currScore)
                # chance player places a 2 on available board tiles
                self.simulator.tile_matrix[row][col] = 2
                childNode = Node(self.simulator.current_state(), MAX_PLAYER)
                children.append((None, childNode))
                self.build_tree(childNode, depth - 1)

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node=None):
        """
        Recursively compute the best score possible
        - The MAX_PLAYER will store and update the best move and score
        - The CHANCE_PLAYER will compute the exepected value across all of its possible moves
        """
        if not node:
            return (None, 0)

        # currLayout = node.state[0]
        currScore = node.state[1]
        player = node.player_type
        children = node.children
        numChildren = len(node.children)

        if node.is_terminal():
            return (None, currScore)

        if player == MAX_PLAYER:
            maxVal = float("-inf")
            bestMove = None

            for move, child in children:
                childMove, childScore = self.expectimax(child)
                if childScore > maxVal:
                    maxVal = childScore
                    bestMove = move

            return (bestMove, maxVal)
        else:
            sumVal = 0
            for move, child in children:
                childMove, childScore = self.expectimax(child)
                sumVal += childScore
            return (None, sumVal / numChildren)

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        self.build_tree(self.root, 3)
        direction, _ = self.expectimax_ec(self.root)
        return direction

    def expectimax_ec(self, node=None):
        """
        Recursively compute the best score possible
        - The MAX_PLAYER will store and update the best move and score
        - The CHANCE_PLAYER will compute the exepected value across all of its possible moves
        """
        if not node:
            return None, 0

        currLayout = node.state[0]
        currScore = self.customScore(currLayout, node.state[1])
        player = node.player_type
        children = node.children
        numChildren = len(node.children)

        if node.is_terminal():
            return None, currScore

        if player == MAX_PLAYER:
            maxVal = float("-inf")
            bestMove = None

            for move, child in children:
                childMove, childScore = self.expectimax_ec(child)
                if childScore > maxVal:
                    maxVal = childScore
                    bestMove = move

            return bestMove, maxVal
        else:
            sumVal = 0
            for move, child in children:
                childMove, childScore = self.expectimax_ec(child)
                sumVal += childScore
            return None, sumVal / numChildren

    # helper function to calculate score that prioritizes non-decreasing row and column values
    def customScore(self, grid, score):
        gridSize = len(grid)

        # want row values to be non-decreasing
        for i in range(gridSize):
            isNonDecreasing = True
            for j in range(1, gridSize):
                if grid[i][j] < grid[i][j - 1]:
                    isNonDecreasing = False
                    break
            if isNonDecreasing:
                for num in grid[i]:
                    score += num

        # want column values to be non-decreasing
        for i in range(gridSize):
            isNonDecreasing = True
            for j in range(1, gridSize):
                if grid[j][i] < grid[j - 1][i]:
                    isNonDecreasing = False
                    break
            if isNonDecreasing:
                for row in grid:
                    score += row[i]

        return score
