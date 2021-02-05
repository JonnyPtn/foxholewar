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

class Map:
	"""A class representing a map (hex)"""
	rawName = None
	prettyName = None

class Report:
	map = Map()
	totalEnlistments = None
	colonialCasualties = None
	wardenCasualties = None
	dayOfWar = None


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
	mapData = getData("worldconquest/maps")

	maps = []
	for rawMapName in mapData:
		map = Map()
		map.rawName = rawMapName

		# For the pretty name we strip "Hex" from the end and add spaces
		map.prettyName = re.sub(r"(\w)([A-Z])", r"\1 \2", rawMapName[:-3])
		maps.append(map)
	return maps

def getReport( map ):
	reportData = getData("worldconquest/warReport/" + map.rawName)
	report = Report()
	report.totalEnlistments = reportData["totalEnlistments"]
	report.colonialCasualties = reportData["colonialCasualties"]
	report.wardenCasualties = reportData["wardenCasualties"]
	report.dayOfWar = reportData["dayOfWar"]
	return report



