from pythonFiles.functions import getRiotLock, getAuthorizationString, makeDictForChampionId, makeDictForSummonerSpell, getSslContext
import requests
import json

import socketio
connected = False
sio = socketio.Client()
sio.connect('http://localhost:5000')
@sio.event
def connect():
    global connected
    connected = True
    print('connection established')
@sio.event
def disconnect():
    global connected
    connected = True
    print('disconnected from server')

class ChampionSelectUpdater:

    def __init__(self):
        self._lockList = getRiotLock()
        self._authorizationString = getAuthorizationString(self._lockList)
        self._sslContext = getSslContext()
        self._championDictionary = makeDictForChampionId()
        self._summonerSpellDictionary = makeDictForSummonerSpell()
        self._jsonData = None
        self._playerData = None
        self._banData = None
        self._timeData = None
        self._actionData = None
        self._prevActionData = None
        self._minInfo = {"bans":"","player":"","action":"", "prevAction":""}
        self._lengthChecker = 1
        self._orderData = {"picks":"", "bans":""}
        self._nameDictionary = {}
        self._teamData = None
        self._currentAction = None



    def returnChampDict(self):
        return self._championDictionary
    #returns the port for the riot LCU
    def getPort(self):
        port = self._lockList[2]
        return port
    #returns the header for the websocket
    def getHeader(self):
        header = [("Authorization", "Basic "+ self._authorizationString)]
        return header
    #returns the ssl_context
    def getSsl(self):
        #print(self._sslContext)
        return self._sslContext

    def update(self):
        print("---------------UPDATING---------------json")
        return

    def updateJsonData(self, data):
        self._jsonData = data
    def updatePlayerData(self, decider):
        self._playerData = self._getChampionSelectInfo(decider)
    def updateBanData(self):
        self._banData = self._getBans()

    def updateActionData(self):
        self._actionData = self._getCurrentAction()
        self._prevActionData = self._getPreviousAction()
    def updateMinInfo(self):
        self._minInfo["bans"] = self._banData
        self._minInfo["player"] = self._playerData
        self._minInfo["action"] = self._actionData
        self._minInfo["prevAction"] = self._prevActionData
        self._minInfo["team"] = self.getAllPlayerData()

    def printJsonData(self):
        print(self._jsonData)
    def clear(self):
        clearData = {"bans": {"myTeamBans": ["None", "None", "None", "None", "None"], "theirTeamBans": ["None", "None", "None", "None", "None"]}, "player": "None", "action": "None", "prevAction": "None", "team": {"myTeam": [], "theirTeam": []}}
        if(connected):
            #sio.emit('champSelectUpdate', clearData)
            sio.emit("clearChampSelectWebsocket", {"data":""})
            
        self.writeToJSONFile("minInfo", clearData)
        return
    def setOrderData(self):
        if( (len(self._jsonData["myTeam"]) + len(self._jsonData["theirTeam"])) == 10):
            self._orderData["picks"] = [6,9,10,17,18,7,8,11,16,19]
            self._orderData["bans"] = [[0,2,4,13,15],[1,3,5,12,14]]
    def getCurrentId(self):

        if self._jsonData != None and len(self._jsonData["actions"])>0 and self._jsonData != None:
            return self._getCurrentAction()["id"]
        else:
            return 0


    def _getTime(self):
        dataLocal = self._jsonData["timer"]
        mellomDict = {}
        mellomDict["epochTime"] = dataLocal["internalNowInEpochMs"]
        mellomDict["timeInPhase"] = dataLocal["phase"]
        return mellomDict
    #This makes get requests to get each players name
    def _findPlayerNamesByID(self, id):
        if id != 0:
            jsonPerPlayer = requests.get("https://riot:"+ self._lockList[3] +"@127.0.0.1:"+self._lockList[2]+"/lol-summoner/v1/summoners/" + str(id),
                                        headers = {"Accept": "application/json",
                                         "Authorization": "Basic " + self._authorizationString},
                                          verify = False)
            perPlayer = jsonPerPlayer.json()
            summonerName = perPlayer["displayName"]
            return summonerName
        else:
            return "Bot"
    #calls _getteamData to get all the data of each team and saving it as a dicstionary
    def getAllPlayerData(self):
        mellomDict = {"myTeam":"", "theirTeam":""}
        mellomDict["myTeam"] = self._getTeamData("myTeam")
        mellomDict["theirTeam"] = self._getTeamData("theirTeam")
        return mellomDict
    def _getTeamData(self, team):
        teamData = self._jsonData[team]
        teamList = []
        previousPlayer = None
        for player in teamData:
            mellomDict = {}
            #IF PLAYER
            try:
                if player["summonerId"] != 0:
                    mellomDict["Name"] = self._nameDictionary[player["summonerId"]]
                    mellomDict["Pick"] = self._getChampionId(player["championId"])
                    mellomDict["Position"] = player["cellId"]
                    mellomDict["Hover"] = self._getPlayerHover(player)
                    mellomDict["SummonerSpell1"] = self._getPlayerSummoner(player["spell1Id"])
                    mellomDict["SummonerSpell2"] = self._getPlayerSummoner(player["spell2Id"])
                #IF BOT
                elif player["summonerId"] == 0:
                    mellomDict["Name"] = "BOT"
                    mellomDict["Pick"] = self._getChampionId(player["championId"])
                    mellomDict["Position"] = player["cellId"]
                    mellomDict["Hover"] = "None"
                    mellomDict["SummonerSpell1"] = "None"
                    mellomDict["SummonerSpell2"] = "None"
                #elif player["playerType"] == "":
                else:
                    mellomDict["Name"] = self._nameDictionary[player["summonerId"]]
                    mellomDict["Pick"] = self._getChampionId(player["championId"])
                    mellomDict["Position"] = player["cellId"]
                    mellomDict["Hover"] = self._getPlayerHover(player)
                    mellomDict["SummonerSpell1"] = self._getPlayerSummoner(player["spell1Id"])
                    mellomDict["SummonerSpell2"] = self._getPlayerSummoner(player["spell2Id"])
            except:
                mellomDict["Name"] = self._nameDictionary[player["summonerId"]]
                mellomDict["Pick"] = self._getChampionId(player["championId"])
                mellomDict["Position"] = player["cellId"]
                mellomDict["Hover"] = self._getPlayerHover(player)
                mellomDict["SummonerSpell1"] = self._getPlayerSummoner(player["spell1Id"])
                mellomDict["SummonerSpell2"] = self._getPlayerSummoner(player["spell2Id"])
            else:
                pass
            teamList.append(mellomDict)
        return teamList


    def _getChampionId(self,id):
        if id != 0:
            return self._championDictionary[id]
        else:
            return "None"
    #Compares the last action to the player in reference
    def _getPlayerHover(self, player):
        actions = self._jsonData["actions"] #Actions-List
        '''
        if len(actions)>2:
            if player["cellId"] == actions[-2][0]["actorCellId"] and actions[-2][0]["completed"] == False: #player is [-2]
                return "Picking"

        if player["cellId"] == actions[-1][0]["actorCellId"]:# player [-1]
            if len(actions) > 2:
                if actions[-2][0]["completed"] == False:
                    return "Picking Next"
            if actions[-1][0]["completed"] == True:
                return "Picked"
            elif actions[-1][0]["type"] == "pick":
                return "Picking"
            elif actions[-1][0]["type"] == "ban":
                return "Banning"
        else:
            return "None"
            '''
        if player["cellId"] == self._actionData["position"]:
            return self._actionData["completed"]
        else:
            return "None"
    def _getPlayerSummoner(self,summoner):
        if summoner != 0:
            return self._summonerSpellDictionary[summoner]
        else:
            return "None"

    #This gets the playerInfo from the json File


    def setNameDictionary(self):
        self._getTeamNames("myTeam")
        self._getTeamNames("theirTeam")
        if connected:
            sio.emit("playerNameUpdateFromWebsocket", {"updatedNames":True})
    def _getTeamNames(self,team):
        teamData = self._jsonData[team]
        for player in teamData:
            id = player["summonerId"]
            self._nameDictionary[id] = self._findPlayerNamesByID(id)



    ##############################################
    #######    OLD ################
    def _getChampionSelectInfo(self, typeInfo):
        if typeInfo=="list":
            championSelectInfo = [0,1,2,3,4,5,6,7,8,9]

        else:
            championSelectInfo = {}

        myTeam = self._jsonData["myTeam"]
        enemyTeam = self._jsonData["theirTeam"]
        teams = [myTeam, enemyTeam]
        tall = 0

        for i in teams:
            for players in i:
                mellomDict = {}
                player = self._findPlayerNamesByID(players["summonerId"])
                mellomDict["Name"] = player
                if players["championId"]==0 and players["championPickIntent"]!=0:
                    mellomDict["ChampionPick"]=self._championDictionary[players["championPickIntent"]]
                    mellomDict["ChampionHover"]=1
                elif players["championId"]==0 and players["championPickIntent"]==0:
                    mellomDict["ChampionPick"]='None'
                    mellomDict["ChampionHover"]=0
                else:
                    mellomDict["ChampionPick"]=self._championDictionary[players["championId"]]
                    mellomDict["ChampionHover"]= self._getHover(tall)

                ################################################
                if players["spell1Id"] == 0:
                    mellomDict["SummonerSpell1"] = 'None'
                    mellomDict["SummonerSpell2"] = 'None'
                else:
                    mellomDict["SummonerSpell1"] = self._summonerSpellDictionary[players["spell1Id"]]
                    mellomDict["SummonerSpell2"] = self._summonerSpellDictionary[players["spell2Id"]]
                championSelectInfo[tall] = mellomDict
                tall+=1

        return championSelectInfo
    def _getHover(self,tall):
        pickActionList = [6,9,10,17,18,7,8,11,16,19]
        pickNumber = pickActionList[tall]
        if len(self._jsonData["actions"])>pickNumber:
            return self._jsonData["actions"][pickNumber][0]["completed"]
        else:
            return -1
    ##############################################
    #######    OLD ################


    ############################################################################
    #ACTION
    def _getCurrentAction(self):
        actions = self._jsonData["actions"]
        if len(actions)>0:
            lastAction = actions[-1][0]
            #
            for perAction in actions:
                if perAction[0]["completed"] == False:
                    return self._getDataAction(perAction[0])
            return self._getDataAction(lastAction)
    def _getPreviousAction(self):
            actions = self._jsonData["actions"]
            if len(actions)>0:
                if self._lengthChecker < len(actions):
                    self._lengthChecker = len(actions)
                    prevAction = actions[-2][0]
                    return self._getDataAction(prevAction)
    def _getDataAction(self, data):
        mellomDict = {}
        mellomDict["position"] = data["actorCellId"]
        if data["championId"] == 0:
            mellomDict["championName"] = "None"
        else:
            mellomDict["championName"] = self._championDictionary[data["championId"]]
        mellomDict["completed"] = data["completed"]
        if data["type"] == "ban":
            mellomDict["pickType"] = "Banning"
        else:
            mellomDict["pickType"] = "Picking"
        mellomDict["id"] = data["id"]
        return mellomDict



    #This gets the bans
    def _getBans(self):
        mellomDict = {}
        bans = self._jsonData["bans"]
        myTeamBans = bans["myTeamBans"]
        #print(bans["myTeamBans"])
        theirTeamBans = bans["theirTeamBans"]
        mellomDict["myTeamBans"] = self._lagListe(myTeamBans)
        mellomDict["theirTeamBans"] = self._lagListe(theirTeamBans)
        #print(mellomDict)



        return mellomDict
    #This creates a list for bans
    def _lagListe(self, banInfo):
        liste = []
        tall = 0
        for i in range(5):
            liste.append("None")
        for bans in banInfo:
            liste[tall] = self._championDictionary[bans]
            #print(self._championDictionary[bans])
            tall +=1
        #print(liste)
        return liste




    ############################################################################
    ############################################################################
    #                               SAVE METHODS                               #

    #This Saves the self._minInfo dictionary as a json file
    def saveMinInfoJson(self):
        fileName = "minInfo"
        filePathNameWithExt = "./jsonFiles/"+fileName + ".json"
        with open(filePathNameWithExt, "w") as fp:
            json.dump(self._minInfo, fp)
        self.pushMinInfoToWebserver()
    def pushMinInfoToWebserver(self, data = True):
        #url = "http://localhost:5000/championselect/websocketUpdate"
        print(data)
        if data:
            data = self._minInfo
        if(connected):
            sio.emit('champSelectUpdate', data)
        print(data)
        #print()
        #pushMinInfoRequest = requests.post(url, json.dumps(data))
        #print(pushMinInfoRequest)
    def savePreviousChampionSelectData(self):
        fileName = "previousInfo"
        filePathNameWithExt = "./jsonFiles/"+fileName + ".json"
        with open(filePathNameWithExt, "w") as fp:
            json.dump(self._minInfo, fp)
    #Writes to json
    def writeToJSONFile(self, fileName, data):
        filePathNameWithExt = "./jsonFiles/"+fileName + ".json"
        with open(filePathNameWithExt, "w") as fp:
            json.dump(data, fp)
