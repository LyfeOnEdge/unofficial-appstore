from PIL import Image, ImageTk
import tkinter as tk
import modules.style as style
from .customwidgets import ThemedFrame, button, tooltip, ThemedLabel 
from modules.appstore import getPackageIcon
from modules.locations import notfoundimage

class storeAppSquare(ThemedFrame):
    def __init__(self, parent, controller, framework, category_frame, repo):
        self.controller = controller
        self.parent = parent
        self.framework = framework
        self.category_frame = category_frame
        self.repo = repo
        self.image_sharer = self.controller.image_sharer
        self.imageset = False
        self.base_x = None #Stores the base x location to build the button from for dynamic building
        self.base_y = None #Stores the base y location to build the button from for dynamic building
        self.canvas = None
        self.placed = False
        ThemedFrame.__init__(self, parent, background = style.w)


        # button_image = ImageTk.PhotoImage(Image.open(notfoundimage).resize((style.thumbnailwidth, style.thumbnailheight), Image.ANTIALIAS))
        
        self.buttonobj = button(self,image_object=None,callback=lambda: self.open_details(repo),background = style.w)
        self.buttonobj.place(relx=0,y=-50,relwidth=1,relheight=1)

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
        self.button_ttp = tooltip(self.buttonobj,ttp)
        
        #Placeholders used by the category frame when building the button, fixes the disappearing text issue
        self.buttontitlelabel = None #Placeholder used for the button title
        self.buttonauthorlabel = None #Placeholder for the button author
        self.buttonversionlabel = None #Placeholder for the current cersion
        self.buttonseparator = None #Placeholder for underline in each button
        self.buttonstatuslabel = None #Placeholder for download / version status

    def open_details(self, repo):
        self.controller.frames["detailPage"].show(repo)

    def set_image(self):
        repo = self.repo
        package = repo["name"]

        #Checks a shared dict to see if this package already has an image loaded, returns none if not
        self.button_image = self.image_sharer.get_image(package)

        if not self.button_image:
            try:
                image_file = getPackageIcon(package) or notfoundimage
                button_image = Image.open(image_file)

                #Resizes and saves image if it's the wrong size for faster loads in the future
                if not button_image.size[0] == [style.thumbnailwidth, style.thumbnailheight]:
                    button_image = button_image.resize((style.thumbnailwidth, style.thumbnailheight), Image.ANTIALIAS)

                self.button_image = ImageTk.PhotoImage(button_image)
                if not image_file == notfoundimage:
                    self.image_sharer.set_image(package, self.button_image)

            except Exception as e:
                self.button_image = self.category_frame.notfoundimage
                self.image_sharer.set_image(package, self.button_image)

        self.buttonobj.setimage(self.button_image)
        self.imageset = True

    def set_xy_canvas(self, base_x, base_y, canvas):
        self.base_x = base_x
        self.base_y = base_y
        self.canvas = canvas

    def get_xy(self):
        return((self.base_x, self.base_y))

    def build_button(self):
        if not self.placed:
            self.placed = True
            if self.base_y and self.base_x and self.canvas:
                if not self.imageset:
                    self.set_image()

                label_y = self.base_y + style.thumbnailheight - style.buttontextheight + 40
                
                def place_buttontitlelabel():
                    if not self.buttontitlelabel:
                        self.buttontitlelabel = ThemedLabel(self.canvas,self.repo["title"],anchor="e",label_font=style.mediumboldtext,foreground=style.b,background=style.w)
                        self.buttontitlelabel.bind("<MouseWheel>", self.canvas.on_mouse_wheel)
                    self.buttontitlelabel.place(x = self.base_x, y =  label_y - 1.5 * style.buttontextheight, width = style.thumbnailwidth)

                def place_buttonauthorlabel():
                    if not self.buttonauthorlabel:
                        self.buttonauthorlabel = ThemedLabel(self.canvas,self.repo["author"],anchor="e",label_font=style.smallboldtext,foreground=style.lg,background=style.w)
                        self.buttonauthorlabel.bind("<MouseWheel>", self.canvas.on_mouse_wheel)
                    self.buttonauthorlabel.place(x = self.base_x, y = label_y, width = style.thumbnailwidth)

                def place_buttonstatuslabel():
                    if not self.buttonstatuslabel:
                        self.buttonstatuslabel = ThemedLabel(self.canvas,"",anchor="w",label_font=style.smallboldtext,foreground=style.lg,background=style.w)
                        self.buttonstatuslabel.bind("<MouseWheel>", self.canvas.on_mouse_wheel)
                    self.buttonstatuslabel.place(x = self.base_x, y = label_y - 1.5 * style.buttontextheight + 4)

                    status = None
                    package = self.repo["name"]
                    if self.controller.appstore_handler.packages:
                        if package in self.controller.appstore_handler.packages:
                            installed_version = self.controller.appstore_handler.get_package_version(package)

                            if self.controller.appstore_handler.clean_version(installed_version, package) == self.controller.appstore_handler.clean_version(installed_version, package):
                                status = "UPTODATE"
                            elif self.controller.appstore_handler.clean_version(installed_version, package) < self.controller.appstore_handler.clean_version(installed_version, package):
                                status = "NEEDSUPDATE"
                        else:
                            status = "NOTINSTALLED"
                    else:
                        status = "NOTINSTALLED"

                    self.buttonstatuslabel.configure(image=self.category_frame.status_map[status])

                def place_buttonversionlabel():
                    if not self.buttonversionlabel:
                        self.buttonversionlabel = ThemedLabel(self.canvas,self.repo["version"],anchor="w",label_font=style.smallboldtext,foreground=style.lg,background=style.w)
                        self.buttonversionlabel.bind("<MouseWheel>", self.canvas.on_mouse_wheel)
                    self.buttonversionlabel.place(x = self.base_x, y = label_y)

                def place_buttonseparator():
                    if not self.buttonseparator:
                        self.buttonseparator = tk.Label(self.canvas, background=style.lg, borderwidth= 0)
                    self.buttonseparator.place(x = self.base_x, y = label_y + 2 * style.offset + style.buttontextheight, height = 1, width = style.thumbnailwidth)

                place_buttonauthorlabel()
                place_buttontitlelabel()
                place_buttonstatuslabel()
                place_buttonversionlabel()
                place_buttonseparator()
                self.place(x=self.base_x, y = self.base_y, height = style.thumbnailwidth + 2 * style.offset, width = style.thumbnailwidth)
                self.placed = True