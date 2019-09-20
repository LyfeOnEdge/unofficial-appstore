import tkinter as tk
from PIL import Image, ImageTk

import modules.style as style
from .storeappsquare import storeAppSquare
from .customwidgets import ThemedLabel
from modules.appstore import getPackageIcon
from modules.locations import notfoundimage

class categoryFrame(tk.Frame):
    def __init__(self,parent,controller,framework, repos, appstore_handler, icon_dict):
        #list of repos to be displayed by this frame
        self.repos = repos
        self.parent = parent
        self.controller = controller #Frame manager
        self.framework = framework #**Scheduler
        self.appstore_handler = appstore_handler #Tool to get installed package data etc
        self.buttons = []   #List to hold buttons for this page
        self.current_buttons = [] #list to hold currently displayed buttons
        self.isSearching = False
        self.search_pending = False
        self.icon_dict = icon_dict
        self.selected = False
        tk.Frame.__init__(self, parent, background = style.w, border = 0, highlightthickness = 0)

        #Shared images for the squares
        self.get_image = ImageTk.PhotoImage(Image.open("assets/GET.png").resize((style.statussize, style.statussize), Image.ANTIALIAS))
        self.installed_image = ImageTk.PhotoImage(Image.open("assets/INSTALLED.png").resize((style.statussize, style.statussize), Image.ANTIALIAS))
        self.update_image = ImageTk.PhotoImage(Image.open("assets/UPDATE.png").resize((style.statussize, style.statussize), Image.ANTIALIAS))

        #make canvas and scroll bar
        self.canvas = tk.Canvas(self, bg=style.w, relief=tk.constants.SUNKEN)
        self.canvas.config(
            width=100, #Parent frame width
            highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self)

        #Bind sidebar to canvas and vv
        self.scrollbar.config(command=self.canvas.yview)                   
        self.canvas.config(yscrollcommand=self.scrollbar.set) 

        #pack the sidebar and canvas
        self.scrollbar.pack(side=tk.constants.RIGHT, fill=tk.constants.Y)                     
        self.canvas.pack(side=tk.constants.LEFT, expand=tk.constants.YES, fill=tk.constants.BOTH)

        #A frame to put in the canvas window
        self.canvas_frame = tk.Frame(self.canvas, background = style.w, border = 0, highlightthickness = 0)
        self.canvas_frame.bind("<MouseWheel>", self.on_mouse_wheel)

        #Creates a "window" and places the canvas in it
        self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')

        #Bind resize
        self.bind("<Configure>", self.configure)

        #Bind frame raise
        self.bind("<<ShowFrame>>", self.configure)

        #Build buttons from passed repo
        self.makeButtonList()
        self.buildFrame()

        self.framework.add_on_refresh_callback(self.buildFrame)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def is_selected(self):
        return self.selected

    def rebuild(self, new_repos):
        print("Rebuilding")
        self.repos = new_repos
        self.current_buttons = None
        self.clear()
        self.makeButtonList()
        self.buildFrame()

    def makeButtonList(self):
        self.buttons = []
        for repo in self.repos:
            self.makeButton(self.canvas_frame, self.framework, repo, self.icon_dict)
        self.current_buttons = self.buttons

    #instantiates button, adds it to list
    def makeButton(self,frame, framework, repo, icon_dict):
        button = storeAppSquare(frame, self.controller, framework, repo, icon_dict)
        button.buttonobj.bind("<MouseWheel>", self.on_mouse_wheel)
        self.buttons.append(button)

        #Tiles buttons
    def buildFrame(self): 
        #If frame is visible
        if self.selected:
            #if there is content to build with
            if self.current_buttons:
                _spacing = style.thumbnailwidth+2*style.tileoffset
                #Set the width 
                _framewidth = self.winfo_width() - self.scrollbar.winfo_width()
                self.canvas_frame.config(width=_framewidth)

                #Get integer number of tiles fittable in the window
                _maxperrow = _framewidth // _spacing

                #If there's not enough room to build anything
                if not _maxperrow:
                    return

                empty_space = _framewidth - (_maxperrow * _spacing)

                space_offset = empty_space / (_maxperrow + 1)

                _y = 0
                _x = 0

                for button in self.current_buttons:
                    button.place(x=_x * (_spacing) + style.tileoffset + (_x + 1) * (space_offset), y = _y * _spacing + style.tileoffset, height = style.thumbnailwidth, width = style.thumbnailwidth)
                    
                    if not button.buttontitlelabel:
                        button.buttontitlelabel = ThemedLabel(self.canvas_frame,button.repo["title"],anchor="e",label_font=style.mediumboldtext,foreground=style.b,background=style.w)
                        button.buttontitlelabel.bind("<MouseWheel>", self.on_mouse_wheel)

                    if not button.buttonauthorlabel:
                        button.buttonauthorlabel = ThemedLabel(self.canvas_frame,button.repo["author"],anchor="e",label_font=style.smallboldtext,foreground=style.lg,background=style.w)
                        button.buttonauthorlabel.bind("<MouseWheel>", self.on_mouse_wheel)

                    if not button.buttonstatuslabel:
                        button.buttonstatuslabel = ThemedLabel(self.canvas_frame,"",anchor="w",label_font=style.smallboldtext,foreground=style.lg,background=style.w)
                        button.buttonstatuslabel.bind("<MouseWheel>", self.on_mouse_wheel)

                    if not button.buttonversionlabel:
                        button.buttonversionlabel = ThemedLabel(self.canvas_frame,button.repo["version"],anchor="w",label_font=style.smallboldtext,foreground=style.lg,background=style.w)
                        button.buttonversionlabel.bind("<MouseWheel>", self.on_mouse_wheel)

                    if not button.buttonseparator:
                        button.buttonseparator = tk.Label(self.canvas_frame, background=style.lg, borderwidth= 0)

                    button.buttontitlelabel.place(x = _x * (_spacing) + style.tileoffset + (_x + 1) * (space_offset), y = _y * _spacing + style.tileoffset + style.thumbnailwidth - 2.5 * style.buttontextheight + 3, width = style.thumbnailwidth)
                    button.buttonauthorlabel.place(x = _x * (_spacing) + style.tileoffset + (_x + 1) * (space_offset), y = _y * _spacing + style.tileoffset + style.thumbnailwidth - style.buttontextheight + 3, width = style.thumbnailwidth)
                    button.buttonversionlabel.place(x = _x * (_spacing) + style.tileoffset + (_x + 1) * (space_offset), y = _y * _spacing + style.tileoffset + style.thumbnailwidth - style.buttontextheight + 3)
                    button.buttonseparator.place(x = _x * (_spacing) + style.tileoffset + (_x + 1) * (space_offset), y = _y * _spacing + style.tileoffset + style.thumbnailwidth + 8, height = 1, width = style.thumbnailwidth)
                    button.buttonstatuslabel.place(x = _x * (_spacing) + style.tileoffset + (_x + 1) * (space_offset), y = _y * _spacing + style.tileoffset + style.thumbnailwidth - 2.5 * style.buttontextheight + 3)

                    status = None
                    package = button.repo["name"]
                    if self.appstore_handler.packages:
                        if package in self.appstore_handler.packages:
                            installed_version = self.appstore_handler.get_package_version(package)

                            if self.appstore_handler.clean_version(installed_version, package) == self.appstore_handler.clean_version(installed_version, package):
                                status = "UPTODATE"
                            elif self.appstore_handler.clean_version(installed_version, package) < self.appstore_handler.clean_version(installed_version, package):
                                status = "NEEDSUPDATE"
                        else:
                            status = "NOTINSTALLED"
                    else:
                        status = "NOTINSTALLED"

                    status_map = {
                    "UPTODATE" : self.installed_image,
                    "NEEDSUPDATE" : self.update_image,
                    "NOTINSTALLED" : self.get_image
                    }

                    button.buttonstatuslabel.configure(image=status_map[status])

                    _x += 1

                    if _x == _maxperrow:
                        _x = 0
                        _y += 1

                #Update the size of the canvas and configure the scrollable area
                _canvasheight = (_y + 1) * (style.thumbnailwidth+2*style.tileoffset)
                if _canvasheight < self.winfo_height():
                    _canvasheight = self.winfo_height()
                self.canvas_frame.config(height = _canvasheight,width= _framewidth)
                self.canvas.config(scrollregion=(0,0,_framewidth, _canvasheight))
                self.canvas_frame.update_idletasks()

    def search(self, searchterm):
        def doSearch():
            search_categories = ["name", "title", "author"]

            new_buttons = []

            for button in self.buttons:
                for category in search_categories:
                    compare_string = button.repo[category]
                    if compare_string:
                        if searchterm.lower() in compare_string.lower():
                            if not button in new_buttons:
                                new_buttons.append(button)

            return new_buttons

        if searchterm:
            result = doSearch()
        else:
            result = self.buttons[:]

        self.current_buttons = result

        #Clear button layout
        self.clear()

        self.buildFrame()

    def clear(self):
        # for child in self.scroller.winfo_children():
        #     child.grid_forget()
        for button in self.buttons:
            button.place_forget()
            if button.buttontitlelabel:
                button.buttontitlelabel.place_forget()
            if button.buttonauthorlabel:
                button.buttonauthorlabel.place_forget()
            if button.buttonversionlabel:
                button.buttonversionlabel.place_forget()
            if button.buttonseparator:
                button.buttonseparator.place_forget()
            if button.buttonstatuslabel:
                button.buttonstatuslabel.place_forget()

    def configure(self, event):
        self.framework.refresh()

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"