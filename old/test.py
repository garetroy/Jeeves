import unittest
import urllib.request
import riotapi
import json

def getJsonData():
    with open('info.json', 'r') as jsonf:
        return json.load(jsonf)

jsondata  = getJsonData()
nonexcess = True

class TestRiotApi(unittest.TestCase):

    def setUp(self):
        self.api_key = jsondata['riot']    
        self.riotapi = riotapi.Riot(self.api_key)
        self.lolvers = "8.1.1"
    
    @unittest.skipIf(nonexcess,"Reduce Excessive requests")
    def test_keyString(self):
        self.assertEqual(self.riotapi.keyString, '?api_key={}'\
                    .format(self.api_key)) 

    @unittest.skipIf(nonexcess,"Reduce Excessive requests")
    def test_version(self):
        self.assertEqual(self.riotapi.version, self.lolvers)

    def test_summoner(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.riotapi.summoner("thiswontejfowejfoqiwjefq")
        self.assertEqual(cm.exception.code,404)
        self.assertIsNot(self.riotapi.summoner("Prolixed"),{})

    def test_summonerLevel(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.riotapi.summonerLevel("thiswontejfowejfoqiwjefq")
        self.assertEqual(cm.exception.code,404)
        self.assertIsNot(self.riotapi.summonerLevel("Prolixed"),{})

    def test_summonerMatches(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.riotapi.summonerMatches("thiswontejfowejfoqiwjefq")
        self.assertEqual(cm.exception.code,404)
        self.assertIsNot(self.riotapi.summonerMatches("prolixed"),{})

    def test_recentMatch(self):
        with self.assertRaises(urllib.error.HTTPError) as cm:
            self.riotapi.recentMatch("thiswontejfowejfoqiwjefq")
        self.assertEqual(cm.exception.code,404)
        self.assertIsNot(self.riotapi.recentMatch("prolixed"),{})


if __name__ == '__main__':
    unittest.main()
