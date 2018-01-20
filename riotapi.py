"""
    Filename: riotapi.py
    Author:   Garett Roberts
    Repo:     https://github.com/garetroy/Jeeves

    This is the api for getting riot queries. 
    Part of a larger project named Jeeves, but can work independantly.

    REQUIRED:
        Please, have a json file named "champions.json" that contain
        champion info (should come with repository)

"""
   
     
import urllib.request
import json
import tabulate

class Riot:
    """
        The class for making riot requests
    """
    def __init__(self,api_key):
        """
        :param api_key - Your riot_api_key
        """
        self.base_api_url   = "https://na1.api.riotgames.com"
        self.summoner_name  = "/lol/summoner/v3/summoners/by-name/"
        self.summoner_match = "/lol/match/v3/matchlists/by-account/"
        self.match_dets     = "/lol/match/v3/matches/"
        self.api_key        = api_key
        self.summonerht     = {} #summoner name hash table
        self.summonermht    = {} #summoner matches hash table
        self.matchesht      = {} #matches hash table
        self.champions      = self.loadChampions()

    @property
    def keyString(self):
        """
        :returns the correct ending, appending the riot api key
        """
        return "?api_key=" + self.api_key 

    @property
    def version(self):
        """
        This makes a request to the riot api to get the current
        leauge version

        :returns the current version of leauge
        """
        url  = "https://na1.api.riotgames.com/lol/static-data/v3/versions"
        url += self.keyString
        try:
            return self.requestJson(url)[0]
        except:
            print("Could not get version")
            raise

    def loadChampions(self):
        """
        Loads all of the champions from json
        :returns json formatted data of champions
        """
        with open('champions.json', 'r') as jsonf:
            return json.load(jsonf)
        
    def getChampionByName(self,name):
        """
        :param name - a champions name : str
        :returns champion object associated with a champion name
        """
        return self.champions[name]

    def getChampionById(self,_id):
        """
        This has to do more work, because the keys are names

        :param _id - a champions id
        :returns champion object associated with champion id
        """
        for i in self.champions:
            if(self.champions[i]['id'] == _id):
                return self.champions[i]
    
    def summoner(self,name):
        """
        Checks to see if the name given is in hash table, then it uses that
        else makes a json request for it
        :param name - The name assoicated with a summoner
        :returns summonor object associated with sumonner name
        """
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
        """
        :param name - The name associated with a summoner
        :returns the summoners level
        """
        return self.summoner(name)['summonerLevel']

    def summonerMatches(self,name,forceupdate=False):
        """
        If the matches for the user already exist present them,
        else fetch them...
        You can also force it to update when you call this method
        :param name        - The name assicated with a summoner
        :param forceupdate - Forces the update of the hash tables
        :returns returns all Matches associated with the summoner name
        """
        if(name in self.summonermht and not forceupdate):
            return self.summonermht[name]

        sumid   = self.summoner(name)['accountId']
        string  = self.base_api_url + self.summoner_match + str(sumid)
        string += self.keyString

        self.summonermht[name] = self.requestJson(string)
        return self.summonermht[name]

    def recentMatch(self,name,forceupdate=False):
        """
        If match data already exists, why fetch it?

        :params name        - The name associated with a summoner
        :params forceupdate - Forces the update of the hash table entry
        :returns the recent match data from the corresponding sum name
        """
        matchid   = str(self.summonerMatches(name,forceupdate)\
            ['matches'][0]['gameId'])

        if(matchid in self.matchesht and not forceupdate):
            return self.matchesht[matchid]
        
        string  = self.base_api_url + self.match_dets + str(matchid) 
        string += self.keyString

        self.matchesht[matchid] = self.requestJson(string) 
        return self.matchesht[matchid] 

    def getLiveMatch(self,name):
        """
        Gets most recent match forcing it's update. Then sending a string
        with data
        :params name        - name associated with a summoner
        :params forceupdate - Forces the update of the has tables
        """
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
            datainf = []

            for i in red:
                datainf.append([i,red[i][0],"Red"])
            for i in blue:
                datainf.append([i,blue[i][0],"Blue"])
        
        return tabulate.tabulate(datainf, headers=["Summonder","Champion","Team"])

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
