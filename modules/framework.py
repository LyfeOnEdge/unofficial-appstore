import tkinter as tk
from modules.style import dark_color

class Frame(tk.Frame):
    def __init__(self, parent, controller, tick_delay = 250):
        self.controller = controller
        self.tick_delay = tick_delay
        self.needsRefresh = False
        self.on_refresh_callbacks = []
        self.on_tick_callbacks = []
        self.done_loading = False

        tk.Frame.__init__(self,parent, 
            background = dark_color,
            highlightthickness=0,
            highlightbackground=dark_color,
            borderwidth = 0
            )

        self.bind("<<ShowFrame>>", self.on_show_frame) #Bind on_show_frame to showframe event so whenever the frame is raised by the controller it reloads
        self.klock()

    #Ques refresh
    def refresh(self):
        self.needsRefresh = True
    
    #Generally forces a reload
    def on_show_frame(self,event=None):
        self.refresh()

    #Call klock at end of each framework-based frame to start it
    def klock(self):
        self.controller.after(self.tick_delay, self.klock)
        self.tick()
    def tick(self):
        self.on_tick()
        if self.needsRefresh:
            self.on_refresh()
            self.needsRefresh = False

    def on_tick(self):
        self.do_callbacks_list(self.on_tick_callbacks)

    def on_refresh(self):
        self.do_callbacks_list(self.on_refresh_callbacks)

    def add_on_refresh_callback(self, callback):
        self.on_refresh_callbacks.append(callback)

    def add_on_tick_callback(self, callback):
        self.on_tick_callbacks.append(callback)
            
    def do_callbacks_list(self, callbacks_list):
        if callbacks_list:
            try:
                for callback in callbacks_list:
                    self.controller.after(1,callback())
            except Exception as e:
                print("do_callbacks_list error %s" % e)

    def schedule_callback(self, callback):
        self.controller.after(1, callback)

    def schedule_callbacks(self, callbacks):
        for callback in callbacks:
            self.schedule_callback(callback)

    def loaded(self):
        self.done_loading = True

    def loaded_status(self):
        return self.done_loading
