import modules.customwidgets as cw
from modules.appstore_web import getPackageIcon, getScreenImage
from modules.style import dark_color, light_color, w, lg, smallboldtext
from modules.locations import notfoundimage
from PIL import Image, ImageTk
import tkinter as tk
TILEWIDTH = 150
SEPARATORWIDTH = 4

class categoryFrame(cw.ThemedFrame):
    def __init__(self,parent,controller,framework, repos):
        self.repos = repos
        self.parent = parent
        self.controller = controller
        self.framework = framework
        self.buttons = []
        cw.ThemedFrame.__init__(self, parent, background_color = w)

        self.canvas = tk.Canvas(self, bg=w, relief=tk.constants.SUNKEN)
        self.canvas.config(width=self.winfo_width(), height=self.winfo_height())     
        self.canvas.config(highlightthickness=0)                 

        sbar = tk.Scrollbar(self)
        sbar.config(command=self.canvas.yview)                   
        self.canvas.config(yscrollcommand=sbar.set)              
        sbar.pack(side=tk.constants.RIGHT, fill=tk.constants.Y)                     
        self.canvas.pack(side=tk.constants.LEFT, expand=tk.constants.YES, fill=tk.constants.BOTH)       

        self.bind("<Configure>", self.configure)
        self.bind("<<ShowFrame>>", self.on_show_frame)

        self.makeButtonList()
        self.buildFrame()

        self.framework.add_on_refresh_callback(self.buildFrame)

    def makeButtonList(self):
        for repo in self.repos:
            self.makeButton(self.canvas, self.framework, repo)

    def makeButton(self,frame, framework, repo):
        button = store_app_square(frame, framework, repo)
        self.buttons.append(button)


    def buildFrame(self):
        _framewidth = self.canvas.winfo_width()
        _maxperrow = _framewidth // TILEWIDTH

        #If there's not enough room to build anything
        if not _maxperrow:
            return

        _y = 0
        _x = 0

        for button in self.buttons:
            button.grid(row=_y, column = _x, sticky="nsew")

            _x += 1

            if _x == _maxperrow:
                _x = 0
                _y += 1

        for xs in range(0, _maxperrow):
            self.canvas.grid_columnconfigure(xs, minsize=TILEWIDTH+2*SEPARATORWIDTH, pad=SEPARATORWIDTH)

        for ys in range(0, _y):
            self.canvas.grid_rowconfigure(ys, minsize=TILEWIDTH+2*SEPARATORWIDTH, pad=SEPARATORWIDTH)
           

    def clear(self):
        # for child in self.scroller.winfo_children():
        #     child.grid_forget()
        for button in self.buttons:
            button.grid_forget()

    def configure(self, event):
        self.framework.refresh()

    def on_show_frame(self, event):
        self.framework.refresh()   

        

class store_app_square(cw.ThemedFrame):
    def __init__(self, parent, framework, repo):
        self.framework = framework
        self.repo = repo
        self.imageset = False
        cw.ThemedFrame.__init__(self, parent, background_color = w)
        self.place(width=TILEWIDTH, height=TILEWIDTH)

        button_image =ImageTk.PhotoImage(Image.open(notfoundimage).resize((TILEWIDTH, TILEWIDTH), Image.ANTIALIAS))
        
        self.buttonobj = button(self,image_object=button_image,callback=None,background = w)
        self.buttonobj.place(relwidth=1,relheight=1)

        try:
            web_dls = repo["web_dls"]
        except:
            web_dls = 0

        try:
            app_dls = repo["app_dls"]
        except:
            app_dls = 0


        ttl_dls = web_dls + app_dls
        ttp = "{}\nAuthor: {}\nDownloads: {}".format(repo["description"], repo["author"], ttl_dls)
        self.button_ttp = cw.tooltip(self.buttonobj,ttp)
        
        try:
            self.buttonlabel = cw.ThemedLabel(self.buttonobj,repo["name"],anchor="center",label_font=smallboldtext,foreground=lg,background=w)
            self.buttonlabel.place(rely=1, relx=0.5, x=-0.5*TILEWIDTH, width=TILEWIDTH, y = -20,height=20) #width = TILEWIDTH-2*SEPARATORWIDTH
        except:
            pass

        self.framework.after(5000, self.image_loop)

    def set_image(self):
        repo = self.repo
        try:
            image_file = getPackageIcon(repo["name"]) or notfoundimage
            button_image = Image.open(image_file)

            #Resizes and saves image if it's the wrong size for faster loads in the future
            if not button_image.size[0] == [TILEWIDTH, TILEWIDTH]:
                button_image = button_image.resize((TILEWIDTH, TILEWIDTH), Image.ANTIALIAS)
                button_image.save(image_file)

            self.button_image = ImageTk.PhotoImage(button_image)
        except Exception as e:
            print(e)
            self.button_image = ImageTk.PhotoImage(Image.open(notfoundimage).resize((TILEWIDTH, TILEWIDTH), Image.ANTIALIAS))

        self.buttonobj.setimage(self.button_image)

    #This function polls until the image has been set
    def image_loop(self):
        if self.framework.loaded_status():
            self.imageset = True
            self.framework.after(10, self.set_image)

        #Until the image has been set
        if not self.imageset:
            self.framework.after(1000, self.image_loop)


class button(tk.Label):
    def __init__(self,frame,callback=None,image_object= None,text_string=None,background=dark_color):
        self.callback = callback

        tk.Label.__init__(self,frame,
            background=background,
            foreground= w,
            borderwidth= 0,
            activebackground=light_color,
            image=image_object,
            text = text_string,
            font = smallboldtext,
            )
        self.bind('<Button-1>', self.on_click)

    #Use callback when our makeshift "button" clicked
    def on_click(self, event=None):
        if self.callback:
            self.callback()

    #Function to set the button's image
    def setimage(self,image):
        self.configure(image=image)

    #Function to set the button's text
    def settext(self,text):
        self.configure(text=text)