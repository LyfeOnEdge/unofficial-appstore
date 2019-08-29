from PIL import Image, ImageTk

import modules.style as style
from .customwidgets import ThemedFrame, button, tooltip, ThemedLabel 
from modules.appstore import getPackageIcon
from modules.locations import notfoundimage

class storeAppSquare(ThemedFrame):
    def __init__(self, parent, controller, framework, repo):
        self.controller = controller
        self.framework = framework
        self.repo = repo
        self.imageset = False
        ThemedFrame.__init__(self, parent, background = style.w)
        self.place(width=style.thumbnailsize, height=style.thumbnailsize)

        button_image = ImageTk.PhotoImage(Image.open(notfoundimage).resize((style.thumbnailsize, style.thumbnailsize), Image.ANTIALIAS))
        
        self.buttonobj = button(self,image_object=button_image,callback=lambda: self.open_details(repo),background = style.w)
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
        
        try:
            self.buttonlabel = ThemedLabel(self.buttonobj,repo["title"],anchor="center",label_font=style.smallboldtext,foreground=style.lg,background=style.w)
            self.buttonlabel.place(rely=1, relx=0.5, x=-0.5*style.thumbnailsize, width=style.thumbnailsize, y = -20,height=20) #width = style.thumbnailsize-2*SEPARATORWIDTH
        except:
            pass

        self.framework.after(5000, self.image_loop)

    def open_details(self, repo):
        self.controller.frames["detailPage"].show(repo)

    def set_image(self):
        repo = self.repo
        try:
            image_file = getPackageIcon(repo["name"]) or notfoundimage
            button_image = Image.open(image_file)

            #Resizes and saves image if it's the wrong size for faster loads in the future
            if not button_image.size[0] == [style.thumbnailsize, style.thumbnailsize]:
                button_image = button_image.resize((style.thumbnailsize, style.thumbnailsize), Image.ANTIALIAS)
                button_image.save(image_file)

            self.button_image = ImageTk.PhotoImage(button_image)
        except Exception as e:
            print(e)
            self.button_image = ImageTk.PhotoImage(Image.open(notfoundimage).resize((style.thumbnailsize, style.thumbnailsize), Image.ANTIALIAS))

        self.buttonobj.setimage(self.button_image)

    #This function polls until the image has been set
    def image_loop(self):
        if self.framework.loaded_status():
            self.imageset = True
            self.framework.after(10, self.set_image)

        #Until the image has been set
        if not self.imageset:
            self.framework.after(1000, self.image_loop)