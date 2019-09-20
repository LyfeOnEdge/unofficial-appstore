import os
import tkinter.filedialog
import modules.style as style
import modules.locations as locations
from modules.widgets import ThemedFrame, ThemedListbox, ThemedLabel, searchBox, categoryFrame, installed_categoryFrame, activeFrame, scrolledText, button
from modules.tk_image_sharer import icon_dict

class appstorePage(activeFrame):
    def __init__(self, parent, controller, page_name, appstore_handler, repo_parser):
        self.current_frame = None
        self.last_selection = None
        self.controller = controller
        self.path_set = None
        self.appstore_handler = appstore_handler
        self.repo_parser = repo_parser
        self.icon_dict = icon_dict()
        activeFrame.__init__(self,parent,controller)

        self.column = ThemedFrame(self, background = style.light_color)
        self.column.place(relx = 0, rely = 0, width = style.sidecolumnwidth, relheight = 1)

        self.category_list = ThemedFrame(self.column, background = style.light_color)
        self.category_list.place(x=0, y=style.headerheight, relwidth=1, relheight=1, height = - (style.headerheight + style.footerheight))

        self.category_listbox = ThemedListbox(self.category_list)
        self.category_listbox.configure(activestyle = "dotbox")
        self.category_listbox.pack(fill="both", anchor="w")
        self.category_listbox.bind('<<ListboxSelect>>',self.select_frame)

        self.column_header = ThemedFrame(self.column, background = style.light_color)
        self.column_header.place(relx = 0, rely = 0, relwidth = 1, height = style.headerheight)

        self.column_header_title = ThemedLabel(self.column_header,"Unofficial Appstore\nGPLv3",anchor="center",label_font=style.giantboldtext, background = style.light_color)
        self.column_header_title.place(relx = 0,rely = 0, relwidth = 1, relheight = 1, height = - 1)

        self.column_header_separator = ThemedLabel(self.column_header, "", background=style.lg)
        self.column_header_separator.place(x = style.offset, rely = 1, y = - 1, relwidth = 1, width = -2 * style.offset)

        self.column_footer = ThemedFrame(self.column, background = style.light_color)
        self.column_footer.place(relx = 0, rely = 1, relwidth = 1, height = style.headerheight, y = - style.footerheight)

        self.column_set_sd = button(self.column_footer, 
            callback = self.set_sd, 
            text_string = "Select Switch SD Root", 
            font=style.mediumboldtext, 
            background=style.dark_color
            ).place(relwidth = 1, relheight = 0.5, y = style.offset, x = style.offset, width = - 2 * style.offset, height = - 2 * style.offset)

        self.column_sd_status_label = ThemedLabel(self.column_footer,"SD: Not Set",anchor="w",label_font=style.giantboldtext, background = style.light_color, foreground=style.b)
        self.column_sd_status_label.place(x = style.offset, relheight = 0.5, rely=0.5, height = -style.offset, relwidth = 1, width = - 2 * style.offset)

        self.content_frame = ThemedFrame(self)
        self.content_frame.place(x = style.sidecolumnwidth, width = -style.sidecolumnwidth, rely = 0, relheight = 1, relwidth = 1)

        self.content_frame_header = ThemedFrame(self.content_frame)
        self.content_frame_header.place(relx = 0, rely = 0, relwidth = 1, height = style.searchboxheight)

        self.category_label = ThemedLabel(self.content_frame_header,"",anchor="w",label_font=style.giantboldtext, background = style.w, foreground=style.b)
        self.category_label.place(relheight = 1, rely=0.5, y=-0.5*style.searchboxheight)

        self.content_frame_header_search_bar = searchBox(self.content_frame_header, command = self.search)
        
        #The various content gets stacked on top of each other here.
        self.content_stacking_frame = ThemedFrame(self.content_frame)
        self.content_stacking_frame.place(relx = 0, y=(style.searchboxheight + style.offset), relwidth = 1, relheight = 1, height=-(style.searchboxheight + style.offset))

        all_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.all, self.appstore_handler, self.icon_dict)
        advanced_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.advanced, self.appstore_handler, self.icon_dict)
        emus_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.emus, self.appstore_handler, self.icon_dict)
        games_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.games, self.appstore_handler, self.icon_dict)
        themes_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.themes, self.appstore_handler, self.icon_dict)
        tools_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.tools, self.appstore_handler, self.icon_dict)
        misc_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.misc, self.appstore_handler, self.icon_dict)
        installed_frame = installed_categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.all, self.appstore_handler, self.icon_dict)
        about_frame = aboutFrame(self.content_stacking_frame)

        self.category_frames = [all_frame,advanced_frame,emus_frame,games_frame,themes_frame,tools_frame,misc_frame, installed_frame]

        self.frames = [
            {
            "frame" : all_frame,
            "text" : "All Apps"
            },
            {
            "frame" : games_frame,
            "text" : "Games"
            },
            {
            "frame" : emus_frame,
            "text" : "Emulators"
            },
            {
            "frame" : tools_frame,
            "text" : "Tools"
            },
            {
            "frame" : advanced_frame,
            "text" : "Advanced"
            },
            {
            "frame" : themes_frame,
            "text" : "Themes"
            },
            {
            "frame" : misc_frame,
            "text" : "MISC"
            },
            {
            "frame" : installed_frame,
            "text" : "Installed"
            },
            {
            "frame" : about_frame,
            "text" : "About"
            }
        ]

        #Add pages as frames to dict, with keyword being the name of the frame
        self.content_frames = {}
        for E in self.frames:
            page_name = E["text"]
            frame = E["frame"]
            self.content_frames[page_name] = frame
            frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
            self.category_listbox.insert("end", " {}".format(page_name))
            self.category_listbox.select_set(0) #sets focus on the first item in listbox
            self.category_listbox.event_generate("<<ListboxSelect>>")

        self.show_frame("All Apps")
        self.loaded()

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.content_frames[page_name]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()
        self.category_label.set(page_name)
        self.controller.after(20, self.update_search_bar_position)
        self.current_frame = frame

    def update_search_bar_position(self):
        if not self.current_frame in self.category_frames:
            self.content_frame_header_search_bar.place_forget()
        else:
            category_label_offset = self.category_label.winfo_width()
            #If the category label has been populated, otherwise the offset is usually just a few pixels (prevents an ugly draw on launch)
            if category_label_offset > style.offset:
                self.content_frame_header_search_bar.place(x = category_label_offset + style.offset, rely=0.5, y=-0.5*style.searchboxheight,relheight =1, relwidth = 1, width = - (category_label_offset + 2 * style.offset))
            else:
                self.content_frame_header_search_bar.place_forget()
                self.controller.after(20, self.update_search_bar_position)

    def select_frame(self, event):
        try:
            widget = event.widget
            selection=widget.curselection()
            picked = widget.get(selection[0])
            if not picked == self.last_selection:
                frame = None
                for f in self.frames:
                    t = f["text"]
                    if t.strip() == picked.strip():
                        self.show_frame(t)
                        break
                self.last_selection = picked
        except Exception as e:
            print(e)

    def search(self, searchterm):
        self.current_frame.search(searchterm)

    def reload_category_frames(self):
        print("Reloading frames")
        for frame in self.category_frames:
            frame.configure(None)

    def set_sd(self):
        chosensdpath = tkinter.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
        self.appstore_handler.set_path(chosensdpath)
        self.reload_category_frames()
        self.path_set = True

        if chosensdpath:
            #Get the basename
            basepath = os.path.basename(os.path.normpath(chosensdpath))
            #If we didn't find it, assume it's a root dir and just return the whole path
            if not basepath:
                basepath = chosensdpath
        else:
            basepath = "Not Set"
        self.column_sd_status_label.set("SD: {}".format(basepath))

#Super basic about frame, pulls from about.txt
class aboutFrame(ThemedFrame):
    def __init__(self,frame):
        ThemedFrame.__init__(self, frame)

        with open(locations.aboutfile) as aboutfile:
            abouttext = aboutfile.read()

        self.abouttext = scrolledText(self, wrap = 'word', font = style.mediumtext)
        self.abouttext.place(relwidth=1, relheight =1)
        self.abouttext.insert("1.0", abouttext)
        self.abouttext.configure(state="disabled")