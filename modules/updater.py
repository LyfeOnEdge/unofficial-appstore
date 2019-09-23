# This script grabs the latest release of a repo from github
import os, sys, json, shutil, io
from zipfile import ZipFile
import urllib.request
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

UPDATE_NAME = "unofficial_appstore"
asset_pattern = [["unofficial-appstore"], ".zip"]
UPDATEURL = "https://api.github.com/repos/LyfeOnEdge/unofficial-appstore/releases"

print("Lyfe's github update grabber, using python {}.{}".format(sys.version_info[0],sys.version_info[1]))

def download_object(remote_name, filename):
    r = urllib.request.urlopen(remote_name)
    if r.getcode() == 200:
        return r.read()

def openJson(file):
    with open(file, encoding="utf-8") as f:
        return json.load(f)

def get_members(zip):
    parts = []
    # get all the path prefixes
    for name in zip.namelist():
        # only check files (not directories)
        if not name.endswith('/'):
            # keep list of path elements (minus filename)
            parts.append(name.split('/')[:-1])
    # now find the common path prefix (if any)
    prefix = os.path.commonprefix(parts)
    if prefix:
        # re-join the path elements
        prefix = '/'.join(prefix) + '/'
    # get the length of the common prefix
    offset = len(prefix)
    # now re-set the filenames
    for zipinfo in zip.infolist():
        name = zipinfo.filename
        # only check files (not directories)
        if len(name) > offset:
            # remove the common prefix
            zipinfo.filename = name[offset:]
            yield zipinfo

#Takes a zip file in a bytream and extracts it
def handleZIP(file, extract_dir):
    print("Extracting...")
    with ZipFile(io.BytesIO(file), 'r') as zipObj:
        zipObj.extractall(extract_dir, get_members(zipObj))
        print("Extracted files - {}".format(zipObj.namelist()))

def findasset(pattern, assets):
    if not pattern:
        print("No pattern specified")
        return

    if not assets:
        print("no repo json specified")
        return

    downloadlink = None

    for asset in assets:
        asseturl = asset["browser_download_url"]
        assetname = asseturl.rsplit("/",1)[1].lower()
        assetwithoutfiletype = assetname.split(".")[0]
        for firstpartpattern in pattern[0]:
            if firstpartpattern.lower() in assetwithoutfiletype.lower():
                if assetname.endswith(pattern[1].lower()):
                    print("found asset: {}".format(assetname))
                    downloadlink = asseturl
                    asset = assetname
                    break
        return { 
            "link" : downloadlink,
            "asset" : asset
        }

def update():
    #Download update json from github
    update_file = download_object(UPDATEURL, "{}.json".format(UPDATE_NAME))
    if not update_file: sys.exit("Failed to download github api json")

    update_data = json.loads(update_file)[0]
    if not update_data: sys.exit("No update data in github api json")

    #Find the asset in the assets
    assets = update_data["assets"]

    asset_info = findasset(asset_pattern, assets)

    if not asset_info: sys.exit("Failed to find download link in github api json")
    print(asset_info)

    print("Downloading {} version {}".format(UPDATE_NAME, update_data["tag_name"]))

    update_zip = download_object(asset_info["link"], asset_info["asset"])

    #Extract wherever it is being run from
    extract_dir = os.path.join(sys.path[0])
    Extract to root
    handleZIP(update_zip, extract_dir)

    sys.exit("Update complete!")

def check_for_update(current_version):
    #Download update json from github
    update_file = download_object(UPDATEURL, "{}.json".format(UPDATE_NAME))
    if not update_file: sys.exit("Failed to download github api json")

    update_data = json.loads(update_file)[0]
    if not update_data: sys.exit("No update data in github api json")

    latest_version = update_data["tag_name"]

    if float(latest_version) > float(current_version):
        return True

if __name__ == "__main__":
    update()