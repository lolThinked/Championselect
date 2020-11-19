import asyncio
import websockets
from pythonFiles.championselectUpdater import ChampionSelectUpdater
from pythonFiles.functions import getRiotLock, getAuthorizationString
import threading
from minTimer import MinTimer
import json
import urllib3
import time
from pythonFiles import shared_things
import math
import requests
#import pythonFiles.shared_things
urllib3.disable_warnings()
import flaskpage
app = getattr(flaskpage, "app")

#1559347199
#1år
#1577836801
#August
#1566703134
#30/12/2020
#1609286400
if(time.time()>1609286400):
    print("Time for this trial has expired, please contact the creator for more information, email: fabianhopland@gmail.com")
    passordSjekk = input("Type password: ")
    if((passordSjekk != "Thinked") or passordSjekk !="Caster" or passordSjekk != "thinked" or passordSjekk != "caster"):
        pass
    while((passordSjekk != "Thinked") or passordSjekk !="Caster" or passordSjekk != "thinked" or passordSjekk != "caster"):
        if(passordSjekk =="" or passordSjekk ==" " or passordSjekk =="exit" or passordSjekk =="exit()"):
            exit()
        print("Password is wrong, type '' or ' ' or 'exit' to exit the program, or type passord again")
        if((passordSjekk == "Thinked") or passordSjekk =="Caster" or passordSjekk == "thinked" or passordSjekk == "caster"):
            break
        passordSjekk = input("Type password: ")
'''
##############                   For Compiling Only               ###########################
print("STARTING WEBSERVER")
threading.Thread(target=app.run, daemon = True).start()
print("###"*100)
print("\n\n\n STARTING PROGRAM")
##############                   For Compiling Only               ###########################
'''

webSocketerLockList = getRiotLock()
webSocketerAuthString = getAuthorizationString(webSocketerLockList)


def writeToJSONFile(fileName, data):
        filePathNameWithExt = "./jsonFiles/"+fileName + ".json"
        with open(filePathNameWithExt, "w") as fp:
            json.dump(data, fp)
def hentJson(navn):
    with open("jsonFiles/" + navn + ".json", "r") as f:
        minInfo = json.load(f)
    return minInfo

CSU = ChampionSelectUpdater()
port = CSU.getPort()
cert = CSU.getSsl()
headers = CSU.getHeader()

#shared_things.inChampionSelect = False
LobbyTimer = 0

print(CSU.returnChampDict())
testDict = CSU.returnChampDict()
f = open("test2.txt","w+")
for champions in testDict:
    f.write(str(champions) + ":" + testDict[champions]+"\n")
f.close()

print(port)
print(cert)
print(headers)


async def consume(data):
    if len(data) > 0:
        d = json.loads(data)
        #print(d[2]['uri'])
        #print(d[2]['uri'])
        if d[2]['uri'] == "/lol-champ-select/v1/session":
            #print(d)
            await update(d[2]["data"], d[2]["eventType"])
            #print(d)
        elif (d[2]['uri'] == "/lol-end-of-game/v1/eog-stats-block"):
            print("END OF GAME:")
            print(d[2]['uri'])
            print("\n")
            print(d)
            print("\n\n")
        elif (d[2]['uri'] == "/lol-lobby/v2/lobby"):
            #print("\n"*20)
            #print(d[2]['uri'])
            #print(d[2]["data"])
            await updateLobby(d[2]["data"], d[2]["eventType"])
        elif(d[2]['uri'] == "/lol-lobby/v2/lobby/members"):
            print("\n"*20)
            print(d[2]['uri'])
            print(d[2]["data"])
        elif(d[2]['uri'] =="/lol-chat/"):
            print("\n"*20)
            print(d[2]['uri'])
            print(d[2]["data"])
        else:
            '''
            print("\n")
            print("RANDOM CALL:")
            print(d[2]['uri'])
            '''

async def update(data, eventType):
    print("#"*20)
    firstTimeSetup = False

    if eventType=="Create":
        print("EVENT:CREATE")
        CSU.update()
        CSU.updateJsonData(data)
        CSU.setNameDictionary()
        CSU.setOrderData()
        #CSU.printJsonData()
        #CSU.updatePlayerData("list")
        CSU.updateBanData()
        CSU.updateActionData()
        CSU.updateMinInfo()
        CSU.saveMinInfoJson()

        shared_things.firstTimeSetup = True
        shared_things.finalizationSetup = True
        shared_things.oldEpoch = 0
        shared_things.inChampionSelect = True
        LobbyTimer = MinTimer(300, "lobbyTimer")
        LobbyTimer.start()
    elif eventType =="Update":
        print("oldEpoch: ",str(shared_things.oldEpoch))
        print("Lengden av data: ",str(len(data["actions"])))
        if(shared_things.oldEpoch != CSU.getCurrentId() and CSU.getCurrentId() != 0 and data["timer"]["totalTimeInPhase"] != 0):
            print("--------IsDifferent----------")
            print("Timer: ", str(math.ceil((data["timer"]["adjustedTimeLeftInPhase"])/1000)))
            shared_things.oldEpoch = CSU.getCurrentId()
            if math.ceil((data["timer"]["adjustedTimeLeftInPhase"])/1000) == 0:
                print("__1__")
                TimeKeeper = MinTimer(27, shared_things.oldEpoch)
                TimeKeeper.start()
            else:
                print("__2__")
                TimeKeeper = MinTimer(math.ceil((data["timer"]["adjustedTimeLeftInPhase"])/1000), shared_things.oldEpoch)
                TimeKeeper.start()
        else:
            if shared_things.firstTimeSetup and data["timer"]["totalTimeInPhase"] != 0:
                print("__3__")
                shared_things.oldEpoch = CSU.getCurrentId()
                TimeKeeper = MinTimer(math.ceil((data["timer"]["adjustedTimeLeftInPhase"])/1000), shared_things.oldEpoch)
                TimeKeeper.start()
                shared_things.firstTimeSetup = False
                CSU.setNameDictionary()
            else:
                print("__4__")
                print(shared_things.oldEpoch)
                print(CSU.getCurrentId())
        if data["timer"]["phase"] == "FINALIZATION" and shared_things.finalizationSetup:
            shared_things.oldEpoch =50
            TimeKeeper = MinTimer(math.ceil((data["timer"]["adjustedTimeLeftInPhase"])/1000), shared_things.oldEpoch)
            TimeKeeper.start()
            shared_things.finalizationSetup = False
        elif data["timer"]["phase"] =="GAME_STARTING":
            shared_things.oldEpoch =75
            TimeKeeper = MinTimer(math.ceil((data["timer"]["adjustedTimeLeftInPhase"])/1000), shared_things.oldEpoch)
            TimeKeeper.start()
        CSU.update()
        CSU.updateJsonData(data)
        CSU.setNameDictionary()
        #CSU.printJsonData()
        #CSU.updatePlayerData("list")
        CSU.updateBanData()
        CSU.updateActionData()
        CSU.updateMinInfo()
        CSU.saveMinInfoJson()
        #CSU.printJsonData()
        print("\n\n\n\n")
    elif eventType =="Delete":
        shared_things.oldEpoch = 0
        CSU.savePreviousChampionSelectData()
        CSU.clear()
        shared_things.inChampionSelect = False
        #LobbyTimer.join()
    elif eventType == "GAME_STARTING":
        shared_things.oldEpoch =125
        TimeKeeper = MinTimer(math.ceil((data["timer"]["adjustedTimeLeftInPhase"])/1000), shared_things.oldEpoch)
        TimeKeeper.start()
        shared_things.inChampionSelect = False
async def hello():
    async with websockets.connect('wss://localhost:' + port,
                                    ssl=cert,
                                    extra_headers=headers) as websocket:
        send_msg = [5, "OnJsonApiEvent"]

        await websocket.send(json.dumps(send_msg))
        while(True):
            resp = await websocket.recv()
            await consume(resp)

async def updateLobby(data, eventType):
    print(data)
    print(eventType)
    writeToJSONFile("lobbyData", data)
def customRequest(link):
    r = requests.get("https://riot:"+ webSocketerLockList[3] +"@127.0.0.1:"+webSocketerLockList[2]+link,
                                headers = {"Accept": "application/json",
                                "Authorization": "Basic " + webSocketerAuthString},
                                verify = False)
    dataInfo = r.json()
    print("\n\n")
    print(link)
    print(dataInfo)
    return dataInfo
print("https://riot:"+ webSocketerLockList[3] +"@127.0.0.1:"+webSocketerLockList[2])
print("https://"+webSocketerAuthString +"@127.0.0.1:"+webSocketerLockList[2])
'''
test2 = customRequest("/lol-chat/v1/config")
test3 = customRequest("/lol-chat/v1/conversations")
test4 = customRequest("/lol-chat/v1/conversations/active")
test5 = customRequest("/lol-chat/v1/conversations/notify")
'''
asyncio.get_event_loop().run_until_complete(hello())

print("Program completed")
input("Program has exited, please restart the program")

def getPlayerDataFromId(id):
    if id != 0:
        jsonPerPlayer = requests.get("https://riot:"+ webSocketerLockList[3] +"@127.0.0.1:"+webSocketerLockList[2]+"/lol-summoner/v1/summoners/" + str(id),
                                    headers = {"Accept": "application/json",
                                    "Authorization": "Basic " + self._authorizationString},
                                    verify = False)
        perPlayer = jsonPerPlayer.json()
        summonerName = perPlayer["displayName"]
        return summonerName
    else:
        return "Bot"
