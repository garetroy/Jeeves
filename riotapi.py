import urllib.request
import json

class Riot:
    def __init__(self,api_key):
        self.base_api_url   = "https://na1.api.riotgames.com"
        self.summoner_name  = "/lol/summoner/v3/summoners/by-name/"
        self.summoner_match = "/lol/match/v3/matchlists/by-account/"
        self.match_dets     = "/lol/match/v3/matches/"
        self.api_key        = api_key
        self.summonerht     = {}
        self.summonermht    = {}
        self.matchesht      = {}

    @property
    def keyString(self):
        return "?api_key=" + self.api_key 

    @property
    def version(self):
        url  = "https://na1.api.riotgames.com/lol/static-data/v3/versions"
        url += self.keyString
        return self.requestJson(url)[0]
    
    def summoner(self,name):
        if(name in self.summonerht):
            return self.summonerht[name]

        string  = self.base_api_url + self.summoner_name + name + "/"
        string += self.keyString

        self.summonerht[name] = self.requestJson(string)
        return self.summonerht[name]
    
    def summonerLevel(self,name):
        return self.summoner(name)['summonerLevel']

    def summonerMatches(self,name,forceupdate=False):
        if(name in self.summonermht and not forceupdate):
            return self.summonermht[name]

        sumid   = self.summoner(name)['accountId']
        string  = self.base_api_url + self.summoner_match + str(sumid)
        string += self.keyString

        self.summonermht[name] = self.requestJson(string)
        return self.summonermht[name]

    def recentMatch(self,name,forceupdate=False):
        matchid   = str(self.summonerMatches(name)['matches'][0]['gameId'])
        if(matchid in self.matchesht and not forceUpdate):
            return self.matchesht[matchid]
        
        string  = self.base_api_url + self.match_dets + str(matchid) 
        string += self.keyString

        self.matchesht[matchid] = self.requestJson(string)
        return self.matchesht[matchid]

    def requestJson(self,url):
        with urllib.request.urlopen(url) as f:
            data = json.loads(f.read().decode())
            return data
