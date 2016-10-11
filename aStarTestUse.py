# Authors: 
# A* Pathfinding in Python (2.7) by Christian Careaga (christian.careaga7@gmail.com)
# ArduinoRobot class by Dhruv Sharma

# TODO: Make the algo work while avoiding 2 (aka close to the obstacle).
    #DONE
# TODO: Talk with Arduino team on moving left/right and research on Arduino library
    #DONE
# TODO Implement the ArduinoRobot class
# TODO: Visualize the progress to Android, PENDING ON THURSDAY
# TODO: Go for Visa internship *poke Dhruv

import numpy
from heapq import *
from serial import Serial

startzone = [(17,0),(17,1),(17,2),(18,0),(18,1),(18,2),(19,0),(19,1),(19,2)]
goalzone = [(0,12),(0,13),(0,14),(1,12),(1,13),(1,14),(2,12),(2,13),(2,14)]

direction = []

nmap1 = numpy.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]])

StartPos = {
    'row':18,
    'col':1
}

GoalPos = {
    'row':1,
    'col':13
}

EmptyArena = nmap1

class ArduinoRobot:
    CurrPos = {
        'col':StartPos['col'],
        'row':StartPos['row']
    }
    topRight = {
        'col':StartPos['col'],
        'row':StartPos['row']
    }
    topLeft = {
        'col':StartPos['col']-1,
        'row':StartPos['row']
    }
    bottomRight = {
        'col': StartPos['col'],
        'row': StartPos['row']+1
    }
    bottomLeft = {
        'col': StartPos['col']-1,
        'row': StartPos['row']+1
    }
    orientation = 0

    def UpdateCurPosVisited(self):
        EmptyArena[self.topLeft['row']][self.topLeft['col']] = 2
        EmptyArena[self.topRight['row']][self.topRight['col']] = 2
        EmptyArena[self.bottomLeft['row']][self.bottomLeft['col']] = 2
        EmptyArena[self.bottomRight['row']][self.bottomRight['col']] = 2

    def UpdateCornerPositions(self):
        orientation = self.orientation
        CurrPos = self.CurrPos
        if(orientation == 0):
            self.topRight['col'] = CurrPos['col']
            self.topRight['row'] = CurrPos['row']

            self.topLeft['col'] = CurrPos['col']-1
            self.topLeft['row'] = CurrPos['row']

            self.bottomRight['col'] = CurrPos['col']
            self.bottomRight['row'] = CurrPos['row']+1

            self.bottomLeft['col'] = CurrPos['col']-1
            self.bottomLeft['row'] = CurrPos['row']+1
        elif(orientation == 1):

            self.topLeft['col'] = CurrPos['col']
            self.topLeft['row'] = CurrPos['row']

            self.bottomLeft['col'] = CurrPos['col']-1
            self.bottomLeft['row'] = CurrPos['row']
       
            self.bottomRight['col'] = CurrPos['col']-1
            self.bottomRight['row'] = CurrPos['row']+1

            sedlf.topRight['col'] = CurrPos['col']
            self.topRight['row'] = CurrPos['row'] + 1

        elif(orientation == 2):
            self.bottomLeft['col'] = CurrPos['col']
            self.bottomLeft['row'] = CurrPos['row']

            self.bottomRight['col'] = CurrPos['col']-1
            self.bottomRight['row'] = CurrPos['row']

            self.topRight['col'] = CurrPos['col']-1
            self.topRight['row'] = CurrPos['row']+1

            self.topLeft['col'] = CurrPos['col']
            self.topLeft['row'] = CurrPos['row']+1
        else:
            self.bottomRight['col'] = CurrPos['col']
            self.bottomRight['row'] = CurrPos['row']

            self.topRight['col'] = CurrPos['col']-1
            self.topRight['row'] = CurrPos['row']

            self.topLeft['col'] = CurrPos['col']-1
            self.topLeft['row'] = CurrPos['row']+1

            self.bottomLeft['col'] = CurrPos['col']
            self.bottomLeft['row'] = CurrPos['row']+1

    def __init__(self):
        self.UpdateCurPosVisited()

def initiateCom():
    while(1==1):
        if(DataChannel.inWaiting()>0):
            InitCode = DataChannel.readline()
            if(InitCode=="Ready"):
                print "Arduino Ready"
                return true
            else:
                print "Error! Arduino sent this Data:"+InitCode
                return false

def TurnRobot(robot, direction):
    #DataChannel.write("turn "+direction)
    if ( direction == "right"):
        robot.orientation = (robot.orientation + 1) % 4
    else:
        robot.orientation = (4 + robot.orientation - 1) % 4

    robot.UpdateCornerPositions()
    return

def MoveRobot(robot, blocks):
    #DataChannel.write("move "+blocks)
    pastPos = robot.CurrPos
    if(robot.orientation==0):
        for i in range(blocks):
            robot.CurrPos['row']-=(1)
            robot.UpdateCornerPositions()
            robot.UpdateCurPosVisited()
    elif(robot.orientation==1):
        for i in range(blocks):
            robot.CurrPos['col']+=1
            robot.UpdateCornerPositions()
            robot.UpdateCurPosVisited()
    elif(robot.orientation==2):
        for i in range(blocks):
            robot.CurrPos['row']+=1
            robot.UpdateCornerPositions()
            robot.UpdateCurPosVisited()
    else:
        for i in range(blocks):
            robot.CurrPos['col']-=1
            robot.UpdateCornerPositions()
            robot.UpdateCurPosVisited()
    
    return
#TODO:Refactor Update Arena
def UpdateArena(robot):
    
    if(robot.orientation==0):
        mul = mulfactor['north']
    elif(robot.orientation==1):
        mul = mulfactor['east']
    elif(robot.orientation==2):
        mul = mulfactor['south']
    else:
        mul = mulfactor['west']

def heuristic(a, b):
	return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

def adjacent(array):
	arrayshape = array.shape
	neighbours = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
	for a in range(arrayshape[0]):
		for b in range(arrayshape[1]):
			current = array[a][b]
			for i, j in neighbours:
				neighbour = a + i, b + j
				if 0 <= neighbour[0] < array.shape[0]:
					if 0 <= neighbour[1] < array.shape[1]:
						if array[neighbour[0]][neighbour[1]] == 0 and current == 1:                                
							array[neighbour[0]][neighbour[1]] = 2
	for i in range(arrayshape[0]):
		if array[i][0] == 0:
			array[i][0] = 2
		if array[i][arrayshape[1]-1] == 0:
			array[i][arrayshape[1]-1] = 2
	for j in range(arrayshape[1]):
		if array[0][j] == 0:
			array[0][j] = 2
		if array[arrayshape[0]-1][j] == 0:
			array[arrayshape[0]-1][j] = 2
			
	#assume start and goal are clear!
	for i, j in goalzone:
		array[i][j] = 0
	for i, j in startzone:
		array[i][j] = 0

	#for i in range(arrayshape[0]):
	#	print(array[i])
	return False
	
def astar1(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    global route
    route = []
    
    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            route = []
            while current in came_from:
                route.append(current)
                current = came_from[current]
            route.append(start)
            return route

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] != 0:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return void

def astar2(array, robot):

    neighbors = [
        [(0,2),(-1,2)],
        [(0,-1),(-1,-1)],
        [(1,0),(-2,0)],
        [(1,1),(-2,1)]]

    startcol = StartPos['col']
    startrow = StartPos['row']
    start = (startcol,startrow)
    goalcol = GoalPos['col']
    goalrow = GoalPos['row']
    goal = (goalcol,goalrow)
    
    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))

    global route
    route = []
    
    while oheap:

        current = heappop(oheap)[1]

        if robot.CurrPos == GoalPos:
            route = []
            while robot.CurrPos in came_from:
                route.append(current)
                current = came_from[current]
            route.append(start)
            
            return route

        close_set.add(current)
        for i, j in neighbors:
            neighbor = robot.CurrPos['col'] + i, robot.CurrPos['row'] + j            
            tentative_g_score = gscore[current] + heuristic(robot.currPos, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        #obstacle!
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                 
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return void
	
def robotdirection(array1):
    global directionlist
    directionlist = []
    
    for i in range(len(array1) - 1):
        direction1 = array1[i+1][0] - array1[i][0]
        direction2 = array1[i+1][1] - array1[i][1]
        direction = (direction1,direction2)

        if direction == (0,1):
            directionlist.append(1)
        elif direction == (0,-1):
            directionlist.append(3)
        elif direction == (1,0):
            directionlist.append(2)
        elif direction == (-1,0):
            directionlist.append(0)
        else:
            directionlist.append(-1)
    return directionlist

def robotmotion(array,initialdirection):
    #can be changed to robot movement
    global motion
    motion = []
    counter = 0
    
    for i in range(len(array)):
        if i == 0:
            if initialdirection == array[0]:
                print ("straight", counter)
            else:
                print ("straight", counter)
                motion.append(("straight", counter))
                print ("right")
                motion.append(("right",0))
                print ("straight", counter)
        else:
            print ("straight", counter)
            counter += 1
            if array[i-1] == array[i]:
                continue
            else:
                print ("straight", counter)
                counter += 1
                print ("straight", counter)
                motion.append(("straight", counter))
                counter = 0
                #turn left
                if (array[i-1] - array[i]) % 4 == 1:
                    print ("left")
                    motion.append(("left",0))
                    continue 
                #turn right
                else:
                    print ("right")
                    motion.append(("right",0))
    motion.append(("straight", counter))
    return motion

def rotate (topright,dir1,dir2):
    if dir1 == 0:
        if  dir2 == 3:
            topright[0] -= 1
        else:
            topright[1] += 1
    elif dir1 == 1:
        if dir2 == 0:
            topright[1] -= 1
        else:
            topright[0] -= 1
    elif dir1 == 2:
        if dir2 == 1:
            topright[0] += 1
        else:
            topright[1] -= 1
    else:
        if dir2 == 2:
            topright[1] += 1
        else:
            topright[0] += 1

def pathway (maparray,topright,direction):
    if direction == 0:
        topleft = (topright[0]-1,topright[1])
        bottomleft = (topright[0]-1,topright[1]-1)
           bottomright = (topright[0],topright[1]-1)
    elif direction == 1:
        topleft = (topright[0],topright[1]+1)
        bottomleft = (topright[0]-1,topright[1]+1)
        bottomright = (topright[0]-1,topright[1])
    elif direction == 2:
        topleft = (topright[0]+1,topright[1])
        bottomleft = (topright[0]+1,topright[1]+1)
        bottomright = (topright[0],topright[1]+1)
    elif direction == 3:
        topleft = (topright[0],topright[1]+1)
        bottomleft = (topright[0]+1,topright[1]+1)
        bottomright = (topright[0],topright[1]+1)
    
    maparray[topleft[0]][topleft[1]] = 9
    maparray[topright[0]][topright[1]] = 8
    maparray[bottomleft[0]][bottomright[1]] = 7
    maparray[bottomright[0]][bottomright[1]] = 6

    return maparray

def cleanpathway (maparray,topright,direction):
    if direction == 0:
        topleft = (topright[0]-1,topright[1])
        bottomleft = (topright[0]-1,topright[1]-1)
        bottomright = (topright[0],topright[1]-1)
    elif direction == 1:
        topleft = (topright[0],topright[1]+1)
        bottomleft = (topright[0]-1,topright[1]+1)
        bottomright = (topright[0]-1,topright[1])
    elif direction == 2:
        topleft = (topright[0]+1,topright[1])
        bottomleft = (topright[0]+1,topright[1]+1)
        bottomright = (topright[0],topright[1]+1)
    elif direction == 3:
        topleft = (topright[0],topright[1]+1)
        bottomleft = (topright[0]+1,topright[1]+1)
        bottomright = (topright[0],topright[1]+1)

    maparray[topleft[0]][topleft[1]] = '0'
    maparray[topright[0]][topright[1]] = '0'
    maparray[bottomleft[0]][bottomright[1]] = '0'
    maparray[bottomright[0]][bottomright[1]] = '0'

    return False
    
#commands here!

print adjacent(nmap1)
robot = ArduinoRobot()

print ('1')

print astar1(nmap1, (18,1),(1,13))
route.reverse()
print route

astar2(nmap1, robot)
#route.reverse()
#route
#direction(route)
#print robotmotion(directionlist,0)
