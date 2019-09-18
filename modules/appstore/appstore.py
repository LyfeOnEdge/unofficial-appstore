#Some basic scripts for installing appstore zips given the package name
#Copyright LyfeOnEdge 2019
#Licensed under GPL3
import sys, os, shutil, json
from zipfile import ZipFile
from .appstore_web import getPackage

#Standard path to find the appstore at
PACKAGES_DIR = "switch/appstore/.get/packages"
#Name of package info file
PACKAGE_INFO = "info.json"
#Name of pagkade manifest file
PACKAGE_MANIFEST = "manifest.install"

#python object to hold appstore entrys data
class appstore_handler(object):
    def __init__(self):
        self.base_install_path = None

    #Check if the appstore packages folder has been inited
    def check_if_get_init(self,path):
        if not path: return
        #Append package name to packages directory
        packagesdir = os.path.join(path, PACKAGES_DIR)
        try:
            return os.path.isdir(packagesdir)
        except:
            pass

    def init_get(self, path):
        if not path: return
        if not check_if_get_init(path):
            packagesdir = os.path.join(path, PACKAGES_DIR)
            os.mkdir(packagesdir)
        else:
            print("Appstore packages dir already inited")
            return

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
        if not self.check_if_get_init(self.base_install_path):
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

            print("Extracted: {}".format(json.dumps(zipObj.namelist(), indent = 4)))

        print("Installed {} version {}".format(repo["title"], repo["version"]))


    #THIS DOES NOT UNINSTALL THE CONTENT
    #Removes a package entry by deleting the package 
    #folder containing the manifest and info.json
    def remove_store_entry(self, package):
        if not self.check_path(): return self.warn_path_not_set()
        #Append package name to packages directory
        pacdir = os.path.join(PACKAGES_DIR, package)
        #Append base directory to packages directory
        packagedir = os.path.join(self.base_install_path, pacdir)
        try:
            shutil.rmtree(packagedir, ignore_errors=True)
            print("Removed appstore entry")
        except Exception as e:
            print("Error removing store entry for {} - {}".format(package, e))


    #Get the contents of a package's info file as a dict
    def get_package_entry(self, package):
        if not self.check_path(): return self.warn_path_not_set()
        #Append package name to packages directory
        pacdir = os.path.join(PACKAGES_DIR, package)
        #Append base directory to packages directory
        packagedir = os.path.join(self.base_install_path, pacdir)
        #Append package loc to info file name
        pkg = os.path.join(packagedir, PACKAGE_INFO)

        try:
            with open(pkg, encoding="utf-8") as infojson:
                return json.load(infojson)
        except FileNotFoundError:
            pass
        except:
            print("Failed to open repo data for {}".format(package))

    #Get a package's json file value, returns none if it fails
    def get_package_value(self, package, value):
        if not self.check_path(): return self.warn_path_not_set()
        #Get the package json data
        package_info = get_package_entry(self.base_install_path, package)
        #If data was retrieved, return the value
        if package_info:
            # print(package_info[value])
            return package_info[value]

    #Get the installed version of a package, return "not installed" if failed
    def get_package_version(self, package):
        #Get the package json data
        ver = get_package_value(self.base_install_path, package, "version")
        return ver or "not installed"

    #Returns a package's manifest as a list
    def get_package_manifest(self, package):
        if not self.check_path(): return self.warn_path_not_set()
        #Append package name to packages directory
        pacdir = os.path.join(PACKAGES_DIR, package)
        #Append base directory to packages directory
        packagedir = os.path.join(self.base_install_path, pacdir)
        #Append package loc to manifest file name
        manifestfile = os.path.join(packagedir, PACKAGE_MANIFEST)
        print(manifestfile)
        if not os.path.isfile(manifestfile):
            print("couldn't find manifest")
            return

        mf = []
        #open the manifest, append the current base path to each line
        with open(manifestfile, "r") as maf:
            for fileline in maf:
                fl = fileline.replace(MANIFEST_PREFIX, "")
                fl = fl.strip().replace("\n", "")
                mf.append(os.path.join(self.base_install_path,fl))

        return mf