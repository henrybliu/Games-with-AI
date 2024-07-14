from __future__ import print_function
import heapq
from collections import deque

ACTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = set()
        elif self.type == "bfs":
            self.frontier = deque([self.grid.start])
            self.explored = set()
        elif self.type == "ucs":
            self.frontier = [(self.grid.nodes[self.grid.start].cost(), self.grid.start)]
            self.explored = set()
        elif self.type == "astar":
            self.frontier = [
                (
                    self.manHatDist(self.grid.start)
                    + self.grid.nodes[self.grid.start].cost(),
                    self.grid.nodes[self.grid.start].cost(),
                    self.grid.start,
                )
            ]  # (totalCost, actualCost, node)
            self.explored = set()

    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = (
                True  # This turns the color of the node to red
            )
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    # DFS: BUGGY, fix it first
    def dfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop()

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        self.explored.add(current)

        children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(
                self.grid.col_range
            ):
                if not self.grid.nodes[n].puddle and n not in self.explored:
                    self.previous[n] = current
                    self.frontier.append(n)
                    self.explored.add(n)
                    self.grid.nodes[n].color_frontier = True

    # Implement BFS here (Don't forget to implement initialization in set_search function)
    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        current = self.frontier.popleft()

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        self.explored.add(current)

        children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(
                self.grid.col_range
            ):
                if not self.grid.nodes[n].puddle and n not in self.explored:
                    self.previous[n] = current
                    self.frontier.append(n)
                    self.explored.add(n)
                    self.grid.nodes[n].color_frontier = True

    # Implement UCS here (Don't forget to implement initialization in set_search function)
    # Hint: You can use heappop and heappush from the heapq library (imported for you above)
    def ucs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        heapq.heapify(self.frontier)
        currCost, current = heapq.heappop(self.frontier)

        if current == self.grid.goal:
            self.finished = True
            return

        self.explored.add(current)

        children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(
                self.grid.col_range
            ):
                childCost = currCost + self.grid.nodes[n].cost()
                if not self.grid.nodes[n].puddle and n not in self.explored:

                    # not in frontier
                    if n not in [x[1] for x in self.frontier]:
                        self.previous[n] = current
                        self.grid.nodes[n].color_frontier = True
                        self.frontier.append((childCost, n))

                    # in frontier and a lesser cost path exists
                    else:
                        for i in range(len(self.frontier)):
                            if (
                                self.frontier[i][1] == n
                                and childCost < self.frontier[i][0]
                            ):
                                self.frontier[i] = (childCost, n)
                                self.previous[n] = current

    # Implement Astar here (Don't forget to implement initialization in set_search function)
    # Hint: You can use heappop and heappush from the heapq library (imported for you above)
    def astar_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        heapq.heapify(self.frontier)

        # at each step, there should be a new heuristic value -- NOT just adding to the previous heuristic value
        currTotalCost, currRealCost, current = heapq.heappop(self.frontier)

        if current == self.grid.goal:
            self.finished = True
            return

        self.explored.add(current)

        children = [(current[0] + a[0], current[1] + a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(
                self.grid.col_range
            ):
                childCost = currRealCost + self.grid.nodes[n].cost()
                if not self.grid.nodes[n].puddle and n not in self.explored:

                    # not in frontier
                    if n not in [x[2] for x in self.frontier]:
                        self.previous[n] = current
                        self.grid.nodes[n].color_frontier = True
                        self.frontier.append(
                            (childCost + self.manHatDist(n), childCost, n)
                        )

                    # in frontier and a lesser cost path exists
                    else:
                        for i in range(len(self.frontier)):
                            if (
                                self.frontier[i][2] == n
                                and childCost < self.frontier[i][1]
                            ):
                                self.frontier[i] = (
                                    childCost + self.manHatDist(n),
                                    childCost,
                                    n,
                                )
                                self.previous[n] = current

    def manHatDist(self, position):
        return abs(position[0] - self.grid.goal[0]) + abs(
            position[1] - self.grid.goal[1]
        )
