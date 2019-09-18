import os
import tkinter.filedialog
import modules.style as style
import modules.locations as locations
from modules.widgets import ThemedFrame, ThemedListbox, ThemedLabel, searchBox, categoryFrame, activeFrame, scrolledText, button

class appstorePage(activeFrame):
    def __init__(self, parent, controller, page_name, appstore_handler, repo_parser):
        activeFrame.__init__(self,parent,controller)
        self.current_frame = None
        self.controller = controller
        self.appstore_handler = appstore_handler
        self.repo_parser = repo_parser

        self.column = ThemedFrame(self, background = style.light_color)
        self.column.place(relx = 0, rely = 0, width = style.sidecolumnwidth, relheight = 1)

        self.category_list = ThemedFrame(self.column, background = style.light_color)
        self.category_list.place(x=0, y=style.headerheight, relwidth=1, relheight=1, height = - (style.headerheight + style.footerheight))

        self.category_listbox = ThemedListbox(self.category_list)
        self.category_listbox.configure(activestyle = "none")
        self.category_listbox.pack(fill="both", anchor="w")
        self.category_listbox.bind('<<ListboxSelect>>',self.CurSelet)

        self.column_header = ThemedFrame(self.column, background = style.light_color)
        self.column_header.place(relx = 0, rely = 0, relwidth = 1, height = style.headerheight)

        self.column_header_title = ThemedLabel(self.column_header,"Unofficial Appstore\nGPLv3",anchor="center",label_font=style.mediumboldtext, background = style.light_color)
        self.column_header_title.place(relx = 0,rely = 0, relwidth = 1, relheight = 1)

        self.column_footer = ThemedFrame(self.column, background = style.light_color)
        self.column_footer.place(relx = 0, rely = 1, relwidth = 1, height = style.headerheight, y = - style.footerheight)

        self.column_set_sd = button(self.column_footer, 
            callback = self.set_sd, 
            text_string = "Select Switch SD Root", 
            font=style.mediumboldtext, 
            background=style.dark_color
            ).place(relwidth = 1, relheight = 1, y = style.offset, x = style.offset, width = - 2 * style.offset, height = - 2 * style.offset)

        self.content_frame = ThemedFrame(self)
        self.content_frame.place(x = style.sidecolumnwidth, width = -style.sidecolumnwidth, rely = 0, relheight = 1, relwidth = 1)

        self.content_frame_header = ThemedFrame(self.content_frame)
        self.content_frame_header.place(relx = 0, rely = 0, relwidth = 1, height = style.headerheight)

        self.category_label = ThemedLabel(self.content_frame_header,"",anchor="w",label_font=style.giantboldtext, background = style.w, foreground=style.b)
        self.category_label.place(height=style.headerheight, rely=0.5, y=-25)

        self.content_frame_header_searh_bar = searchBox(self.content_frame_header, command = self.search)
        
        #The various content gets stacked on top of each other here.
        self.content_stacking_frame = ThemedFrame(self.content_frame)
        self.content_stacking_frame.place(relx = 0, y=style.headerheight, relwidth = 1, relheight = 1, height=-style.headerheight)

        all_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.all, self.appstore_handler)
        advanced_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.advanced, self.appstore_handler)
        concepts_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.concepts, self.appstore_handler)
        emus_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.emus, self.appstore_handler)
        games_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.games, self.appstore_handler)
        loaders_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.loaders, self.appstore_handler)
        themes_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.themes, self.appstore_handler)
        tools_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.tools, self.appstore_handler)
        misc_frame = categoryFrame(self.content_stacking_frame, self.controller, self, self.repo_parser.misc, self.appstore_handler)
        about_frame = aboutFrame(self.content_stacking_frame)

        self.category_frames = [all_frame,advanced_frame,concepts_frame,emus_frame,games_frame,loaders_frame,themes_frame,tools_frame,misc_frame]

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
            # {
            # "frame" : loaders_frame,
            # "text" : "Loaders"
            # },
            {
            "frame" : concepts_frame,
            "text" : "Concepts"
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
            self.content_frame_header_searh_bar.place_forget()
        else:
            category_label_offset = self.category_label.winfo_width()
            #If the category label has been populated, otherwise the offset is usually just a few pixels (prevents an ugly draw on launch)
            if category_label_offset > style.offset:
                self.content_frame_header_searh_bar.place(x = category_label_offset + style.offset, rely=0.5, y=-0.5*style.searchboxheight, height = style.searchboxheight, relwidth = 1, width = - (category_label_offset + 2 * style.offset))
            else:
                self.content_frame_header_searh_bar.place_forget()
                self.controller.after(20, self.update_search_bar_position)

    def CurSelet(self, event):
        try:
            widget = event.widget
            selection=widget.curselection()
            picked = widget.get(selection[0])
            frame = None
            for f in self.frames:
                t = f["text"]
                if t.strip() == picked.strip():
                    self.show_frame(t)
                    break
        except:
            pass

    def search(self, searchterm):
        for frame in self.category_frames:
            frame.search(searchterm)

    def reload_category_frames(self):
        for frame in self.category_frames:
            frame.configure(None)

    def set_sd(self):
        chosensdpath = tkinter.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
        self.appstore_handler.set_path(chosensdpath)
        self.reload_category_frames()

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