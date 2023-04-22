from NewsParser import *

myParser = NewsParser()
myParser.setSettings("settings/formatSettings.conf", "settings/parserSettings.conf")
myParser.parse()