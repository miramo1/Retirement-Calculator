import tkinter as tk
import ctypes
from retirement import retirement
from investment import investment


class Calculator_Main(tk.Tk):
    def __init__(self): 
        
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        container.grid(sticky="news")
        self.resizable(False, False)

        self.frames = {}
        for frame in (investment, retirement):
            page_name = frame.__name__
            frame = frame(master=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("investment")
        self.title("Investment Calculator")

    def show_frame(self, frame_name):
        
        '''Show a frame for the given page name'''
        # frame = self.frames[frame_name]

        self.frames[frame_name].tkraise()

if __name__ == "__main__":
    app = Calculator_Main()
    app.mainloop()
