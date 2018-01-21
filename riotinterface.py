"""
    Filename: riotinterface.py
    Author:   Garett Roberts
    Repo:     https://github.com/garetroy/Jeeves
    
    This is the api for processing riot queries from cassiopeia and
    making them into desired results for jeeves
"""

import cassiopeia as cass
import json

class RiotInterface:
    def __init__(self,api_key,region="NA"):
        cass.set_riot_api_key(api_key)
        cass.set_default_region(region)

    @property
    def version(self):
        return cass.get_version()

    def summonerLevel(self,name):
        return cass.Summoner(name=name).level

    def mapString(self,_id):
        return self.maps[str(_id)]['name']

    def gameType(self,_id):
        return self.qtype[str(_id)]['string']
    
    def getRecentMatch(self,name):
        return cass.get_match_history(summoner=name,end_index=1)[0]

    def checkLive(self,match):
        #print(match.duration)
        #print(match.red_team.win)
        return True

    def returnLiveString(self,name):
        recentmatch = self.getRecentMatch(name) 
        if not self.checkLive(name):
            return "Sorry, {} does not have a live game currently.".format(name)

        blue     = recentmatch.blue_team
        red      = recentmatch.red_team
        print(recentmatch.mode.name)

        tpattern = "\n{:^50}\n"
        string = ""
        for p in blue.participants:
            print(p.summoner.name)
    
if __name__ == '__main__':
    r = RiotInterface(key)
    print(r.version)
    print(r.summonerLevel("prolixed"))
    print(r.getRecentMatch("prolixed"))
    r.returnLiveString('prolixed')
