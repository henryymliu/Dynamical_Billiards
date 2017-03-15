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
        stadiums = ('Test1', 'Test2')
        # Ball Formation Selection
        ballFormations = ('Test1', 'Test2')

        self.grid()  # sets up grid

        # define a button to start simulation, runs startSimulation() when
        # clicked
        button = tkinter.Button(self, text=u'Start simulation',
                                command=self.startSimulation)
        button.grid(column=1, row=9)
        # open image using PIL
        if platform.system == 'Windows':
            image = Image.open('images\HLS-EFS-CSC-Owl.bmp')
        else:
            image = Image.open('images/HLS-EFS-CSC-Owl.bmp')
        # make Tk compatible PhotoImage object, must save as object parameter
        # to avoid garbage collection
        self.photo = ImageTk.PhotoImage(image)
        # make canvas and add photo
        preview = tkinter.Canvas(self, width=275, height=183)
        preview.grid(column=2, row=1)
        preview.create_image(0, 0, anchor='nw', image=self.photo)

        self.grid_columnconfigure(0, weight=1)
        # self.resizable(True,False)

        self.stadiumList = Pmw.ComboBox(self, label_text='Choose Stadium', labelpos='nw', selectioncommand=None,
                                        scrolledlist_items=stadiums, dropdown=1)
        self.stadiumList.grid(column=0, row=1)
        self.stadiumList.selectitem(0)

        self.ballFormationList = Pmw.ComboBox(self, label_text='Choose Ball Formation', labelpos='nw',
                                              selectioncommand=None,
                                              scrolledlist_items=ballFormations, dropdown=1)
        self.ballFormationList.grid(column=0, row=2)
        self.ballFormationList.selectitem(0)

        self.initialVelScale = tkinter.Scale(self, from_=-10, to=10, orient=tkinter.HORIZONTAL,
                                             label='Initial Velocity')
        self.initialVelScale.grid(column=0, row=3, columnspan=2, sticky='W' + 'E')

        # note to bound these next two sliders based on size of stadium
        self.initialXScale = tkinter.Scale(self, from_=-10, to=10, orient=tkinter.HORIZONTAL,
                                           label='Initial Position (X)')
        self.initialXScale.grid(column=0, row=4, columnspan=2, sticky='W' + 'E')

        self.initialYScale = tkinter.Scale(self, from_=-10, to=10, orient=tkinter.HORIZONTAL,
                                           label='Initial Position (Y)')
        self.initialYScale.grid(column=0, row=5, columnspan=2, sticky='W' + 'E')

        self.playbackSpeedScale = tkinter.Scale(self, from_=-10, to=10, orient=tkinter.HORIZONTAL,
                                                label='Playback Speed')
        self.playbackSpeedScale.grid(column=0, row=8, columnspan=2, sticky='W' + 'E')

        self.toTrace = False
        traceCheck = tkinter.Checkbutton(self, text="Trace", variable=self.toTrace)
        traceCheck.grid(column=2, row=9, sticky='W')

    #runs when start simulation button is pressed
    def startSimulation(self):
        # TODO: Handle unselected combobox case

        #put all selections into dictionary
        simArgs = dict()
        simArgs['stadium'] = self.stadiumList.get(first=None, last=None)
        simArgs['ballF'] = self.ballFormationList.get(first=None, last=None)

        simArgs['initVel'] = self.initialVelScale.get()
        simArgs['initX'] = self.initialXScale.get()
        simArgs['initY'] = self.initialYScale.get()
        simArgs['playbackSpeed'] = self.playbackSpeedScale.get()

        #create simulation
        game = sim.SquareTable(**simArgs)
        #run simulation
        game.main()


if __name__ == '__main__':
    app = Main(None)
    app.title('Billiards Simulator')
    app.mainloop()
