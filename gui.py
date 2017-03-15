import tkinter
import Pmw
import square as sim
from PIL import Image, ImageTk
import platform


class Main(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Stadium selection
        stadiums = ('Test1', 'Square')
        # Ball Formation Selection
        ballFormations = ('Test1', 'Test2')

        self.grid()  # sets up grid

        # define a button to start simulation, runs startSimulation() when
        # clicked
        button = tkinter.Button(self, text=u'Start simulation',
                                command=self.startSimulation)
        button.grid(column=1, row=9)


        self.grid_columnconfigure(0, weight=1)
        # self.resizable(True,False)

        self.stadiumList = Pmw.ComboBox(self, label_text='Choose Stadium', labelpos='nw', selectioncommand=self.changeImage,
                                        scrolledlist_items=stadiums, dropdown=1)
        self.stadiumList.grid(column=0, row=1)
        self.stadiumList.selectitem(1)

        self.ballFormationList = Pmw.ComboBox(self, label_text='Choose Ball Formation', labelpos='nw',
                                              selectioncommand=None,
                                              scrolledlist_items=ballFormations, dropdown=1)
        self.ballFormationList.grid(column=0, row=2)
        self.ballFormationList.selectitem(0)

        self.initialXVelScale = tkinter.Scale(self, from_=-3, to=3, orient=tkinter.HORIZONTAL,
                                             label='Initial X Velocity',resolution=0.1)
        self.initialXVelScale.grid(column=0, row=3, columnspan=2, sticky='W' + 'E')

        self.initialYVelScale = tkinter.Scale(self, from_=-3, to=3, orient=tkinter.HORIZONTAL,
                                             label='Initial Y Velocity',resolution=0.1)
        self.initialYVelScale.grid(column=0, row=4, columnspan=2, sticky='W' + 'E')

        # note to bound these next two sliders based on size of stadium
        self.initialXScale = tkinter.Scale(self, from_=0, to=2, orient=tkinter.HORIZONTAL,
                                           label='Initial X Position',resolution=0.1)
        self.initialXScale.grid(column=0, row=5, columnspan=2, sticky='W' + 'E')

        self.initialYScale = tkinter.Scale(self, from_=0, to=2, orient=tkinter.HORIZONTAL,
                                           label='Initial Y Position',resolution=0.1)
        self.initialYScale.grid(column=0, row=6, columnspan=2, sticky='W' + 'E')

        self.playbackSpeedScale = tkinter.Scale(self, from_=-10, to=10, orient=tkinter.HORIZONTAL,
                                                label='Playback Speed')
        self.playbackSpeedScale.grid(column=0, row=8, columnspan=2, sticky='W' + 'E')

        self.toTrace = tkinter.BooleanVar()
        traceCheck = tkinter.Checkbutton(self, text="Trace", variable=self.toTrace)
        traceCheck.grid(column=2, row=9, sticky='W')

        # make canvas
        self.preview = tkinter.Canvas(self, width=400, height=300)
        self.preview.grid(column=2, row=1, rowspan=5)
        self.changeImage()

    #changes the preview image when a new stadium is selected
    def changeImage(self,*args):
        #get the current stadium
        stadium = self.stadiumList.get(first=None, last=None)
        #select image based on operating system
        if platform.system == 'Windows':
            directory='images\{}.png'.format(stadium)
            image = Image.open(directory)
        else:
            directory='images/{}.png'.format(stadium)
            image = Image.open(directory)

        # make Tk compatible PhotoImage object, must save as object parameter
        # to avoid garbage collection
        self.photo = ImageTk.PhotoImage(image)
        #display image
        self.preview.create_image(0, 0, anchor='nw', image=self.photo)


    #runs when start simulation button is pressed
    def startSimulation(self):
        # TODO: Handle unselected combobox case

        #put all selections into dictionary
        simArgs = dict()
        simArgs['stadium'] = self.stadiumList.get(first=None, last=None)
        simArgs['ballF'] = self.ballFormationList.get(first=None, last=None)

        simArgs['initXVel'] = self.initialXVelScale.get()
        simArgs['initYVel'] = self.initialYVelScale.get()
        simArgs['initX'] = self.initialXScale.get()
        simArgs['initY'] = self.initialYScale.get()
        simArgs['playbackSpeed'] = self.playbackSpeedScale.get()
        simArgs['trace'] = self.toTrace.get()
        print(self.toTrace.get())

        #create simulation
        simulation = sim.SquareTable(**simArgs)
        simulation.main()



if __name__ == '__main__':
    app = Main(None)
    app.title('Billiards Simulator')
    app.mainloop()
