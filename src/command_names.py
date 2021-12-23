import json
import os

## Json file reading
SET_FILE  = "config/settings.json"
TEMP_FILE = "config/temp.json"
#Removes comments
with open(SET_FILE , "r+", encoding="utf8") as f0, \
	 open(TEMP_FILE, "w+", encoding="utf8") as f1 :
	text = f0.readlines()
	for line in text :
		if "//" not in line :
			f1.write(line)
 		
with open(TEMP_FILE,"r",encoding="utf8") as f1 :
	data = json.load(f1)
os.remove('config/temp.json')
	
# Command prefix
COMMAND_SYMBOL= data["command prefix"]
PLAYLIST = data["playlist"]
# Commands names
class CommandFields() :
	def __init__(self, name) :
		self.name  = data[name + " command"]
		self.alias = data[name + " aliases"]
		self.emoji = data[name +   " emoji"]
		self.msg   = data[name + " message"]
		self.args  = {"name" : self.name, "aliases" : self.alias}


JOIN    = CommandFields("join")
LEAVE   = CommandFields("leave")
VOLUME  = CommandFields("volume")
NOW     = CommandFields("now")
PAUSE   = CommandFields("pause")
RESUME  = CommandFields("resume")
SKIP    = CommandFields("skip")
QUEUE   = CommandFields("queue")
SHUFFLE = CommandFields("shuffle")
REMOVE  = CommandFields("remove")
LOOP    = CommandFields("loop")
PLAY    = CommandFields("play")
CLEAR   = CommandFields("clear")