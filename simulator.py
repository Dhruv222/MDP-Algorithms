from sys import *

Arena = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]



SensorMax = {
    'LeftBehind' : 5,
    'LeftAhead' : 5,
    'FrontLeft' : 5,
    'FrontRight' : 5,
    'RightAhead' : 5,
    'RightBehind' : 5
}

MaxSensorMax = 5




def getSensorArray(orientation, CurrPos):
    SensorMaxValues = []
    SensorArray = []
    topRight = {
        'row': CurrPos['row'],
        'col': CurrPos['col']
    }
    topCenter = {
        'row': CurrPos['row'],
        'col': CurrPos['col']-1
    }
    topLeft= {
        'row': CurrPos['row'],
        'col': CurrPos['col']-2
    }
    bottomLeft = {
        'row': CurrPos['row']+2,
        'col': CurrPos['col']-2
    }
    bottomCenter = {
        'row': CurrPos['row']+2,
        'col': CurrPos['col']-1
    }
    bottomRight = {
        'row': CurrPos['row']+2,
        'col': CurrPos['col']
    }
    LeftCenter = {
        'row': CurrPos['row']+1,
        'col': CurrPos['col']-2
    }
    RightCenter = {
        'row': CurrPos['row']+1,
        'col': CurrPos['col']
    }

    Arena[topRight['row']][topRight['col']] = 4
    Arena[topCenter['row']][topCenter['col']] = 4
    Arena[topLeft['row']][topLeft['col']] = 4
    Arena[bottomRight['row']][bottomRight['col']] = 4
    Arena[bottomLeft['row']][bottomLeft['col']] = 4

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[bottomLeft['row']][bottomLeft['col']-i] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[LeftCenter['row']][LeftCenter['col']-i] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[topLeft['row']][topLeft['col']-i] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[topLeft['row']-i][topLeft['col']] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[topCenter['row']-i][topCenter['col']] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[topRight['row']-i][topRight['col']] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[topRight['row']][topRight['col']+i] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[RightCenter['row']][RightCenter['col']+i] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[bottomRight['row']][bottomRight['col']+i] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[bottomRight['row']+i][bottomRight['col']] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[bottomCenter['row']+i][bottomCenter['col']] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    count = 0
    for i in range(1,MaxSensorMax+1):
        count += 1
        if(Arena[bottomLeft['row']+i][bottomLeft['col']] == 1):
            SensorMaxValues.append(count)
            break
        elif(i == MaxSensorMax):
            SensorMaxValues.append(0)

    SensorAllDirection = [
        ['LeftBehind', 'skip', 'LeftAhead', 'FrontLeft', 'FrontCenter', 'FrontRight', 'RightAhead', 'skip', 'skip', 'skip','skip','skip'],
        ['skip','skip','skip','LeftBehind','skip', 'LeftAhead', 'FrontLeft', 'FrontCenter', 'FrontRight', 'RightAhead','skip','skip'],
        ['RightAhead','skip','skip','skip','skip','skip','LeftBehind','skip', 'LeftAhead', 'FrontLeft', 'FrontCenter', 'FrontRight'],
        ['FrontLeft', 'FrontCenter', 'FrontRight', 'RightAhead', 'skip','skip','skip', 'skip','skip','LeftBehind','skip', 'LeftAhead']
    ]
    SensorArray.append(SensorMaxValues[SensorAllDirection[orientation].index('LeftBehind')])
    SensorArray.append(SensorMaxValues[SensorAllDirection[orientation].index('LeftAhead')])
    SensorArray.append(SensorMaxValues[SensorAllDirection[orientation].index('FrontLeft')])
    SensorArray.append(SensorMaxValues[SensorAllDirection[orientation].index('FrontCenter')])
    SensorArray.append(SensorMaxValues[SensorAllDirection[orientation].index('FrontRight')])
    SensorArray.append(SensorMaxValues[SensorAllDirection[orientation].index('RightAhead')])

    return SensorArray

def PrintMap():
    for i in range(len(Arena)):
        print Arena[i]
    print

#PrintMap()