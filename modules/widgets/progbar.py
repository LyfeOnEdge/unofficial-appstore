import tkinter as tk
import modules.style as style

#A super basic progress bar

class progBar(tk.Frame):
	def __init__(self, frame):
		tk.Frame.__init__(self,frame,background=style.w)
		self.progress = tk.Frame(self, background=style.dark_color)
		self.geo = None
		self.placed = False
		self.setValue(None)

	def setValue(self, val):
		if val and not val == 0:
			if not self.placed:
				self.show()
			self.progress.place(x=style.offset, y=style.offset, relheight=1, height=-(2*style.offset),relwidth=(val/100.0),width=-2*style.offset)
		else:
			if self.placed:
				self.hide()

	def show(self):
		self.place(self.geo)
		self.placed = True

	def hide(self):
		self.place_forget()
		self.placed = False

	def Place(self, **geo):
		self.place(**geo)
		self.placed = True
		self.geo = geo