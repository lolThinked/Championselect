import requests
import json

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
LeagueID= 6955 #Vår 2020
LeagueID= 7993 #Høst 2020
#LeagueID= 7979

print("Henter personlig data for brukere")
#https:\/\/www.gamer.no\/turneringer\/telialigaen-league-of-legends-hosten-2020\/7979\/tabeller\/#divisjon7993
def hentPerBrukerData(bruker = 44513):
    response1 = requests.get(
        "https://www.gamer.no/api/v1/users/"+str(bruker)+"/lolstats",
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    print(response1)
hentPerBrukerData()
#https://www.gamer.no/klubber/nordavind-dnb/28821/lag/37826

print("GETTING TABLES for TeliaLigaen - Standings...")
def lagTables():
    response1 = requests.get(
        "https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/tables",
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
    else:
        print("BAD  - ",apiLink)
def test2(apiLink):
    response1 = requests.get(
        apiLink,
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    print(response1)


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
def lagDataBaseFraLag():
    #miderltidig dataBase
    tempDatabase =[]
    lolStatsOnly =[]
    gamernoDatabase ={}
    databaseStats = {
        "amountPlayers":0,
        "amountTeams":0,
        "noLoLStats":0,
        "failedGamernos":[]
        }
    #Hent Lagene i 1.Divisjon
    tabellForLeague = requests.get(
        "https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/tables",
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    #print(tabellForLeague)

    for team in tabellForLeague:
        teamId = team["participant"]["teamId"]
        #print(team["participant"]["teamId"])
        databaseStats["amountTeams"] +=1
        lolLagFraGamerno = requests.get(
            "https://www.gamer.no/api/v1/teams/"+str(teamId)+"/players",
            headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
        #print(lolLagFraGamerno)
        for gamernoUser in lolLagFraGamerno:
            databaseStats["amountPlayers"] +=1
            gamernoDatabase[gamernoUser["id"]] = gamernoUser
            playerStats = requests.get(
                "https://www.gamer.no/api/v1/users/"+str(gamernoUser["id"])+"/lolstats",
                headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
            #print(playerStats)
            #print(type(playerStats))
            print("\n"*50,"PROGRESS - ",str(databaseStats["amountTeams"]),"/10")
            if(playerStats == "Not found"):
                print("NOT FOUND")
                print("Gamerno ID:", str(gamernoUser["id"]))
                print("Gamerno Link:", str(gamernoUser["url"]))
                databaseStats["failedGamernos"].append(gamernoUser["url"])
                print("\n\n\n")
            else:
                lolStatsOnly.append(playerStats)
                playerStats["user"] = gamernoUser
                tempDatabase.append(playerStats)
                databaseStats["noLoLStats"] +=1
        print("_"*10,"\n\n\n","Users with no LoL-Stats: ",str(databaseStats["noLoLStats"]),"/",str(databaseStats["amountPlayers"]))
    print("Teams: ",str(databaseStats["amountTeams"]))
    print("Players: ",str(databaseStats["amountPlayers"]))
    #print(tempDatabase)
    #print(databaseStats["failedGamernos"])
    return tempDatabase

    #lag1Div
    #Hent hver spiller på alle Lagene
    '''
    https://www.gamer.no/api/v1/teams/"+str(37826)+"/players - spillere på lag

    https://www.gamer.no/api/v1/users/"+str(44513)+"/lolstats - lolstats fra brukere
    '''

table = lagTables()
dataBase = lagDataBase()
#dataBase = lagDataBaseH()
database = lagDataBaseFraLag()
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
writeToJSONFile("tableStanding", table)
writeToJSONFile("database", dataBase)

print("\n\n")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/tables")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/lolstats")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/lolstats?page=1")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(6955)+"/lolstats?page=1")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(6955)+"/")

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
testDefings("https://www.gamer.no/api/v1/users/"+str(44513)+"/lolstats")
testDefings("https://www.gamer.no/api/v1/teams/"+str(37826)+"/")
testDefings("https://www.gamer.no/api/v1/teams/"+str(37826)+"/players")
testDefings("https://www.gamer.no/api/v1/teams/"+str(37826)+"/players/lolstats")
testDefings("https://www.gamer.no/api/v1/tournaments/"+str(LeagueID)+"/teams")
#test2("https://www.gamer.no/api/v1/teams/"+str(37826)+"/players")
print("\n\n")
#test2("https://www.gamer.no/api/v1/teams/"+str(37826)+"/")
#test2("https://www.gamer.no/api/v1/tournaments/")

#test2("https://www.gamer.no/api/v1/users/"+str(44513)+"/lolstats")
#test2("https://www.gamer.no/api/v1/users/"+str(44513)+"/")


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
