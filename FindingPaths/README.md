# Finding Paths

Setting Up
----
First, make sure you have Python 3.\* and the latest pip version (Check the `Notes & FAQ` section below if you're having trouble with this). Here is our preferred way to set up (if you have another way, feel free to do it):

1. Install [anaconda](https://docs.anaconda.com/anaconda/install/) to set up a virtual environment
2. `conda create -n cse150b python=3.10`
3. `conda activate cse150b`
4. To install PyGame, `pip install pygame`. We will use PyGame for all assignments in this class.
 
You can run `conda deactivate` to deactivate the environment. The next time you want to work on the assignment, type `conda activate cse150b` first to use the exact same environment with PyGame installed.

Task To Complete
----
The task is to find paths from the start (yellow node) to the goal (orange node). Once you load up the program (You'll see how in the `Usage` section below) and press `enter` you will see what that means. In class I briefly explained the meaning of the different colors of the nodes (green is "grass" that incurs high cost, blue is "puddle" that the agent can not pass through). Check slides, lecture recording, and read the code to figure things out. If you are stuck, feel free to discuss on slack or attend office hours.

The code for DFS is **partially** given to make it easy for you to understand the code. But it is intentionally buggy. Before you start implementing the other algorithms, fix DFS first.

Implement the following search strategies in `ai.py`:

- DFS (buggy)
- BFS
- Uniform Cost Search
- A\* Search using Manhattan Distance as the heuristic

You can find the function definitions in the file. Feel free to add more auxiliary functions if needed. You can use other **standard Python libraries** such as math etc. but they are not really needed. Do not use libraries not standard to Python (i.e. numpy, torch); if you are not sure whether a library is ok to use or not, ask in the slack group.

Usage
----
Simply run `python main.py` and you will see the grid world window. By pressing `enter` you see how DFS finds a path (given DFS is buggy, as you will see). Pressing 2, 3, or 4 should respectively run BFS, UCS, A\* in a similar way, which you will implement (since right now it does nothing). 

The `tests` file contains a lot of test maps. If you want to load in the maps as test cases (`python main.py -l [test case number]`), we have provided a few fun cases for you to play with:

0. Random 1
1. Random 2
2. Spiral
3. Zigzag
4. "Two roads diverged in a wood, and I - I took the one less traveled by, and that has made all the difference."
5. CSE ~~11~~ 150b style (homage to Rick Ord)
6. "It's a-me, Mario!"

We give you an additional 20 randomly generated test cases (lines 7 and on) to test the correctness of your code; to test on all given tests automatically, you can do `python main.py -t` which autogrades the algorithms with respect to the correct optimal costs in the test maps above.