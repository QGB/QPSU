from tkinter import *
from tkinter import ttk


class Sketchpad(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.new_line)
        self.bind("<B1-Motion>", self.add_to_line)

    def new_line(self, event):
        self.points = [event.x, event.y]
        self.line = self.create_line(event.x, event.y, event.x, event.y, width=1, capstyle=ROUND)

    def add_to_line(self, event):
        self.points.extend([event.x, event.y])
        self.coords(self.line, *self.points)


root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sketch = Sketchpad(root)
sketch.grid(column=0, row=0, sticky=(N, W, E, S))

root.mainloop()