import unittest

import foxholewar

class TestFoxholeWar(unittest.TestCase):

    def testWarInfo(self):
        war = foxholewar.getCurrentWar()
        self.assertTrue(war.warId)
        self.assertTrue(war.warNumber)
        self.assertTrue(war.winner)
        self.assertTrue(war.conquestStartTime)
        self.assertTrue(war.conquestEndTime or war.winner is foxholewar.Team.NONE)
        self.assertTrue(war.resistanceStartTime or not war.conquestEndTime)
        self.assertTrue(war.requiredVictoryTowns)

    def testMapList(self):
        mapList = foxholewar.getMapList()
        self.assertTrue(mapList)
        
        for map in mapList:
            self.assertTrue(map.rawName)
            self.assertTrue(map.prettyName)
            self.assertTrue(map.scorchedVictoryTowns is not None)
            self.assertTrue(map.regionId)

            for item in map.mapTextItems:
                self.assertTrue(item.text)
                self.assertTrue(item.x)
                self.assertTrue(item.y)
                self.assertTrue(item.mapMarkerType)

            for item in map.mapItems:
                self.assertTrue(item.teamId)
                self.assertTrue(item.iconType)
                self.assertTrue(item.x)
                self.assertTrue(item.y)
                self.assertTrue(item.flags)

    

if __name__ == '__main__':
    unittest.main()