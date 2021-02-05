import datetime
import enum
import json
import requests
import re

BaseURL = "https://war-service-live.foxholeservices.com/api/"

class Team(enum.Enum):
	NONE = 0
	COLONIAL = 1
	WARDENS = 2


class War:
	"""A class representing war details"""
	warId = None
	warNumber = None
	winner = None
	conquestStartTime = None
	conquestEndTime = None
	resistanceStartTime = None
	requiredVictoryTowns = None

def getData(endpoint):
	requestUrl = BaseURL + endpoint
	response = requests.get(requestUrl)
	return json.loads(response.text)

def getCurrentWar():
	jsonData = getData("worldconquest/war")

	war = War()
	war.warId = jsonData["warId"],
	war.warNumber = jsonData["warNumber"]
	war.winner = jsonData["winner"]
	war.conquestStartTime = jsonData["conquestStartTime"]
	war.conquestEndTime = jsonData["conquestEndTime"]
	war.resistanceStartTime = jsonData["resistanceStartTime"]
	war.requiredVictoryTowns = jsonData["requiredVictoryTowns"]
	return war

def getMapList():
	maps = getData("worldconquest/maps")

	# Each map name has a "Hex" suffix, so strip that, and add spaces where required
	maps[:] = [re.sub(r"(\w)([A-Z])", r"\1 \2", map[:-3]) for map in maps]
	return maps
