"""
Gui module for the Dynamical Billiards project.
Run this module as main to start the program.

Created March 2017
"""

import tkinter as tk
import tkinter.ttk as ttk
import Pmw
from PIL import Image, ImageTk
import numpy as np
import LTable as Ltab
import RectTable as rect
import circle
import Buminovich
import Lorentz
from PIL import Image, ImageTk
import platform


class AbstractTab(tk.Frame):
    """
    Abstract class for the tabs that select which table to simulate.

    Subclasses must implement:
        initialize(self)
        updateSize(self)
        startSimulation(self)
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.nBalls = 1
        self.initialize()

    def initialize(self):
        """
        Sets up base gui widgets that are used in every tab:
            initial x and y
            initial velocity
            trace checkbox
            ball formation selection
            number of balls
            start simulation button
        """
        # dictionary for the simulation arguments
        self.simArgs={}

        # ComboBox item lists


        # self.ballFormations = ["1 Ball", "2 Balls", "3 Balls", "4 Balls"]
        # # self.balls = ['Ball 1', 'Ball 2', 'Ball 3', 'Ball 4']
        self.balls = tuple(map(str, range(self.nBalls)))
        # initial states
        self.initBallState = [1, 1, 1, -3]
        self.ballStates = {1 : self.initBallState}
        self.currentBall = 1

        # sets up grid
        self.grid()
        self.grid_columnconfigure(0, weight=1)

        # set up selector for number of balls
        # self.numberOfBallsSelector = Pmw.ComboBox(self,
        #     label_text='Choose Ball Formation', labelpos='nw',
        #     selectioncommand=self.changeFormation,
        #     scrolledlist_items=self.ballFormations, dropdown=1)
        self.numberOfBallsSelector = Pmw.EntryField(self, validate=Pmw.numericvalidator, label_text='# balls',
                                                    labelpos='nw', modifiedcommand=self.changeFormation)
        self.numberOfBallsSelector.grid(column=0, row=1)
        self.numberOfBallsSelector.setvalue(1)

        # label for ball parameters
        self.ballLabel = tk.Label(self, text='Ball Parameters')
        self.ballLabel.grid(column=0, row=2, sticky='ew')

        # selector for which ball to adjust parameters for
        self.ballSelector = Pmw.ComboBox(self,label_text='Choose Ball',
            labelpos='nw',selectioncommand=self.changeBall,
            scrolledlist_items=self.balls, dropdown=1)
        #
        self.ballSelector.grid(column=0, row=3)
        self.ballSelector.selectitem(0)

        # scale for initial x velocity
        self.initialXVelScale = tk.Scale(self, from_=-3, to=3,
            orient=tk.HORIZONTAL, label='Initial X Velocity', resolution=0.1)
        self.initialXVelScale.grid(column=0, row=4, columnspan=2,
            sticky='W' + 'E')
        self.initialXVelScale.set(self.ballStates[self.currentBall][2])

        # scale for initial y velocity
        self.initialYVelScale = tk.Scale(self, from_=-3, to=3,
            orient=tk.HORIZONTAL, label='Initial Y Velocity', resolution=0.1)
        self.initialYVelScale.grid(column=0, row=5, columnspan=2,
            sticky='W' + 'E')
        self.initialYVelScale.set(self.ballStates[self.currentBall][3])

        # scale for initial x position
        self.initialXScale = tk.Scale(self, from_=0, to=2, orient=tk.HORIZONTAL,
            label='Initial X Position', resolution=0.01)
        self.initialXScale.grid(column=0, row=6, columnspan=2, sticky='W' + 'E')
        self.initialXScale.set(self.ballStates[self.currentBall][0])

        # scale for initial y position
        self.initialYScale = tk.Scale(self, from_=0, to=2, orient=tk.HORIZONTAL,
            label='Initial Y Position', resolution=0.01)
        self.initialYScale.grid(column=0, row=7, columnspan=2, sticky='W' + 'E')
        self.initialYScale.set(self.ballStates[self.currentBall][1])

        # label for simulation parameters
        self.simLabel = tk.Label(self, text='Simulation Parameters')
        self.simLabel.grid(column=0, row=9, sticky='ew')

        # scale for playback speed
        self.playbackSpeedScale = tk.Scale(self, from_=0, to=60,
            orient=tk.HORIZONTAL, label='Playback Speed (fps)', resolution=1)
        self.playbackSpeedScale.grid(column=0, row=10, columnspan=2,
            sticky='W' + 'E')
        self.playbackSpeedScale.set(30)

        # button to start simulation
        self.button = tk.Button(self, text=u'Start simulation',
            command=self.startSimulation)
        self.button.grid(column=1, row=11)

        # button to generate preview image
        self.previewButton = tk.Button(self, text=u'Generate Preview',
            command=self.generatePreview)
        self.previewButton.grid(column=2, row=11)


        # checkbox for wether or not to trace the path
        self.toTrace = tk.BooleanVar()
        self.traceCheck = tk.Checkbutton(self, text="Trace",
            variable=self.toTrace)
        self.traceCheck.grid(column=2, row=11, sticky='W')
        self.traceCheck.select()

        # table preview canvas
        self.preview = tk.Canvas(self, width=300, height=300)
        self.preview.grid(column=2, row=1, rowspan=5)

    def saveParameters(self):
        """
        saves the current ball state.
        puts all the general values in the simArgs dictionary

        subclasses should implement
        def saveParameters(self):
            super(SubClass,self).saveParameters()

            any extra stuff that table needs goes here
        """
        # save current scale values into the ball state for the current ball
        x = self.initialXScale.get()
        y = self.initialYScale.get()
        xVel = self.initialXVelScale.get()
        yVel = self.initialYVelScale.get()
        self.ballStates[self.currentBall] = [x, y, xVel, yVel]
        # set new currentBall if changed
        self.currentBall = int(self.ballSelector.get())
        # the states of all the balls to be simulated
        self.simArgs['balls']=self.ballStates
        self.simArgs['playbackSpeed'] = self.playbackSpeedScale.get()
        self.simArgs['trace'] = self.toTrace.get()
        # get number of balls from formation string
        self.simArgs['nBalls'] = self.nBalls
        # for s in self.numberOfBallsSelector.get().split():
        #     if s.isdigit():
        #         self.simArgs['nBalls']=int(s)

    def generatePreview(self):
        """
        Saves parameters, generates the preview and displays it to the canvas
        """
        self.saveParameters()
        image=self.simulation.generatePreview()
        # convert pil image to a tkinter image
        self.photo = ImageTk.PhotoImage(image)

        # display image
        self.preview.create_image(0, 0, anchor='nw', image=self.photo)

    def changeFormation(self, *args):
        """
        Changes what balls can be selected to change values for.
        Gets called when number of balls is changed

        Also saves the parameters
        """

        # get the number of balls
        # formation = self.numberOfBallsSelector.get(first=None, last=None)
        upnballs = int(self.numberOfBallsSelector.get())
        if upnballs >= self.nBalls:
            # self.createmorestates = True
            for i in range(self.nBalls, upnballs):
                self.ballStates[i] = self.initBallState

                # TODO: change this later after we figure out proper initial ball locations
                self.ballStates[i][3] +=0.1

        self.nBalls = upnballs
        self.balls = tuple(map(str, range(self.nBalls)))
        # self.saveParameters()
        # recreate combobox with updated number of balls
        self.ballSelector = Pmw.ComboBox(self, label_text='Choose Ball',
                                         labelpos='nw', selectioncommand=self.changeBall,
                                         scrolledlist_items=self.balls, dropdown=1)
        self.ballSelector.grid(column=0, row=3)
        self.ballSelector.selectitem(0)
        # self.saveParameters()
        # set the ball selector based on what formation is chosen
        # if formation == self.ballFormations[0]:
        #     self.ballSelector.selectitem(0)
        # elif formation == self.ballFormations[1] and (self.ballSelector.get()\
        #     == self.balls[2] or self.ballSelector.get() == self.balls[3]):
        #     self.ballSelector.selectitem(1)
        # elif formation == self.ballFormations[2] and self.ballSelector.get() ==\
        #     self.balls[3]:
        #     self.ballSelector.selectitem(2)

        # set sliders to new ball state if it was chaged above
        # r

    def updateSize(self, *args):
        """
        should reset x and y sliders when they are moved outside the domain.
        must be implemented for each subclass.
        """
        return None

    def changeBall(self, *args):
        """
            run when a different ball is selected.
            saveParameters and sets sliders to settings for new ball.
            also checks that you have selected the appropriate number of balls.
        """

        # formation = self.numberOfBallsSelector.get()
        # # set ball selector if needed
        # if formation == self.ballFormations[0]:
        #     self.ballSelector.selectitem(0)
        # elif formation == self.ballFormations[1] and (self.ballSelector.get() == self.balls[2]
        #                                               or self.ballSelector.get() == self.balls[3]):
        #     self.ballSelector.selectitem(1)
        # elif formation == self.ballFormations[2] and self.ballSelector.get() == self.balls[3]:
        #     self.ballSelector.selectitem(2)

        self.saveParameters()
        # set sliders to state for new ball
        newState = self.ballStates[self.currentBall]
        self.initialXScale.set(newState[0])
        self.initialYScale.set(newState[1])
        self.initialXVelScale.set(newState[2])
        self.initialYVelScale.set(newState[3])

    # must be implemented for each type
    def startSimulation(self):
        """Saves parameters and starts simulation."""
        self.saveParameters()
        self.simulation.main()

class Main(tk.Tk):
    """
    The tkinter window and Notebook that holds all the tabs
    """
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        """makes the Notebook and adds all the frames for each table"""
        # Notebook holds all the tabs
        n = ttk.Notebook(self)
        f1 = RectTab(self)
        f2 = LTab(self)
        f3 = CircTab(self)
        f4 = BuminTab(self)
        f5 = LorentzTab(self)
        n.add(f1, text='Rectangle')
        n.add(f2, text='L')
        n.add(f3, text='Circle ')
        n.add(f4, text='Buminovich')
        n.add(f5, text='Lorentz')
        # need to pack for the Notebook to display
        n.pack()

class RectTab(AbstractTab):
    """
    subclass of AbstractTab for the Rectangle table
    """
    def initialize(self):
        """
        initializes the super class and adds the height and widthScale for
        the Rectangle.
        """

        super(RectTab,self).initialize()
        # special tkinter variables that will be changed with the scales
        self.width = tk.IntVar()
        self.height = tk.IntVar()

        # make width scale
        self.widthScale = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL,
            label='Width', resolution=1, variable=self.width,
            command=self.updateSize)
        self.widthScale.grid(column=2, row=6, columnspan=1, sticky='W' + 'E')
        self.widthScale.set(2)

        # make height scale
        self.heightScale = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL,
            label='Height', resolution=1, variable=self.height,
            command=self.updateSize)
        self.heightScale.grid(column=2, row=7, columnspan=1, sticky='W' + 'E')
        self.heightScale.set(2)

    def updateSize(self, *args):
        """sets range of x and y sliders, and validates states"""
        width = self.width.get()
        height = self.height.get()
        self.initialXScale.config(to=width)
        self.initialYScale.config(to=height)
        # error check that state is not outside bounds
        for ball, state in self.ballStates.items():
            if state[0] > width:
                state[0] = width
            if state[1] > height:
                state[1] = height

    def saveParameters(self):
        """
        Saves super class parameters as well as height and width.
        Also initializes simulation if not already done or updates it.
        """
        super(RectTab,self).saveParameters()
        self.simArgs['width'] = self.width.get()
        self.simArgs['height'] = self.height.get()
        # updates simulation if it exists
        # makes one if it doesn't
        try:
            self.simulation.update(**self.kwargs)
        except AttributeError:
            self.simulation = rect.RectTable(**self.simArgs)

class LTab(AbstractTab):
    """
    subclass of AbstractTab for the L table
    """
    def saveParameters(self):
        """
        saves superclass parameters and updates or initializes simulation
        """
        super(LTab,self).saveParameters()
        # updates simulation if it exists
        # makes one if it doesn't
        try:
            self.simulation.update(**self.kwargs)
        except AttributeError:
            self.simulation = Ltab.LTable(**self.simArgs)

class CircTab(AbstractTab):
    """
    subclass of AbstractTab for the Circle table
    """

    def initialize(self):
        """
        initializes the super class and adds the radius. also changes the
        x and y scales
        """
        super(CircTab,self).initialize()
        self.radius = 2
        # set x and y scales for the circle size and use checkXPos and
        # checkYPos instead of updateSize
        self.initialXScale.config(from_=-self.radius, to=self.radius,
            command=self.checkXPos,resolution=0.01)
        self.initialYScale.config(from_=-self.radius, to=self.radius,
            command=self.checkYPos,resolution=0.01)
    def checkYPos(self, *args):
        """
        checks if the y position set will be outside the circle and will hold
        it at that point
        """
        x = self.initialXScale.get()
        y = self.initialYScale.get()

        if x ** 2 + y ** 2 > self.radius**2:
            if y > 0:
                self.initialYScale.set(np.sqrt(self.radius**2 - x ** 2))
            else:
                self.initialYScale.set(-np.sqrt(self.radius**2 - x ** 2))

    def checkXPos(self, *args):
        """
        checks if the x position set will be outside the circle and will hold
        it at that point
        """
        x = self.initialXScale.get()
        y = self.initialYScale.get()

        if x ** 2 + y ** 2 > self.radius**2:
            if x > 0:
                self.initialXScale.set(np.sqrt(self.radius**2 - y ** 2))
            else:
                self.initialXScale.set(-np.sqrt(self.radius**2 - y ** 2))

    def saveParameters(self):
        """
        Saves super class parameters.
        Updates or initializes the simulation
        """
        super(CircTab,self).saveParameters()
        # updates simulation if it exists
        # makes one if it doesn't
        try:
            self.simulation.update(**self.kwargs)
        except AttributeError:
            self.simulation = circle.CircleTable(**self.simArgs)

class BuminTab(AbstractTab):
    """
    subclass of AbstractTab for the Buminovich stadium
    """
    def saveParameters(self):
        """
        Saves super class parameters.
        Updates or initializes the simulation
        """
        super(BuminTab,self).saveParameters()
        # updates simulation if it exists
        # makes one if it doesn't
        try:
            self.simulation.update(**self.kwargs)
        except AttributeError:
            self.simulation = Buminovich.Buminovich(**self.simArgs)

class LorentzTab(AbstractTab):
    """
    subclass of AbstractTab for the Lorentz table
    """
    def saveParameters(self):
        """
        Saves super class parameters.
        Updates or initializes the simulation
        """
        super(LorentzTab,self).saveParameters()
        # updates simulation if it exists
        # makes one if it doesn't
        try:
            self.simulation.update(**self.kwargs)
        except AttributeError:
            self.simulation = Lorentz.Lorentz(**self.simArgs)

if __name__ == '__main__':
    app = Main(None)
    app.title('Billiards Simulator')
    app.mainloop()
