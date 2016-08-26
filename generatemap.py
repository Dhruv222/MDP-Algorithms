import random
length = 15
breadth = 20
#0=Unexplored 1=Free -1=obstacle

def generate():
    arena=[[0 for i in range(length)] for j in range(breadth)]
    for i in range(breadth):
        print(arena[i])
    for i in range(breadth):
        for j in range(length):
            randnum = random.randint(1, 10)
            if randnum < 3:
                arena[i][j] = -1
    print("\n")
    for i in range(breadth):
        print(arena[i])
    return arena
