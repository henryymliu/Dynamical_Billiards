import tkinter as tk
import tkinter.ttk as ttk
import Pmw
import RectTable as rect
import LTable as Ltab
import circle
from PIL import Image, ImageTk
import numpy as np
import platform


class Main(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        n=ttk.Notebook(self)
        f1=RectTab(self)
        f2=LTab(self)
        f3=CircTab(self)
        n.add(f1,text='Rectangle')
        n.add(f2,text='L')
        n.add(f3,text='Circle ')
        n.pack()


class RectTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Ball Formation Selection
        self.ballFormations = ["1 Ball", "2 Balls", "3 Balls", "4 Balls"]
        self.width=tk.IntVar()
        self.height=tk.IntVar()
        self.balls=['Ball 1', 'Ball 2','Ball 3','Ball 4']
        self.ballStates={'Ball 1':[0.5,0.5,1,0.5],'Ball 2':[1.5,1.5,1,-0.5],'Ball 3':[0.5,1.5,-1,0.5],'Ball 4':[1.5,0.5,-0.5,1]}
        self.currentBall='Ball 1'

        self.grid()  # sets up grid



        self.grid_columnconfigure(0, weight=1)
        # self.resizable(True,False)

        self.ballFormationList = Pmw.ComboBox(self, label_text='Choose Ball Formation', labelpos='nw',
                                              selectioncommand=self.changeFormation,
                                              scrolledlist_items=self.ballFormations, dropdown=1)
        self.ballFormationList.grid(column=0, row=1)
        self.ballFormationList.selectitem(0)

        self.ballLabel = tk.Label(self,text='Ball Parameters')
        self.ballLabel.grid(column=0,row=2,sticky='ew')

        # self.seperatorTop = ttk.Separator(self,orient=tk.HORIZONTAL)
        # self.seperatorTop.grid(column=0,row=3)

        self.ballSelector = Pmw.ComboBox(self, label_text='Choose Ball', labelpos='nw',
                                              selectioncommand=self.changeBall,
                                              scrolledlist_items=self.balls, dropdown=1)
        self.ballSelector.grid(column=0,row=3)
        self.ballSelector.selectitem(0)

        self.initialXVelScale = tk.Scale(self, from_=-3, to=3, orient=tk.HORIZONTAL,
                                             label='Initial X Velocity',resolution=0.1)
        self.initialXVelScale.grid(column=0, row=4, columnspan=2, sticky='W' + 'E')
        self.initialXVelScale.set(self.ballStates[self.currentBall][2])

        self.initialYVelScale = tk.Scale(self, from_=-3, to=3, orient=tk.HORIZONTAL,
                                             label='Initial Y Velocity',resolution=0.1)
        self.initialYVelScale.grid(column=0, row=5, columnspan=2, sticky='W' + 'E')
        self.initialYVelScale.set(self.ballStates[self.currentBall][3])

        self.initialXScale = tk.Scale(self, from_=0, to=2, orient=tk.HORIZONTAL,
                                           label='Initial X Position',resolution=0.1)
        self.initialXScale.grid(column=0, row=6, columnspan=2, sticky='W' + 'E')
        self.initialXScale.set(self.ballStates[self.currentBall][0])

        self.initialYScale = tk.Scale(self, from_=0, to=2, orient=tk.HORIZONTAL,
                                           label='Initial Y Position',resolution=0.1)
        self.initialYScale.grid(column=0, row=7, columnspan=2, sticky='W' + 'E')
        self.initialYScale.set(self.ballStates[self.currentBall][1])

        self.widthScale = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL,
                                           label='Width',resolution=1,variable=self.width,
                                           command=self.updateSize)
        self.widthScale.grid(column=2, row=6, columnspan=1, sticky='W' + 'E')
        self.widthScale.set(2)

        self.heightScale = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL,
                                           label='Height',resolution=1,variable=self.height,
                                           command=self.updateSize)
        self.heightScale.grid(column=2, row=7, columnspan=1, sticky='W' + 'E')
        self.heightScale.set(2)

        self.simLabel = tk.Label(self,text='Simulation Parameters')
        self.simLabel.grid(column=0,row=9,sticky='ew')

        self.playbackSpeedScale = tk.Scale(self, from_=0, to=60, orient=tk.HORIZONTAL,
                                                label='Playback Speed (fps)',resolution=1)
        self.playbackSpeedScale.grid(column=0, row=10, columnspan=2, sticky='W' + 'E')
        self.playbackSpeedScale.set(30)

        # define a button to start simulation, runs startSimulation() when
        # clicked
        self.button = tk.Button(self, text=u'Start simulation',
                                command=self.startSimulation)
        self.button.grid(column=1, row=11)


        self.toTrace = tk.BooleanVar()
        self.traceCheck = tk.Checkbutton(self, text="Trace", variable=self.toTrace)
        self.traceCheck.grid(column=2, row=11, sticky='W')
        self.traceCheck.select()


        # make canvas
        self.preview = tk.Canvas(self, width=400, height=300)
        self.preview.grid(column=2, row=1, rowspan=5)
        self.changeFormation()

    #changes the preview image when a new stadium is selected
    def changeFormation(self,*args):
        #get the current stadium
        formation = self.ballFormationList.get(first=None, last=None)
        #select image based on operating system
        if platform.system == 'Windows':
            directory='images\Rect_1Ball.png'
            image = Image.open(directory)
        else:
            directory='images/Rect_1Ball.png'
            image = Image.open(directory)

        # make Tk compatible PhotoImage object, must save as object parameter
        # to avoid garbage collection
        self.photo = ImageTk.PhotoImage(image)
        #display image
        self.preview.create_image(0, 0, anchor='nw', image=self.photo)

        lastBall= self.ballSelector.get()
        x=self.initialXScale.get()
        y=self.initialYScale.get()
        xVel=self.initialXVelScale.get()
        yVel=self.initialYVelScale.get()
        self.ballStates[lastBall]=[x,y,xVel,yVel]

        if formation == self.ballFormations[0]:
            self.ballSelector.selectitem(0)
        elif formation == self.ballFormations[1] and (self.ballSelector.get() == \
                        self.balls[2] or self.ballSelector.get() == self.balls[3]):
            self.ballSelector.selectitem(1)
        elif formation == self.ballFormations[2] and self.ballSelector.get() == \
                        self.balls[3]:
            self.ballSelector.selectitem(2)

        self.currentBall=self.ballSelector.get()

        newX=self.ballStates[self.currentBall][0]
        newY=self.ballStates[self.currentBall][1]
        newXVel=self.ballStates[self.currentBall][2]
        newYVel=self.ballStates[self.currentBall][3]

        self.initialXScale.set(newX)
        self.initialYScale.set(newY)
        self.initialXVelScale.set(newXVel)
        self.initialYVelScale.set(newYVel)




    def updateSize(self,*args):
        width=self.width.get()
        height=self.height.get()
        self.initialXScale.config(to=width)
        self.initialYScale.config(to=height)

        for ball, state in self.ballStates.items():
            if state[0] > width:
                state[0] = width
            if state[1] > height:
                state[1] = height

    def changeBall(self,*args):
        formation = self.ballFormationList.get()
        if formation == self.ballFormations[0]:
            self.ballSelector.selectitem(0)
        elif formation == self.ballFormations[1] and (self.ballSelector.get() == \
                        self.balls[2] or self.ballSelector.get() == self.balls[3]):
            self.ballSelector.selectitem(1)
        elif formation == self.ballFormations[2] and self.ballSelector.get() == \
                        self.balls[3]:
            self.ballSelector.selectitem(2)

        newBall=self.ballSelector.get()
        x=self.initialXScale.get()
        y=self.initialYScale.get()
        xVel=self.initialXVelScale.get()
        yVel=self.initialYVelScale.get()

        self.ballStates[self.currentBall]=[x,y,xVel,yVel]

        newX=self.ballStates[newBall][0]
        newY=self.ballStates[newBall][1]
        newXVel=self.ballStates[newBall][2]
        newYVel=self.ballStates[newBall][3]

        self.initialXScale.set(newX)
        self.initialYScale.set(newY)
        self.initialXVelScale.set(newXVel)
        self.initialYVelScale.set(newYVel)

        self.currentBall=newBall




    #runs when start simulation button is pressed
    def startSimulation(self):
        x=self.initialXScale.get()
        y=self.initialYScale.get()
        xVel=self.initialXVelScale.get()
        yVel=self.initialYVelScale.get()
        self.ballStates[self.currentBall]=[x,y,xVel,yVel]

        #put all selections into dictionary
        simArgs = dict()
        simArgs['ballF'] = self.ballFormationList.get(first=None, last=None)
        simArgs['playbackSpeed'] = self.playbackSpeedScale.get()
        simArgs['trace'] = self.toTrace.get()
        simArgs['width'] = self.width.get()
        simArgs['height'] = self.height.get()
        simArgs['balls'] = self.ballStates
        simArgs['ballFormation'] = self.ballFormationList.get()

        #create simulation
        simulation = rect.RectTable(**simArgs)
        simulation.main()

class LTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Ball Formation Selection
        ballFormations = ["1 Ball"]

        self.lastXPos=1

        self.grid()  # sets up grid

        # define a button to start simulation, runs startSimulation() when
        # clicked
        self.button = tk.Button(self, text=u'Start simulation',
                                command=self.startSimulation)
        self.button.grid(column=1, row=9)


        self.grid_columnconfigure(0, weight=1)
        # self.resizable(True,False)

        self.ballFormationList = Pmw.ComboBox(self, label_text='Choose Ball Formation', labelpos='nw',
                                              selectioncommand=self.changeImage,
                                              scrolledlist_items=ballFormations, dropdown=1)
        self.ballFormationList.grid(column=0, row=2)
        self.ballFormationList.selectitem(0)

        self.initialXVelScale = tk.Scale(self, from_=-3, to=3, orient=tk.HORIZONTAL,
                                             label='Initial X Velocity',resolution=0.1)
        self.initialXVelScale.grid(column=0, row=3, columnspan=2, sticky='W' + 'E')
        self.initialXVelScale.set(1)

        self.initialYVelScale = tk.Scale(self, from_=-3, to=3, orient=tk.HORIZONTAL,
                                             label='Initial Y Velocity',resolution=0.1)
        self.initialYVelScale.grid(column=0, row=4, columnspan=2, sticky='W' + 'E')
        self.initialYVelScale.set(0.5)

        self.initialXScale = tk.Scale(self, from_=0, to=4, orient=tk.HORIZONTAL,
                                           label='Initial X Position',resolution=0.1,command=self.checkPos)
        self.initialXScale.grid(column=0, row=5, columnspan=2, sticky='W' + 'E')
        self.initialXScale.set(1)

        self.initialYScale = tk.Scale(self, from_=0, to=6, orient=tk.HORIZONTAL,
                                           label='Initial Y Position',resolution=0.1,command=self.checkPos)
        self.initialYScale.grid(column=0, row=6, columnspan=2, sticky='W' + 'E')
        self.initialYScale.set(1)

        # self.widthScale = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL,
        #                                    label='Width',resolution=1,variable=self.width,
        #                                    command=self.updateSize)
        # self.widthScale.grid(column=2, row=6, columnspan=1, sticky='W' + 'E')
        # self.widthScale.set(2)
        #
        # self.heightScale = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL,
        #                                    label='Height',resolution=1,variable=self.height,
        #                                    command=self.updateSize)
        # self.heightScale.grid(column=2, row=7, columnspan=1, sticky='W' + 'E')
        # self.heightScale.set(2)

        self.playbackSpeedScale = tk.Scale(self, from_=0, to=60, orient=tk.HORIZONTAL,
                                                label='Playback Speed (fps)',resolution=0.1)
        self.playbackSpeedScale.grid(column=0, row=8, columnspan=2, sticky='W' + 'E')
        self.playbackSpeedScale.set(30)

        self.toTrace = tk.BooleanVar()
        self.traceCheck = tk.Checkbutton(self, text="Trace", variable=self.toTrace)
        self.traceCheck.grid(column=2, row=9, sticky='W')
        self.traceCheck.select()


        # make canvas
        self.preview = tk.Canvas(self, width=400, height=300)
        self.preview.grid(column=2, row=1, rowspan=5)
        self.changeImage()

    #changes the preview image when a new stadium is selected
    def changeImage(self,*args):
        #get the current stadium
        formation = self.ballFormationList.get(first=None, last=None)
        #select image based on operating system
        if platform.system == 'Windows':
            directory='images\L_{}.png'.format(formation).replace(' ','')
            image = Image.open(directory)
        else:
            directory='images/L_{}.png'.format(formation).replace(' ','')
            image = Image.open(directory)

        # make Tk compatible PhotoImage object, must save as object parameter
        # to avoid garbage collection
        self.photo = ImageTk.PhotoImage(image)
        #display image
        self.preview.create_image(0, 0, anchor='nw', image=self.photo)

    def checkPos(self,*args):
        if self.initialXScale.get() > 2 and self.initialYScale.get() > 2:
            if self.lastXPos < 2:
                self.initialXScale.set(2)
            else:
                self.initialYScale.set(2)

        self.lastXPos=self.initialXScale.get()


    #runs when start simulation button is pressed
    def startSimulation(self):
        # TODO: Handle unselected combobox case

        #put all selections into dictionary
        simArgs = dict()
        simArgs['ballF'] = self.ballFormationList.get(first=None, last=None)

        simArgs['initXVel'] = self.initialXVelScale.get()
        simArgs['initYVel'] = self.initialYVelScale.get()
        simArgs['initX'] = self.initialXScale.get()
        simArgs['initY'] = self.initialYScale.get()
        simArgs['playbackSpeed'] = self.playbackSpeedScale.get()
        simArgs['trace'] = self.toTrace.get()

        #create simulation
        simulation = Ltab.LTable(**simArgs)
        simulation.main()

class CircTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        global radius
        radius = circle.CircleTable().radius
        # Ball Formation Selection
        ballFormations = ["1 Ball"]

        self.grid()  # sets up grid

        # define a button to start simulation, runs startSimulation() when
        # clicked
        button = tk.Button(self, text=u'Start simulation',
                                command=self.startSimulation)
        button.grid(column=1, row=9)


        self.grid_columnconfigure(0, weight=1)
        # self.resizable(True,False)

        self.ballFormationList = Pmw.ComboBox(self, label_text='Choose Ball Formation', labelpos='nw',
                                              selectioncommand=self.changeImage,
                                              scrolledlist_items=ballFormations, dropdown=1)
        self.ballFormationList.grid(column=0, row=2)
        self.ballFormationList.selectitem(0)

        self.initialXVelScale = tk.Scale(self, from_=-3, to=3, orient=tk.HORIZONTAL,
                                             label='Initial X Velocity',resolution=0.1)
        self.initialXVelScale.grid(column=0, row=3, columnspan=2, sticky='W' + 'E')
        self.initialXVelScale.set(1)

        self.initialYVelScale = tk.Scale(self, from_=-3, to=3, orient=tk.HORIZONTAL,
                                             label='Initial Y Velocity',resolution=0.1)
        self.initialYVelScale.grid(column=0, row=4, columnspan=2, sticky='W' + 'E')
        self.initialYVelScale.set(0.5)

        self.initialXScale = tk.Scale(self, from_=-radius, to=radius, orient=tk.HORIZONTAL,
                                           label='Initial X Position',resolution=0.1, command=self.checkXPos)
        self.initialXScale.grid(column=0, row=5, columnspan=2, sticky='W' + 'E')
        self.initialXScale.set(0)

        self.initialYScale = tk.Scale(self, from_=-radius, to=radius, orient=tk.HORIZONTAL,
                                           label='Initial Y Position',resolution=0.1,command=self.checkYPos)
        self.initialYScale.grid(column=0, row=6, columnspan=2, sticky='W' + 'E')
        self.initialYScale.set(0)

        self.radiusScale = tk.Scale(self, from_=1, to_= 5, orient = tk.HORIZONTAL, label = 'Radius',
            resolution = 0.1,command = self.setRadius)
        #self.radiusScale.grid(column = 2,  row = 7, columnspan = 1, sticky = 'W' + 'E')
        self.radiusScale.set(2)

        self.playbackSpeedScale = tk.Scale(self, from_=0, to=60, orient=tk.HORIZONTAL,
                                                label='Playback Speed (fps)',resolution=0.1)
        self.playbackSpeedScale.grid(column=0, row=8, columnspan=2, sticky='W' + 'E')
        self.playbackSpeedScale.set(30)

        self.toTrace = tk.BooleanVar()
        self.traceCheck = tk.Checkbutton(self, text="Trace", variable=self.toTrace)
        self.traceCheck.grid(column=2, row=9, sticky='W')
        self.traceCheck.select()


        # make canvas
        self.preview = tk.Canvas(self, width=400, height=300)
        self.preview.grid(column=2, row=1, rowspan=5)
        self.changeImage()

    #changes the preview image when a new stadium is selected
    def changeImage(self,*args):
        #get the current stadium
        formation = self.ballFormationList.get(first=None, last=None)
        #select image based on operating system
        if platform.system == 'Windows':
            directory='images\Circle_1Ball.png'.format(formation).replace(' ','')
            image = Image.open(directory)
        else:
            directory='images/Circle_{}.png'.format(formation).replace(' ','')
            image = Image.open(directory)

        # make Tk compatible PhotoImage object, must save as object parameter
        # to avoid garbage collection
        self.photo = ImageTk.PhotoImage(image)
        #display image
        self.preview.create_image(0, 0, anchor='nw', image=self.photo)

    def checkYPos(self,*args):
        x=self.initialXScale.get()
        y=self.initialYScale.get()

        if x**2+y**2 > radius**2:
            if y>0:
                self.initialYScale.set(np.sqrt(abs(radius**2 -x**2)))
            else:
                self.initialYScale.set(-np.sqrt(abs((radius**2 -x**2))))
    def checkXPos(self,*args):
        x=self.initialXScale.get()
        y=self.initialYScale.get()

        if x**2+y**2 > radius**2:
            if x>0:
                self.initialXScale.set(np.sqrt(radius**2 -y**2))
            else:
                self.initialXScale.set(-np.sqrt(radius**2 -y**2))

    def setRadius(self, *args):
        radius = self.radiusScale.get();

    #runs when start simulation button is pressed
    def startSimulation(self):
        # TODO: Handle unselected combobox case

        #put all selections into dictionary
        simArgs = dict()
        simArgs['ballF'] = self.ballFormationList.get(first=None, last=None)

        simArgs['initXVel'] = self.initialXVelScale.get()
        simArgs['initYVel'] = self.initialYVelScale.get()
        simArgs['initX'] = self.initialXScale.get()
        simArgs['initY'] = self.initialYScale.get()
        simArgs['radius'] = radius
        simArgs['playbackSpeed'] = self.playbackSpeedScale.get()
        simArgs['trace'] = self.toTrace.get()

        #create simulation
        simulation = circle.CircleTable(**simArgs)
        simulation.main()

if __name__ == '__main__':
    app = Main(None)
    app.title('Billiards Simulator')
    app.mainloop()
