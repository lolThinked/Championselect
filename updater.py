import requests
import json
import time
import re

print("Reading Settings...\n")
infile = open("settings.txt", "r")
settings = []
for line in infile:
    settings.append(line.rstrip("\n"))
#print(settings)
print("Settings Read...\n\n\n")
print("Getting updated information...")
ddragonInformation = requests.get("http://ddragon.leagueoflegends.com/api/versions.json").json()
currentPatch = ddragonInformation[0]
#print("http://ddragon.leagueoflegends.com/cdn/" + currentPatch + "/data/en_US/summoner.json")
infile.close()
savefile = open("settings.txt", "w+")
print("UPDATING:")
savefile.write(settings[0]+"\n")
savefile.write("http://ddragon.leagueoflegends.com/cdn/" + currentPatch + "/data/en_US/champion.json\n")
savefile.write("http://ddragon.leagueoflegends.com/cdn/" + currentPatch + "/data/en_US/summoner.json\n")
savefile.close()
tlV2020= 6955 #Vår 2020
tlH2020= 7993 #Høst 2020
bigV2021= 8597 #Vår 2021 HELE Lol
LeagueID = 8647 #Bare 1.Div
League2DivV2021 = 8648
TeliaID = 8500
#LeagueID= 7979

errors = []
def hentJson(navn):
    with open("jsonFiles/" + navn + ".json", "r") as f:
        return json.load(f)
spillereMedObsNinjaLink = hentJson("spillere/obsninja/oversikt")

print("Henter personlig data for brukere")
#https:\/\/www.gamer.no\/turneringer\/telialigaen-league-of-legends-hosten-2020\/7979\/tabeller\/#divisjon7993
def hentPerBrukerData(bruker = 44513):
    response1 = requests.get(
        "https://www.gamer.no/api/v1/users/"+str(bruker)+"/lolstats",
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    print(response1)
hentPerBrukerData()
#https://www.gamer.no/klubber/nordavind-dnb/28821/lag/37826

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

print("GETTING TABLES for TeliaLigaen - Standings...")
def lagTables():
    response1 = requests.get(
        "https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/tables",
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    #print(response1)
    return response1
def lagTabellmedID(ligaID):
    response1 = requests.get(
        "https://www.gamer.no/api/v1/tournaments/"+str(ligaID)+"/tables",
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    #print(response1)
    return response1

def testDefings(apiLink):
    try:
        response1 = requests.get(
            apiLink,
            headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
        #print(response1)
    except:
        print("BAD  - ",apiLink)
        return
    if(response1 != "Unauthorized"):
        print("GOOD - ",apiLink)
        #print(response1)
    else:
        print("BAD  - ",apiLink)
def test2(apiLink):
    response1 = requests.get(
        apiLink,
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    print(response1)



def createObsNinjaLinkWithGamernoInfo(gamernoUser):
    finnesIkke = True
    # global spillereMedObsNinjaLink
    # for spiller in spillereMedObsNinjaLink:
    #     if spiller == gamernoUser["id"]:
    #         finnesIkke = False

    if finnesIkke:
        obsNinjaId = gamernoUser["country"]["code"]+str(gamernoUser["id"])+gamernoUser["name"]
        #re.sub('[^A-Za-z0-9]+', '', obsNinjaId)
        ferdigNinjaId = ""
        "".join(e for e in obsNinjaId if e.isalnum())
        #print(ferdigNinjaId)

        obsNinjaId = re.sub('[^A-Za-z0-9\s]+', '', obsNinjaId)
        obsNinjaId = re.sub('\W+','_', obsNinjaId)
        #print(obsNinjaId)
        ferdigNinjaId = obsNinjaId
        obsNinjaInfo = {
            "name":gamernoUser["name"],
            "id":gamernoUser["id"],
            "push":"https://obs.ninja/?push="+ferdigNinjaId,
            "view":"https://obs.ninja/?view="+ferdigNinjaId,
            "settings": "&webcam&quality=0&autostart"
        }
        if gamernoUser["id"] == 93960 and False:
            print(obsNinjaInfo)
            print(gamernoUser)
            input("VENT FOR NESTE SPILLER")
        with open("jsonFiles/spillere/obsninja/"+str(gamernoUser["id"])+".json","w") as f:
            json.dump(obsNinjaInfo, f)
        spillereMedObsNinjaLink.append(gamernoUser["id"])

print("GETTING DataBase for Telialigaen...")
def lagDataBase():         #Vår 2020
    tempDatabase = []
    response1 = requests.get(
        "https://www.gamer.no/api/v1/tournaments/6955/lolstats?page=1",
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    #print(response1)
    lastPage = response1["last_page"] + 1
    for i in range(1,lastPage):
        if(i != 1):
            response = requests.get(
                " https://www.gamer.no/api/v1/tournaments/6955/lolstats?page="+str(i) +"",
                headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
            tempDatabase += response["data"]
        else:
            tempDatabase += response1["data"]
    return tempDatabase

#LeagueID= 7993
def lagDataBaseH():       #Høst 2020
    tempDatabase = []
    response1 = requests.get(
        "https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/lolstats?page=1",
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    '''
    print(LeagueID)
    print("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/lolstats?page=1")
    print(response1)
    '''
    if(response1 != "Unauthorized"):
        lastPage = response1["last_page"] + 1
        for i in range(1,lastPage):
            if(i != 1):
                response = requests.get(
                    " https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/lolstats?page="+str(i) +"",
                    headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
                tempDatabase += response["data"]
            else:
                tempDatabase += response1["data"]
        #print(tempDatabase)
        return tempDatabase
    else:
        print("ERROR:" + response1)
        return {"error":"error"}
def lagDataBaseFraLag(big = False):
    
    #miderltidig dataBase
    spillerListe = []
    tempDatabase =[]
    lolStatsOnly =[]
    gamernoDatabase ={}
    databaseStats = {
        "amountPlayers":0,
        "amountTeams":0,
        "noLoLStats":0,
        "failedGamernos":[],
        "playersWithProImage":[]
        }
    #Hent Lagene i 1.Divisjon
    if big:
        heleLigaRequest = requests.get("https://www.gamer.no/api/v1/tournaments/"+str(bigV2021)+"/",
            headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
        tabellForLeague = lagTabellmedID(TeliaID)
        tabellForLeague+= lagTabellmedID(tlH2020)
        for tournamentID in heleLigaRequest["divisions"]:
            print(tournamentID["name"] + " - Liga")
            tabellForLeague += lagTabellmedID(tournamentID["id"])
    else:
        tabellForLeague = requests.get(
            "https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/tables",
            headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
        tabellForLeague = lagTabellmedID(LeagueID)
        tabellForLeague+= lagTabellmedID(TeliaID)
        tabellForLeague+= lagTabellmedID(tlH2020)
        tabellForLeague+= lagTabellmedID(League2DivV2021)
    #print(tabellForLeague)
    teamIds =[]
    lenFirstEnumurate = len(tabellForLeague)
    for i, team in enumerate(tabellForLeague):
        
        teamId = team["participant"]["teamId"]
        hasNotSeenBefore = True
        for id in teamIds:
            if id == teamId:
                hasNotSeenBefore = False
        if hasNotSeenBefore:
            teamIds.append(teamId)
            #print(team["participant"]["teamId"])
            databaseStats["amountTeams"] +=1
            lolLagFraGamerno = requests.get(
                "https://www.gamer.no/api/v1/teams/"+str(teamId)+"/players",
                headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
            #print(lolLagFraGamerno)
            lenSecondEnumurate = len(lolLagFraGamerno)
            for j, gamernoUser in enumerate(lolLagFraGamerno):
                databaseStats["amountPlayers"] +=1
                gamernoDatabase[gamernoUser["id"]] = gamernoUser
                playerStats = requests.get(
                    "https://www.gamer.no/api/v1/users/"+str(gamernoUser["id"])+"/lolstats",
                    headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
                #print(playerStats)
                #print(type(playerStats))
                #print("\n"*50,"PROGRESS - ",str(databaseStats["amountTeams"]),"/10")
                printProgressBar(j + 1, l, prefix = 'LAG Progress:', suffix = 'Complete', length = lenSecondEnumurate)
                createObsNinjaLinkWithGamernoInfo(gamernoUser)
                if(playerStats == "Not found"):
                    #print("NOT FOUND")
                    #print("Gamerno ID:", str(gamernoUser["id"]))
                    #print("Gamerno Link:", str(gamernoUser["url"]))
                    databaseStats["failedGamernos"].append(gamernoUser["url"])
                    #print("\n\n\n")
                    databaseStats["noLoLStats"] +=1
                else:
                    
                    lolStatsOnly.append(playerStats)
                    playerStats["user"] = gamernoUser
                    if(playerStats["user"]["name"] == "Dacreq"):
                        #print(playerStats)
                        #input("DACREQ")
                        pass
                    tempDatabase.append(playerStats)
                    with open("jsonFiles/spillere/lolstats/"+str(playerStats["user"]["id"])+".json", "w") as f:
                        json.dump(playerStats, f)
                    #print(playerStats)
                    try:
                        spiller = {
                            "navn": playerStats["user"]["name"],
                            "lolIngame": playerStats["summonerName"],
                            "id": playerStats["user"]["id"],
                            "gamernoBilde":playerStats["user"]["image"]
                        }
                    except:
                        print("ERROR")
                        print(playerStats)
                        errors.append(playerStats)
                    spillerListe.append(spiller)
            #print("_"*10,"\n\n\n","Users with no LoL-Stats: ",str(databaseStats["noLoLStats"]),"/",str(databaseStats["amountPlayers"]))
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = lenFirstEnumurate)
    print("Teams: ",str(databaseStats["amountTeams"]))
    print("Players: ",str(databaseStats["amountPlayers"]))
    #print(tempDatabase)
    #print(databaseStats["failedGamernos"])
    print(len(lolStatsOnly))
    print(len(tempDatabase))
    return tempDatabase, spillerListe, databaseStats

    #lag1Div
    #Hent hver spiller på alle Lagene
    '''
    https://www.gamer.no/api/v1/teams/"+str(37826)+"/players - spillere på lag

    https://www.gamer.no/api/v1/users/"+str(44513)+"/lolstats - lolstats fra brukere
    '''



#hentJson("minInfo")
#testDefings()
def writeToJSONFile(fileName, data):
        filePathNameWithExt = "./jsonFiles/"+fileName + ".json"
        with open(filePathNameWithExt, "w") as fp:
            json.dump(data, fp)

def hentJson(navn):
    with open("jsonFiles/" + navn + ".json", "r") as f:
        minInfo = json.load(f)
    return minInfo





# A List of Items
items = list(range(0, 57))
l = len(items)

# Initial call to print 0% progress
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 13)
for i, item in enumerate(items):
    pass
    # Do stuff...
    #time.sleep(0.1)
    # Update Progress Bar
    #printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 13)


table = lagTables()
teliaEsportTabell = lagTabellmedID(TeliaID)

writeToJSONFile("tableStanding", table)
writeToJSONFile("TESStanding", teliaEsportTabell)
databaseIput = input("Lag database [Y/N] Big for alle lag i hele Tl \n:")
if(databaseIput =="Y" or databaseIput=="y" or databaseIput =="yes" or databaseIput=="Yes"):
    print("\n\n")
    dataBaseVaar = lagDataBase()
    #dataBase = lagDataBaseH()
    dataBase, spillerListe, databaseStatistikk = lagDataBaseFraLag()
    print(databaseStatistikk)
    print("\n")
    print("DATABASE_LENGTH: "+str(len(dataBase)))
    print("SpillerListe_LENGTH: "+str(len(spillerListe)))
    
    for failed in databaseStatistikk["failedGamernos"]:
        #print(failed["user"]["name"], "\n", failed["user"]["url"])
        print(failed)
    writeToJSONFile("database", dataBase)
    writeToJSONFile("spillerListe", spillerListe)
elif(databaseIput == "Big"):
    print("\nBig!")
    print("\n\n")

    dataBaseVaar = lagDataBase()
    #dataBase = lagDataBaseH()
    dataBase, spillerListe, databaseStatistikk = lagDataBaseFraLag(True)
    print(databaseStatistikk)
    print("\n")
    print("DATABASE_LENGTH: "+str(len(dataBase)))
    print("SpillerListe_LENGTH: "+str(len(spillerListe)))
    
    for failed in databaseStatistikk["failedGamernos"]:
        #print(failed["user"]["name"], "\n", failed["user"]["url"])
        print(failed)
    writeToJSONFile("database", dataBase)
    writeToJSONFile("spillerListe", spillerListe)


writeToJSONFile("spillere/obsninja/oversikt", spillereMedObsNinjaLink)
print("\n\n")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/tables")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/lolstats")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/lolstats?page=1")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(6955)+"/lolstats?page=1")
#testDefings("https://www.gamer.no/api/v1/tournaments/"+str(6955)+"/")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/")
#test2("https://www.gamer.no/api/v1/tournaments/"+8597)

#test2("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/lolstats?page=1")
'''
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/klubber")
testDefings("https://www.gamer.no/api/v1/klubber/")
testDefings("https://www.gamer.no/api/v1/klubber/"+str(37826)+"/")
testDefings("https://www.gamer.no/api/v1/klubber/"+str(37826)+"/lolstats")
testDefings("https://www.gamer.no/api/v1/klubber/"+str(37826)+"/games")
testDefings("https://www.gamer.no/api/v1/clubs/"+str(37826)+"/")
testDefings("https://www.gamer.no/api/v1/club/"+str(37826)+"/")
'''
testDefings("https://www.gamer.no/api/v1/tournaments/")
testDefings("https://www.gamer.no/api/v1/")
testDefings("https://www.gamer.no/api/v2/")
'''
testDefings("https://www.gamer.no/api/v1/users/"+str(44513)+"/lolstats")
testDefings("https://www.gamer.no/api/v1/teams/"+str(37826)+"/")
testDefings("https://www.gamer.no/api/v1/teams/"+str(37826)+"/players")
testDefings("https://www.gamer.no/api/v1/teams/"+str(37826)+"/players/lolstats")
'''
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/teams")
#test2("https://www.gamer.no/api/v1/tournaments/"+str(8597)+"/")
#test2("https://www.gamer.no/api/v1/teams/"+str(37826)+"/players")
print("\n\n")
#test2("https://www.gamer.no/api/v1/teams/"+str(37826)+"/")
#test2("https://www.gamer.no/api/v1/tournaments/")

#test2("https://www.gamer.no/api/v1/users/"+str(44513)+"/lolstats")
#test2("https://www.gamer.no/api/v1/users/"+str(44513)+"/")
test2("https://www.gamer.no/api/v1/users/"+str(53123)+"/")


#53123 THinked

####
#LINKER
'''
https://www.gamer.no/api/v1/teams/"+str(37826)+"/players - spillere på lag

https://www.gamer.no/api/v1/users/"+str(44513)+"/lolstats - lolstats fra brukere

'''

print("\n\n\nUPDATED:")
print("Press a button to exit")
input()
'''C:\Riot Games\League of Legends\lockfile
http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json
http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/summoner.json'''
