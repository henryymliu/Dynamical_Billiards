import tkinter as tk
import tkinter.ttk as ttk
import Pmw
import square as sim
from PIL import Image, ImageTk
import platform


class Main(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        n=ttk.Notebook(self)
        f1=SquareTab(self)
        n.add(f1,text='Square')
        n.pack()


class SquareTab(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        # Ball Formation Selection
        ballFormations = ('Test1', 'Square')

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

        self.initialYVelScale = tk.Scale(self, from_=-3, to=3, orient=tk.HORIZONTAL,
                                             label='Initial Y Velocity',resolution=0.1)
        self.initialYVelScale.grid(column=0, row=4, columnspan=2, sticky='W' + 'E')

        # note to bound these next two sliders based on size of stadium
        self.initialXScale = tk.Scale(self, from_=0, to=2, orient=tk.HORIZONTAL,
                                           label='Initial X Position',resolution=0.1)
        self.initialXScale.grid(column=0, row=5, columnspan=2, sticky='W' + 'E')

        self.initialYScale = tk.Scale(self, from_=0, to=2, orient=tk.HORIZONTAL,
                                           label='Initial Y Position',resolution=0.1)
        self.initialYScale.grid(column=0, row=6, columnspan=2, sticky='W' + 'E')

        self.playbackSpeedScale = tk.Scale(self, from_=-10, to=10, orient=tk.HORIZONTAL,
                                                label='Playback Speed',resolution=0.1)
        self.playbackSpeedScale.grid(column=0, row=8, columnspan=2, sticky='W' + 'E')

        self.toTrace = tk.BooleanVar()
        traceCheck = tk.Checkbutton(self, text="Trace", variable=self.toTrace)
        traceCheck.grid(column=2, row=9, sticky='W')

        # make canvas
        self.preview = tk.Canvas(self, width=400, height=300)
        self.preview.grid(column=2, row=1, rowspan=5)
        self.changeImage()

    #changes the preview image when a new stadium is selected
    def changeImage(self,*args):
        #get the current stadium
        stadium = self.ballFormationList.get(first=None, last=None)
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
