import random
length = 15
breadth = 20
#0=Unexplored 1=Free -1=obstacle

def generate():
    arena=[[0 for i in range(length)] for j in range(breadth)]
    for i in range(breadth):
        for j in range(length):
            randnum = random.randint(1, 10)
            if randnum < 3:
                arena[i][j] = 1
    arena[19][0] = 0
    arena[19][1] = 0
    arena[19][2] = 0
    arena[18][0] = 0
    arena[18][1] = 0
    arena[18][2] = 0
    arena[17][0] = 0
    arena[17][1] = 0
    arena[17][2] = 0
    
    arena[0][14] = 0
    arena[1][14] = 0
    arena[2][14] = 0
    arena[0][13] = 0
    arena[1][13] = 0
    arena[2][13] = 0
    arena[0][12] = 0
    arena[1][12] = 0
    arena[2][12] = 0        
    return arena
