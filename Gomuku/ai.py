from __future__ import absolute_import, division, print_function
from math import sqrt, log
from game import Game, WHITE, BLACK, EMPTY
import copy
import time
import random


class Node:
    # NOTE: modifying this block is not recommended
    def __init__(self, state, actions, parent=None):
        self.state = (state[0], copy.deepcopy(state[1]))
        self.num_wins = 0  # number of wins at the node
        self.num_visits = 0  # number of visits of the node
        self.parent = parent  # parent node of the current node
        self.children = (
            []
        )  # store actions and children nodes in the tree as (action, node) tuples
        self.untried_actions = copy.deepcopy(
            actions
        )  # store actions that have not been tried
        simulator = Game(*state)
        self.is_terminal = simulator.game_over


# NOTE: deterministic_test() requires BUDGET = 1000
# You can try higher or lower values to see how the AI's strength changes
BUDGET = 1000


class AI:
    # NOTE: modifying this block is not recommended because it affects the random number sequences
    def __init__(self, state):
        self.simulator = Game()
        self.simulator.reset(*state)  # using * to unpack the state tuple
        self.root = Node(state, self.simulator.get_actions())

    def mcts_search(self):

        # TODO: Implement the main MCTS loop

        iters = 0
        action_win_rates = {}  # store the table of actions and their ucb values

        # TODO: Implement the MCTS Loop
        while iters < BUDGET:
            if (iters + 1) % 100 == 0:
                # NOTE: if your terminal driver doesn't support carriage returns you can use:
                # print("{}/{}".format(iters + 1, BUDGET))
                print("\riters/budget: {}/{}".format(iters + 1, BUDGET), end="")

            # TODO: select a node, rollout, and backpropagate
            bestNode = self.select(self.root)  # TreePolicy(s_root)
            reward = self.rollout(bestNode)  # DefaultPolicy(s)
            self.backpropagate(bestNode, reward)  # BAckup(s, winner)

            iters += 1
        print()

        # Note: Return the best action, and the table of actions and their win values
        #   For that we simply need to use best_child and set c=0 as return values
        _, action, action_win_rates = self.best_child(self.root, 0)

        return action, action_win_rates

    def select(self, node):

        # TODO: select a child node
        # HINT: you can use 'is_terminal' field in the Node class to check if node is terminal node
        # NOTE: deterministic_test() requires using c=1 for best_child()
        while not node.is_terminal:
            if len(node.untried_actions):
                return self.expand(node)
            else:
                node, _, _ = self.best_child(node, 1)

        return node

    def expand(self, node):

        # TODO: add a new child node from an untried action and return this new node

        child_node = None  # choose a child node to grow the search tree

        # NOTE: passing the deterministic_test() requires popping an action like this
        action = node.untried_actions.pop(0)
        actionX, actionY = action

        # NOTE: Make sure to add the new node to node.children
        # NOTE: You may find the following methods useful:
        #   self.simulator.state()
        #   self.simulator.get_actions()

        self.simulator.reset(node.state[0], node.state[1])
        self.simulator.place(actionX, actionY)

        child_node = Node(
            self.simulator.state(), self.simulator.get_actions(), parent=node
        )
        node.children.append((action, child_node))

        return child_node

    def best_child(self, node, c=1):

        # TODO: determine the best child and action by applying the UCB formula

        best_child_node = None  # to store the child node with best UCB
        best_action = None  # to store the action that leads to the best child
        action_ucb_table = (
            {}
        )  # to store the UCB values of each child node (for testing)

        numerator = 2 * log(node.num_visits)

        # NOTE: deterministic_test() requires iterating in this order
        for child in node.children:
            # NOTE: deterministic_test() requires, in the case of a tie, choosing the FIRST action with
            # the maximum upper confidence bound
            childAction, childNode = child
            avgReward = childNode.num_wins / childNode.num_visits
            freshness = sqrt(numerator / childNode.num_visits)
            ucbVal = avgReward + (c * freshness)

            action_ucb_table[childAction] = ucbVal

            if not best_child_node or ucbVal > action_ucb_table[best_action]:
                best_child_node = childNode
                best_action = childAction

        return best_child_node, best_action, action_ucb_table

    def backpropagate(self, node, result):

        # while node is not None:
        while node and node.parent:
            # TODO: backpropagate the information about winner
            # IMPORTANT: each node should store the number of wins for the player of its **parent** node
            parentPlayerType = node.parent.state[0]
            node.num_visits += 1
            # apply 1 - result
            # inverse is necessary to flip between min and max players

            # example:
            # if BLACK wins (result[BLACK] == 1), then we don't increment WHTIE's # wins
            # if BLACK loses (result[BLACK] == 0), then we increment WHITE's # wins
            node.num_wins += 1 - (
                result[BLACK] if parentPlayerType == WHITE else result[WHITE]
            )
            node = node.parent

        # for root node that doesn't have a parent, only increment its number of visits
        node.num_visits += 1

    def rollout(self, node):

        # TODO: rollout (called DefaultPolicy in the slides)

        # HINT: you may find the following methods useful:
        #   self.simulator.reset(*node.state)
        #   self.simulator.game_over
        #   self.simulator.rand_move()
        #   self.simulator.place(r, c)
        # NOTE: deterministic_test() requires that you select a random move using self.simulator.rand_move()
        self.simulator.reset(node.state[0], node.state[1])
        while not self.simulator.game_over:
            randomMoveX, randomMoveY = self.simulator.rand_move()
            self.simulator.place(randomMoveX, randomMoveY)

        # Determine reward indicator from result of rollout
        reward = {}
        if self.simulator.winner == BLACK:
            reward[BLACK] = 1
            reward[WHITE] = 0
        elif self.simulator.winner == WHITE:
            reward[BLACK] = 0
            reward[WHITE] = 1
        return reward
