from algorithm import Algorithm
from drawgui import Drawgui
import sys

def searchMethod(method, search):
    # the user input is not case sensitive
    method = method.lower()
    if method == "bfs":
        return search.breathFirstSearch()
    elif method == "dfs":
        return search.depthFirstSearch()
    elif method == "gbfs":
        return search.greedyBestFirst()
    elif method == "as":
        return search.aStar()
    elif method == "iddfs":
        return search.iterativeDeepeningDepthFirstSearch()
    elif method == "hc":
        return search.hillClimbingSearch()
    else:
        raise ValueError(f"Unknown search method: {method}")

def main():
    filename = sys.argv[1]
    method = sys.argv[2]
    algorithm = Algorithm(filename)
    drawGUI = Drawgui(algorithm)
    print(searchMethod(method, algorithm))
    drawGUI.draw()

if __name__ == "__main__":
    main()