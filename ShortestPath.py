import random
import math
import operator
x_max = 15
y_max = 20

class Pos:
    x = 0
    y = 0
    
startPos = Pos()
startPos.x = 1
startPos.y = 18

goalPos = Pos()
goalPos.x = 14
goalPos.y = 0

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

StartPos = {'row':18,'col':1}
class ArduinoRobot:
    orientation = 0
    
    CurrPos         = {'col':StartPos['col'],'row':StartPos['row']}
    topRight        = {'col':StartPos['col'],'row':StartPos['row']}
    topLeft         = {'col':StartPos['col']-1,'row':StartPos['row']}
    bottomRight      = {'col':StartPos['col'],'row':StartPos['row']+1}
    bottomLeft     = {'col':StartPos['col']-1,'row':StartPos['row']+1}
    bumpLeftPos     = {'col':StartPos['col']-1,'row':StartPos['row']-1}
    bumpRightPos    = {'col':StartPos['col'],'row':StartPos['row']-1}

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

            self.bumpLeftPos['col'] = CurrPos['col']-1
            self.bumpLeftPos['row'] = CurrPos['row']-1

            self.bumpRightPos['col'] = CurrPos['col']
            self.bumpRightPos['row'] = CurrPos['row']-1
        elif(orientation == 1):

            self.topLeft['col'] = CurrPos['col']
            self.topLeft['row'] = CurrPos['row']

            self.bottomLeft['col'] = CurrPos['col']-1
            self.bottomLeft['row'] = CurrPos['row']
       
            self.bottomRight['col'] = CurrPos['col']-1
            self.bottomRight['row'] = CurrPos['row']+1

            self.topRight['col'] = CurrPos['col']
            self.topRight['row'] = CurrPos['row'] + 1

            self.bumpLeftPos['col'] = CurrPos['col']+1
            self.bumpLeftPos['row'] = CurrPos['row']

            self.bumpRightPos['col'] = CurrPos['col']+1
            self.bumpRightPos['row'] = CurrPos['row']+1

        elif(orientation == 2):
            self.bottomLeft['col'] = CurrPos['col']
            self.bottomLeft['row'] = CurrPos['row']

            self.bottomRight['col'] = CurrPos['col']-1
            self.bottomRight['row'] = CurrPos['row']

            self.topRight['col'] = CurrPos['col']-1
            self.topRight['row'] = CurrPos['row']+1

            self.topLeft['col'] = CurrPos['col']
            self.topLeft['row'] = CurrPos['row']+1

            self.bumpLeftPos['col'] = CurrPos['col']
            self.bumpLeftPos['row'] = CurrPos['row']+2

            self.bumpRightPos['col'] = CurrPos['col']-1
            self.bumpRightPos['row'] = CurrPos['row']+2
        else:
            self.bottomRight['col'] = CurrPos['col']
            self.bottomRight['row'] = CurrPos['row']

            self.topRight['col'] = CurrPos['col']-1
            self.topRight['row'] = CurrPos['row']

            self.topLeft['col'] = CurrPos['col']-1
            self.topLeft['row'] = CurrPos['row']+1

            self.bottomLeft['col'] = CurrPos['col']
            self.bottomLeft['row'] = CurrPos['row']+1
            
            self.bumpLeftPos['col'] = CurrPos['col']-2
            self.bumpLeftPos['row'] = CurrPos['row']+1

            self.bumpRightPos['col'] = CurrPos['col']-2
            self.bumpRightPos['row'] = CurrPos['row']

def TurnLeft(robot,arena):
    robot.orientation = (4 + robot.orientation - 1) % 4
    robot.UpdateCornerPositions()
    arena = updateArena(arena,robot)
    return arena

def TurnRight(robot,arena):
    robot.orientation = (robot.orientation + 1) % 4
    robot.UpdateCornerPositions()
    arena = updateArena(arena,robot)
    return arena

def MoveRobot(robot,arena):
    pastPos = robot.CurrPos
    if(robot.orientation==0):
        robot.CurrPos['row']-=1
    elif(robot.orientation==1):
        robot.CurrPos['col']+=1
    elif(robot.orientation==2):
        robot.CurrPos['row']+=1
    else:
        robot.CurrPos['col']-=1
    robot.UpdateCornerPositions()
    arena = updateArena(arena,robot)
    return arena

def updateArena(arena,robot):
    for i in range(y_max):
        for j in range(x_max):
            if robot.orientation==0:
                if ((i==robot.topRight['row'] and j==robot.topRight['col'])
                    or (i==robot.topLeft['row'] and j==robot.topLeft['col'])
                    or (i==robot.bottomLeft['row'] and j==robot.bottomLeft['col'])
                    or (i==robot.bottomRight['row'] and j==robot.bottomRight['col'])):
                        arena[i][j] = "^"
                elif arena[i][j] != "X":
                    arena[i][j] = 0
            elif robot.orientation==1:
                if ((i==robot.topRight['row'] and j==robot.topRight['col'])
                    or (i==robot.topLeft['row'] and j==robot.topLeft['col'])
                    or (i==robot.bottomLeft['row'] and j==robot.bottomLeft['col'])
                    or (i==robot.bottomRight['row'] and j==robot.bottomRight['col'])):
                        arena[i][j] = ">"
                elif arena[i][j] != "X":
                    arena[i][j] = 0
            elif robot.orientation==2:
                if ((i==robot.topRight['row'] and j==robot.topRight['col'])
                    or (i==robot.topLeft['row'] and j==robot.topLeft['col'])
                    or (i==robot.bottomLeft['row'] and j==robot.bottomLeft['col'])
                    or (i==robot.bottomRight['row'] and j==robot.bottomRight['col'])):
                        arena[i][j] = "V"
                elif arena[i][j] != "X":
                        arena[i][j] = 0
            elif robot.orientation==3:
                if ((i==robot.topRight['row'] and j==robot.topRight['col'])
                    or (i==robot.topLeft['row'] and j==robot.topLeft['col'])
                    or (i==robot.bottomLeft['row'] and j==robot.bottomLeft['col'])
                    or (i==robot.bottomRight['row'] and j==robot.bottomRight['col'])):
                        arena[i][j] = "<"
                elif arena[i][j] != "X":
                        arena[i][j] = 0
    return arena

def detectBump(robot,arena):
    if ((arena[robot.bumpLeftPos['row']][robot.bumpLeftPos['col']]==0 and
        arena[robot.bumpRightPos['row']][robot.bumpRightPos['col']]==0) and
        not(robot.orientation == 1 and robot.CurrPos['col'] == (x_max - 1)) and
        not(robot.orientation == 2 and robot.CurrPos['row'] == (y_max - 2)) and
        not(robot.orientation == 3 and robot.CurrPos['col'] == 1)):
        return False;
    else: return True

def findPossiblePath(arena):
    arenaP = arena
    for i in range(0,y_max-1):
        for j in range(1,x_max):
            if (arenaP[i][j] in {0,"0"} and
                arenaP[i+1][j] in {0,"0"} and
                arenaP[i][j-1] in {0,"0"} and
                arenaP[i+1][j-1] in {0,"0"}):
                    arenaP[i][j] = "0"
                    arenaP[i+1][j] = "0"
                    arenaP[i][j-1] = "0"
                    arenaP[i+1][j-1] = "0"
    return arenaP

def haha():
    arena = genArena()
    findPossiblePath(arena)
    printArena(arena)

class Node:                     #initial values to be changed
    pos = Pos()
    orientation = 0
    pathArray = []
    pathCost = 0
    hCost = 0

###########################################################################

def calculateHCost(xpos,ypos):
    return math.sqrt((xpos-goalPos.x)**2 + (ypos-goalPos.y)**2)
    
def shortestPath():
    #arena = genArena()
    arena = readArenaTxt()
    printArena(arena)
    #arenaP = findPossiblePath(arena)

    queueFirstNode = {'xpos':startPos.x, 'ypos':startPos.y, 'orientation':0, 'pathArray':[], 'pathCost':0, 'hCost':calculateHCost(startPos.x,startPos.y)}

    #queue = Node()
    #queueFirstNode['xpos'] = startPos.x
    #queueFirstNode['ypos'] = startPos.y
    #queueFirstNode['orientation'] = 0
    #queueFirstNode['pathArray'] = [startPos]
    #queueFirstNode['pathCost'] = 0
    #queueFirstNode['hCost'] = calculateHCost(startPos)

    aStarQueue = [queueFirstNode]
    
    finalPath = astar(arena,aStarQueue)

    if (finalPath == None):
        print "No possible path"
    else: print finalPath

    for i in range(len(finalPath)):
         yFinal = finalPath[i][1]
         xFinal = finalPath[i][0]
         arena[yFinal][xFinal] = "-"
    printArena(arena)

def checkBump(node,direction,arena):
    true = True
    false = False
    if (direction == "left"):
        if (node['orientation'] == 0):
            if ((node['xpos']-2) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']-2] == "0" and
                arena[node['ypos']+1][node['xpos']-2] == "0"):
                    return True
            else:
     #           print("false1")
                return false
        elif (node['orientation'] == 1):
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']-1) in range(0,y_max) and
                arena[node['ypos']-1][node['xpos']] == "0" and
                arena[node['ypos']-1][node['xpos']-1] == "0"):
                    return True
            else:
     #           print("false2")
                return false
        elif (node['orientation'] == 2):
            if ((node['xpos']+1) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']+1] == "0" and
                arena[node['ypos']+1][node['xpos']+1] == "0"):
                    return True
            else:
     #           print("false3")
                return false
        else:
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']+2) in range(0,y_max) and
                arena[node['ypos']+2][node['xpos']] == "0" and
                arena[node['ypos']+2][node['xpos']-1] == "0"):
                    return True
            else:
     #           print("false4")
                return false

    elif (direction == "right"): 
        if (node['orientation'] == 0):
            if ((node['xpos']+1) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']+1] == "0" and
                arena[node['ypos']+1][node['xpos']+1] == "0"):
                    return True
            else:
     #           print("false5")
                return false
        elif (node['orientation'] == 1):
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']+2) in range(0,y_max) and
                arena[node['ypos']+2][node['xpos']] == "0" and
                arena[node['ypos']+2] [node['xpos']-1]== "0"):
                    return True
            else:
    #            print("false6")
                return false
        elif (node['orientation'] == 2):
            if ((node['xpos']-2) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']-2] == "0" and
                arena[node['ypos']+1][node['xpos']-2] == "0"):
                    return true
            else:
    #            print("false7")
                return false
        else:
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']-1) in range(0,y_max) and
                arena[node['ypos']-1][node['xpos']] == "0" and
                arena[node['ypos']-1][node['xpos']-1] == "0"):
                    return True
            else:
                return false
    #            print("false8")

    else:
        if (node['orientation'] == 0):
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']-1) in range(0,y_max) and
                arena[node['ypos']-1][node['xpos']] == "0" and
                arena[node['ypos']-1][node['xpos']-1] == "0"):
                    return True
            else:
    #            print("false9")
                return false
        elif (node['orientation'] == 1):
            if ((node['xpos']+1) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']][node['xpos']+1] == "0" and
                arena[node['ypos']+1][node['xpos']+1] == "0"):
                    return true
            else:
    #            print("false10")
                return false
        elif (node['orientation'] == 2):
            if ((node['xpos']-1) in range(0,x_max) and
                (node['ypos']+2) in range(0,y_max) and
                arena[node['ypos']+2][node['xpos']] == "0" and
                arena[node['ypos']+2][node['xpos']-1] == "0"):
                    return true
            else:
     #           print("false11")
                return false
        else:
            if ((node['xpos']-2) in range(0,x_max) and
                (node['ypos']+1) in range(0,y_max) and
                arena[node['ypos']+1][node['xpos']-2] == "0" and
                arena[node['ypos']+1][node['xpos']-2] == "0"):
                    return true
            else:
     #           print("false12")
                return false

def astar(arena,queue):
    while (True):
        moveForwPos = Pos()
        moveLeftPos = Pos()
        moveRightPos = Pos()

        ##print("1)",end="")
        ##for i in range(len(queue)):
        ##    print("[",queue[i]['xpos'],",",queue[i]['ypos'],"]",end="")
        ##print("")
        
        node = queue[0]
        queue = queue[1:]

        '''print("2)",end="")
        for i in range(len(queue)):
            print("[",queue[i]['xpos'],",",queue[i]['ypos'],"]",end="")
        print("")'''

        ##print("Node: [",node['xpos']," ",node['ypos'],"]")
        ##print(node)
        #3print(node['pathArray'])

        moveForwardNode = {} #Node()
        moveLeftNode = {} #Node()
        moveRightNode = {} #Node()
        checkBumpForward = checkBump(node,"forward",arena)
        checkBumpLeft = checkBump(node,"left",arena)
        checkBumpRight = checkBump(node,"right",arena)

        ##print(checkBumpForward," ",checkBumpLeft," ",checkBumpRight)
    
        if node['orientation'] == 0:
            moveForwardNode['xpos'] = node['xpos']
            moveForwardNode['ypos'] = node['ypos']-1
            moveForwardNode['orientation'] = 0
            moveForwardNode['pathArray'] = node['pathArray'] + [[node['xpos'],node['ypos']]]
            moveForwardNode['pathCost'] = node['pathCost'] + 1
            moveForwardNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveForwardNode['xpos'],moveForwardNode['ypos'])
        
            moveLeftNode['xpos'] = node['xpos']-1
            moveLeftNode['ypos'] = node['ypos']
            moveLeftNode['orientation'] = 4
            moveLeftNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveLeftNode['pathCost'] = node['pathCost'] + 2
            moveLeftNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveLeftNode['xpos'],moveLeftNode['ypos'])

            moveRightNode['xpos'] = node['xpos']+1
            moveRightNode['ypos'] = node['ypos']
            moveRightNode['orientation'] = 1
            moveRightNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveRightNode['pathCost'] = node['pathCost'] + 2
            moveRightNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveRightNode['xpos'],moveRightNode['ypos'])
    
        elif node['orientation'] == 1:
            moveForwardNode['xpos'] = node['xpos']+1
            moveForwardNode['ypos'] = node['ypos']
            moveForwardNode['orientation'] = 1
            moveForwardNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveForwardNode['pathCost'] = node['pathCost'] + 2
            moveForwardNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveForwardNode['xpos'],moveForwardNode['ypos'])

            moveLeftNode['xpos'] = node['xpos']
            moveLeftNode['ypos'] = node['ypos']-1
            moveLeftNode['orientation'] = 0
            moveLeftNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveLeftNode['pathCost'] = node['pathCost'] + 2
            moveLeftNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveLeftNode['xpos'],moveLeftNode['ypos'])

            moveRightNode['xpos'] = node['xpos']
            moveRightNode['ypos'] = node['ypos']+1
            moveRightNode['orientation'] = 2
            moveRightNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveRightNode['pathCost'] = node['pathCost'] + 1
            moveRightNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveRightNode['xpos'],moveRightNode['ypos'])

        elif node['orientation'] == 2:
            moveForwardNode['xpos'] = node['xpos']
            moveForwardNode['ypos'] = node['ypos']+1
            moveForwardNode['orientation'] = 2
            moveForwardNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveForwardNode['pathCost'] = node['pathCost'] + 1
            moveForwardNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveForwardNode['xpos'],moveForwardNode['ypos'])

            moveLeftNode['xpos'] = node['xpos']+1
            moveLeftNode['ypos'] = node['ypos']
            moveLeftNode['orientation'] = 1
            moveLeftNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveLeftNode['pathCost']= node['pathCost'] + 2
            moveLeftNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveLeftNode['xpos'],moveLeftNode['ypos'])

            moveRightNode['xpos'] = node['xpos']-1
            moveRightNode['ypos'] = node['ypos']
            moveRightNode['orientation'] = 3
            moveRightNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveRightNode['pathCost'] = node['pathCost'] + 2
            moveRightNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveRightNode['xpos'],moveRightNode['ypos'])

        else:
            moveForwardNode['xpos'] = node['xpos']-1
            moveForwardNode['ypos'] = node['ypos']
            moveForwardNode['orientation'] = 3
            moveForwardNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveForwardNode['pathCost'] = node['pathCost'] + 1
            moveForwardNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveForwardNode['xpos'],moveForwardNode['ypos'])

            moveLeftNode['xpos'] = node['xpos']
            moveLeftNode['ypos'] = node['ypos']+1
            moveLeftNode['orientation'] = 2
            moveLeftNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveLeftNode['pathCost'] = node['pathCost'] + 2
            moveLeftNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveLeftNode['xpos'],moveLeftNode['ypos'])

            moveRightNode['xpos'] = node['xpos']
            moveRightNode['ypos'] = node['ypos']-1
            moveRightNode['orientation'] = 0
            moveRightNode['pathArray'] = node['pathArray']+ [[node['xpos'],node['ypos']]]
            moveRightNode['pathCost'] = node['pathCost'] + 2
            moveRightNode['hCost'] = moveForwardNode['pathCost'] + calculateHCost(moveRightNode['xpos'],moveRightNode['ypos'])
        
        ##print(moveForwardNode)
        ##print(moveLeftNode)
        ##print(moveRightNode)
        ##print("")
        ##print(queue)

        if (checkBumpForward and checkNodeinQueue(moveForwardNode,queue)):
            queue.append(moveForwardNode)
            ##print("forward checked")
        if (checkBumpLeft and checkNodeinQueue(moveLeftNode,queue)):
            queue.append(moveLeftNode)
            ##print("left checked")
        if (checkBumpRight and checkNodeinQueue(moveRightNode,queue)):
            queue.append(moveRightNode)
            ##print("right checked")

        ##print("")
        ##print("3)",end="")
        ##for i in range(len(queue)):
        ##    print("[",queue[i]['xpos'],",",queue[i]['ypos'],"]",end="")
        ##print("")
        
        queue = sorted(queue, key=operator.itemgetter('hCost'))

        ##print("4)",end="")
        ##for i in range(len(queue)):
        ##    print("[",queue[i]['xpos'],",",queue[i]['ypos'],"]",end="")
        ##print("")

        if (queue == []):
            return None
            break
        elif (queue[0]['xpos'] == goalPos.x and queue[0]['ypos'] == goalPos.y):
            ##print("\n",queue[0]['xpos'],",",queue[0]['ypos'],"\nPathArray:",queue[0]['pathArray'])
            return (queue[0]['pathArray'] + [[queue[0]['xpos'],queue[0]['ypos']]])
            break
        #else:
            ##print("\n",queue[0]['xpos'],",",queue[0]['ypos'],"\nPathArray:",queue[0]['pathArray'])
            #return astar(arena,queue)

def checkNodeinQueue(node,queue):
    i = 0
    while (i in range(len(queue))):
    #for i in range(len(queue)):
        ##print("hahaStart",i)
        ##print(queue)
        ##print("Length: ",len(queue),"\n")
        if (node['xpos'] == queue[i]['xpos'] and
            node['ypos'] == queue[i]['ypos']):
            #print("QueueHCost: ", queue[i]['hCost'])
            #print("NodeHCost: ",node['hcost'])
            if (node['hCost'] >= queue[i]['hCost']):
                return False;
            else:
                queue = queue[:i] + queue[(i+1):]
        i += 1
        ##print("haha",i)
    return True;

def readArenaTxt():
    arena=[[0 for i in range(x_max)] for j in range(y_max)]
    i = 0
    j = 0
    start = 1
    with open("test11.txt") as f:
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
    
                
            
