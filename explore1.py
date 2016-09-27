#usr/bin/python
from generatemap import generate
from serial import Serial
from sys import *

DataChannel = Serial("",)
arena = generate()
# In the arena: 
# 0=unexplored,
# 1=Obstacle,
# 2=Visited,
# 3=Explored


StartPos = {
    x : sys.argv[0],
    y : sys.argv[1]
}

SensorMax = {
    LeftBehind : 5,
    LeftAhead : 5,
    FrontLeft : 5,
    FrontRight : 5,
    RightAhead : 5,
    RightBehind : 5
}

robot = {
    currPos: StartPos,
    topRight: self.currPos,
    topLeft: {
        x:StartPos.x-1,
        y:StartPos.y
    },
    bottomLeft: {
        x: StartPos.x-1,
        y: StartPos.y-1
    },
    bottomRight: {
        x: StartPos.x,
        y: StartPos.y-1
    },
    # 0=North, 1=East, 2=West, 3=South
    orientation: 0

}

mulfactor={
    north:[-1,1,1],
    east:[1,1,-1],
    south:[1,-1,-1],
    west:[-1,1,1]
}

SensorData = {
    LeftBehind : 0,
    LeftAhead : 0,
    FrontLeft : 0,
    FrontRight : 0,
    RightAhead : 0,
    RightBehind : 0
}


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


def CheckSensor():
    SensorArray = [int(x) for x in DataChannel.readline().split(" ")]
    SensorData.LeftBehind = SensorArray[0]
    SensorData.LeftAhead = SensorArray[1]
    SensorData.FrontLeft = SensorArray[2]
    SensorData.FrontRight = SensorArray[3]
    SensorData.RightBehind = SensorArray[4]
    SensorData.RightBehind = SensorArray[5]
        

def MoveForward(blocks):
    DataChannel.write("forward "+str(blocks))
    
    ##TODO: Update to accomodate the orientation
    arena[robot.topRight.x][robot.topRight.y] = 2               #TopRight of Robot
    arena[robot.bottomRight.x][robot.bottomRight.y] = 2         #BottomRight of Robot
    arena[robot.topLeft.x][robot.topLeft.y] = 2                 #TopLeft of Robot
    arena[robot.bottomRight.x][robot.bottomRight.y] = 2         #BottomLeft of Robot

    return

def TurnRobot(direction):
    DataChannel.write("turn "+direction)
    if ( direction == "right"):
        robot.orientation = (robot.orientation + 1) % 4
    else:
        robot.orientation = (4 + robot.orientation - 1) % 4
    return

def UpdateArena():
    
    # for LeftBehind sensor
    for i in range((SensorMax.LeftBehind if SensorData.LeftBehind == 0 else SensorData.LeftBehind)-1):
        if(arena[CurPos[x]-1-i][CurPos[y]-1] != 2):
            arena[CurPos[x]-1-i][CurPos[y]-1] = 3
    #Prevent Wall Errors
    if(CurPos[x]-1-SensorData.LeftBehind>0 && SensorData.LeftBehind != 0):
        arena[CurPos[x]-1-SensorData.LeftBehind][CurPos[y]-1] = 1
        
    #########################################
    
    # for LeftAhead sensor
    for i in range((SensorMax.LeftBehind if SensorData.LeftAhead == 0 else SensorData.LeftAhead)-1):
        if(arena[CurPos[x]-1-i][CurPos[y]] != 2):
            arena[CurPos[x]-1-i][CurPos[y]] = 3
    #Prevent Wall Errors
    if(CurPos[x]-1-SensorData.LeftAhead>0 && SensorData.LeftAhead != 0):
        arena[CurPos[x]-1-SensorData.LeftAhead][CurPos[y]] = 1

    #########################################
    
    # for FrontLeft sensor
    for i in range((SensorMax.FrontLeft if SensorData.FrontLeft == 0 else SensorData.FrontLeft)-1):
        if(arena[CurPos[x]-1][CurPos[y]+i] != 2):
            arena[CurPos[x]-1][CurPos[y]+i] = 3
    #Prevent Wall Errors
    if(CurPos[y]+SensorData.FrontLeft>0 && SensorData.FrontLeft != 0):
        arena[CurPos[x]-1][CurPos[y]+SensorData.FrontLeft] = 1
    
    #########################################

    # for FrontRight sensor
    for i in range((SensorMax.LeftBehind if SensorData.leftBehind == 0 else SensorData.leftBehind)-1):
        if(arena[CurPos[x]][CurPos[y]+i] != 2):
            arena[CurPos[x]][CurPos[y]+i] = 3
    #Prevent Wall Errors
    if(CurPos[y]+SensorData.FrontRight>0) && SensorData.FrontRight != 0:
        arena[CurPos[x]][CurPos[y]+SensorData.FrontRight] = 1

    #########################################

    # for RightAhead sensor
    for i in range((SensorMax.LeftBehind if SensorData.leftBehind == 0 else SensorData.leftBehind)-1):
        if(arena[CurPos[x]+i][CurPos[y]] != 2):
            arena[CurPos[x]+i][CurPos[y]] = 3
    #Prevent Wall Errors
    if(CurPos[x]+SensorData.RightAhead>0):
        arena[CurPos[x]+SensorData.RightAhead][CurPos[y]] = 1

    #########################################

    # for RightBehind sensor
    for i in range((SensorMax.LeftBehind if SensorData.leftBehind == 0 else SensorData.leftBehind)-1):
        if(arena[CurPos[x]+i][CurPos[y]-1] != 2):
            arena[CurPos[x]+i][CurPos[y]-1] = 3
    #Prevent Wall Errors
    if(CurPos[x]+SensorData.RightBehind>0):
        arena[CurPos[x]+SensorData.RightBehind][CurPos[y]-1] = 1
    
def CalculateMove():
    print "hello"