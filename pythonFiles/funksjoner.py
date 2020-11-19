import base64
import urllib3
import json
import os.path
from os import path
def getRiotLock():#opens the lockfile from riot games and extracts its info
    if(path.exists("C:\Riot Games\League of Legends\lockfile")):
        infile = open("C:\Riot Games\League of Legends\lockfile")
        for line in infile:

            liste = line.split(":")

        return liste
    else:
        print("ERROR:")
        print("Cannot find lockfile:")
        print("Check if the LoL-client is launched or if you have the right settings")
        print("\n\n Please restart the program to fix issues")
        print("if you continue to have issues, open CMD and type webSocketer.exe in this folder, and copy the logOutput and send it to me.")
        input("\n\n\n\nPress a button to exit")
        exit()
#liste = getRiotLock()
def getStringAuth(liste):#takes and argument(liste) and encodes parts of the content

        urllib3.disable_warnings()
        strRiotKey = "riot:" + liste[3]
        strRiotKey = strRiotKey.encode("utf-8")
        nyString = base64.b64encode(strRiotKey)
        nyStringDecoded = nyString.decode("utf-8")
        return nyStringDecoded

def makeDictForChampionId():#makes a dictionary for championids and champion names
    championIDDict = {}
    championJson = requests.get("http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json").json()
    championData = championJson["data"]
    championFor = championData.items()
    #print(championFor)
    for champion in championFor:
        #print(champion)
        championIDDict[int(champion[1]["key"])] = champion[1]["id"] #Gir Navn
    return championIDDict
def makeDictForSummonerSpell():#makes a dictionary for spellIds and spell names
    championIDDict = {}
    championJson = requests.get("http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/summoner.json").json()
    championData = championJson["data"]
    championFor = championData.items()
    for champion in championFor:
        championIDDict[int(champion[1]["key"])] = champion[1]["id"]
        #print(champion)
    #print(championFor)
    return championIDDict
def writeToJSONFile(fileName, data):
    filePathNameWithExt = "./json/"+fileName + ".json"
    with open(filePathNameWithExt, "w") as fp:
        json.dump(data, fp)
