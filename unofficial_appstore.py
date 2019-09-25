version = "1.5"
print("Unofficial appstore version %s" % version)

import os, sys, platform, json, threading
print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6: #Trying to import tkinter in the new syntax after python 2 causes a crash
	sys.exit("Python 3.6 or greater is required to run this program.")

try:
	import tkinter as tk
except:
	input("Cannot start: Tkinter not installed, try `pip install Pillow` consult the readme for more information.")
	sys.exit()

try:
	import PIL #Import pillow library
except:
	input("Cannot start: Pillow module not installed, try `pip install Pillow` or consult the readme for more information.")
	sys.exit()

print("Using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))

#Import local modules
from modules.widgets import frameManager
from modules.appstore import getPackageIcon, parser, appstore_handler
from modules.webhandler import getJson
from modules.locations import appstore_repo_url
from modules.async_threader import asyncThreader
from modules.updater import check_for_update
from pages import pagelist
from timeit import default_timer as timer

#Async threader tool for getting downloads and other functions asyncronously
threader = asyncThreader()
#Download the appstore json, uses etagging to check if it needs an update to minimize bandwidth
print("Getting updated appstore repo file")
store_json = getJson("appstore_repo",appstore_repo_url)
#Parse the json into categories
repo_parser = parser()
repo_parser.blacklist_categories(["loader", "theme"])
threader.do_async(repo_parser.load, [store_json])
#Shared tool for installing and managing hbas apps via the switchbru site on the sd card
store_handler = appstore_handler()

geometry = {
	"width" : 780,
	"height" : 575,
}

def startGUI(update_status):
	pre_load_icons()
	gui = frameManager(pagelist,geometry,store_handler,repo_parser,threader,update_status)
	gui.title("unofficial appstore %s" % version)

	#Set icon
	favicon = None
	if platform.system() == 'Windows':
		print("Windows detected, setting icon")
	elif platform.system() == "Linux":
		print("Linux detected, setting icon")
		favicon = os.path.join("assets", 'favicon.xbm')
	elif platform.system() == "Darwin":
		print("Mac detected, not setting icon as it is not supported")

	if favicon:
		if os.path.exists(favicon):
			#Set icon
			gui.iconbitmap(favicon)
		else:
			print("Icon file not found, not setting favicon")

	gui.mainloop()

#Helps by pre-downloading the various icons
def pre_load_icons():
	threads = [] 
	for repo in repo_parser.all:
		threads.append(threading.Thread(target=getPackageIcon, args=[repo["name"]]))

	for t in threads:
		t.start()

if __name__ == '__main__':
	update_status = check_for_update(version)
	startGUI(update_status)