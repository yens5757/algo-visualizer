from algorithm import Algorithm
import pygame

class Drawgui:
    def __init__(self, algorithm):
        # this is just init the pygame as well as storing the algorithm data
        pygame.init()
        self.screenWidth = 800
        self.screenHeight = 600
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.run = True
        self.file = algorithm.readFile
        self.algorithm = algorithm
        self.blockSize = min(self.screenWidth // self.file.gridSize[1], self.screenHeight // self.file.gridSize[0])
        if self.file.gridSize[0] * self.file.gridSize[1] > 2500:
            self.outlineWidth = 1
        else:
            self.outlineWidth = 3
        
    # this draws the diagram for the solution
    def draw(self):
        self.screen.fill((255, 255, 255))
        delay = 100
        currentTime = pygame.time.get_ticks()
        lastTime = pygame.time.get_ticks()
        pathPointer = 0
        expandedPointer = 0

        # since the grid, walls, startpos in static, we can leave it away from the game loop, this also make the loop easier to run, therefore increasing the fps(frames per seconds)
        # fps also changes the program speed
        # draw the grid
        for ygrid in range(self.file.gridSize[0]):
            for xgrid in range(self.file.gridSize[1]):
                self.drawGrid(xgrid, ygrid, (255, 255, 255))
        # draw the walls
        for wall in self.file.walls:
            self.drawGrid(wall[0], wall[1], (128, 128, 128))
        # draw the start pos
        self.drawGrid(self.file.startPos[0], self.file.startPos[1], (255, 0 , 0))
        # draw the goals
        for goal in self.file.goals:
            self.drawGrid(goal[0], goal[1], (0, 255, 0))
        
        startdrawPath = False
        while self.run:
            # get the current time
            currentTime = pygame.time.get_ticks()
            # draw the expanded
            if not startdrawPath:
                if (currentTime - lastTime >= delay and expandedPointer < len(self.algorithm.expanded)):
                    expandedNode = self.algorithm.expanded[expandedPointer]
                    if expandedNode not in self.file.goals and expandedNode != self.file.startPos:
                        self.drawGrid(expandedNode[0], expandedNode[1], (200, 200, 200))
                    expandedPointer += 1
                    lastTime = currentTime
            
            # keep track of the expanded drawn, if every expanded is drawn, start drawing path
            if expandedPointer >= len(self.algorithm.expanded):
                startdrawPath = True

            # draw the path
            if startdrawPath and not self.algorithm.failed:
                if (currentTime - lastTime >= delay and pathPointer < len(self.algorithm.path)):
                    path = self.algorithm.path[pathPointer]
                    if path not in self.file.goals and expandedNode != self.file.startPos:
                        self.drawGrid(path[0], path[1], (128, 128, 255))
                    pathPointer += 1
                    lastTime = currentTime
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.flip()
        pygame.QUIT
    
    def drawGrid(self, xPos, yPos,  color):
        x = xPos * self.blockSize
        y = yPos * self.blockSize
        pygame.draw.rect(self.screen, color, (x, y, self.blockSize, self.blockSize))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.blockSize, self.blockSize), self.outlineWidth)