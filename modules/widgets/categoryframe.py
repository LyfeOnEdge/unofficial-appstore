import tkinter as tk
from PIL import Image, ImageTk
from timeit import default_timer as timer
import modules.style as style
from .storeappsquare import storeAppSquare
from .customwidgets import ThemedLabel
from modules.locations import notfoundimage


class categoryFrame(tk.Frame):
    def __init__(self,parent,controller,framework, repos):
        #list of repos to be displayed by this frame
        self.repos = repos
        self.parent = parent
        self.controller = controller #Frame manager
        self.framework = framework #**Scheduler
        self.appstore_handler = controller.appstore_handler #Tool to get installed package data etc
        self.buttons = []   #List to hold buttons for this page
        self.current_buttons = [] #list to hold currently displayed buttons
        self.icon_dict = self.controller.image_sharer
        self.selected = False
        self.is_displaying = False #Debounce used for the display function to prevent multiple threads grabbing an updated image
        self.is_searching = True #Used to remember if we are currently searching
        self.currentsearch = False #Used to remember the current qued search term (helps with search lag)
        self.lastsearch = False #Used to remember the last term searched
        self.searchtimer = None

        tk.Frame.__init__(self, parent, background = style.w, border = 0, highlightthickness = 0)

        #Shared images for the squares
        self.get_image = ImageTk.PhotoImage(Image.open("assets/GET.png").resize((style.statussize, style.statussize), Image.ANTIALIAS))
        self.installed_image = ImageTk.PhotoImage(Image.open("assets/INSTALLED.png").resize((style.statussize, style.statussize), Image.ANTIALIAS))
        self.update_image = ImageTk.PhotoImage(Image.open("assets/UPDATE.png").resize((style.statussize, style.statussize), Image.ANTIALIAS))
        self.notfoundimage = ImageTk.PhotoImage(Image.open(notfoundimage).resize((style.thumbnailwidth, style.thumbnailheight - 10), Image.ANTIALIAS))

        self.status_map = {
            "UPTODATE" : self.installed_image,
            "NEEDSUPDATE" : self.update_image,
            "NOTINSTALLED" : self.get_image
        }

        #make canvas and scroll bar
        self.canvas = tk.Canvas(self, bg=style.w, relief=tk.constants.SUNKEN)
        self.canvas.config(
            width=100, #Parent frame width
            highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self)

        #Bind sidebar to canvas and vv
        self.scrollbar.config(command=self.on_scroll_bar)           
        self.canvas.config(yscrollcommand=self.scrollbar.set) 

        #pack the sidebar and canvas
        self.scrollbar.pack(side=tk.constants.RIGHT, fill=tk.constants.Y)                     
        self.canvas.pack(side=tk.constants.LEFT, expand=tk.constants.YES, fill=tk.constants.BOTH)

        #A frame to put in the canvas window
        self.canvas_frame = tk.Frame(self.canvas, background = style.w, border = 0, highlightthickness = 0)
        self.canvas_frame.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas_frame.on_mouse_wheel = self.on_mouse_wheel

        #Creates a "window" and places the canvas in it
        self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')

        #Bind resize
        self.bind("<Configure>", self.configure)

        #Bind frame raise
        self.bind("<<ShowFrame>>", self.configure)

        #Build buttons from passed repo
        self.makeButtonList()
        self.buildFrame()

        self.framework.add_on_refresh_callback(self.clear_then_update)

    def select(self):
        self.selected = True
        self.rebuild()

    def deselect(self):
        self.selected = False

    def is_selected(self):
        return self.selected

    def rebuild(self):
        self.clear()
        self.buildFrame()
        self.update_displayed_buttons()

    def remake(self, new_repos):
        print("Remaking")
        self.repos = new_repos
        self.current_buttons = []
        self.buttons = []
        self.rebuild()

    def makeButtonList(self):
        self.buttons = []
        for repo in self.repos:
            self.makeButton(self.canvas_frame, self.framework, repo)
        self.current_buttons = self.buttons

    #instantiates button, adds it to list
    def makeButton(self,frame, framework, repo):
        button = storeAppSquare(frame, self.controller, framework, self, repo)
        button.buttonobj.bind("<MouseWheel>", self.on_mouse_wheel)
        button.appstore_handler = self.appstore_handler
        self.buttons.append(button)

        #Tiles buttons
    def buildFrame(self): 
        #If frame is visible
        if self.selected:
            #if there is content to build with
            if self.current_buttons:
                # buildstart = timer()
                x_spacing = style.thumbnailwidth + 2 * style.offset
                y_spacing = style.thumbnailheight + 13 * style.offset
                #Set the width 
                _framewidth = self.winfo_width() - self.scrollbar.winfo_width()
                self.canvas_frame.config(width=_framewidth)

                #Get integer number of tiles fittable in the window
                _maxperrow = _framewidth // x_spacing

                #If there's not enough room to build anything
                if not _maxperrow:
                    return

                empty_space = _framewidth - (_maxperrow * x_spacing)

                space_offset = empty_space / (_maxperrow + 1)

                _y = 0
                _x = 0

                
                for realbutton in self.buttons:
                    for button in self.current_buttons:
                        found = False
                        if realbutton.repo["name"] == button.repo["name"]:
                            found = True
                            base_y = _y * y_spacing + style.offset
                            base_x = _x * (x_spacing) + style.offset + (_x + 1) * (space_offset)

                            # self.controller.async_threader.do_async(self.buildButton, [button, base_x, base_y])
                            realbutton.set_xy_canvas(base_x, base_y, self.canvas_frame)
                            _x += 1

                            if _x == _maxperrow:
                                _x = 0
                                _y += 1
                            break
                        else:
                            realbutton.set_xy_canvas(None, None, None)

                #Update the size of the canvas and configure the scrollable area
                _canvasheight = (_y + 1) * (y_spacing)
                if _canvasheight < self.winfo_height():
                    _canvasheight = self.winfo_height()

                self.canvas_frame.config(height = _canvasheight,width= _framewidth)
                self.canvas.config(scrollregion=(0,0,_framewidth, _canvasheight))
                # buildend = timer()
                # print("build took {} seconds".format(buildend - buildstart))

    def update_displayed_buttons(self):
        if not self.is_displaying:
            self.is_displaying = True
            #If frame is visible
            if self.selected:
                button_height = style.thumbnailheight + 13 * style.offset
                canvas_height = self.canvas_frame.winfo_height()
                if not canvas_height:
                    print("canvas height is zero")
                    return
                # #The smallest a frame can be is one pixel, which means the canvas unpopulated
                # if not canvas_height > 1:
                #     print("unpopulated canvas")
                #     return

                ratio = 1 / canvas_height

                viewable_buffer = (1.25 * button_height) * ratio

                #add a buffer to the range to search for buttons that need placing
                canvas_top = self.canvas.yview()[0] - viewable_buffer
                if canvas_top < 0:
                    canvas_top = 0

                canvas_bottom = self.canvas.yview()[1] + viewable_buffer
                if canvas_bottom > 1:
                    canvas_bottom = 1

                for button in self.buttons:
                    if not button.placed:
                        if button.get_xy()[1]:
                            button_y_proportion = button.get_xy()[1] * ratio
                            if canvas_top < button_y_proportion and button_y_proportion < canvas_bottom:
                                self.controller.async_threader.do_async(button.build_button)
            self.is_displaying = False

    def clear_then_update(self):
        self.clear()
        self.update_displayed_buttons()

    # def clear_then_update_displayed_buttons(self):
    #     self.clear()
    #     self.controller.async_threader.do_async(self.update_displayed_buttons)

    def search(self, searchterm):
        self.is_searching = True
        self.currentsearch = searchterm
        self.searchtimer = timer()
        self.controller.after(100, self.search_poll())

    def search_poll(self):
        if self.is_searching:
            #.4 second delay on search debouncer
            if (timer() - self.searchtimer) > (0.4):
                self.controller.async_threader.do_async(self.do_search_query)
            else:
                self.controller.after(100, self.search_poll)

    def do_search_query(self):
        def doSearch(searchterm):
            search_categories = ["name", "title", "author", "description"]

            new_buttons = []

            for button in self.buttons:
                for category in search_categories:
                    compare_string = button.repo[category]
                    if compare_string:
                        if searchterm.lower() in compare_string.lower():
                            if not button in new_buttons:
                                new_buttons.append(button)

            return new_buttons

        if self.currentsearch:
            result = doSearch(self.currentsearch)
        else:
            result = self.buttons[:]

        self.current_buttons = result

        self.is_searching = False
        self.lastsearch = self.currentsearch
        self.currentsearch = None

        self.rebuild()

        #Most efficiant way to un-place items on the canvas
    def clear(self):
        for child in self.canvas_frame.winfo_children():
            child.place_forget()
        for button in self.buttons:
            button.placed = False

    def configure(self, event):
        self.buildFrame()
        self.framework.refresh()

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units") #Scrolls the canvas
        self.update_displayed_buttons()
        return "break"

    def on_scroll_bar(self, b, c):
        self.update_displayed_buttons()
        self.canvas.yview(b, c)

