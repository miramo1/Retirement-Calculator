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

        self.show_frame("retirement")
        self.title("Retirement Calculator")

    def show_frame(self, frame_name):
        
        '''Show a frame for the given page name'''
        # frame = self.frames[frame_name]

        self.frames[frame_name].tkraise()

    def scale_app_size(self):
        try:
                '''get the horizontal res of user screen'''
                user32 = ctypes.windll.user32
                user32.SetProcessDPIAware()
                user_screen_horizontal = user32.GetSystemMetrics(0)
                horizontal_resolution = user_screen_horizontal
        except:
                '''when in doubt, default to 1920'''
                horizontal_resolution = 1920

        '''height adjusted to equal Calculation window, width set to 1.35 height'''

        if horizontal_resolution <= 1440:
                return {'TITLE_FONT':('Helvetica', 14, 'bold'),
                'HEAVY_BOLD_FONT' :('Helvetica', 11, 'bold'),
                'DEFAULT_FONT': ('Helvetica', 9, 'bold')}, 707, 505, horizontal_resolution

        elif horizontal_resolution <= 1920:
                return {'TITLE_FONT':('Helvetica', 17, 'bold'),
                'HEAVY_BOLD_FONT' :('Helvetica', 13, 'bold'),
                'DEFAULT_FONT': ('Helvetica', 11, 'bold')}, 787, 575, horizontal_resolution

        else:
                return {'TITLE_FONT':('Helvetica', 22, 'bold'),
                'HEAVY_BOLD_FONT' :('Helvetica', 15, 'bold'),
                'DEFAULT_FONT': ('Helvetica', 13, 'bold')}, 850, 625, horizontal_resolution


if __name__ == "__main__":
    app = Calculator_Main()
    app.mainloop()
