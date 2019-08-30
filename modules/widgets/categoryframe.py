import tkinter as tk
from PIL import Image, ImageTk

import modules.style as style
from .storeappsquare import storeAppSquare
from modules.appstore import getPackageIcon
from modules.locations import notfoundimage

class categoryFrame(tk.Frame):
    def __init__(self,parent,controller,framework, repos):
        #list of repos to be displayed by this frame
        self.repos = repos
        self.parent = parent
        self.controller = controller #Frame manager
        self.framework = framework #**Scheduler
        self.buttons = []   #List to hold buttons for this page
        self.current_buttons = [] #list to hold currently displayed buttons
        self.isSearching = False
        self.search_pending = False
        tk.Frame.__init__(self, parent, background = style.w, border = 0, highlightthickness = 0)

        self.canvas = tk.Canvas(self, bg=style.w, relief=tk.constants.SUNKEN)
        self.canvas.config(
            width=100, #Parent frame width
            highlightthickness=0)
        sbar = tk.Scrollbar(self)
        sbar.config(command=self.canvas.yview)                   
        self.canvas.config(yscrollcommand=sbar.set)              
        sbar.pack(side=tk.constants.RIGHT, fill=tk.constants.Y)                     
        self.canvas.pack(side=tk.constants.LEFT, expand=tk.constants.YES, fill=tk.constants.BOTH)

        self.canvas_frame = tk.Frame(self.canvas, background = style.w, border = 0, highlightthickness = 0)

        self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')

        self.bind("<Configure>", self.configure)
        self.bind("<<ShowFrame>>", self.on_show_frame)

        self.makeButtonList()
        self.buildFrame()

        self.framework.add_on_tick_callback(self.searchPoll)

        self.framework.add_on_refresh_callback(self.buildFrame)

    def makeButtonList(self):
        for repo in self.repos:
            self.makeButton(self.canvas_frame, self.framework, repo)
        self.current_buttons = self.buttons

    #instantiates button, adds it to list
    def makeButton(self,frame, framework, repo):
        button = storeAppSquare(frame, self.controller, framework, repo)
        self.buttons.append(button)

    #Tiles buttons
    def buildFrame(self):
        _framewidth = self.winfo_width()
        self.canvas_frame.config(width=_framewidth)

        #Get integer number of tiles fittable in the window
        _maxperrow = _framewidth // style.thumbnailsize

        #If there's not enough room to build anything
        if not _maxperrow:
            return

        _y = 0
        _x = 0

        spacing = style.thumbnailsize+2*style.tileoffset
        for button in self.current_buttons:
            button.place(x=_x * spacing + style.tileoffset, y = _y * spacing + style.tileoffset, height = style.thumbnailsize, width = style.thumbnailsize)

            _x += 1

            if _x == _maxperrow:
                _x = 0
                _y += 1

        #Update the size of the canvas and configure the scrollable area
        _canvasheight = (_y + 1) * (style.thumbnailsize+2*style.tileoffset)
        self.canvas_frame.config(height = _canvasheight,width= _framewidth)
        self.canvas.config(scrollregion=(0,0,_framewidth, _canvasheight))
        # self.canvas.update_idletasks()
           

    def search(self, searchterm):
        if not self.isSearching:
            self.isSearching = True
            if searchterm:
                search_categories = ["name", "title", "description"]

                new_buttons = []

                for button in self.buttons:
                    for category in search_categories:
                        if searchterm.lower() in button.repo[category].lower():
                            if not button in new_buttons:
                                new_buttons.append(button)

                self.current_buttons = new_buttons
            else:
                self.current_buttons = self.buttons

            #Clear button layout
            self.clear()

            self.buildFrame()
            self.isSearching = False
        else:
            self.search_pending = True
            self.searchterm = searchterm

    #This function is called at a set tickrate by the pages parent class scheduler, 
    #allows a search to que as well as update the searchterm while causing less blocking
    #Tkinter optimization
    def searchPoll(self):
        if not self.isSearching:
            if self.search_pending:
                self.search_pending = False
                self.search(self.searchterm)        


    def clear(self):
        # for child in self.scroller.winfo_children():
        #     child.grid_forget()
        for button in self.buttons:
            button.grid_forget()

    def configure(self, event):
        self.framework.refresh()

    def on_show_frame(self, event):
        self.framework.refresh()
