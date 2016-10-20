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

        #For Time and Coverage Constraints
        self.timeCount = 0
        self.CoverageLimit = 100
        self.timeLimit = 500
        self.percentageCovered = 0

        #For MdfString generation and usage
        self.mdfString1 = ""
        self.mdfString2 = ""

        #Buttons
        self.mdfEntry1 = Entry(self.frame)
        self.mdfEntry1.pack()
        self.mdfEntry2 = Entry(self.frame)
        self.mdfEntry2.pack()
        self.CreateArena_button = Button(self.frame, width=20, height=2, text="Create Map", bg="orange", command=self.initArena).pack()
        self.reset_button = Button(self.frame, width=20, height=2, text="Reset Map", bg="orange", command=self.initCanvas).pack()
        self.TimeEntry = Entry(self.frame)
        self.TimeEntry.pack()
        self.TimeEntry.insert(0, "500")
        self.PercentEntry = Entry(self.frame)
        self.PercentEntry.pack()
        self.PercentEntry.insert(0, "100")
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
                elif(exploredArena[i][j] == 6):
                    self.canvas.itemconfig(self.widgetArray[i][j], fill="#00245e")
                elif(exploredArena[i][j] == 5):
                    self.canvas.itemconfig(self.widgetArray[i][j], fill="#629bf7")
        return


    def initArena(self):
        mdf1 = self.mdfEntry1.get()
        mdf2 = self.mdfEntry2.get()
        newArena = mdfConvert.MDFtoSPArena(mdf1, mdf2)
        self.initCanvas()
        self.UpdateCanvas(newArena)
        self.arena = newArena
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
        self.initCanvas()
        return

    def RunExplore(self):
        self.timeLimit = int(self.TimeEntry.get())
        self.CoverageLimit = int(self.PercentEntry.get())
        simulator.Arena = self.arena
        newArena = explore.CalculateMove()
        if(newArena != -1):
            self.percentageCovered = 0
            for i in range(1, len(newArena)-1):
                for j in range(1, len(newArena[i])-1):
                    if newArena[i][j] != 0:
                        self.percentageCovered += 1
            self.percentageCovered /= 3
        print self.percentageCovered, self.CoverageLimit
        if(newArena != -1 and self.percentageCovered <= self.CoverageLimit and self.timeCount < self.timeLimit):
            self.UpdateCanvas(newArena)
            self.master.after(10, self.RunExplore)
            self.timeCount += 0.2
            self.exploredArena = newArena
        else:
            tkMessageBox.showinfo("Run Exploration", "Exploration Completed with "+str(self.percentageCovered)+"'%' area covered and "+str(self.timeCount)+"secs taken.")
            self.mdfString1 = mdfConvert.ExploreArrayToMDF(self.exploredArena)

            self.mdfEntry1.delete(0, END)
            self.mdfEntry1.insert(0,self.mdfString1)

            print self.mdfString1
            tkMessageBox.showinfo("MDF String for Exploration", self.mdfString1)
            self.mdfString2 = mdfConvert.obstacleArrayToMDF(self.exploredArena)

            self.mdfEntry2.delete(0, END)
            self.mdfEntry2.insert(0,self.mdfString2)

            print self.mdfString2
            tkMessageBox.showinfo("MDF String for Obstacles", self.mdfString2)
            return


    def RunShortestPath(self):
        if(self.count==0):
            SP.shortestPath(self.mdfString1,self.mdfString2)
        if(self.count<len(SP.finalPath)):
            shortestarena = SP.printCommand(self.count)
            self.UpdateShortestCanvas(shortestarena)
            self.count += 1
            self.master.after(50, self.RunShortestPath)
        else:
            tkMessageBox.showinfo("Run ShortestPath", "Shortest Path Complete!")
            self.count = 0
            return

    def initCanvas(self):
        explore.EmptyArena=[[0 for i in range(17)] for j in range(22)]
        explore.StartPos = {
            'row':18,
            'col':3
        }
        explore.GoalPos = {
            'row':1,
            'col':15
        }
        explore.robot = explore.ArduinoRobot()
        explore.previousmove = ""
        self.timeCount = 0

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
