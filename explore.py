#usr/bin/python
from serial import Serial
from sys import *
from generatemap import generate

#initiate serial connection with the Arduino
#DataChannel = Serial("",)

Arena = generate()
EmptyArena=[[0 for i in range(15)] for j in range(20)]

StartPos = {
    'row':18,
    'col':1
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

            self.topRight['col'] = CurrPos['col']
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

SensorMax = {
    'LeftBehind' : 5,
    'LeftAhead' : 5,
    'FrontLeft' : 5,
    'FrontRight' : 5,
    'RightAhead' : 5,
    'RightBehind' : 5
}

SensorData = {
    'LeftBehind' : 0,
    'LeftAhead' : 0,
    'FrontLeft' : 0,
    'FrontRight' : 0,
    'RightAhead' : 0,
    'RightBehind' : 0 
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
    #SensorArray = [int(x) for x in DataChannel.readline().split(" ")]
    SensorArray = [3,3,3,3,3,3]
    SensorData['LeftBehind'] = SensorArray[0]
    SensorData['LeftAhead'] = SensorArray[1]
    SensorData['FrontLeft'] = SensorArray[2]
    SensorData['FrontRight'] = SensorArray[3]
    SensorData['RightAhead'] = SensorArray[4]
    SensorData['RightBehind'] = SensorArray[5]


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

    ############################################

    #LeftBehind Sensor
    DistanceSensor = SensorMax['LeftBehind'] if SensorData['LeftBehind'] == 0 else SensorData['LeftBehind']
    for i in range(1, DistanceSensor):
        
        if(-1<robot.bottomLeft['col']+ mul['col'][0]*i<20 and -1<robot.bottomLeft['row']+ mul['row'][0]*i<20):
            if(EmptyArena[robot.bottomLeft['row']+mul['row'][0]*i][robot.bottomLeft['col'] + mul['col'][0]*i] != 2):
                EmptyArena[robot.bottomLeft['row']+mul['row'][0]*i][robot.bottomLeft['col'] + mul['col'][0]*i] = 3
        
    #Prevent Wall Errors
    if(-1 < (mul['col'][0]**2)*(robot.bottomLeft['col'] + mul['col'][0]*DistanceSensor)+(mul['row'][0]**2)*(robot.bottomLeft['row'] + mul['row'][0]*DistanceSensor) < 20 and SensorData['LeftBehind'] != 0 and EmptyArena[robot.bottomLeft['row']+mul['row'][0]*i][robot.bottomLeft['col'] + mul['col'][0]*i] != 2):
        EmptyArena[robot.bottomLeft['row']+mul['row'][0]*DistanceSensor][robot.bottomLeft['col'] + mul['col'][0]*DistanceSensor] = 1

    ############################################

    #LeftAhead Sensor
    DistanceSensor = SensorMax['LeftAhead'] if SensorData['LeftAhead'] == 0 else SensorData['LeftAhead']
    for i in range(1, DistanceSensor):
        if(-1<robot.topLeft['col']+ mul['col'][0]*i<20):
            if(EmptyArena[robot.topLeft['row']+mul['row'][0]*i][robot.topLeft['col'] + mul['col'][0]*i] != 2):
                EmptyArena[robot.topLeft['row']+mul['row'][0]*i][robot.topLeft['col'] + mul['col'][0]*i] = 3
        
    #Prevent Wall Errors
    if(-1 < (mul['col'][0]**2)*(robot.topLeft['col'] + mul['col'][0]*DistanceSensor)+(mul['row'][0]**2)*(robot.topLeft['row'] + mul['row'][0]*DistanceSensor) < 20 and SensorData['LeftAhead'] != 0 and EmptyArena[robot.topLeft['row']+mul['row'][0]*i][robot.topLeft['col'] + mul['col'][0]*i] != 2):
        EmptyArena[robot.topLeft['row']+mul['row'][0]*DistanceSensor][robot.topLeft['col'] + mul['col'][0]*DistanceSensor] = 1

    ############################################

    #FrontLeft Sensor
    DistanceSensor = SensorMax['FrontLeft'] if SensorData['FrontLeft'] == 0 else SensorData['FrontLeft']
    for i in range(1, DistanceSensor):
        if(-1<robot.topLeft['col']+ mul['col'][1]*i<20):
            if(EmptyArena[robot.topLeft['row']+mul['row'][1]*i][robot.topLeft['col'] + mul['col'][1]*i] != 2):
                EmptyArena[robot.topLeft['row']+mul['row'][1]*i][robot.topLeft['col'] + mul['col'][1]*i] = 3
        
    #Prevent Wall Errors
    if(-1 < (mul['col'][1]**2)*(robot.topLeft['col'] + mul['col'][1]*DistanceSensor)+(mul['row'][1]**2)*(robot.topLeft['row'] + mul['row'][1]*DistanceSensor) < 20 and SensorData['FrontLeft'] != 0 and EmptyArena[robot.topLeft['row']+mul['row'][1]*i][robot.topLeft['col'] + mul['col'][1]*i] != 2):
        EmptyArena[robot.topLeft['row']+mul['row'][1]*DistanceSensor][robot.topLeft['col'] + mul['col'][1]*DistanceSensor] = 1

    ############################################

    #FrontRight Sensor
    DistanceSensor = SensorMax['FrontRight'] if SensorData['FrontRight'] == 0 else SensorData['FrontRight']
    for i in range(1, DistanceSensor):
        if(-1<robot.topRight['col']+ mul['col'][1]*i<20):
            if(EmptyArena[robot.topRight['row']+mul['row'][1]*i][robot.topRight['col'] + mul['col'][1]*i] != 2):
                EmptyArena[robot.topRight['row']+mul['row'][1]*i][robot.topRight['col'] + mul['col'][1]*i] = 3
        
    #Prevent Wall Errors
    if(-1 < (mul['col'][1]**2)*(robot.topRight['col'] + mul['col'][1]*DistanceSensor)+(mul['row'][1]**2)*(robot.topRight['row'] + mul['row'][1]*DistanceSensor) < 20 and SensorData['FrontRight'] != 0 and EmptyArena[robot.topRight['row']+mul['row'][1]*i][robot.topRight['col'] + mul['col'][1]*i] != 2):
        EmptyArena[robot.topRight['row']+mul['row'][1]*DistanceSensor][robot.topRight['col'] + mul['col'][1]*DistanceSensor] = 1

    ############################################

    #RightAhead Sensor
    DistanceSensor = SensorMax['RightAhead'] if SensorData['RightAhead'] == 0 else SensorData['RightAhead']
    for i in range(1, DistanceSensor):
        if(-1<robot.topRight['col']+ mul['col'][2]*i<20):
            if(EmptyArena[robot.topRight['row']+mul['row'][2]*i][robot.topRight['col'] + mul['col'][2]*i] != 2):
                EmptyArena[robot.topRight['row']+mul['row'][2]*i][robot.topRight['col'] + mul['col'][2]*i] = 3
                
    #Prevent Wall Errors
    if(-1 < (mul['col'][2]**2)*(robot.topRight['col'] + mul['col'][2]*DistanceSensor)+(mul['row'][2]**2)*(robot.topRight['row'] + mul['row'][2]*DistanceSensor) < 20 and SensorData['RightAhead'] != 0 and EmptyArena[robot.topRight['row']+mul['row'][2]*i][robot.topRight['col'] + mul['col'][2]*i] != 2):
        EmptyArena[robot.topRight['row']+mul['row'][2]*DistanceSensor][robot.topRight['col'] + mul['col'][2]*DistanceSensor] = 1

    ############################################

    #RightBehind Sensor
    DistanceSensor = SensorMax['LeftBehind'] if SensorData['LeftBehind'] == 0 else SensorData['LeftBehind']
    for i in range(1, DistanceSensor):
        if(-1<robot.bottomRight['col']+ mul['col'][2]*i<20):
            if(EmptyArena[robot.bottomRight['row']+mul['row'][2]*i][robot.bottomRight['col'] + mul['col'][2]*i] != 2):
                EmptyArena[robot.bottomRight['row']+mul['row'][2]*i][robot.bottomRight['col'] + mul['col'][2]*i] = 3
                
    #Prevent Wall Errors
    if(-1 < (mul['col'][2]**2)*(robot.bottomRight['col'] + mul['col'][2]*DistanceSensor)+(mul['row'][2]**2)*(robot.bottomRight['row'] + mul['row'][2]*DistanceSensor) < 20 and SensorData['LeftBehind'] != 0 and EmptyArena[robot.bottomRight['row']+mul['row'][2]*i][robot.bottomRight['col'] + mul['col'][2]*i] != 2):
        EmptyArena[robot.bottomRight['row']+mul['row'][2]*DistanceSensor][robot.bottomRight['col'] + mul['col'][2]*DistanceSensor] = 1

robot = ArduinoRobot()

for i in range(len(EmptyArena)):
    print EmptyArena[i]
print
CheckSensor()
UpdateArena(robot)
for i in range(len(EmptyArena)):
    print EmptyArena[i]
print
MoveRobot(robot, 18)
CheckSensor()
UpdateArena(robot)
for i in range(len(EmptyArena)):
    print EmptyArena[i]
print
TurnRobot(robot, "right")

MoveRobot(robot, 12)
for i in range(len(EmptyArena)):
    print EmptyArena[i]
print
CheckSensor()
UpdateArena(robot)
for i in range(len(EmptyArena)):
    print EmptyArena[i]
print
