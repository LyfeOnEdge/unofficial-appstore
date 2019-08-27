import os, sys
#Folder and file definitions for easy access
appstore_repo_url = "https://www.switchbru.com/appstore/repo.json"


wd = sys.path[0]

folders_to_init = []
#Folder to hold cache folders
cachefolder =  os.path.join(wd, "cache")
folders_to_init.append(cachefolder)
#Folder to cache repo jsons
jsoncachefolder = os.path.join(cachefolder,"json")
folders_to_init.append(jsoncachefolder)
#Folder to cache author images
imagecachefolder = os.path.join(cachefolder,"images")
folders_to_init.append(imagecachefolder)

for folder in folders_to_init:
	if not os.path.isdir(folder):
		print("initializing folder {}".format(folder))
		os.mkdir(folder)

etagfile = os.path.join(jsoncachefolder, "etags.json")

notfoundimage = os.path.join(os.path.join(wd, "assets"), "notfound.png")
backimage = os.path.join(os.path.join(wd, "assets"), "return.png")