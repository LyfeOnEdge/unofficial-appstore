import tkinter as tk
from tkinter.constants import *
import platform, os
from modules.style import *

#Basic Widgets

#Frame to use instead of default tk.frame, by default themed with light_color
class ThemedFrame(tk.Frame):
	def __init__(self,parent,frame_borderwidth = 0,frame_highlightthickness = 0,background_color = dark_color,frame_highlightcolor=dark_color):
		tk.Frame.__init__(self,parent, 
			background = background_color,
			highlightcolor = frame_highlightcolor,
			highlightthickness=frame_highlightthickness,
			highlightbackground=light_color,
			borderwidth = frame_borderwidth,
			)


#themed author/ etc label
class ThemedLabel(tk.Label):
	def __init__(self,frame,label_text,label_font=smalltext,text_variable=None,background = light_color,foreground=lg,anchor="w",wraplength = None, image = None):
		tk.Label.__init__(self,frame,
			background = background,
			highlightthickness=0,
			anchor=anchor,
			text = label_text,
			font=label_font,
			foreground= foreground,
			textvariable = text_variable,
			image = image
			)
		if not wraplength == None:
			self.configure(wraplength=wraplength)
	def set(self,text):
		self.configure(text=text)
	def set_image(self,image):
		self.configure(image=image)


#themed author/ etc label
class ThemedListbox(tk.Listbox):
	def __init__(self,frame):
		tk.Listbox.__init__(self,frame,
			background = light_color,
			selectbackground = dark_color,
			borderwidth = 0,
			highlightthickness=0,
			foreground= lg,
			font = mediumboldtext,
			activestyle=None
		)
		
#Custom button
#A tkinter label with a bound on-click event to fix some issues 
#that were happening with normal tkinter buttons on MacOS.
#Unfortunately MacOS was causing a weird white translucent
#effect to be applied to all classes that used the tk.Button Widget.
#This fixes it but making our own "button" by binding a callback to 
#an on_click event. Feel free to use this in other projects where mac
#compatibility is an issue, also special thanks to Kabiigon for testing
#this widget until I got it right since I don't have a mac
class navbutton(tk.Label):
	def __init__(self,frame,command_name=None,image_object= None,text_string=None,background=dark_color):
		self.command = command_name

		tk.Label.__init__(self,frame,
			background=background,
			foreground= w,
			borderwidth= 0,
			activebackground=light_color,
			image=image_object,
			text = text_string,
			font = navbuttonfont,
			)
		self.bind('<Button-1>', self.on_click)

	#Use callback when our makeshift "button" clicked
	def on_click(self, event=None):
		if self.command:
			self.command()

	#Function to update the button's set command
	def setcommand(self,command):
		self.command = command

	#Function to set the button's image
	def setimage(self,image):
		self.configure(image=image)

	#Function to set the button's text
	def settext(self,text):
		self.configure(text=text)

#Tooltip
class ToolTipBase:
	def __init__(self, button):
		self.button = button
		self.tipwindow = None
		self.id = None
		self.x = self.y = 0
		self._id1 = self.button.bind("<Enter>", self.enter)
		self._id2 = self.button.bind("<Leave>", self.leave)
		self._id3 = self.button.bind("<ButtonPress>", self.leave)

	def enter(self, event=None):
		self.schedule()

	def leave(self, event=None):
		self.unschedule()
		self.hidetip()

	def schedule(self):
		self.unschedule()
		self.id = self.button.after(10, self.showtip)

	def unschedule(self):
		id = self.id
		self.id = None
		if id:
			self.button.after_cancel(id)

	def showtip(self):
		if self.tipwindow:
			return
		# The tip window must be completely outside the button;
		# otherwise when the mouse enters the tip window we get
		# a leave event and it disappears, and then we get an enter
		# event and it reappears, ad naseum.
		x = self.button.winfo_rootx() + 0
		y = self.button.winfo_rooty() + self.button.winfo_height() + 1
		self.tipwindow = tw = tk.Toplevel(self.button)
		tw.wm_overrideredirect(1)
		tw.wm_geometry("+%d+%d" % (x, y))
		self.showcontents()

	def showcontents(self, text=""):
		label = tk.Label(self.tipwindow, text=text, justify=LEFT,
					  background=dark_color, 
					  relief=SOLID, 
					  borderwidth=2,
					  foreground=lg,
					  font=mediumboldtext
					  )
		label.pack()

	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()

class tooltip(ToolTipBase):
	def __init__(self, button, text):
		ToolTipBase.__init__(self, button)
		self.text = text

	def showcontents(self):
		ToolTipBase.showcontents(self, self.text)


class button(tk.Label):
    def __init__(self,frame,callback=None,image_object= None,text_string=None,background=dark_color):
        self.callback = callback

        tk.Label.__init__(self,frame,
            background=background,
            foreground= w,
            borderwidth= 0,
            activebackground=light_color,
            image=image_object,
            text = text_string,
            font = smallboldtext,
            )
        self.bind('<Button-1>', self.on_click)

    #Use callback when our makeshift "button" clicked
    def on_click(self, event=None):
        if self.callback:
            self.callback()

    #Function to set the button's image
    def setimage(self,image):
        self.configure(image=image)

    #Function to set the button's text
    def settext(self,text):
        self.configure(text=text)
