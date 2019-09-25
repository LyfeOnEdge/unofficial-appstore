from PIL import Image, ImageTk

import modules.style as style
from .customwidgets import ThemedFrame, button, tooltip, ThemedLabel 
from modules.appstore import getPackageIcon
from modules.locations import notfoundimage

class storeAppSquare(ThemedFrame):
    def __init__(self, parent, controller, framework, repo, icon_dict):
        self.controller = controller
        self.framework = framework
        self.repo = repo
        self.icon_dict = icon_dict
        self.imageset = False
        ThemedFrame.__init__(self, parent, background = style.w)


        # button_image = ImageTk.PhotoImage(Image.open(notfoundimage).resize((style.thumbnailwidth, style.thumbnailheight), Image.ANTIALIAS))
        
        self.buttonobj = button(self,image_object=None,callback=lambda: self.open_details(repo),background = style.w)
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
        self.button_ttp = tooltip(self.buttonobj,ttp)
        
        #Placeholders used by the category frame when building the button, fixes the disappearing text issue
        self.buttontitlelabel = None #Placeholder used for the button title
        self.buttonauthorlabel = None #Placeholder for the button author
        self.buttonversionlabel = None #Placeholder for the current cersion
        self.buttonseparator = None #Placeholder for underline in each button
        self.buttonstatuslabel = None #Placeholder for download / version status
        
        self.framework.after(50, self.image_loop)

    def open_details(self, repo):
        self.controller.frames["detailPage"].show(repo)

    def set_image(self):
        repo = self.repo
        package = repo["name"]

        #Checks a shared dict to see if this package already has an image loaded, returns none if not
        self.button_image = self.icon_dict.get_image(package)

        if not self.button_image:
            try:
                image_file = getPackageIcon(package) or notfoundimage
                button_image = Image.open(image_file)

                #Resizes and saves image if it's the wrong size for faster loads in the future
                if not button_image.size[0] == [style.thumbnailwidth, style.thumbnailheight]:
                    button_image = button_image.resize((style.thumbnailwidth, style.thumbnailheight), Image.ANTIALIAS)
                    # button_image.save(image_file)

                self.button_image = ImageTk.PhotoImage(button_image)
                if not image_file == notfoundimage:
                    self.icon_dict.set_image(package, self.button_image)

            except Exception as e:
                print(e)
                self.button_image = ImageTk.PhotoImage(Image.open(notfoundimage).resize((style.thumbnailwidth, style.thumbnailheight - 10), Image.ANTIALIAS))

        self.buttonobj.setimage(self.button_image)

    #This function polls until the image has been set
    def image_loop(self):
        if self.framework.loaded_status():
            self.imageset = True
            self.set_image()

        #Until the image has been set
        if not self.imageset:
            self.framework.after(50, self.image_loop)