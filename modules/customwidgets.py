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
	def __init__(self,frame,label_text,label_font=smalltext,text_variable=None,background = light_color,foreground=lg,anchor="w",wraplength = None):
		tk.Label.__init__(self,frame,
			background = background,
			highlightthickness=0,
			anchor=anchor,
			text = label_text,
			font=label_font,
			foreground= foreground,
			textvariable = text_variable,
			)
		if not wraplength == None:
			self.configure(wraplength=wraplength)
	def set(self,text):
		self.configure(text=text)



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
    def __init__(self,frame,callback=None,image_object= None,text_string=None,background=dark_color, font=smallboldtext):
        self.callback = callback

        tk.Label.__init__(self,frame,
            background=background,
            foreground= w,
            borderwidth= 0,
            activebackground=light_color,
            image=image_object,
            text = text_string,
            font = font,
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


#Widgets with scroll bars that appear when needed and supporting code
#Automatic scrollbars on certain text boxes
class AutoScroll(object):
	def __init__(self, master):
		try:
			vsb = tk.Scrollbar(master, orient='vertical', command=self.yview)
		except:
			pass
		hsb = tk.Scrollbar(master, orient='horizontal', command=self.xview)

		try:
			self.configure(yscrollcommand=self._autoscroll(vsb))
		except:
			pass
		self.configure(xscrollcommand=self._autoscroll(hsb))

		self.grid(column=0, row=0, sticky='nsew')
		try:
			vsb.grid(column=1, row=0, sticky='ns')
		except:
			pass
		hsb.grid(column=0, row=1, sticky='ew')

		master.grid_columnconfigure(0, weight=1)
		master.grid_rowconfigure(0, weight=1)

		methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
			| tk.Place.__dict__.keys()

		for meth in methods:
			if meth[0] != '_' and meth not in ('config', 'configure'):
				setattr(self, meth, getattr(master, meth))

	@staticmethod
	def _autoscroll(sbar):
		'''Hide and show scrollbar as needed.'''
		def wrapped(first, last):
			first, last = float(first), float(last)
			if first <= 0 and last >= 1:
				sbar.grid_remove()
			else:
				sbar.grid()
			sbar.set(first, last)
		return wrapped

	def __str__(self):
		return str(self.master)

def _create_container(func):
	'''Creates a tk Frame with a given master, and use this new frame to
	place the scrollbars and the widget.'''
	def wrapped(cls, master, **kw):
		container = tk.Frame(master)
		container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
		container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
		return func(cls, container, **kw)
	return wrapped

class ScrolledText(AutoScroll, tk.Text):
	'''A standard Tkinter Text widget with scrollbars that will
	automatically show/hide as needed.'''
	@_create_container
	def __init__(self, master, **kw):
		tk.Text.__init__(self, master, **kw)
		AutoScroll.__init__(self, master)

# class ScrolledListBox(AutoScroll, ThemedListbox):
# 	@_create_container
# 	def __init__(self, master, **kw):
# 		ThemedListbox.__init__(self, master, **kw,)
# 		AutoScroll.__init__(self, master)

def _bound_to_mousewheel(event, widget):
	child = widget.winfo_children()[0]
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
	else:
		child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
		child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
		child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
	if platform.system() == 'Windows' or platform.system() == 'Darwin':
		widget.unbind_all('<MouseWheel>')
		widget.unbind_all('<Shift-MouseWheel>')
	else:
		widget.unbind_all('<Button-4>')
		widget.unbind_all('<Button-5>')
		widget.unbind_all('<Shift-Button-4>')
		widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
	if platform.system() == 'Windows':
		widget.yview_scroll(-1*int(event.delta/120),'units')
	elif platform.system() == 'Darwin':
		widget.yview_scroll(-1*int(event.delta),'units')
	else:
		if event.num == 4:
			widget.yview_scroll(-1, 'units')
		elif event.num == 5:
			widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
	if platform.system() == 'Windows':
		widget.xview_scroll(-1*int(event.delta/120), 'units')
	elif platform.system() == 'Darwin':
		widget.xview_scroll(-1*int(event.delta), 'units')
	else:
		if event.num == 4:
			widget.xview_scroll(-1, 'units')
		elif event.num == 5:
			widget.xview_scroll(1, 'units')


#User Entry Boxes:
class Placeholder_State(object):
	 __slots__ = 'normal_color', 'normal_font', 'placeholder_text', 'placeholder_color', 'placeholder_font', 'contains_placeholder'

def add_placeholder_to(entry, placeholder, color="grey", font=None):
	normal_color = entry.cget("fg")
	normal_font = entry.cget("font")

	if font is None:
		font = normal_font

	state = Placeholder_State()
	state.normal_color=normal_color
	state.normal_font=normal_font
	state.placeholder_color=color
	state.placeholder_font=font
	state.placeholder_text = placeholder
	state.contains_placeholder=True

	def on_focusin(event, entry=entry, state=state):
		if state.contains_placeholder:
			entry.delete(0, "end")
			entry.config(fg = state.normal_color, font=state.normal_font)
		
			state.contains_placeholder = False

	def on_focusout(event, entry=entry, state=state):
		if entry.get() == '':
			entry.insert(0, state.placeholder_text)
			entry.config(fg = state.placeholder_color, font=state.placeholder_font)
			
			state.contains_placeholder = True

	entry.insert(0, placeholder)
	entry.config(fg = color, font=font)

	entry.bind('<FocusIn>', on_focusin, add="+")
	entry.bind('<FocusOut>', on_focusout, add="+")
	
	entry.placeholder_state = state

	return state

	
#Search box, use enter to exec bound callback
class SearchBox(tk.Frame):
	def __init__(self, master, entry_width=30, 
		entry_font=mediumboldtext, 
		entry_background=w, 
		entry_foreground=b,
		placeholder="Search", 
		placeholder_font=mediumboldtext, 
		placeholder_color=lg,
		button_text="Search",
		command=None,
		command_on_keystroke = True,
		):

		tk.Frame.__init__(self, master, borderwidth=0, highlightthickness=0,background=entry_background)

		self._command = command

		self.entry = tk.Entry(self, width=entry_width, background=entry_background, highlightcolor=b, highlightthickness=0, foreground = entry_foreground,borderwidth=2)
		self.entry.place(x=+offset,y=0,relwidth=1,relheight=1,width=-offset)
		
		if entry_font:
			self.entry.configure(font=entry_font)

		if placeholder:
			add_placeholder_to(self.entry, placeholder, color=placeholder_color, font=placeholder_font)

		if command_on_keystroke:
			self.entry.bind("<KeyRelease>", self._on_execute_command)

		self.entry.bind("<Escape>", lambda event: self.entry.nametowidget(".").focus())
		self.entry.bind("<Return>", self._on_execute_command)

	def get_text(self):
		entry = self.entry
		if hasattr(entry, "placeholder_state"):
			if entry.placeholder_state.contains_placeholder:
				return ""
		return entry.get()
		
	def set_text(self, text):
		entry = self.entry
		if hasattr(entry, "placeholder_state"):
			entry.placeholder_state.contains_placeholder = False

		entry.delete(0, END)
		entry.insert(0, text)
		
	def clear(self):
		self.entry_var.set("")
		
	def focus(self):
		self.entry.focus()

	def _on_execute_command(self, event):
		text = self.get_text()
		if self._command:
			self._command(text)