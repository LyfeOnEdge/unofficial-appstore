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
        #Append package folder to packages directory
        packagedir = os.path.join(packagesdir, package)

        #Download the package from the switchbru site
        appstore_zip = getPackage(package)
        if not appstore_zip:
            print("Failed to download zip for package {}".format(package))

        package_data = self.handle_zip(appstore_zip)

        manifest_file = os.path.join(packagedir, PACKAGE_MANIFEST)

        info_file = os.path.join(packagedir, PACKAGE_INFO)

    def handle_zip(self, in_zip):
        if not self.check_path(): return self.warn_path_not_set()
        zip_contents = extract_zip_to_memory(in_zip)

        #Get manifest and info from zip dict, remove em
        manifest = zip_contents.pop("manifest.install")
        info = zip_contents.pop("info.json")

        for f in zip_contents.keys():
            out_file = os.path.join(self.base_install_path, f)
            with open(out_file, 'wb') as out_f:
                out_f.write(zip_contents[f])

        return {"manifest" : manifest, "info" : info}

def extract_zip_to_memory(in_zip):
    in_zip=ZipFile(in_zip)
    return {name: in_zip.read(name) for name in in_zip.namelist()}