from Tkinter import *
import time
import tkMessageBox
import explore
import simulator
import ShortestPath as SP
import mdfConvert


class Simulator:
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(self.master, width=680, height=880)
        self.canvas.bind("<ButtonRelease>", self.addObstacle)
        self.canvas.pack(side="left")

        self.widgetArray = [[0 for i in range(17)] for j in range(22)]
        self.arena = [[0 for i in range(17)] for j in range(22)]
        self.exploredArena = [[0 for i in range(17)] for j in range(22)]
        
        self.frame = Frame(self.master)
        self.frame.pack(side="right")

        #Buttons
        self.reset_button = Button(self.frame, width=20, height=2, text="Reset Map", bg="orange", command=self.initCanvas).pack()
        self.explore_button = Button(self.frame, width=20, height=2, text="Run Exploration", bg="orange", command=self.RunExplore).pack()
        self.shortestPath_button = Button(self.frame, width=20, height=2, text="Run ShortestPath", bg="orange", command=self.RunShortestPath).pack()


        self.count = 0
    def UpdateCanvas(self, exploredArena):
        for i in range(1,21):
            for j in range(1,16):
                if(exploredArena[i][j] == 1):
                    self.canvas.itemconfig(self.widgetArray[i][j], fill="#000000")
                elif(exploredArena[i][j] == 2):
                    self.canvas.itemconfig(self.widgetArray[i][j], fill="#2a933c")
                elif(exploredArena[i][j] == 3):
                    self.canvas.itemconfig(self.widgetArray[i][j], fill="#99dda4")
        return
    
    def UpdateShortestCanvas(self, Arena):
        for i in range(20):
            for j in range(15):
                if(Arena[i][j] == 2):
                    self.canvas.itemconfig(self.widgetArray[i+1][j+1], fill="#231f60")
        return

    def addObstacle(self, event):
        xCoord = event.x//40
        yCoord = event.y//40
        self.arena[yCoord][xCoord] = 1
        if((12<xCoord<16 and 1<yCoord<4) or (17<yCoord<21 and 1<xCoord<4)):
            print "This is a restricted Zone"
        else:
            self.canvas.itemconfig(self.widgetArray[yCoord][xCoord], fill="#333333")
        return

    def clickReset(self):
        self.initCanvas(self.canvas, self.widgetArray)
        return

    def RunExplore(self):
        simulator.Arena = self.arena
        newArena = explore.CalculateMove()
        if(newArena != 0):
            self.UpdateCanvas(newArena)
            self.master.after(200, self.RunExplore)
            self.exploredArena = newArena
        else:
            tkMessageBox.showinfo("Run Exploration", "Exploration Complete")
            MDFstring = mdfConvert.ExploreArrayToMDF(self.exploredArena)
            print MDFstring
            tkMessageBox.showinfo("MDF String for Exploration", MDFstring)
            MDFstring = mdfConvert.obstacleArrayToMDF(self.exploredArena)
            print MDFstring
            tkMessageBox.showinfo("MDF String for Obstacles", MDFstring)
            return


    def RunShortestPath(self):
        if(self.count==0):
            SP.shortestPath()
        if(self.count<len(SP.finalPath)):
            shortestarena = SP.printCommand(self.count)
            self.UpdateShortestCanvas(shortestarena)
            self.count += 1
            self.master.after(200, self.RunShortestPath)
        else:
            tkMessageBox.showinfo("Run ShortestPath", "Shortest Path Complete!")
            self.count = 0
            return

    def initCanvas(self):
        explore.EmptyArena=[[0 for i in range(17)] for j in range(22)]
        explore.StartPos = {
            'row':19,
            'col':2
        }
        explore.GoalPos = {
            'row':1,
            'col':15
        }
        explore.robot = explore.ArduinoRobot()

        self.widgetArray = [[0 for i in range(17)] for j in range(22)]
        self.arena = [[0 for i in range(17)] for j in range(22)]

        for i in range(22):
            self.arena[i][0] = 1
            self.arena[i][16] = 1
        for i in range(17):
            self.arena[0][i] = 1
            self.arena[21][i] = 1


        #Initialise Canvas PaintJob
        for i in range(22):
            for j in range(17):
                self.widgetArray[i][j] = self.canvas.create_rectangle(0+j*40,0+i*40,40+j*40,40+i*40, fill="grey")

        for i in range(22):
            self.canvas.itemconfig(self.widgetArray[i][0], fill="red")
            self.canvas.itemconfig(self.widgetArray[i][16], fill="red")

        for i in range(17):
            self.canvas.itemconfig(self.widgetArray[0][i], fill="red")
            self.canvas.itemconfig(self.widgetArray[21][i], fill="red")

        for i in range(1,4):
            for j in range(1,4):
                self.canvas.itemconfig(self.widgetArray[21-j][i], fill="green")
                self.canvas.itemconfig(self.widgetArray[i][16-j], fill="green")

master = Tk()
master.title("Grp 12 MDP Simulator")


sim = Simulator(master)
mainloop()