import simulator
import mdfConvert as mdf
import time
import pc_test_socket


EmptyArena=[[0 for i in range(17)] for j in range(22)]
PreviousArena = []
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
    bottomCenter = {
        'col': StartPos['col']-1,
        'row': StartPos['row']+2
    }
    orientation = 0

    def UpdateCurPosVisited(self):
        EmptyArena[self.topLeft['row']][self.topLeft['col']] = 2
        EmptyArena[self.topRight['row']][self.topRight['col']] = 2
        EmptyArena[self.topCenter['row']][self.topCenter['col']] = 2
        EmptyArena[self.bottomLeft['row']][self.bottomLeft['col']] = 2
        EmptyArena[self.bottomRight['row']][self.bottomRight['col']] = 2
        EmptyArena[self.bottomCenter['row']][self.bottomCenter['col']] = 2
        #LeftCenter
        EmptyArena[(self.topLeft['row']+self.bottomLeft['row'])/2][(self.topLeft['col']+self.bottomLeft['col'])/2] = 2
        #RightCenter
        EmptyArena[(self.bottomRight['row']+self.topRight['row'])/2][(self.bottomRight['col']+self.topRight['col'])/2] = 2
        #Middle
        EmptyArena[(self.topCenter['row']+self.bottomCenter['row'])/2][(self.topCenter['col']+self.bottomCenter['col'])/2] = 2

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

            self.bottomCenter['col'] = CurrPos['col']-1
            self.bottomCenter['row'] = CurrPos['row']+2

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

            self.bottomCenter['col'] = CurrPos['col']-2
            self.bottomCenter['row'] = CurrPos['row']+1

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

            self.bottomCenter['col'] = CurrPos['col']-1
            self.bottomCenter['row'] = CurrPos['row']

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

            self.bottomCenter['col'] = CurrPos['col']
            self.bottomCenter['row'] = CurrPos['row']+1

    def __init__(self):
        self.UpdateCurPosVisited()

SensorMax = {
    'LeftBehind' : 3,
    'LeftAhead' : 3,
    'FrontLeft' : 3,
    'FrontCenter' : 3,
    'FrontRight' : 3,
    'RightAhead' : 7
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
    PreviousArena = []
    for i in range(len(EmptyArena)):
        printArena.append(list(EmptyArena[i]))
        PreviousArena.append(list(EmptyArena[i]))
    printArena[robot.topRight['row']][robot.topRight['col']] = 6
    printArena[robot.topLeft['row']][robot.topLeft['col']] = 6
    printArena[robot.topCenter['row']][robot.topCenter['col']] = 6
    printArena[robot.bottomLeft['row']][robot.bottomLeft['col']] = 5
    printArena[robot.bottomRight['row']][robot.bottomRight['col']] = 5
    printArena[robot.bottomCenter['row']][robot.bottomCenter['col']] = 5
    #LeftCenter
    printArena[(robot.topLeft['row']+robot.bottomLeft['row'])/2][(robot.topLeft['col']+robot.bottomLeft['col'])/2] = 5
    #RightCenter
    printArena[(robot.bottomRight['row']+robot.topRight['row'])/2][(robot.bottomRight['col']+robot.topRight['col'])/2] = 5
    #Middle
    printArena[(robot.topCenter['row']+robot.bottomCenter['row'])/2][(robot.topCenter['col']+robot.bottomCenter['col'])/2] = 5
    for i in range(len(printArena)):
        print printArena[i]
    print
    return printArena


def CheckSensor(robot):
    #SensorArray = simulator.getSensorArray(robot.orientation, robot.CurrPos)
    print "Checking Sensors"
    data = comThread.receive()
    if data == 'r':
        print "Sensor said 'start'"
        data = comThread.receive()
    print "Sensor Value", data
    TryArray = [x for x in data.split(" ")]
    TryArray[0] = TryArray[0][-1]
    SensorArray = [int(x) for x in TryArray]
    #SensorData['LeftBehind'] = SensorArray[0]
    SensorData['LeftAhead'] = SensorArray[0]
    SensorData['FrontLeft'] = SensorArray[1]
    SensorData['FrontCenter'] = SensorArray[2]
    SensorData['FrontRight'] = SensorArray[3]
    SensorData['RightAhead'] = SensorArray[4]
    #SensorData['RightBehind'] = SensorArray[5]


def TurnRobot(robot, direction):
    comThread.write(direction)
    #DataChannel.write("turn "+direction)
    if ( direction == "d"):
        robot.orientation = (robot.orientation + 1) % 4
    else:
        robot.orientation = (4 + robot.orientation - 1) % 4

    robot.UpdateCornerPositions()
    return

def MoveRobot(robot, blocks):
    comThread.write("w")
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

    # #LeftBehind Sensor
    # DistanceSensor = SensorMax['LeftBehind'] if SensorData['LeftBehind'] == 0 else SensorData['LeftBehind']

    # for i in range(1, DistanceSensor):
    #     if(EmptyArena[robot.bottomLeft['row']+mul['row'][0]*i][robot.bottomLeft['col'] + mul['col'][0]*i] != 2):
    #         EmptyArena[robot.bottomLeft['row']+mul['row'][0]*i][robot.bottomLeft['col'] + mul['col'][0]*i] = 3

    # #Prevent Wall Errors
    # if(SensorData['LeftBehind'] != 0):
    #     EmptyArena[robot.bottomLeft['row']+mul['row'][0]*DistanceSensor][robot.bottomLeft['col'] + mul['col'][0]*DistanceSensor] = 1

    # elif(EmptyArena[robot.bottomLeft['row']+mul['row'][0]*DistanceSensor][robot.bottomLeft['col'] + mul['col'][0]*DistanceSensor] != 2):
    #     EmptyArena[robot.bottomLeft['row']+mul['row'][0]*DistanceSensor][robot.bottomLeft['col'] + mul['col'][0]*DistanceSensor] = 3

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

    #RightBehind Sensor
    # DistanceSensor = SensorMax['RightBehind'] if SensorData['RightBehind'] == 0 else SensorData['RightBehind']

    # for i in range(1, DistanceSensor):
    #     if(EmptyArena[robot.bottomRight['row']+mul['row'][2]*i][robot.bottomRight['col'] + mul['col'][2]*i] != 2):
    #         EmptyArena[robot.bottomRight['row']+mul['row'][2]*i][robot.bottomRight['col'] + mul['col'][2]*i] = 3

    # #Prevent Wall Errors
    # if(SensorData['RightBehind'] != 0 ):
    #     EmptyArena[robot.bottomRight['row']+mul['row'][2]*DistanceSensor][robot.bottomRight['col'] + mul['col'][2]*DistanceSensor] = 1

    # elif(EmptyArena[robot.bottomRight['row']+mul['row'][2]*DistanceSensor][robot.bottomRight['col'] + mul['col'][2]*DistanceSensor] != 2):
    #     EmptyArena[robot.bottomRight['row']+mul['row'][2]*DistanceSensor][robot.bottomRight['col'] + mul['col'][2]*DistanceSensor] = 3


def LeftSideEmpty(robot):
    if(robot.orientation == 0):
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

#Add and Remove Obstacles from the android
def SendDataToAndroid():
    for i in range(1,21):
        for j in range(1, 16):
            if EmptyArena[i][j] != PreviousArena[i][j]:
                if EmptyArena[i][j] == 1:
                    comThread.write("add:{},{}".format(i, j))
                    print "Adding Obstacle to {},{}".format(i, j)
                elif PreviousArena[i][j] == 1:
                    comThread.write("remove:{},{}".format(i, j))
                    print "Removing Obstacle from {},{}".format(i, j)


global previousmove
def CalculateMove():
    try:
        count = 0
        global previousmove
        if(robot.CurrPos == GoalPos):
            if (GoalPos == StartPos):
                print "Completed"
                mdf1 = mdf.ExploreArrayToMDF(EmptyArena)
                mdf2 = mdf.obstacleArrayToMDF(EmptyArena)
                print("mdf1:", mdf1)
                print("mdf2:", mdf2)
                comThread.write("#MDF1:"+mdf1)
                time.sleep(0.2)
                comThread.write("#MDF2:"+mdf2)
                return -1
            else:
                print "Reached Goal Position"
                GoalPos['row'] = StartPos['row']
                GoalPos['col'] = StartPos['col']

        else:
            print "going for sensors"
            CheckSensor(robot)
            print "Updating arena"
            UpdateArena(robot)
            print "Arena Updated"
        #PrintMap(robot)
        #time.sleep(0.5)
        map = PrintMap(robot)
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

        SendDataToAndroid()
        return map
    except Exception as e:
        #comThread.close()
        #print("Error: ", e)
        #exit()
        comThread.write('r')
robot = ArduinoRobot()
previousmove = ""
comThread = pc_test_socket.Test()
