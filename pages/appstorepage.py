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

class appstorePage(framework.Frame):
    def __init__(self, parent, controller, page_name):
        framework.Frame.__init__(self,parent,controller)
        self.current_frame = None
        self.controller = controller

        self.column = cw.ThemedFrame(self, background_color = style.light_color)
        self.column.place(relx = 0, rely = 0, width = style.sidecolumnwidth, relheight = 1)

        self.category_list = cw.ThemedFrame(self.column, background_color = style.light_color)
        self.category_list.place(x=0, y=style.headerheight, relwidth=1, relheight=1, height = - style.headerheight)

        self.category_listbox = cw.ThemedListbox(self.category_list)
        self.category_listbox.configure(activestyle = "none")
        self.category_listbox.pack(fill="both", anchor="w")
        self.category_listbox.bind('<<ListboxSelect>>',self.CurSelet)


        self.column_header = cw.ThemedFrame(self.column, background_color = style.light_color)
        self.column_header.place(relx = 0, rely = 0, relwidth = 1, height = style.headerheight)

        self.column_header_title = cw.ThemedLabel(self.column_header,"Unofficial Appstore\nGPLv3",anchor="center",label_font=style.mediumboldtext, background = style.light_color)
        self.column_header_title.place(relx = 0,rely = 0, relwidth = 1, relheight = 1)


        self.content_frame = cw.ThemedFrame(self, background_color = style.w)
        self.content_frame.place(x = style.sidecolumnwidth, width = -style.sidecolumnwidth, rely = 0, relheight = 1, relwidth = 1)

        self.content_frame_header = cw.ThemedFrame(self.content_frame, background_color = style.w)
        self.content_frame_header.place(relx = 0, rely = 0, relwidth = 1, height = style.headerheight)

        self.category_label = cw.ThemedLabel(self.content_frame_header,"",anchor="w",label_font=style.giantboldtext, background = style.w, foreground=style.b)
        self.category_label.place(height=style.headerheight, rely=0.5, y=-25)

        self.content_frame_header_searh_bar = cw.SearchBox(self.content_frame_header, command = self.search)
        
        #The various content gets stacked on top of each other here.
        self.content_stacking_frame = cw.ThemedFrame(self.content_frame, background_color = style.w)
        self.content_stacking_frame.place(relx = 0, y=style.headerheight, relwidth = 1, relheight = 1, height=-style.headerheight)

        all_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.all)
        advanced_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.advanced)
        concepts_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.concepts)
        emus_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.emus)
        games_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.games)
        loaders_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.loaders)
        themes_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.themes)
        tools_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.tools)
        misc_frame = cf.categoryFrame(self.content_stacking_frame, self.controller, self, repo_parser.misc)
        about_frame = aboutFrame(self.content_stacking_frame)

        self.searchable_frames = [all_frame,advanced_frame,concepts_frame,emus_frame,games_frame,loaders_frame,themes_frame,tools_frame,misc_frame]

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
            self.category_listbox.insert(tkinter.constants.END, page_name)

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
        if not self.current_frame in self.searchable_frames:
            self.content_frame_header_searh_bar.place_forget()
        else:
            self.content_frame_header_searh_bar.place(x = self.category_label.winfo_width() + style.offset, rely=0.5, y=-0.5*style.searchboxheight, height = style.searchboxheight, relwidth = 1, width = - (self.category_label.winfo_width() + 2 * style.offset))


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

    def search(self, searchterm):
        for frame in self.searchable_frames:
            frame.search(searchterm)


class aboutFrame(cw.ThemedFrame):
    def __init__(self,frame):
        cw.ThemedFrame.__init__(self, frame, background_color = style.w)

        with open(locations.aboutfile) as aboutfile:
            abouttext = aboutfile.read()

        self.abouttext = cw.ScrolledText(self, wrap = 'word', font = style.mediumtext)
        self.abouttext.place(relwidth=1, relheight =1)
        self.abouttext.insert("1.0", abouttext)
        self.abouttext.configure(state="disabled")