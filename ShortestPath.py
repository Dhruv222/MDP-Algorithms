#############################################################
## enter shortestPath() to start calculating shortest path ##
#############################################################

import random
import math
import operator
x_max = 15
y_max = 20
    
startPos = {'x':1,'y':18}
goalPos  = {'x':14,'y':0}

# random arena generator
def genArena():
    arena=[[0 for i in range(x_max)] for j in range(y_max)]
    for i in range(y_max):
        for j in range(x_max):
            randnum = random.randint(1, 20)
            if randnum < 4:
                arena[i][j] = "X"

    arena[0][14] = 0
    arena[0][13] = 0
    arena[0][12] = 0
    arena[1][14] = 0
    arena[1][13] = 0
    arena[1][12] = 0
    arena[2][14] = 0
    arena[2][13] = 0
    arena[2][12] = 0
    
    arena[19][0] = 0
    arena[19][1] = 0
    arena[19][2] = 0
    arena[18][0] = 0
    arena[18][1] = 0
    arena[18][2] = 0
    arena[17][0] = 0
    arena[17][1] = 0
    arena[17][2] = 0
    
    print "\n"
    return arena

# print arena
def printArena(arena):
    print "| - - - - - - - - - - - - - - - |"
    for i in range(y_max):
        print "|",
        for j in range(x_max):
            if arena[i][j] == -1:
                print "-1 ",
            else:
                print arena[i][j],
        print "|"
    print "| - - - - - - - - - - - - - - - |"

# calculate heuristic cost for A* algorithm (distance from node position to goal position)
def calculateHCost(xpos,ypos):
    return math.sqrt((xpos-goalPos['x'])**2 + (ypos-goalPos['y'])**2)

# check if moving forward/left/right is possible
#   orientation = 0 => robot facing north
#   orientation = 1 => robot facing east
#   orientation = 2 => robot facing south
#   orientation = 3 => robot facing west
def checkBump(node,direction,arena):
    if (direction == "left"):
        if (node['orientation'] == 0):
            if ((node['xpos']-2) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']-2] == "0" and
                arena[node['ypos']+1][node['xpos']-2] == "0"):
                    return True
            else: return False
        elif (node['orientation'] == 1):
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']-1) in range(0,y_max) and
                arena[node['ypos']-1][node['xpos']] == "0" and
                arena[node['ypos']-1][node['xpos']-1] == "0"):
                    return True
            else: return False
        elif (node['orientation'] == 2):
            if ((node['xpos']+1) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']+1] == "0" and
                arena[node['ypos']+1][node['xpos']+1] == "0"):
                    return True
            else: return False
        else:
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']+2) in range(0,y_max) and
                arena[node['ypos']+2][node['xpos']] == "0" and
                arena[node['ypos']+2][node['xpos']-1] == "0"):
                    return True
            else: return False

    elif (direction == "right"): 
        if (node['orientation'] == 0):
            if ((node['xpos']+1) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']+1] == "0" and
                arena[node['ypos']+1][node['xpos']+1] == "0"):
                    return True
            else: return False
        elif (node['orientation'] == 1):
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']+2) in range(0,y_max) and
                arena[node['ypos']+2][node['xpos']] == "0" and
                arena[node['ypos']+2] [node['xpos']-1]== "0"):
                    return True
            else: return False
        elif (node['orientation'] == 2):
            if ((node['xpos']-2) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']-2] == "0" and
                arena[node['ypos']+1][node['xpos']-2] == "0"):
                    return True
            else: return False
        else:
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']-1) in range(0,y_max) and
                arena[node['ypos']-1][node['xpos']] == "0" and
                arena[node['ypos']-1][node['xpos']-1] == "0"):
                    return True
            else:
                return False

    else:
        if (node['orientation'] == 0):
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']-1) in range(0,y_max) and
                arena[node['ypos']-1][node['xpos']] == "0" and
                arena[node['ypos']-1][node['xpos']-1] == "0"):
                    return True
            else: return False
        elif (node['orientation'] == 1):
            if ((node['xpos']+1) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']+1] == "0" and
                arena[node['ypos']+1][node['xpos']+1] == "0"):
                    return True
            else: return False
        elif (node['orientation'] == 2):
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']+2) in range(0,y_max) and
                arena[node['ypos']+2][node['xpos']] == "0" and
                arena[node['ypos']+2][node['xpos']-1] == "0"):
                    return True
            else: return False
        else:
            if ((node['xpos']-2) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']+1][node['xpos']-2] == "0" and
                arena[node['ypos']+1][node['xpos']-2] == "0"):
                    return True
            else: return False

# A* algorithm function for calculating shortest path
def astar(arena,queue):
    visitedNodes = [[18,1]]
    while (True):   
        node = queue[0]
        queue = queue[1:]
        visitedNodes += [[node['ypos'],node['xpos']]]

        moveForwardNode = {} 
        moveLeftNode = {} 
        moveRightNode = {} 
        checkBumpForward = checkBump(node,"forward",arena)
        checkBumpLeft = checkBump(node,"left",arena)
        checkBumpRight = checkBump(node,"right",arena)

        # 'xpos'        => next column position
        # 'ypos'        => next row position
        # 'orientation' => direction faced by robot
        # 'pathArray'   => previous nodes visited by robot until this node only
        # 'pathCost'    => number of steps taken
        # 'fCost'       => pathCost + heuristic cost
        # if required turning, pathCost increases by 2; else increases by 1
        if node['orientation'] == 0:
            moveForwardNode['xpos'] = node['xpos']
            moveForwardNode['ypos'] = node['ypos']-1
            moveForwardNode['orientation'] = 0
            moveForwardNode['pathArray'] = node['pathArray'] + [[node['xpos'],node['ypos']]]
            moveForwardNode['pathCost'] = node['pathCost'] + 1
            moveForwardNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveForwardNode['xpos'],moveForwardNode['ypos'])
        
            moveLeftNode['xpos'] = node['xpos']-1
            moveLeftNode['ypos'] = node['ypos']
            moveLeftNode['orientation'] = 4
            moveLeftNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveLeftNode['pathCost'] = node['pathCost'] + 2
            moveLeftNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveLeftNode['xpos'],moveLeftNode['ypos'])

            moveRightNode['xpos'] = node['xpos']+1
            moveRightNode['ypos'] = node['ypos']
            moveRightNode['orientation'] = 1
            moveRightNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveRightNode['pathCost'] = node['pathCost'] + 2
            moveRightNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveRightNode['xpos'],moveRightNode['ypos'])
    
        elif node['orientation'] == 1:
            moveForwardNode['xpos'] = node['xpos']+1
            moveForwardNode['ypos'] = node['ypos']
            moveForwardNode['orientation'] = 1
            moveForwardNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveForwardNode['pathCost'] = node['pathCost'] + 2
            moveForwardNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveForwardNode['xpos'],moveForwardNode['ypos'])

            moveLeftNode['xpos'] = node['xpos']
            moveLeftNode['ypos'] = node['ypos']-1
            moveLeftNode['orientation'] = 0
            moveLeftNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveLeftNode['pathCost'] = node['pathCost'] + 2
            moveLeftNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveLeftNode['xpos'],moveLeftNode['ypos'])

            moveRightNode['xpos'] = node['xpos']
            moveRightNode['ypos'] = node['ypos']+1
            moveRightNode['orientation'] = 2
            moveRightNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveRightNode['pathCost'] = node['pathCost'] + 1
            moveRightNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveRightNode['xpos'],moveRightNode['ypos'])

        elif node['orientation'] == 2:
            moveForwardNode['xpos'] = node['xpos']
            moveForwardNode['ypos'] = node['ypos']+1
            moveForwardNode['orientation'] = 2
            moveForwardNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveForwardNode['pathCost'] = node['pathCost'] + 1
            moveForwardNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveForwardNode['xpos'],moveForwardNode['ypos'])

            moveLeftNode['xpos'] = node['xpos']+1
            moveLeftNode['ypos'] = node['ypos']
            moveLeftNode['orientation'] = 1
            moveLeftNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveLeftNode['pathCost']= node['pathCost'] + 2
            moveLeftNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveLeftNode['xpos'],moveLeftNode['ypos'])

            moveRightNode['xpos'] = node['xpos']-1
            moveRightNode['ypos'] = node['ypos']
            moveRightNode['orientation'] = 3
            moveRightNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveRightNode['pathCost'] = node['pathCost'] + 2
            moveRightNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveRightNode['xpos'],moveRightNode['ypos'])

        else:
            moveForwardNode['xpos'] = node['xpos']-1
            moveForwardNode['ypos'] = node['ypos']
            moveForwardNode['orientation'] = 3
            moveForwardNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveForwardNode['pathCost'] = node['pathCost'] + 1
            moveForwardNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveForwardNode['xpos'],moveForwardNode['ypos'])

            moveLeftNode['xpos'] = node['xpos']
            moveLeftNode['ypos'] = node['ypos']+1
            moveLeftNode['orientation'] = 2
            moveLeftNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveLeftNode['pathCost'] = node['pathCost'] + 2
            moveLeftNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveLeftNode['xpos'],moveLeftNode['ypos'])

            moveRightNode['xpos'] = node['xpos']
            moveRightNode['ypos'] = node['ypos']-1
            moveRightNode['orientation'] = 0
            moveRightNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveRightNode['pathCost'] = node['pathCost'] + 2
            moveRightNode['fCost'] = moveForwardNode['pathCost'] + calculateHCost(moveRightNode['xpos'],moveRightNode['ypos'])

        if (checkBumpForward and checkNodeinQueue(moveForwardNode,queue,visitedNodes)):
            if ([moveForwardNode['ypos'],moveForwardNode['xpos']] not in visitedNodes):
                queue.append(moveForwardNode)
                ##visitedNodes += [[moveForwardNode['ypos'],moveForwardNode['xpos']]]
        if (checkBumpLeft and checkNodeinQueue(moveLeftNode,queue,visitedNodes)):
            if ([moveLeftNode['ypos'],moveLeftNode['xpos']] not in visitedNodes):
                queue.append(moveLeftNode)
                ##visitedNodes += [[moveLeftNode['ypos'],moveLeftNode['xpos']]]
        if (checkBumpRight and checkNodeinQueue(moveRightNode,queue,visitedNodes)):
            if ([moveRightNode['ypos'],moveRightNode['xpos']] not in visitedNodes):
                queue.append(moveRightNode)
                ##visitedNodes += [[moveRightNode['ypos'],moveRightNode['xpos']]]

        queue = sorted(queue, key=operator.itemgetter('fCost'))
        #print visitedNodes, '\n'

        if (queue == []):
            return None
            break
        elif (queue[0]['xpos'] == goalPos['x'] and queue[0]['ypos'] == goalPos['y']):
            return (queue[0]['pathArray'] + [[queue[0]['xpos'],queue[0]['ypos']]])
            break

def checkNodeinQueue(node,queue,visitedNodes):
    i = 0
    while (i in range(len(queue))):
        if (node['xpos'] == queue[i]['xpos'] and
            node['ypos'] == queue[i]['ypos']):
            if (node['fCost'] >= queue[i]['fCost']):
                return False
            #elif ([node['ypos'],node['xpos']] not in queue and [node['ypos'],node['xpos']] in visitedNodes):
                #print "haha"
                #return False;
            else:
                #queue = queue[:i] + [node['ypos'],node['xpos']] + queue[(i+1):]
                #return False
                queue = queue[:i] + queue[(i+1):]
                i -= 1       
        i += 1
    return True;

def readArenaTxt():
    arena=[[0 for i in range(x_max)] for j in range(y_max)]
    i = 0
    j = 0
    start = 1
    with open("test12.txt") as f:
        c = f.read(1)
        while c:
            while (c != "\n" and c):
                if start != 0:
                    start = 0
                else: c = f.read(1)              
                arena[i][j] = c
                j += 1
                c = f.read(1)
            i+=1
            j=0
            start = 1
            c = f.read(1)
    return arena

# insert shortestPath() to start finding shortest path    
def shortestPath():
    arena = readArenaTxt()
    printArena(arena)

    queueFirstNode = {'xpos':startPos['x'], 'ypos':startPos['y'], 'orientation':0, 'pathArray':[], 'pathCost':0, 'hCost':calculateHCost(startPos['x'],startPos['y'])}

    aStarQueue = [queueFirstNode]
    
    finalPath = astar(arena,aStarQueue)

    if (finalPath == None):
        print "No possible path"
    else:
        print finalPath
        for i in range(len(finalPath)):
             yFinal = finalPath[i][1]
             xFinal = finalPath[i][0]
             arena[yFinal][xFinal] = "-"
        printArena(arena)

shortestPath()
                
            
