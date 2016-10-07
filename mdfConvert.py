def obstacleArrayToMDF(arena):
    mdf = ""
    for i in range(20, 0, -1):
        for j in range(1, 16):
            if(arena[i][j]>0):
                if (arena[i][j]== 1):
                    mdf += "1"
                else:
                    mdf += "0"
    mdf = mdf + "0"*(8 - len(mdf)%8)
    return binToHex(mdf)
                
def ExploreArrayToMDF(arena):
    mdf="11"
    if (len(arena)==22):
        for i in range(20,0,-1):
            for j in range(1,16):
                if(arena[i][j]==0):
                    mdf += "0"

                else:
                    mdf += "1"
    else:
        for i in range(20):
            for j in range(15):
                if(arena[i][j] == 0):
                    mdf += "0"
                else:
                    mdf += "1"

    mdf += "11"
    return binToHex(mdf)

def MDFtoObstacleArray(mdf, arena):
    mdf = hexToBin(mdf)
    for i  in range(20,0,-1):
        for j in range(1, 16):
            if (arena[i][j] == 1):
                if (mdf[0] == 0):
                    arena[i][j] == 3
                    mdf = mdf[1:]
    return arena
    

def MDFtoExploreArray(mdf):
    arena = []
    shortmdf = hexToBin(mdf)[1:-2]
    for i in range(21,-1,-1):
        arena.append([])
        for j in range(17):
            if (i == 0 or i == 21 or j == 0 or j ==16):
                arena[i].append(1)
            else:
                arena[i].append(int(shortmdf[0]))
                shortmdf = shortmdf[1:]
    return arena
    
        
def binToHex(mdf):
    hexstr = ""
    for i in range(len(mdf)/4):
        hexstr += hex(int(mdf[:4],2))[2:]
        mdf = mdf[4:]
    return hexstr

def hexToBin(mdf):
    return bin(int(mdf,16))[2:]
