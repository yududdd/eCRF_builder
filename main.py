__author__ = "Yu Du"
__Email__ = "yu.du@clinchoice.com"
__date__ = "Nov 19,2020"
#######################################################################################################################

import tkinter as tk  # python 3
from tkinter import font as tkfont
from PageZero import Selector
from PageOne import Editor
from PageTwo import Exporter

class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=20, weight="bold")
        self.title("Clinchoice")
        self.wm_geometry("1500x1000") 
        self.selected = dict()
        self.file_bol = None
        self.filename = None
        # the container is where we'll stackB a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the othersb
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Selector, Editor, Exporter):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Selector")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_selected(self):
        return self.selected

if __name__ == "__main__":
    app = TkinterApp()
    app.mainloop()
