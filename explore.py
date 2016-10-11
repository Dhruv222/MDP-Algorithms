import simulator
import time
import pc_test_socket

EmptyArena=[[0 for i in range(17)] for j in range(22)]

StartPos = {
    'row':18,
    'col':3
}

GoalPos = {
    'row':1,
    'col':15
}

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
        'col':StartPos['col']-2,
        'row':StartPos['row']
    }
    bottomRight = {
        'col': StartPos['col'],
        'row': StartPos['row']+2
    }
    bottomLeft = {
        'col': StartPos['col']-2,
        'row': StartPos['row']+2
    }
    topCenter = {
        'col': StartPos['col']-1,
        'row': StartPos['row']
    }
    orientation = 0

    def UpdateCurPosVisited(self):
        EmptyArena[self.topLeft['row']][self.topLeft['col']] = 2
        EmptyArena[self.topRight['row']][self.topRight['col']] = 2
        EmptyArena[self.topCenter['row']][self.topCenter['col']] = 2
        EmptyArena[self.bottomLeft['row']][self.bottomLeft['col']] = 2
        EmptyArena[self.bottomRight['row']][self.bottomRight['col']] = 2

    def UpdateCornerPositions(self):
        orientation = self.orientation
        CurrPos = self.CurrPos
        if(orientation == 0):
            self.topRight['col'] = CurrPos['col']
            self.topRight['row'] = CurrPos['row']

            self.topLeft['col'] = CurrPos['col']-2
            self.topLeft['row'] = CurrPos['row']

            self.topCenter['col'] = CurrPos['col']-1
            self.topCenter['row'] = CurrPos['row']

            self.bottomRight['col'] = CurrPos['col']
            self.bottomRight['row'] = CurrPos['row']+2

            self.bottomLeft['col'] = CurrPos['col']-2
            self.bottomLeft['row'] = CurrPos['row']+2

        elif(orientation == 1):

            self.topLeft['col'] = CurrPos['col']
            self.topLeft['row'] = CurrPos['row']

            self.bottomLeft['col'] = CurrPos['col']-2
            self.bottomLeft['row'] = CurrPos['row']
       
            self.bottomRight['col'] = CurrPos['col']-2
            self.bottomRight['row'] = CurrPos['row']+2

            self.topRight['col'] = CurrPos['col']
            self.topRight['row'] = CurrPos['row'] + 2

            self.topCenter['col'] = CurrPos['col']
            self.topCenter['row'] = CurrPos['row'] + 1

        elif(orientation == 2):
            self.bottomLeft['col'] = CurrPos['col']
            self.bottomLeft['row'] = CurrPos['row']

            self.bottomRight['col'] = CurrPos['col']-2
            self.bottomRight['row'] = CurrPos['row']

            self.topRight['col'] = CurrPos['col']-2
            self.topRight['row'] = CurrPos['row']+2

            self.topLeft['col'] = CurrPos['col']
            self.topLeft['row'] = CurrPos['row']+2

            self.topCenter['col'] = CurrPos['col']-1
            self.topCenter['row'] = CurrPos['row']+2

        else:
            self.bottomRight['col'] = CurrPos['col']
            self.bottomRight['row'] = CurrPos['row']

            self.topRight['col'] = CurrPos['col']-2
            self.topRight['row'] = CurrPos['row']

            self.topLeft['col'] = CurrPos['col']-2
            self.topLeft['row'] = CurrPos['row']+2

            self.topCenter['col'] = CurrPos['col']-2
            self.topCenter['row'] = CurrPos['row']+1

            self.bottomLeft['col'] = CurrPos['col']
            self.bottomLeft['row'] = CurrPos['row']+2

    def __init__(self):
        self.UpdateCurPosVisited()

SensorMax = {
    'LeftBehind' : 5,
    'LeftAhead' : 5,
    'FrontLeft' : 5,
    'FrontCenter' : 5,
    'FrontRight' : 5,
    'RightAhead' : 5
}

SensorData = {
    'LeftBehind' : 0,
    'LeftAhead' : 0,
    'FrontLeft' : 0,
    'FrontCenter' : 0,
    'FrontRight' : 0,
    'RightAhead' : 0 
}

mulfactor={
    'north':{
        'row':[0,-1,0],
        'col':[-1,0,1]
        },
    'east':{
        'row':[-1,0,1],
        'col':[0,1,0]
        },
    'south':{
        'row':[0,1,0],
        'col':[1,0,-1]
        },
    'west':{
        'row':[1,0,-1],
        'col':[0,-1,0]
        }
}

def PrintMap(robot):
    printArena = []
    for i in range(len(EmptyArena)):
        printArena.append(list(EmptyArena[i]))
    printArena[robot.topRight['row']][robot.topRight['col']] = 6
    printArena[robot.bottomRight['row']][robot.bottomRight['col']] = 5
    printArena[robot.topLeft['row']][robot.topLeft['col']] = 6
    printArena[robot.topCenter['row']][robot.topCenter['col']] = 6
    printArena[robot.bottomLeft['row']][robot.bottomLeft['col']] = 5
    for i in range(len(printArena)):
        print printArena[i]
    print 


def CheckSensor(robot):
    SensorArray = simulator.getSensorArray(robot.orientation, robot.CurrPos)
    #TryArray = [x for x in comThread.receive().split(" ")]
    #TryArray[0] = TryArray[0][-1]
    #SensorArray = [int(x) for x in TryArray]
    SensorData['LeftBehind'] = SensorArray[0]
    SensorData['LeftAhead'] = SensorArray[1]
    SensorData['FrontLeft'] = SensorArray[2]
    SensorData['FrontCenter'] = SensorArray[3]
    SensorData['FrontRight'] = SensorArray[4]
    SensorData['RightAhead'] = SensorArray[5]
    #SensorData['RightBehind'] = SensorArray[5]


def TurnRobot(robot, direction):
    #comThread.write(direction)
    #DataChannel.write("turn "+direction)
    if ( direction == "d"):
        robot.orientation = (robot.orientation + 1) % 4
    else:
        robot.orientation = (4 + robot.orientation - 1) % 4

    robot.UpdateCornerPositions()
    return

def MoveRobot(robot, blocks):
    #comThread.write("w")
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

def UpdateArena(robot):
    
    if(robot.orientation==0):
        mul = mulfactor['north']
    elif(robot.orientation==1):
        mul = mulfactor['east']
    elif(robot.orientation==2):
        mul = mulfactor['south']
    else:
        mul = mulfactor['west']

    ############################################

    #LeftBehind Sensor
    DistanceSensor = SensorMax['LeftBehind'] if SensorData['LeftBehind'] == 0 else SensorData['LeftBehind']
      
    for i in range(1, DistanceSensor):
        if(EmptyArena[robot.bottomLeft['row']+mul['row'][0]*i][robot.bottomLeft['col'] + mul['col'][0]*i] != 2):
            EmptyArena[robot.bottomLeft['row']+mul['row'][0]*i][robot.bottomLeft['col'] + mul['col'][0]*i] = 3
        
    #Prevent Wall Errors
    if(SensorData['LeftBehind'] != 0):
        EmptyArena[robot.bottomLeft['row']+mul['row'][0]*DistanceSensor][robot.bottomLeft['col'] + mul['col'][0]*DistanceSensor] = 1

    elif(EmptyArena[robot.bottomLeft['row']+mul['row'][0]*DistanceSensor][robot.bottomLeft['col'] + mul['col'][0]*DistanceSensor] != 2):
        EmptyArena[robot.bottomLeft['row']+mul['row'][0]*DistanceSensor][robot.bottomLeft['col'] + mul['col'][0]*DistanceSensor] = 3

    ############################################

    #LeftAhead Sensor
    DistanceSensor = SensorMax['LeftAhead'] if SensorData['LeftAhead'] == 0 else SensorData['LeftAhead']
      
    for i in range(1, DistanceSensor):
        if(EmptyArena[robot.topLeft['row']+mul['row'][0]*i][robot.topLeft['col'] + mul['col'][0]*i] != 2):
            EmptyArena[robot.topLeft['row']+mul['row'][0]*i][robot.topLeft['col'] + mul['col'][0]*i] = 3
        
    #Prevent Wall Errors
    if(SensorData['LeftAhead'] != 0):
        EmptyArena[robot.topLeft['row']+mul['row'][0]*DistanceSensor][robot.topLeft['col'] + mul['col'][0]*DistanceSensor] = 1

    elif(EmptyArena[robot.topLeft['row']+mul['row'][0]*DistanceSensor][robot.topLeft['col'] + mul['col'][0]*DistanceSensor] != 2):
        EmptyArena[robot.topLeft['row']+mul['row'][0]*DistanceSensor][robot.topLeft['col'] + mul['col'][0]*DistanceSensor] = 3

    ############################################

    #FrontLeft Sensor
    DistanceSensor = SensorMax['FrontLeft'] if SensorData['FrontLeft'] == 0 else SensorData['FrontLeft']
      
    for i in range(1, DistanceSensor):
        if(EmptyArena[robot.topLeft['row']+mul['row'][1]*i][robot.topLeft['col'] + mul['col'][1]*i] != 2):
            EmptyArena[robot.topLeft['row']+mul['row'][1]*i][robot.topLeft['col'] + mul['col'][1]*i] = 3
        
    #Prevent Wall Errors
    if(SensorData['FrontLeft'] != 0):
        EmptyArena[robot.topLeft['row']+mul['row'][1]*DistanceSensor][robot.topLeft['col'] + mul['col'][1]*DistanceSensor] = 1

    elif(EmptyArena[robot.topLeft['row']+mul['row'][1]*DistanceSensor][robot.topLeft['col'] + mul['col'][1]*DistanceSensor] != 2):
        EmptyArena[robot.topLeft['row']+mul['row'][1]*DistanceSensor][robot.topLeft['col'] + mul['col'][1]*DistanceSensor] = 3

    ############################################

    #FrontRight Sensor
    DistanceSensor = SensorMax['FrontRight'] if SensorData['FrontRight'] == 0 else SensorData['FrontRight']
      
    for i in range(1, DistanceSensor):
        if(EmptyArena[robot.topRight['row']+mul['row'][1]*i][robot.topRight['col'] + mul['col'][1]*i] != 2):
            EmptyArena[robot.topRight['row']+mul['row'][1]*i][robot.topRight['col'] + mul['col'][1]*i] = 3
        
    #Prevent Wall Errors
    if(SensorData['FrontRight'] != 0):
        EmptyArena[robot.topRight['row']+mul['row'][1]*DistanceSensor][robot.topRight['col'] + mul['col'][1]*DistanceSensor] = 1

    elif(EmptyArena[robot.topRight['row']+mul['row'][1]*DistanceSensor][robot.topRight['col'] + mul['col'][1]*DistanceSensor] != 2):
        EmptyArena[robot.topRight['row']+mul['row'][1]*DistanceSensor][robot.topRight['col'] + mul['col'][1]*DistanceSensor] = 3

    ############################################

    #FrontCenter Sensor
    DistanceSensor = SensorMax['FrontCenter'] if SensorData['FrontCenter'] == 0 else SensorData['FrontCenter']
      
    for i in range(1, DistanceSensor):
        if(EmptyArena[robot.topCenter['row']+mul['row'][1]*i][robot.topCenter['col'] + mul['col'][1]*i] != 2):
            EmptyArena[robot.topCenter['row']+mul['row'][1]*i][robot.topCenter['col'] + mul['col'][1]*i] = 3
        
    #Prevent Wall Errors
    if(SensorData['FrontCenter'] != 0):
        EmptyArena[robot.topCenter['row']+mul['row'][1]*DistanceSensor][robot.topCenter['col'] + mul['col'][1]*DistanceSensor] = 1

    elif(EmptyArena[robot.topCenter['row']+mul['row'][1]*DistanceSensor][robot.topCenter['col'] + mul['col'][1]*DistanceSensor] != 2):
        EmptyArena[robot.topCenter['row']+mul['row'][1]*DistanceSensor][robot.topCenter['col'] + mul['col'][1]*DistanceSensor] = 3
    
    ############################################

    #RightAhead Sensor
    DistanceSensor = SensorMax['RightAhead'] if SensorData['RightAhead'] == 0 else SensorData['RightAhead']
      
    for i in range(1, DistanceSensor):
        if(EmptyArena[robot.topRight['row']+mul['row'][2]*i][robot.topRight['col'] + mul['col'][2]*i] != 2):
            EmptyArena[robot.topRight['row']+mul['row'][2]*i][robot.topRight['col'] + mul['col'][2]*i] = 3
                
    #Prevent Wall Errors
    if(SensorData['RightAhead'] != 0):
        EmptyArena[robot.topRight['row']+mul['row'][2]*DistanceSensor][robot.topRight['col'] + mul['col'][2]*DistanceSensor] = 1
        
    elif(EmptyArena[robot.topRight['row']+mul['row'][2]*DistanceSensor][robot.topRight['col'] + mul['col'][2]*DistanceSensor] != 2):
        EmptyArena[robot.topRight['row']+mul['row'][2]*DistanceSensor][robot.topRight['col'] + mul['col'][2]*DistanceSensor] = 3

    ############################################
'''
    #RightBehind Sensor
    DistanceSensor = SensorMax['RightBehind'] if SensorData['RightBehind'] == 0 else SensorData['RightBehind']
      
    for i in range(1, DistanceSensor):
        if(EmptyArena[robot.bottomRight['row']+mul['row'][2]*i][robot.bottomRight['col'] + mul['col'][2]*i] != 2):
            EmptyArena[robot.bottomRight['row']+mul['row'][2]*i][robot.bottomRight['col'] + mul['col'][2]*i] = 3
                
    #Prevent Wall Errors
    if(SensorData['RightBehind'] != 0 ):
        EmptyArena[robot.bottomRight['row']+mul['row'][2]*DistanceSensor][robot.bottomRight['col'] + mul['col'][2]*DistanceSensor] = 1

    elif(EmptyArena[robot.bottomRight['row']+mul['row'][2]*DistanceSensor][robot.bottomRight['col'] + mul['col'][2]*DistanceSensor] != 2):
        EmptyArena[robot.bottomRight['row']+mul['row'][2]*DistanceSensor][robot.bottomRight['col'] + mul['col'][2]*DistanceSensor] = 3        

'''
def LeftSideEmpty(robot):
    if(robot.orientation == 0):
        print "inside this"
        return EmptyArena[robot.topLeft['row']][robot.topLeft['col']-1] != 1 and EmptyArena[robot.bottomLeft['row']][robot.bottomLeft['col']-1] != 1 and EmptyArena[robot.bottomLeft['row'] - 1][robot.bottomLeft['col'] - 1] != 1
    elif(robot.orientation == 1):
        return EmptyArena[robot.topLeft['row']-1][robot.topLeft['col']] != 1 and EmptyArena[robot.bottomLeft['row']-1][robot.bottomLeft['col']] != 1 and EmptyArena[robot.bottomLeft['row'] - 1][robot.bottomLeft['col'] + 1] != 1
    elif(robot.orientation == 2):
        return EmptyArena[robot.topLeft['row']][robot.topLeft['col']+1] != 1 and EmptyArena[robot.bottomLeft['row']][robot.bottomLeft['col']+1] != 1 and EmptyArena[robot.bottomLeft['row'] + 1][robot.bottomLeft['col'] + 1] != 1
    else:
        return EmptyArena[robot.topLeft['row']+1][robot.topLeft['col']] != 1 and EmptyArena[robot.bottomLeft['row']+1][robot.bottomLeft['col']] != 1 and EmptyArena[robot.bottomLeft['row'] + 1][robot.bottomLeft['col'] - 1] != 1


def FrontSideEmpty(robot):
    if(robot.orientation == 0):
        return EmptyArena[robot.topLeft['row']-1][robot.topLeft['col']] != 1 and EmptyArena[robot.topRight['row']-1][robot.topRight['col']] != 1 and EmptyArena[robot.topCenter['row']-1][robot.topCenter['col']] != 1
    elif(robot.orientation == 1):
        return EmptyArena[robot.topLeft['row']][robot.topLeft['col']+1] != 1 and EmptyArena[robot.topRight['row']][robot.topRight['col']+1] != 1 and EmptyArena[robot.topCenter['row']][robot.topCenter['col']+1] != 1
    elif(robot.orientation == 2):
        return EmptyArena[robot.topLeft['row']+1][robot.topLeft['col']] != 1 and EmptyArena[robot.topRight['row']+1][robot.topRight['col']] != 1 and EmptyArena[robot.topCenter['row']+1][robot.topCenter['col']] != 1
    else:
        return EmptyArena[robot.topLeft['row']][robot.topLeft['col']-1] != 1 and EmptyArena[robot.topRight['row']][robot.topRight['col']-1] != 1 and EmptyArena[robot.topCenter['row']][robot.topCenter['col']-1] != 1



                

def CalculateMove():
    count = 0
    previousmove = ""
    while(1 == 1):
        count += 1
        print count
        if(robot.CurrPos == GoalPos):
            if (GoalPos == StartPos):
                print "Completed"
                return -1
            else:
                print "Reached Goal Position"
                GoalPos['row'] = StartPos['row']
                GoalPos['col'] = StartPos['col']
        else:
            CheckSensor(robot)
            UpdateArena(robot)
        PrintMap(robot)
        time.sleep(0.5)
        if(previousmove == "a"):
            print "Moving Forward"
            previousmove = "w"
            MoveRobot(robot, 1)

        elif(LeftSideEmpty(robot)):
            print "Turning left"
            previousmove = "a"
            TurnRobot(robot, "a")
            
        elif(FrontSideEmpty(robot)):
            print "Moving Forward"
            previousmove = "w"
            MoveRobot(robot, 1)
        else:
            print "Turning Right"
            previousmove = "d"
            TurnRobot(robot, "d")
        



def RunExplore():
    while(1==1):
        if(CalculateMove() == -1):
            print "Exploration Completed"
            return EmptyArena

robot = ArduinoRobot()
#comThread = pc_test_socket.Test()
RunExplore()