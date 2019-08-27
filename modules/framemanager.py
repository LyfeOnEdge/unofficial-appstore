import tkinter as tk

#Frame handler, raises and pages in z layer
class FrameManager(tk.Tk):
    def __init__(self, pages, geometry):
        tk.Tk.__init__(self)
               
        self.geometry("{}x{}".format(geometry["width"],geometry["height"])) 
        # self.resizable(False, False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, borderwidth = 0, highlightthickness = 0)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Add pages as frames to dict, with keyword being the name of the frame
        self.frames = {}
        if pages:
            for F in (pages):
                page_name = F.__name__
                frame = F(parent=container, controller=self,page_name=page_name) 
                self.frames[page_name] = frame

                frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        #Show frame for the given page name
        frame = self.frames[page_name]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()