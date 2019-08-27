#A basic python object for parsing the appstore json into lists per category
#Copyright LyfeOnEdge 2019
#Licensed under GPL3

import json
#python object to hold appstore repo
class parser(object):
    def __init__(self):
        self.all = []
        self.advanced = []
        self.concepts = []
        self.emus = []
        self.games = []
        self.loaders = []
        self.themes = []
        self.tools = []
        self.misc = []

        self.map = {
            "advanced" : self.advanced,
            "concept" : self.concepts,
            "emu" : self.emus,
            "game" : self.games,
            "loader" : self.loaders,
            "theme" : self.themes,
            "tool" : self.tools,
            "_misc" : self.misc,
            "misc" : self.misc,
        }

        self.list_list = [ self.all ]
        for key in self.map:
            self.list_list.append(self.map[key])

    def clear(self):
        for lis in self.list_list:
            lis = []

    #Loads appstore json as a large list of dicts
    def load(self, appstore_json):
        self.clear()
        try:
            with open(appstore_json, encoding="utf-8") as repojson:
                self.all = json.load(repojson)["packages"]
        except Exception as e:
            print("Exception loading appstore json %s" % e)
        self.sort()

    #sorts list into smaller chunks
    def sort(self):
        if self.all:
            for entry in self.all:
                try:
                    self.map[entry["category"]].append(entry)
                except:
                    print("Error sorting %s" % entry["name"])