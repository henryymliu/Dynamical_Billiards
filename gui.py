import tkinter as tk
import tkinter.ttk as ttk
import Pmw
import RectTable as rect
import LTable as Ltab
from PIL import Image, ImageTk
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
        n.add(f1,text='Rectangle')
        n.add(f2,text='L')
        n.pack()


class RectTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Ball Formation Selection
        ballFormations = ["1 Ball"]
        self.width=tk.IntVar()
        self.height=tk.IntVar()

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

        self.initialXScale = tk.Scale(self, from_=0, to=2, orient=tk.HORIZONTAL,
                                           label='Initial X Position',resolution=0.1)
        self.initialXScale.grid(column=0, row=5, columnspan=2, sticky='W' + 'E')
        self.initialXScale.set(1)

        self.initialYScale = tk.Scale(self, from_=0, to=2, orient=tk.HORIZONTAL,
                                           label='Initial Y Position',resolution=0.1)
        self.initialYScale.grid(column=0, row=6, columnspan=2, sticky='W' + 'E')
        self.initialYScale.set(1)

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
            directory='images\Rect_{}.png'.format(formation).replace(' ','')
            image = Image.open(directory)
        else:
            directory='images/Rect_{}.png'.format(formation).replace(' ','')
            image = Image.open(directory)

        # make Tk compatible PhotoImage object, must save as object parameter
        # to avoid garbage collection
        self.photo = ImageTk.PhotoImage(image)
        #display image
        self.preview.create_image(0, 0, anchor='nw', image=self.photo)

    def updateSize(self,*args):
        self.initialXScale.config(to=self.width.get())
        self.initialYScale.config(to=self.height.get())


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
        simArgs['width'] = self.width.get()
        simArgs['height'] = self.height.get()

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

if __name__ == '__main__':
    app = Main(None)
    app.title('Billiards Simulator')
    app.mainloop()
