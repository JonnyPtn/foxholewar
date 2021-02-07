import datetime
import enum
import json
import requests
import re

BaseURL = "https://war-service-live.foxholeservices.com/api/"

class Team(enum.Enum):
	"""The teams"""
	NONE = 0
	COLONIAL = 1
	WARDENS = 2
	
	def __str__(self):
		return self.name

class MapMarkerType(enum.Enum):
	"""Types of map marker"""
	MAJOR = 0
	MINOR = 0


class War:
	"""The information for a war"""
	warId = None
	warNumber = None
	winner = Team.NONE
	conquestStartTime = None
	conquestEndTime = None
	resistanceStartTime = None
	requiredVictoryTowns = None

class Map:
	"""A (hex) map"""
	rawName = None
	prettyName = None
	regionId = None
	scorchedVictoryTowns = None
	mapItems = []
	mapTextItems = []

	def getReport( self ):
		"""
		Returns
		-------
		Report
		    A report on the current status of this map
		"""
		reportData = getData("worldconquest/warReport/" + self.rawName)
		report = Report()
		report.totalEnlistments = reportData["totalEnlistments"]
		report.colonialCasualties = reportData["colonialCasualties"]
		report.wardenCasualties = reportData["wardenCasualties"]
		report.dayOfWar = reportData["dayOfWar"]
		return report

class MapItem:
	"""An item on the map"""
	teamId = Team.NONE
	iconType = None
	x = None
	y = None
	flags = None

class MapTextItem:
	"""A text item on the map"""
	text = None
	x = None
	y = None
	mapMarkerType = None

class Report:
	"""A war report for a map"""
	map = None
	totalEnlistments = None
	colonialCasualties = None
	wardenCasualties = None
	dayOfWar = None


def getData(endpoint):
	"""
	Parameters
	----------
	endpoint : str
	    The endpoint to request data from
	
	Returns
	-------
	dict
	    The loaded json data from the endpoint
	"""
	requestUrl = BaseURL + endpoint
	response = requests.get(requestUrl)
	return json.loads(response.text)

def getCurrentWar():
	"""
	Returns
	-------
	War
	    The War object for the war currently takin place
	"""
	jsonData = getData("worldconquest/war")

	war = War()
	war.warId = jsonData["warId"],
	war.warNumber = jsonData["warNumber"]
	war.winner = Team[jsonData["winner"]]
	war.conquestStartTime = jsonData["conquestStartTime"]
	war.conquestEndTime = jsonData["conquestEndTime"]
	war.resistanceStartTime = jsonData["resistanceStartTime"]
	war.requiredVictoryTowns = jsonData["requiredVictoryTowns"]
	return war

def getMapList():
	"""
	Returns
	-------
	list
	    A list of all the maps
	"""
	mapData = getData("worldconquest/maps")

	maps = []
	for rawMapName in mapData:
		map = Map()
		map.rawName = rawMapName

		# For the pretty name we strip "Hex" from the end and add spaces
		map.prettyName = re.sub(r"(\w)([A-Z])", r"\1 \2", rawMapName[:-3])

		# We get the static and dynamic data too
		staticMapData = getData("worldconquest/maps/" + map.rawName + "/static")
		dynamicMapData = getData("worldconquest/maps/" + map.rawName + "/dynamic/public")

		map.scorchedVictoryTowns = staticMapData["scorchedVictoryTowns"]
		map.regionId = staticMapData["regionId"]
		
		# It seems as though we only get text items from static data and regular items from dynamic data?
		for item in staticMapData["mapTextItems"]:
			textItem = MapTextItem()
			textItem.text = item["text"]
			textItem.x = item["x"]
			textItem.y = item["y"]
			textItem.mapMarkerType = item["mapMarkerType"]
			map.mapTextItems.append(textItem)
			
		for item in dynamicMapData["mapItems"]:
			mapItem = MapItem()
			mapItem.teamId = item["teamId"]
			mapItem.iconType = item["iconType"]
			mapItem.x = item["x"]
			mapItem.y = item["y"]
			mapItem.flags = item["flags"]
			map.mapItems.append(mapItem)

		maps.append(map)

	return maps


