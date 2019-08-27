version = "0.0"
print("Unofficial appstore version {}".format(version))

import os, sys, platform, json, threading
print("Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))
if sys.version_info[0] < 3 or sys.version_info[1] < 6: #Trying to import tkinter in the new syntax after python 2 causes a crash
	sys.exit("Python 3.6 or greater is required to run this program.")

import tkinter as tk
print("Using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))

from modules.framemanager import FrameManager
from modules.appstore_web import getPackageIcon
from modules.appstore_parser import parser
from modules.webhandler import getJson
from modules.locations import appstore_repo_url
import pages.appstorepage as appstorepage

#Download the appstore json, uses etagging to check if it needs an update to minimize bandwidth
store_json = getJson("appstore_repo",appstore_repo_url)
#Parse the json into categories
repo_parser = parser()
repo_parser.load(store_json)

pages = [appstorepage.appstorePage]

geometry = {
	"width" : 1080,
	"height" : 720,
}

def startGUI():
	gui = FrameManager(pages,geometry)
	get_repo_icons(gui)
	gui.title("unofficial appstore %s" % version)
	gui.mainloop()

#Helps with pre-loading a lot of images
def get_repo_icons(app):
	threads = [] 

	for repo in repo_parser.all:
		threads.append(threading.Thread(target=getPackageIcon, args=[repo["name"]]))

	for t in threads:
		t.start()

if __name__ == '__main__':
	startGUI()
	