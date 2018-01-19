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
        self.champions      = self.loadChampions()

    @property
    def keyString(self):
        return "?api_key=" + self.api_key 

    @property
    def version(self):
        url  = "https://na1.api.riotgames.com/lol/static-data/v3/versions"
        url += self.keyString
        try:
            return self.requestJson(url)[0]
        except:
            print("Could not get version")
            raise

    def loadChampions(self):
        with open('champions.json', 'r') as jsonf:
            return json.load(jsonf)
        
    def getChampionByName(self,name):
        return self.champions[name]

    def getChampionById(self,_id):
        for i in self.champions:
            if(self.champions[i]['id'] == _id):
                return self.champions[i]
    
    def summoner(self,name):
        if(name in self.summonerht):
            return self.summonerht[name]

        string  = self.base_api_url + self.summoner_name + name + "/"
        string += self.keyString

        try:
            self.summonerht[name] = self.requestJson(string)
        except Exception as e:
            print("Could not get summoner by name")
            raise e

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
        matchid   = str(self.summonerMatches(name,forceupdate)\
            ['matches'][0]['gameId'])

        if(matchid in self.matchesht and not forceupdate):
            return self.matchesht[matchid]
        
        string  = self.base_api_url + self.match_dets + str(matchid) 
        string += self.keyString

        self.matchesht[matchid] = self.requestJson(string) 
        return self.matchesht[matchid] 

    def getLiveMatch(self,name):
        #NEED CHECK HERE TO PREVENT EXCESSIVE REQUESTS
        match   = self.recentMatch(name,True)
        blueid  = match['teams'][0]['teamId']      
        redid   = match['teams'][1]['teamId']
        blue    = {}
        red     = {}
        matcht  = match['gameMode']

        for participant in match['participants']:
            if(participant['teamId'] == blueid):
                blue[participant['participantId']] = \
                    (self.getChampionById(participant['championId']) \
                    ['name'], participant['timeline']['role'])
            else:
                red[participant['participantId']] = \
                    (self.getChampionById(participant['championId']) \
                    ['name'], participant['timeline']['role'])
        
        for participant in match['participantIdentities']:
            pid = participant["participantId"] 
            if pid in blue:
                blue[participant['player']['summonerName']] = blue[pid]
                del blue[pid]
            elif pid in red:
                red[participant['player']['summonerName']] = red[pid]
                del red[pid]
            else:
                continue
                
        if(matcht == "ARAM"):
            #OH GOD FIX ME
            pattern = "{: <20}{:^3}{: ^20}{:^3}{: ^8}\n"
            string  = "\n{:^50}\n\n".format("\----Game Mode: ARAM----\ ")
            string += pattern.format("Participants", "|", "Champion", "|", "Team")

            pattern = "{0:37}{1:<}{2:30}\n"
            for i in red:
                string += pattern.format(i,red[i][0],"Red")
            for i in blue:
                string += pattern.format(i,blue[i][0],"Blue")
        
        return string

    def requestJson(self,url):
        try:
            with urllib.request.urlopen(url) as f:
                data = json.loads(f.read().decode())
                return data
        except urllib.error.URLError as e:
            print("Connection error -- riotapi requestJson")
            print(e)
            print("Url: " + str(url))
            raise e
        except urllib.error.HTTPError as e:
            print("Connection error -- riotapi requestJson")
            print(e.reason)
            input()
            print("Url: " + str(url))
            raise e
        except urllib.error.ContentTooShortError as e:
            print("Too short error")
            print(e)
            print("Url: " + str(url))
            print("Header: " + str(header))
            raise e 
        except json.JSONDecodeError as e:
            print("Requested information was not json content")
            print(e)
            print("Url: " + str(url))
            print("Header: " + str(header))
            raise e
        else:
            print("Unknown error in getjdata with connecting") 
            print("Url: " + str(url))
            print("Header: " + str(header))
            raise

if __name__ == '__main__':
    def getJsonData():
        with open('info.json', 'r') as jsonf:
            return json.load(jsonf)

    jsondata  = getJsonData()
    r = Riot(jsondata['riot'])
    r.getLiveMatch('prolixed')
