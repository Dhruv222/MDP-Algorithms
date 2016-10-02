import explore
def PrintMap(printArena):
    for i in range(len(printArena)):
        print printArena[i]
    print

printArena = explore.RunExplore()

PrintMap(printArena)

