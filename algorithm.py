from filereader import FileReader
from collections import deque
import sys

class Algorithm:
    def __init__(self, fileAddress):
        self.fileAddress = fileAddress
        self.readFile = FileReader(fileAddress)
        # this suppose to be set() instead of array for O(1) time complexity, however, set() is also not an ordered list, which will be hard to draw in pygame
        self.expanded = [self.readFile.startPos]
        self.frontier = None
        self.path = None
        self.direction = None
        self.failed = False
    
    def breathFirstSearch(self):
        # this changed to deque instead of array for O(1) time complexity, the queue stores frontier, path, direction
        queue = deque([(self.readFile.startPos, [], [])])
        while queue:
            self.frontier, self.path, self.direction = queue.popleft()
            if self.frontier in self.readFile.goals:
                return f"{self.fileAddress} BFS\n<Node {self.frontier}> {len(self.expanded)}\n{self.direction}"
            # since BFS is FIFO, we need to add the top node first to ensure the agent try to move UP before attempting LEFT, before attempting DOWN, before attempting RIGHT
            movements = {
                "up": (self.frontier[0], self.frontier[1] - 1),
                "left": (self.frontier[0] - 1, self.frontier[1]),
                "down": (self.frontier[0], self.frontier[1] + 1),
                "right": (self.frontier[0] + 1, self.frontier[1])
            }
            for direction, node in movements.items():
                if self.checkRoad(node):
                    self.expanded.append(node)
                    queue.append((node, self.path + [node], self.direction + [direction]))
        self.failed = True
        return f"{self.fileAddress} BFS\nNo goal is reachable; {len(self.expanded)}"

    def depthFirstSearch(self):
        # this changed to stack because we need LIFO
        stack = [(self.readFile.startPos, [], [])]
        while stack:
            self.frontier, self.path, self.direction = stack.pop()
            # we only expanding the route we trying
            if self.checkRoad(self.frontier):
                self.expanded.append(self.frontier)
            if self.frontier in self.readFile.goals:
                return f"{self.fileAddress} DFS\n<Node {self.frontier}> {len(self.expanded)}\n{self.direction}"
            movements = {
                "up": (self.frontier[0], self.frontier[1] - 1),
                "left": (self.frontier[0] - 1, self.frontier[1]),
                "down": (self.frontier[0], self.frontier[1] + 1),
                "right": (self.frontier[0] + 1, self.frontier[1])
            }
            # positions is reverse because DFS is LIFO
            for direction, node in reversed(movements.items()):
                if self.checkRoad(node):
                    stack.append((node, self.path + [node], self.direction + [direction]))
        self.failed = True
        return f"{self.fileAddress} DFS\nNo goal is reachable; {len(self.expanded)}"
    
    def greedyBestFirst(self):
        # apart from the frontier, path, direction, we also stored the heuristic cost of the node
        queue = deque([(self.readFile.startPos, [], [], self.heuristic(self.readFile.startPos, self.readFile.goals))])
        while queue:
            self.frontier, self.path, self.direction, cost = queue.popleft()
            if self.checkRoad(self.frontier):
                self.expanded.append(self.frontier)
            if self.frontier in self.readFile.goals:
                return f"{self.fileAddress} GBFS\n<Node {self.frontier}> {len(self.expanded)}\n{self.direction}"
            movements = {
                "up": (self.frontier[0], self.frontier[1] - 1),
                "left": (self.frontier[0] - 1, self.frontier[1]),
                "down": (self.frontier[0], self.frontier[1] + 1),
                "right": (self.frontier[0] + 1, self.frontier[1])
            }
            for direction, node in movements.items():
                if self.checkRoad(node):
                    queue.append((node, self.path + [node], self.direction + [direction], self.heuristic(node, self.readFile.goals)))
            # we can use merge sort or quick sort for this, however the default sorted uses Timsort, which I think is better than merge or quick sort for this
            # this sort it base on the cost of the heuristic function
            queue = deque(sorted(queue, key=lambda item: item[3]))
        self.failed = True
        return f"{self.fileAddress} GBFS\nNo goal is reachable; {len(self.expanded)}"

    def aStar(self):
        # we use 0 + heuristic to clarify that we need both heruistic cost and the total cost to get to that node, and since this is the starting node, we put 0 for the cost to the node
        queue = deque([(self.readFile.startPos, [], [], 0 + self.heuristic(self.readFile.startPos, self.readFile.goals))])
        # this is a dictionary to keep track of the actual cost to reach each node from the start node
        gCost = {self.readFile.startPos: 0}
        while queue:
            self.frontier, self.path, self.direction, cost = queue.popleft()
            if self.checkRoad(self.frontier):
                self.expanded.append(self.frontier)
            if self.frontier in self.readFile.goals:
                return f"{self.fileAddress} AS\n<Node {self.frontier}> {len(self.expanded)}\n{self.direction}"
            movements = {
                "up": (self.frontier[0], self.frontier[1] - 1),
                "left": (self.frontier[0] - 1, self.frontier[1]),
                "down": (self.frontier[0], self.frontier[1] + 1),
                "right": (self.frontier[0] + 1, self.frontier[1])
            }
            for direction, node in movements.items():
                if self.checkRoad(node):
                    # we get the new cost for the node by adding 1 to the frontier
                    newGCost = gCost[self.frontier] + 1
                    # if the node is not in the gCost(meaning that it's a new discovered node), or the current path to the node is more efficient, we replace/add the node into the dictionary
                    if node not in gCost or newGCost < gCost[node]:
                        # update the dictionary
                        gCost[node] = newGCost
                        fCost = newGCost + self.heuristic(node, self.readFile.goals)
                        # we add f cost instead of g cost for the queue
                        queue.append((node, self.path + [node], self.direction + [direction], fCost))
            # this part doesn't get changed because we are already storing the f cost of the route inside the queue, and we sort it base on that
            queue = deque(sorted(queue, key=lambda item: item[3]))
        self.failed = True
        return f"{self.fileAddress} AS\nNo goal is reachable; {len(self.expanded)}"

    def iterativeDeepeningDepthFirstSearch(self):
        # Iterate with increasing depth limits, sys.maxsize means the max size the system can handle
        for depth in range(sys.maxsize):
            if self.depthLimitedSearch(depth):
                return f"{self.fileAddress} IDDFS\n<Node {self.frontier}> {len(self.expanded)}\n{self.direction}\nDepth:{depth}"
        self.failed = True
        return f"{self.fileAddress} IDDFS\nNo goal is reachable; {len(self.expanded)}\nDepth:{depth}"

    # this part is basically depth first search with a limit
    def depthLimitedSearch(self, limit):
        # this also stores the depth
        stack = [(self.readFile.startPos, [], [], 0)]
        # expanded will reset every time we search
        self.expanded = []
        while stack:
            self.frontier, self.path, self.direction, depth = stack.pop()
            if self.checkRoad(self.frontier):
                self.expanded.append(self.frontier)
            if self.frontier in self.readFile.goals:
                return True
            # Check if the current depth is within the limit
            if depth < limit:
                # positions is reverse because DFS is LIFO
                movements = {
                    "up": (self.frontier[0], self.frontier[1] - 1),
                    "left": (self.frontier[0] - 1, self.frontier[1]),
                    "down": (self.frontier[0], self.frontier[1] + 1),
                    "right": (self.frontier[0] + 1, self.frontier[1])
                }
                for direction, node in reversed(movements.items()):
                    if self.checkRoad(node):
                        # just add 1 whenever we add new node so we know the depth
                        stack.append((node, self.path + [node], self.direction + [direction], depth + 1))
        return False
    
    def hillClimbingSearch(self):
        # we don't need an list or queue to store, because hill climbing only care the current node and ignore the rest
        current = self.readFile.startPos
        self.path = []
        self.direction = []
        while current not in self.readFile.goals:
            nextNode = None
            self.expanded.append(current)
            movements = {
                "up": (current[0], current[1] - 1),
                "left": (current[0] - 1, current[1]),
                "down": (current[0], current[1] + 1),
                "right": (current[0] + 1, current[1])
            }
            tempCost = float('inf')
            nextMove = None
            nextDirection = None
            # we are looking for a movement with the lowest cost and we ignore anything else and will not store it
            for direction, node in movements.items():
                if self.checkRoad(node):
                    # we store the current cost of the node and compare it to the best one we find so far. And replace it if the current route is better
                    currentCost = self.heuristic(node, self.readFile.goals)
                    if currentCost < tempCost:
                        tempCost = currentCost
                        nextMove = node
                        nextDirection = direction
            # if no next Move is found, we will just treat it as fail, even though there might be nodes that we didn't explore
            if nextMove is None:
                self.failed = True
                return f"{self.fileAddress} HC\nNo goal is reachable; {len(self.expanded)}"
            self.path.append(nextMove)
            self.direction.append(nextDirection)
            current = nextMove
        return f"{self.fileAddress} HC\n<Node {current}> {len(self.expanded)}\n{self.direction}"

    def checkRoad(self, node):
        if node[0] >= 0 and node[1] >= 0 and node[0] < self.readFile.gridSize[1] and node[1] < self.readFile.gridSize[0] and node not in self.readFile.walls and node not in self.expanded:
            return True
        else:
            return False
    
    def heuristic(self, node, goals):
        # set it to inf so any cost is basically lower than this
        low = float('inf')
        for goal in goals:
            route = abs(node[0] - goal[0]) + abs(node[1] - goal[1])
            if low > route:
                low = route
        return low
    
    def readFile(self):
        return self.readFile
    
    def expanded(self):
        return self.expanded
    
    def path(self):
        return self.path
    
    def frontier(self):
        return self.frontier
    
    def direction(self):
        return self.direction
    
    def failed(self):
        return self.failed