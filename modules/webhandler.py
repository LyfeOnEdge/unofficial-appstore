import os, sys, shutil
import modules.locations as locations
import modules.etags as etags

#web handling
import urllib.request 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

#Variable to map previously downloaded jsons to minimize repeated downloads
filedict = {}

#opens a url in a new tab
def opentab(url):
	import webbrowser
	webbrowser.open_new_tab(url)

#Download a file at a url, returns file path
def download(fileURL):
	try:
		downloadedfile, headers = urllib.request.urlretrieve(fileURL)
		print(headers)
		filename = headers["Content-Disposition"].split("filename=",1)[1]
		downloadlocation = os.path.join(locations.downloadsfolder,filename)
		shutil.move(downloadedfile, downloadlocation)
		print("downloaded {} from url {}".format(filename, fileURL))
		return filename
	except Exception as e: 
		print(e)
		return None

def getUpdatedSoftwareLinks(dicttopopulate):
	global filedict
	if not os.path.isdir(locations.jsoncachefolder):
		os.mkdir(locations.jsoncachefolder)
	for softwarechunk in dicttopopulate:
		githubjsonlink = softwarechunk["githubapi"]
		softwarename = softwarechunk["software"]
		projectname = get_project_from_github_api_link(githubjsonlink)
		author = get_author_from_github_api_link(githubjsonlink)

		json_name = "{}_{}".format(projectname, author)

		try:
			file = filedict[json_name]
			#Exit reuse path if not yet downloaded
			if not file:
				raise HBUError('Not yet downloaded')
			softwarechunk["githubjson"] = file
			print("using already downloaded file for {}".format(json_name))
		#If not downloaded file yet
		except:
			jsonfile = os.path.join(locations.jsoncachefolder, "{}.json".format(json_name))

			#Download it, set the chunk's json file path to it, and update the filedict in case it's a shared file
			file = getJsonThread(githubjsonlink, jsonfile, softwarename)
			softwarechunk["githubjson"] = file
			filedict[json_name] = file

		#If project page was not pre-defined set it to the base github project link
		if softwarechunk["projectpage"] == None or softwarechunk["projectpage"] == "":
			softwarechunk["projectpage"] = parse_api_to_standard_github(githubjsonlink)

	dicttopopulate = sorted(dicttopopulate, key = lambda i: i["software"])
	return dicttopopulate

def getJson(softwarename, apiurl):
	try:
		jsonfile = os.path.join(locations.jsoncachefolder, softwarename + ".json")
		jfile = etags.accessETaggedFile(apiurl,jsonfile)
		return jfile
	except:
		print("failed to download json file for {}".format(softwarename))
		return None