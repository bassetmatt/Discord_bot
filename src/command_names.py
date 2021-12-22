import json
import os

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

# Pause
PAUSE_COMMAND = data["pause command"]
PAUSE_ALIASES = data["pause aliases"]
PAUSE_MESSAGE = data["pause message"]
PAUSE_EMOJI = data["pause emoji"]

print(PAUSE_ALIASES)
