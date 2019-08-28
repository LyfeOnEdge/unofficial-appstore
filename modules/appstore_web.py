#Some basic scripts for grabbing icon and screenshot for packages using the appstore site.
#Copyright LyfeOnEdge 2019
#Licensed under GPL3
import sys, os

import urllib.request 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

APPSTORE_URL = "https://www.switchbru.com/appstore/{}"
IMAGE_BASE_URL = APPSTORE_URL.format("packages/{}/{}")
APPSTORE_PACKAGE_URL = "https://www.switchbru.com/appstore/zips/{}.zip"

DOWNLOADSFOLDER = "downloads"

CACHEFOLDER = "cache"
ICON  = "icon.png"
SCREEN = "screen.png"

SCREENBUFFER = {}
ICONBUFFER = {}


###Image handling
def download(url,file):
    try:
        urllib.request.urlretrieve(url,file)
        return file
    except Exception as e:
        print("failed to download file {} from url {}".format(file, url)) 
        return None

def getImage(package, image_type):
    path = os.path.join(os.path.join(sys.path[0], CACHEFOLDER), package.replace(":",""))
    if not os.path.isdir(path):
        os.mkdir(path)

    image_file = os.path.join(path, image_type)

    if os.path.isfile(image_file):
        return(image_file)
    else:
        return download(IMAGE_BASE_URL.format(package, image_type), image_file)

def getPackageIcon(package):
    if package in ICONBUFFER.keys():
        return ICONBUFFER[package]
    icon = getImage(package, ICON)
    ICONBUFFER.update({package : icon})
    return icon

def getScreenImage(package):
    if package in SCREENBUFFER.keys():
        return SCREENBUFFER[package]
    screen = getImage(package, SCREEN)
    SCREENBUFFER.update({package : screen})
    return screen

#Downloads the current zip of a package
def getPackage(package):
    try:
        packageURL = APPSTORE_PACKAGE_URL.format(package)
        packagefile = os.path.join(os.path.join(sys.path[0], DOWNLOADSFOLDER), "{}.zip".format(package))
        return download(packageURL, packagefile)
    except Exception as e:
        print("Error getting package zip {}".format(e))

def test(package):
    getScreenImage(package)
    getPackageIcon(package)
    getPackage(package)

if __name__ == "__main__":
    #Test with the appstore
    test("appstore")