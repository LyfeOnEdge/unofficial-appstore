#Some basic scripts for installing appstore zips given the package name
#Copyright LyfeOnEdge 2019
#Licensed under GPL3
import sys, os, shutil, json
from zipfile import ZipFile
from .appstore import check_if_get_init, init_get, create_store_entry
from .appstore_web import getPackage

#Standard path to find the appstore at
PACKAGES_DIR = "switch/appstore/.get/packages"
#Name of package info file
PACKAGE_INFO = "info.json"
#Name of pagkade manifest file
PACKAGE_MANIFEST = "manifest.install"

#python object to hold appstore repo
class appstore_handler(object):
    def __init__(self):
        self.base_install_path = None

    def warn_path_not_set(self):
        print("Warning: appstore path not set, not continuing with install")

    #Set this to a root of an sd card or in a dir to test
    def set_path(self, path):
        self.base_install_path = path
        print("Set package path to %s" % path)

    def check_path(self):
        return self.base_install_path

    def install_package(self, repo):
        if not self.check_path(): return self.warn_path_not_set()
        if not repo:
            print("No repo data passed to appstore handler, not continuing with install")
        if not check_if_get_init(self.base_install_path):
            print("Appstore get folder not initiated, not continuing with install")

        package = repo["name"]
        #Append base directory to packages directory
        packagesdir = os.path.join(self.base_install_path, PACKAGES_DIR)
        if not os.path.isdir(packagesdir):
            os.makedirs(packagesdir)
        #Append package folder to packages directory
        packagedir = os.path.join(packagesdir, package)
        if not os.path.isdir(packagedir):
            os.mkdir(packagedir)

        #Download the package from the switchbru site
        appstore_zip = getPackage(package)
        if not appstore_zip:
            print("Failed to download zip for package {}".format(package))
            return

        with ZipFile(appstore_zip) as zipObj:
            #Extract everything but the manifest and the info file
            for filename in zipObj.namelist():
                if not ("manifest.install" in filename or "info.json" in filename):
                    zipObj.extract(filename, path = self.base_install_path)
            #Extract manifest
            zipObj.extract(PACKAGE_MANIFEST, path = packagedir)
            #Extract info file
            zipObj.extract(PACKAGE_INFO, path = packagedir)