class FileReader:
    def __init__(self, filePath):
        self.gridSize = (0, 0)
        self.startPos = (0, 0)
        self.goals = []
        # this will avoid wall with same xy stacking
        self.walls = set()
        self.readNavigationFile(filePath)

    def readNavigationFile(self, filePath):
        with open(filePath, 'r') as file:
            # we read the grid size, strip the bracket and split it by comma(it is still a string list)
            read_gridSize = file.readline().strip()[1:-1].split(",")
            # we turn the string list into a int tuple by runing a for loop in read grid size
            self.gridSize = tuple(int(i) for i in read_gridSize)
            # we are doing the same thing here
            read_startPos = file.readline().strip()[1:-1].split(",")
            self.startPos = tuple(int(i) for i in read_startPos)
            # this looks slightly more complicated, but it is the same thing, we store the whole list split by |, and then for each of those item, we do the same thing above, and then append it to a new list
            read_goals = file.readline().strip().split('|')
            for i in read_goals:
                read_goal = i.strip()[1:-1].split(",")
                goal = tuple(int(i) for i in read_goal)
                self.goals.append(goal)
            # this is a really clever design in my opinion, we take x,y,width,height from each line, turn it to a int and then we create walls with it, we convert the width and height into walls so (2,0,2,2) will turn into (2, 0), (2, 1), (3, 0), (3, 1), this will make it easier when we want to know if the position we are going have a wall
            for line in file:
                read_wall = line.strip("()\n ").split(",")
                wall = tuple(int(i) for i in read_wall)
                x = int(wall[0])
                y = int(wall[1])
                width = int(wall[2])
                height = int(wall[3])
                for column in range(width):
                    for row in range(height):
                        current_position = (x + column, y + row)
                        self.walls.add(current_position)

    def gridSize(self):
        return self.gridSize

    def startPos(self):
        return self.startPos

    def goals(self):
        return self.goals

    def walls(self):
        return self.walls