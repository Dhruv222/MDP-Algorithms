#usr/bin/python
from serial import Serial
from sys import *
from generatemap import generate

#initiate serial connection with the Arduino
#DataChannel = Serial("",)

Arena = generate()
EmptyArena=[[0 for i in range(15)] for j in range(20)]

StartPos = {
    'x':1,
    'y':1
}

class ArduinoRobot:
    CurrPos = StartPos
    topRight = StartPos
    topLeft = {
        'x':StartPos['x']-1,
        'y':StartPos['y']
    }
    bottomRight = {
        'x': StartPos['x']-1,
        'y': StartPos['y']-1
    }
    bottomLeft = {
        'x': StartPos['x'],
        'y': StartPos['y']-1
    }
    orientation = 0

    def UpdateCornerPositions(self):
        orientation = self.orientation
        CurrPos = self.CurrPos
        if(orientation == 0):
            self.topRight = CurrPos

            self.topLeft['x'] = CurrPos['x']-1
            self.topLeft['x'] = CurrPos['y']

            self.bottomRight['x'] = CurrPos['x']-1
            self.bottomRight['y'] = CurrPos['y']-1

            self.bottomLeft['x'] = CurrPos['x']
            self.bottomLeft['y'] = CurrPos['y']-1
        elif(orientation == 1):
            self.topLeft = CurrPos

            self.bottomLeft['x'] = CurrPos['x']-1
            self.bottomLeft['x'] = CurrPos['y']

            self.bottomRight['x'] = CurrPos['x']-1
            self.bottomRight['y'] = CurrPos['y']-1

            self.topRight['x'] = CurrPos['x']
            self.topRight['y'] = CurrPos['y']-1
        elif(orientation == 2):
            self.bottomLeft = CurrPos

            self.bottomRight['x'] = CurrPos['x']-1
            self.bottomRight['x'] = CurrPos['y']

            self.topRight['x'] = CurrPos['x']-1
            self.topRight['y'] = CurrPos['y']-1

            self.topLeft['x'] = CurrPos['x']
            self.topLeft['y'] = CurrPos['y']-1
        else:
            self.bottomRight = CurrPos

            self.topRight['x'] = CurrPos['x']-1
            self.topRight['x'] = CurrPos['y']

            self.topLeft['x'] = CurrPos['x']-1
            self.topLeft['y'] = CurrPos['y']-1

            self.bottomLeft['x'] = CurrPos['x']
            self.bottomLeft['y'] = CurrPos['y']-1

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
        'x':[-1,0,+1],
        'y':[0,+1,0]
        },
    'east':{
        'x':[0,+1,0],
        'y':[+1,0,-1]
        },
    'south':{
        'x':[+1,0,-1],
        'y':[0,-1,0]
        },
    'west':{
        'x':[0,-1,0],
        'y':[-1,0,+1]
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
    SensorArray = [int(x) for x in DataChannel.readline().split(" ")]
    SensorData['LeftBehind'] = SensorArray[0]
    SensorData['LeftAhead'] = SensorArray[1]
    SensorData['FrontLeft'] = SensorArray[2]
    SensorData['FronRight'] = SensorArray[3]
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
        robot.CurrPos['y']+=blocks
    elif(robot.orientation==1):
        robot.CurrPos['x']+=blocks
    elif(robot.orientation==2):
        robot.CurrPos['y']-=blocks
    else:
        robot.CurrPos['x']-=blocks

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
        if(-1<robot.bottomLeft['x']+ mul['x'][0]*i<20):
            if(EmptyArena[robot.bottomLeft['x'] + mul['x'][0]*i][robot.bottomLeft['y']+mul['y'][0]*i] != 2):
                EmptyArena[robot.bottomLeft['x'] + mul['x'][0]*i][robot.bottomLeft['y']+mul['y'][0]*i] = 3
        
        #Prevent Wall Errors
        if(-1 < (mul['x'][0]**2)*(robot.bottomLeft['x'] + mul['x'][0]*DistanceSensor)+(mul['y'][0]**2)*(robot.bottomLeft['y'] + mul['y'][0]*DistanceSensor) < 20 and SensorData['LeftBehind'] != 0 ):
            EmptyArena[robot.bottomLeft['x'] + mul['x'][0]*DistanceSensor][robot.bottomLeft['y']+mul['y'][0]*DistanceSensor] = 1


    ############################################

    #LeftAhead Sensor
    DistanceSensor = SensorMax['LeftAhead'] if SensorData['LeftAhead'] == 0 else SensorData['LeftAhead']
    for i in range(1, DistanceSensor):
        if(-1<robot.topLeft['x']+ mul['x'][0]*i<20):
            if(EmptyArena[robot.topLeft['x'] + mul['x'][0]*i][robot.topLeft['y']+mul['y'][0]*i] != 2):
                EmptyArena[robot.topLeft['x'] + mul['x'][0]*i][robot.topLeft['y']+mul['y'][0]*i] = 3
        
        #Prevent Wall Errors
        if(-1 < (mul['x'][0]**2)*(robot.topLeft['x'] + mul['x'][0]*DistanceSensor)+(mul['y'][0]**2)*(robot.topLeft['y'] + mul['y'][0]*DistanceSensor) < 20 and SensorData['LeftAhead'] != 0 ):
            EmptyArena[robot.topLeft['x'] + mul['x'][0]*DistanceSensor][robot.topLeft['y']+mul['y'][0]*DistanceSensor] = 1


    ############################################

    #FrontLeft Sensor
    DistanceSensor = SensorMax['FrontLeft'] if SensorData['FrontLeft'] == 0 else SensorData['FrontLeft']
    for i in range(1, DistanceSensor):
        if(-1<robot.topLeft['x']+ mul['x'][1]*i<20):
            if(EmptyArena[robot.topLeft['x'] + mul['x'][1]*i][robot.topLeft['y']+mul['y'][1]*i] != 2):
                EmptyArena[robot.topLeft['x'] + mul['x'][1]*i][robot.topLeft['y']+mul['y'][1]*i] = 3
        
        #Prevent Wall Errors
        if(-1 < (mul['x'][1]**2)*(robot.topLeft['x'] + mul['x'][1]*DistanceSensor)+(mul['y'][1]**2)*(robot.topLeft['y'] + mul['y'][1]*DistanceSensor) < 20 and SensorData['FrontLeft'] != 0 ):
            EmptyArena[robot.topLeft['x'] + mul['x'][1]*DistanceSensor][robot.topLeft['y']+mul['y'][1]*DistanceSensor] = 1


    ############################################

    #FrontRight Sensor
    DistanceSensor = SensorMax['FrontRight'] if SensorData['FrontRight'] == 0 else SensorData['FrontRight']
    for i in range(1, DistanceSensor):
        if(-1<robot.topRight['x']+ mul['x'][1]*i<20):
            if(EmptyArena[robot.topRight['x'] + mul['x'][1]*i][robot.topRight['y']+mul['y'][1]*i] != 2):
                EmptyArena[robot.topRight['x'] + mul['x'][1]*i][robot.topRight['y']+mul['y'][1]*i] = 3
        
        #Prevent Wall Errors
        if(-1 < (mul['x'][1]**2)*(robot.topRight['x'] + mul['x'][1]*DistanceSensor)+(mul['y'][1]**2)*(robot.topRight['y'] + mul['y'][1]*DistanceSensor) < 20 and SensorData['FrontRight'] != 0 ):
            EmptyArena[robot.topRight['x'] + mul['x'][1]*DistanceSensor][robot.topRight['y']+mul['y'][1]*DistanceSensor] = 1


    ############################################

    #RightAhead Sensor
    DistanceSensor = SensorMax['RightAhead'] if SensorData['RightAhead'] == 0 else SensorData['RightAhead']
    for i in range(1, DistanceSensor):
        if(-1<robot.topRight['x']+ mul['x'][2]*i<20):
            if(EmptyArena[robot.topRight['x'] + mul['x'][2]*i][robot.topRight['y']+mul['y'][2]*i] != 2):
                EmptyArena[robot.topRight['x'] + mul['x'][2]*i][robot.topRight['y']+mul['y'][2]*i] = 3
        
        #Prevent Wall Errors
        if(-1 < (mul['x'][2]**2)*(robot.topRight['x'] + mul['x'][2]*DistanceSensor)+(mul['y'][2]**2)*(robot.topRight['y'] + mul['y'][2]*DistanceSensor) < 20 and SensorData['RightAhead'] != 0 ):
            EmptyArena[robot.topRight['x'] + mul['x'][2]*DistanceSensor][robot.topRight['y']+mul['y'][2]*DistanceSensor] = 1


    ############################################

    #RightBehind Sensor
    DistanceSensor = SensorMax['LeftBehind'] if SensorData['LeftBehind'] == 0 else SensorData['LeftBehind']
    for i in range(1, DistanceSensor):
        if(-1<robot.bottomLeft['x']+ mul['x'][2]*i<20):
            if(EmptyArena[robot.bottomLeft['x'] + mul['x'][2]*i][robot.bottomLeft['y']+mul['y'][2]*i] != 2):
                EmptyArena[robot.bottomLeft['x'] + mul['x'][2]*i][robot.bottomLeft['y']+mul['y'][2]*i] = 3
        
        #Prevent Wall Errors
        if(-1 < (mul['x'][2]**2)*(robot.bottomLeft['x'] + mul['x'][2]*DistanceSensor)+(mul['y'][2]**2)*(robot.bottomLeft['y'] + mul['y'][2]*DistanceSensor) < 20 and SensorData['LeftBehind'] != 0 ):
            EmptyArena[robot.bottomLeft['x'] + mul['x'][2]*DistanceSensor][robot.bottomLeft['y']+mul['y'][2]*DistanceSensor] = 1

robot = ArduinoRobot()
print robot.CurrPos
print robot.topRight
print robot.topLeft
print robot.bottomRight
print robot.bottomLeft
print robot.orientation
TurnRobot(robot, "right")
print robot.CurrPos
print robot.topRight
print robot.topLeft
print robot.bottomRight
print robot.bottomLeft
print robot.orientation