import tkinter as tk
import modules.style as style
from .progbar import progBar

class progressFrame(tk.Frame):
    def __init__(self, frame):
        tk.Frame.__init__(self,frame,background=style.w)
        self.progress = None
        self.progress_text = tk.StringVar()
        self.placed = False

        self.progbartext = tk.Label(self,
            background = style.w,
            highlightthickness=0,
            anchor="center",
            font=style.hugeboldtext,
            foreground= style.b,
            textvariable = self.progress_text,
            ).place(relwidth = 1, height = style.progressbarheight, width = -2*style.offset, rely = 0.5, y = - (2 * style.progressbarheight + 2 * style.offset))

        self.progbar = progBar(self)
        self.progbar.Place(relwidth = 1, height = style.progressbarheight, width = -2*style.offset, rely = 0.5, y = - style.progressbarheight / 2)

    def update(self, update_text, update_percent_int):
        if not update_percent_int or update_percent_int == 100:
            self.hide()
            self.progress_text.set("")
            self.progbar.setValue(0)
        else:
            self.show()
            self.progress_text.set(update_text + " ~ {}%".format(update_percent_int))
            self.progbar.setValue(update_percent_int)

    def show(self):
        self.place(relwidth = 1, relheight = 1)
        self.placed = True

    def hide(self):
        self.place_forget()
        self.placed = False

    def Place(self):
        self.show()