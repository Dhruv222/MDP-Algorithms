import random
length = 17
breadth = 22
#0=Unexplored 1=Free -1=obstacle

def generate():
    arena=[[0 for i in range(length)] for j in range(breadth)]
    for i in range(breadth):
        for j in range(length):
            randnum = random.randint(1, 10)
            if randnum < 3:
                arena[i][j] = 1
    arena[19][3] = 0
    arena[19][1] = 0
    arena[19][2] = 0
    arena[18][3] = 0
    arena[18][1] = 0
    arena[18][2] = 0
    arena[20][3] = 0
    arena[20][1] = 0
    arena[20][2] = 0
    
    arena[3][14] = 0
    arena[1][14] = 0
    arena[2][14] = 0
    arena[3][13] = 0
    arena[1][13] = 0
    arena[2][13] = 0
    arena[3][15] = 0
    arena[1][15] = 0
    arena[2][15] = 0

    for i in range(length):
        arena[0][i] = 1
        arena[21][i] = 1
    for i in range(breadth):
        arena[i][0] = 1
        arena[i][16] = 1       
    return arena
