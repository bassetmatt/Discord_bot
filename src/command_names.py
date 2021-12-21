import json

#Reads the file
with open("config/settings.json") as f:
  data = json.load(f)


# Pause
PAUSE_COMMAND = data["pause command"]
PAUSE_ALIASES = data["pause aliases"]
PAUSE_MESSAGE = data["pause message"]
PAUSE_EMOJI = data["pause emoji"]
