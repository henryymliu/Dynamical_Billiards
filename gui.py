import tkinter
import Pmw
import simulation as sim
from PIL import Image, ImageTk
import platform

class simulation(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid() #sets up grid

        #define a button to start simulation, runs startSimulation() when
        #cliked
        button = tkinter.Button(self,text=u'Start simulation',
            command=self.startSimulation)
        button.grid(column=1,row=1)
        #open image using PIL
        if platform.system == 'Windows':
            image=Image.open('images\HLS-EFS-CSC-Owl.bmp')
        else:
            image=Image.open('images/HLS-EFS-CSC-Owl.bmp')
        #make Tk compatible PhotoImage object, must save as object parameter
        #to avoid garbage collection
        self.photo=ImageTk.PhotoImage(image)
        #make canvas and add photo
        preview = tkinter.Canvas(self,width=275, height=183)
        preview.grid(column=2,row=1)
        preview.create_image(0,0, anchor='nw',image=self.photo)



        self.grid_columnconfigure(0,weight=1)
        #self.resizable(True,False)

        stadiumList = Pmw.ComboBox(self, label_text = 'Choose Stadium', labelpos = 'nw', selectioncommand = None,
                                   scrolledlist_items = ('Test1', 'Test2'), dropdown=1)
        stadiumList.grid(column = 0, row = 1);

        ballFormationList = Pmw.ComboBox(self, label_text='Choose Stadium', labelpos='nw', selectioncommand=None,
                                   scrolledlist_items=('Test1', 'Test2'), dropdown=1)
        ballFormationList.grid(column=0, row=2);

        initialVelScale = tkinter.Scale(self, from_=-10, to=10, orient=tkinter.HORIZONTAL, label='Initial Velocity')
        initialVelScale.grid(column = 0, row = 3);

        # note to bound these next two sliders based on size of stadium
        initialXScale = tkinter.Scale(self, from_=-10, to=10 , orient=tkinter.HORIZONTAL, label='Initial Position (X)')
        initialXScale.grid(column=0, row=4);

        initialYScale = tkinter.Scale(self, from_=-10, to=10, orient=tkinter.HORIZONTAL, label='Initial Position (Y)')
        initialYScale.grid(column=0, row=5);

        playbackSpeedScale = tkinter.Scale(self, from_=-10, to=10, orient=tkinter.HORIZONTAL, label='Initial Position (Y)')
        playbackSpeedScale.grid(column=0, row=9);

        self.toTrace = False
        traceCheck = tkinter.Checkbutton(self, text="Trace", variable=self.toTrace)

    def startSimulation(self):
        sim.main()


if __name__ == '__main__':
    app=simulation(None)
    app.title('Simulation')
    app.mainloop()
