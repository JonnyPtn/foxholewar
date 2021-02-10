import datetime
import enum
import json
import requests
import re

from dataclasses import dataclass, field

BASE_URL = "https://war-service-live.foxholeservices.com/api/"

# Because the user facing names don't map cleanly to the raw ones we need a mapping table like this
rawMapNameToPretty = {
    "GreatMarchHex": "Great March",
    "MarbanHollow": "Marban Hollow",
    "ViperPitHex": "Viper Pit",
    "ShackledChasmHex": "Shackled Chasm",
    "LinnMercyHex": "The Linn of Mercy",
    "DeadLandsHex": "Deadlands",
    "HeartlandsHex": "The Heartlands",
    "ReachingTrailHex": "Reaching Trail",
    "UmbralWildwoodHex": "Umbral Wildwood",
    "CallahansPassageHex": "Callahan's Passage",
    "DrownedValeHex": "The Drowned Vale",
    "MooringCountyHex": "The Moors",
    "LochMorHex": "Loch Mor",
    "StonecradleHex": "Stonecradle",
    "FishermansRowHex": "Fishermans Row",
    "WestgateHex": "Westgate",
    "OarbreakerHex": "Oarbreaker Isles",
    "FarranacCoastHex": "Farranac Coast"
}

prettyMapNameToRaw = dict((reversed(item)
                           for item in rawMapNameToPretty.items()))


def isValidMapName(map):
    return map in rawMapNameToPretty or map in rawMapNameToPretty.values()


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


@dataclass
class War:
    """The information for a war"""
    warId: int
    warNumber: int
    winner: Team
    conquestStartTime: datetime
    conquestEndTime: datetime
    resistanceStartTime: datetime
    requiredVictoryTowns: datetime


@dataclass
class Map:
    """A (hex) map"""
    rawName: str
    prettyName: str
    regionId: int = None
    scorchedVictoryTowns: int = None
    mapItems: list = field(default_factory=list)
    mapTextItems: list = field(default_factory=list)


@dataclass
class MapItem:
    """An item on the map"""
    teamId: Team
    iconType: int
    x: int
    y: int
    flags: int


@dataclass
class MapTextItem:
    """A text item on the map"""
    text: str
    x: int
    y: int
    mapMarkerType: int


@dataclass
class Report:
    """A war report for a map"""
    totalEnlistments: int
    colonialCasualties: int
    wardenCasualties: int
    dayOfWar: int
    version: int


class Client:

    def __init__(self):
        self.session = requests.Session()

    def fetchJSON(self, endpoint: str) -> dict:
        """Request some JSON data from the given endpoint"""
        requestUrl = BASE_URL + endpoint
        response = self.session.get(requestUrl)
        return json.loads(response.text)

    def fetchCurrentWar(self) -> War:
        """Get the data for the current war"""
        jsonData = self.fetchJSON("worldconquest/war")

        return War(**jsonData)

    def fetchReport(self, map: str) -> Report:
        """Get a war report for the given map name"""
        reportData = self.fetchJSON("worldconquest/warReport/" + map.rawName)

        return Report(**reportData)

    def fetchMapList(self):
        """Get the list of maps"""
        mapData = self.fetchJSON("worldconquest/maps")

        maps = []
        for rawMapName in mapData:
            map = Map(rawName=rawMapName,
                      prettyName=rawMapNameToPretty[rawMapName])

            # We get the static and dynamic data too
            staticMapData = self.fetchJSON(
                "worldconquest/maps/" + map.rawName + "/static")
            dynamicMapData = self.fetchJSON(
                "worldconquest/maps/" + map.rawName + "/dynamic/public")

            map.scorchedVictoryTowns = staticMapData["scorchedVictoryTowns"]
            map.regionId = staticMapData["regionId"]

            # It seems as though we only get text items from static data and regular items from dynamic data?
            for item in staticMapData["mapTextItems"]:
                map.mapTextItems.append(MapTextItem(**item))

            for item in dynamicMapData["mapItems"]:
                map.mapItems.append(MapItem(**item))

            maps.append(map)

        return maps
