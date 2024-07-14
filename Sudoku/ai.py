from __future__ import print_function
from game import (
    sd_peers,
    sd_spots,
    sd_domain_num,
    init_domains,
    restrict_domain,
    SD_DIM,
    SD_SIZE,
)
import random, copy


class AI:
    def __init__(self):
        # the board is a 9x9
        self.numSpots = SD_SIZE**2
        pass

    def solve(self, problem):
        assignments = {}
        domains = init_domains()
        restrict_domain(domains, problem)
        decisionStack = []

        while True:
            conflict = False
            conflict, assignments, domains = self.propagate(
                conflict, assignments, domains
            )
            if not conflict:
                if len(assignments) == self.numSpots:
                    return domains
                else:
                    assignments, spot = self.makeDecision(assignments, domains)
                    decisionStack.append(
                        (
                            copy.deepcopy(assignments),
                            copy.deepcopy(spot),
                            copy.deepcopy(domains),
                        )
                    )
            else:
                if not decisionStack:
                    return None
                else:
                    assignments, domains = self.backtrack(decisionStack)

    # continue to make assignments to update domain unless there is a conflict
    def propagate(self, conflict, assignments, domains):
        while True:
            # make assignment if domain becomes singleton
            for spot, domain in domains.items():
                if len(domain) == 1:
                    assignments[spot] = domain[0]

            # if x (spot) has been assigned a value, update its domain
            for spot in assignments:
                domains[spot] = [assignments[spot]]

            # if any domain is empty, then there is a conflict because it cannot be assigned any value
            for spot, domain in domains.items():
                if not domain:
                    conflict = True
                    return conflict, assignments, domains

            arcConsistent = True
            for spot in sd_spots:
                for peer in sd_peers[spot]:
                    if len(domains[peer]) == 1 and domains[peer][0] in domains[spot]:
                        domains[spot].remove(domains[peer][0])
                        arcConsistent = False

            if arcConsistent:
                return conflict, assignments, domains

    # pick a spot that hasn't been assigned, pick a random value (the first one), and assign it as that random value
    def makeDecision(self, assignments, domains):
        for spot, domain in domains.items():
            if spot not in assignments and domain:
                assignments[spot] = domain[0]
                return assignments, spot

    # pop from the decision stack and try again from the last valid assignment and domains
    def backtrack(self, decisionStack):
        assignments, spot, domains = decisionStack.pop()
        assignedVal = assignments[spot]
        del assignments[spot]
        domains[spot].remove(assignedVal)
        return assignments, domains

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains

        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
