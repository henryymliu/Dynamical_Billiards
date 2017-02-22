import tkinter
import pygame_test as game

class app_tk(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        button = tkinter.Button(self,text=u"Click me!", command=self.OnButtonClick)
        button.grid(column=1,row=0)

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)

    def OnButtonClick(self):
        game.main()


if __name__ == '__main__':
    app=app_tk(None)
    app.title('Simulation')
    app.mainloop()
