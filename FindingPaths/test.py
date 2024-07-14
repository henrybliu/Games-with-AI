from ai import AI
from game import Grid

def test():
    with open("tests") as file:
        grid = Grid()
        ai = AI(grid, "dfs")

        lines = file.readlines()
        for line_i, line in enumerate(lines):
            print("test {}/{}: ".format(line_i + 1, len(lines)))

            split = line.split()
            score = {}
            score["bfs"] = split[0]
            score["ucs"] = split[1]
            score["astar"] = split[2]

            grid.load(" ".join(split[3:]))

            for method in ["bfs", "ucs", "astar"]:
                ai.set_type(method)
                ai.set_search()
                while not ai.finished:
                    ai.make_step()

                if not ai.failed:
                    ai.get_result()
                
                expected = int(score[method])
                actual = ai.final_cost

                if expected != actual:
                    print("\t {} FAILED: expected score of {}, actual {}".format(method, expected, actual))

                else:
                    print("\t {} PASSED".format(method))
