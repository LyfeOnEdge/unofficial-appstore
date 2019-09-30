import os
import tkinter.filedialog
import modules.style as style
import modules.locations as locations
from modules.widgets import ThemedFrame, ThemedLabel, activeFrame, scrolledText, button, tooltip, progressFrame
from modules.appstore import parser, getScreenImage
from modules.webhandler import opentab
from .yesnopage import yesnoPage

from PIL import Image, ImageTk

class detailPage(activeFrame):
    def __init__(self, parent, controller):
        activeFrame.__init__(self,parent,controller)
        self.controller = controller
        self.appstore_handler = controller.appstore_handler
        self.repo_parser = controller.repo_parser
        self.repo = None

        #------------------------------
        self.column = ThemedFrame(self, background = style.light_color)
        self.column.place(relx = 1, rely = 0, width = style.sidecolumnwidth, relheight = 1, x = - style.sidecolumnwidth)

        self.column_body = ThemedFrame(self.column, background = style.light_color)
        self.column_body.place(relwidth=1, relheight=1)


        self.column_title = ThemedLabel(self.column_body,"",anchor="w",label_font=style.mediumboldtext, foreground = style.w, background = style.light_color)
        self.column_title.place(x = 5, width = - 5, rely = 0, relwidth = 1, height = style.headerheight)


        #------------------------------
        self.column_author = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.light_color)
        self.column_author.place(x = 5, width = - 5, y = style.headerheight, relwidth = 1, height = 0.333 * style.headerheight)

        self.column_version = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.light_color)
        self.column_version.place(x = 5, width = - 5, y = 1.333 * style.headerheight, relwidth = 1, height = 0.333 * style.headerheight)

        self.column_license = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.light_color)
        self.column_license.place(x = 5, width = - 5, y = 1.666 * style.headerheight, relwidth = 1, height = 0.333 * style.headerheight)
        #------------------------------


        #------------------------------
        self.column_package = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.light_color)
        self.column_package.place(x = 5, width = - 5, y = 2.333 * style.headerheight, relwidth = 1, height = 0.333 * style.headerheight)

        self.column_downloads = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.light_color)
        self.column_downloads.place(x = 5, width = - 5, y = 2.666 * style.headerheight, relwidth = 1, height = 0.333 * style.headerheight)

        self.column_updated = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.light_color)
        self.column_updated.place(x = 5, width = - 5, y = 3.00 * style.headerheight, relwidth = 1, height = 0.333 * style.headerheight)
        #------------------------------

        #------------------------------
        self.column_downloaded = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.light_color)
        self.column_downloaded.place(x = 5, width = - 5, y = 3.66 * style.headerheight, relwidth = 1, height = 0.333 * style.headerheight)
        #------------------------------

        self.column_extracted = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.light_color)
        self.column_extracted.place(x = 5, width = - 5, y = 4 * style.headerheight, relwidth = 1, height = 0.333 * style.headerheight)

        self.column_open_url_button = button(self.column_body, 
            callback = self.trigger_open_tab, 
            text_string = "VISIT PAGE", 
            font=style.mediumboldtext, 
            background=style.dark_color
            ).place(rely=1,relx=0.5,x = - 1.5 * (style.buttonsize), y = - 4 * (style.buttonsize + style.offset), width = 3 * style.buttonsize, height = style.buttonsize)

        self.column_install_button = button(self.column_body, 
            callback = self.trigger_install, 
            text_string = "INSTALL", 
            font=style.mediumboldtext, 
            background=style.dark_color
            )
        self.column_install_button.place(rely=1,relx=0.5,x = - 1.5 * (style.buttonsize), y = - 3 * (style.buttonsize + style.offset), width = 3 * style.buttonsize, height = style.buttonsize)

        self.column_uninstall_button = button(self.column_body, 
            callback = self.trigger_uninstall, 
            text_string = "UNINSTALL", 
            font=style.mediumboldtext, 
            background=style.dark_color
            )

        self.back_image = ImageTk.PhotoImage(Image.open(locations.backimage).resize((style.buttonsize, style.buttonsize), Image.ANTIALIAS))

        self.column_backbutton = button(self.column_body, image_object=self.back_image, callback=self.leave, background=style.light_color)
        self.column_backbutton.place(rely=1,relx=1,x = -(style.buttonsize + style.offset), y = -(style.buttonsize + style.offset))
        self.column_backbutton_ttp = tooltip(self.column_backbutton,"Back to list")

        self.content_frame = ThemedFrame(self, background = style.w)
        self.content_frame.place(x = 0, width = -style.sidecolumnwidth, rely = 0, relheight = 1, relwidth = 1)

        self.content_frame_header = ThemedFrame(self.content_frame, background = style.w)
        self.content_frame_header.place(x = style.offset, width = - 2 * style.offset, rely = 0, relwidth = 1, height = style.headerheight)

        self.content_frame_body = ThemedFrame(self.content_frame, background = style.w)
        self.content_frame_body.place(x = style.offset, width = - 2 * style.offset, y = style.headerheight,relwidth = 1, height = -style.headerheight, relheight=1)

        self.content_banner_image = ThemedLabel(self.content_frame_body,"",background = style.w,foreground=style.w,anchor="center",wraplength = None)
        self.content_banner_image.place(x=0, y = 0, relwidth=1, relheight = 0.5)

        self.content_frame_details = scrolledText(self.content_frame_body, wrap = 'word', font = style.smalltext)
        self.content_frame_details.place(rely=0.5, relx=0,relwidth=1,relheight=0.5,x=+style.offset, width = - 2 * (style.offset), height=-style.offset)

        #Displays app name
        self.header_label = ThemedLabel(self.content_frame_header,"",anchor="w",label_font=style.giantboldtext, background = style.w, foreground=style.b)
        self.header_label.place(rely=0, y=0, relheight=0.65)

        #Displays app name
        self.header_author = ThemedLabel(self.content_frame_header,"",anchor="w",label_font=style.smalltext, background = style.w, foreground=style.light_color)
        self.header_author.place(rely=0.65, y=0, relheight=0.35)

        self.progress_bar = progressFrame(self)

        self.yesnoPage = yesnoPage(self)

    def update_page(self,repo):
        self.repo = repo
        package = repo["name"]

        try:
            web_dls = repo["web_dls"]
        except:
            web_dls = 0

        try:
            app_dls = repo["app_dls"]
        except:
            app_dls = 0

        ttl_dls = web_dls + app_dls

        self.column_title.set("Title: {}".format(repo["title"]))

        self.column_author.set("Author: {}".format(repo["author"]))
        self.column_version.set("Version: {}".format(repo["version"]))
        self.column_license.set("License: {}".format(repo["license"]))


        self.column_package.set("Package: {}".format(package))
        self.column_downloads.set("Downloads: {}".format(ttl_dls))
        self.column_updated.set("Updated: {}".format(repo["updated"]))


        self.column_downloaded.set("Dowloaded size: {} KB".format(repo["filesize"]))
        self.column_extracted.set("Install size: {} KB".format(repo["extracted"]))


        self.content_frame_details.configure(state="normal")
        self.content_frame_details.delete('1.0', "end")

        #Makes newlines in details print correctly. Hacky but :shrug:
        details = repo["details"].replace("\\n", """
"""
            )
        self.content_frame_details.insert("1.0", details)
        self.content_frame_details.configure(state="disabled")


        self.header_label.set(repo["title"])
        self.header_author.set(repo["author"])

        #Hides or places the uninstalll button if not installed or installed respectively
        #get_package_entry returns none if no package is found or if the sd path is not set
        if self.appstore_handler.get_package_entry(package):
            self.column_uninstall_button.place(rely=1,relx=0.5,x = - 1.5 * (style.buttonsize), y = - 2 * (style.buttonsize + style.offset), width = 3 * style.buttonsize, height = style.buttonsize)
            if self.column_install_button:
                if self.appstore_handler.clean_version(self.appstore_handler.get_package_version(package), package) > self.appstore_handler.clean_version(self.appstore_handler.get_package_version(self.repo["version"]), package):
                    self.column_install_button.settext("UPDATE")
                else:
                    self.column_install_button.settext("REINSTALL")
        else:
            self.column_uninstall_button.place_forget()
            if self.column_install_button:
                self.column_install_button.settext("INSTALL")

        def do_update_banner():
            self.bannerimage = getScreenImage(package)
            if self.bannerimage:
                self.update_banner(self.bannerimage)
            else:
                self.update_banner(locations.notfoundimage)
                print("failed to download screenshot for {}".format(package))
            
        self.controller.async_threader.do_async(do_update_banner, [])

    def update_banner(self,image_path):
        art_image = Image.open(image_path)
        art_image = ImageTk.PhotoImage(art_image)
        self.content_banner_image.configure(image=art_image)
        self.content_banner_image.image = art_image

    def show(self, repo):
        self.update_banner(locations.notfoundimage)
        self.controller.async_threader.do_async(self.update_page, [repo], priority = "medium")
        self.tkraise()
        for child in self.winfo_children():
            child.bind("<Escape>", self.leave)

    def leave(self):
        self.controller.show_frame("appstorePage")
        for child in self.winfo_children():
            child.unbind("<Escape>")

    def reload_function(self):
            self.controller.frames["appstorePage"].reload_category_frames()
            self.reload()

    def trigger_install(self):
        if not self.appstore_handler.check_path():
            self.set_sd()
        if self.appstore_handler.check_path():
            if self.appstore_handler.check_if_get_init():
                if self.repo:
                    self.controller.async_threader.do_async(self.appstore_handler.install_package, [self.repo, self.progress_bar.update, self.reload_function, self.progress_bar.set_title], priority = "high")
            else:
                self.yesnoPage.getanswer("The homebrew appstore has not been initiated here yet, would you like to initiate it?", self.init_get_then_continue)

    def init_get_then_continue(self):
        self.appstore_handler.init_get()
        self.trigger_install()

    def trigger_uninstall(self):
        if self.repo:
            self.controller.async_threader.do_async(self.appstore_handler.uninstall_package, [self.repo], priority = "high")
            self.controller.frames["appstorePage"].reload_category_frames()
            self.schedule_callback(self.reload(), 100)

    def reload(self):
        self.controller.async_threader.do_async(self.update_page, [self.repo])

    def trigger_open_tab(self):
        if self.repo:
            try:
                url = self.repo["url"]
                opentab(url)
            except:
                print("Failed to open tab for url {}".format(url))

    def set_sd(self):
        chosensdpath = tkinter.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
        self.appstore_handler.set_path(chosensdpath)
        self.reload()