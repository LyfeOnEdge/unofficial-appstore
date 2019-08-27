import os
import tkinter
import modules.framework as framework
import modules.customwidgets as cw
import modules.style as style
import modules.webhandler as webhandler
import modules.categoryframe as cf
import modules.locations as locations
from modules.appstore_parser import parser
import tkinter.constants

store_json = webhandler.getJson("appstore_repo",locations.appstore_repo_url)
repo_parser = parser()
repo_parser.load(os.path.join(locations.jsoncachefolder, "appstore_repo.json"))

LEFT_COLUMN_WIDTH = 190
HEADER_HEIGHT = 50

class appstorePage(framework.Frame):
    def __init__(self, parent, controller, page_name):
        framework.Frame.__init__(self,parent,controller)
        self.controller = controller

        self.left_column = cw.ThemedFrame(self, background_color = style.light_color)
        self.left_column.place(relx = 0, rely = 0, width = LEFT_COLUMN_WIDTH, relheight = 1)

        self.category_list = cw.ThemedFrame(self.left_column, background_color = style.light_color)
        self.category_list.place(x=0, y=HEADER_HEIGHT, relwidth=1, relheight=1, height = - HEADER_HEIGHT)

        self.category_listbox = cw.ThemedListbox(self.category_list)
        self.category_listbox.configure(activestyle = "none")
        self.category_listbox.place(relwidth=1, relheight=1)
        self.category_listbox.bind('<<ListboxSelect>>',self.CurSelet)



        self.left_column_header = cw.ThemedFrame(self.left_column, background_color = style.light_color)
        self.left_column_header.place(relx = 0, rely = 0, relwidth = 1, height = HEADER_HEIGHT)

        self.left_column_header_title = cw.ThemedLabel(self.left_column_header,"Unofficial Appstore\nGPLv3",anchor="center",label_font=style.mediumboldtext, background = style.light_color)
        self.left_column_header_title.place(relx = 0,rely = 0, relwidth = 1, relheight = 1)


        self.content_frame = cw.ThemedFrame(self, background_color = style.w)
        self.content_frame.place(x = LEFT_COLUMN_WIDTH, width = -LEFT_COLUMN_WIDTH, rely = 0, relheight = 1, relwidth = 1)

        self.content_frame_header = cw.ThemedFrame(self.content_frame, background_color = style.w)
        self.content_frame_header.place(relx = 0, rely = 0, relwidth = 1, height = HEADER_HEIGHT)

        self.category_label = cw.ThemedLabel(self.content_frame_header,"",anchor="w",label_font=style.giantboldtext, background = style.w, foreground=style.b)
        self.category_label.place(height=HEADER_HEIGHT, rely=0.5, y=-25, relwidth=0.5)


        #The various content gets stacked on top of each other here.
        self.content_stacking_frame = cw.ThemedFrame(self.content_frame, background_color = style.w)
        self.content_stacking_frame.place(relx = 0, y=HEADER_HEIGHT, relwidth = 1, relheight = 1, height=-HEADER_HEIGHT)

        all_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.all)
        advanced_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.advanced)
        concepts_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.concepts)
        emus_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.emus)
        games_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.games)
        # loaders_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.loaders)
        themes_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.themes)
        tools_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.tools)
        # misc_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.misc)

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
            # {
            # "frame" : misc_frame,
            # "text" : "MISC"
            # }
        ]

        #Add pages as frames to dict, with keyword being the name of the frame
        self.content_frames = {}
        for E in self.frames:
            page_name = E["text"]
            frame = E["frame"]
            self.content_frames[page_name] = frame
            frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
            self.category_listbox.insert(tkinter.constants.END, page_name)

        self.show_frame("All Apps")
        self.loaded()

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.content_frames[page_name]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()
        self.category_label.set(page_name)

    def CurSelet(self, event):
        try:
            widget = event.widget
            selection=widget.curselection()
            picked = widget.get(selection[0])
            frame = None
            for f in self.frames:
                t = f["text"]
                if t == picked:
                    self.show_frame(t)
                    break
        except:
            pass