import tkinter as tk

class tableConfig(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        self.run = tk.Button(self)
        self.run["text"] = "Run"
        self.run.pack(side="bottom")

        self.selectStadium = tk.


root = tk.Tk()
app = tableConfig(root)
app.mainloop()