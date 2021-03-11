from flaskpage import lag
import json
import requests
import re
import uuid



def hentJson(filnavn):
    with open(filnavn, "r") as f:
        #print(f)
        return json.load(f)
def createObsNinjaLinkWithGamernoInfo(id, nickname, countryCode, ingameEuw):
    
    finnesIkke = True
    for player in spillerListe:
        if player["navn"] == nickname or player["lolIngame"] == ingameEuw or player["id"] == id:
            finnesIkke = False
            break
            print(player)
            print("\n")
            print(id, nickname, ingameEuw)
            inputsvar = input("Hopp over[y], slett[d], nyid [i]")
            if(inputsvar =="y"):
                finnesIkke = False
                break
            elif inputsvar =="i":
                id = uuid.uuid4()
                finnesIkke = True
                break
            elif inputsvar =="d":
                finnesIkke = True
                break
            else:
                pass
    id = "TM"+id
    if finnesIkke:
        obsNinjaId = countryCode+str(id)+nickname

        ferdigNinjaId = ""
        "".join(e for e in obsNinjaId if e.isalnum())
        obsNinjaId = re.sub('[^A-Za-z0-9\s]+', '', obsNinjaId)
        obsNinjaId = re.sub('\W+','_', obsNinjaId)
        ferdigNinjaId = obsNinjaId
        obsNinjaInfo = {
            "name":nickname,
            "id":id,
            "push":"https://obs.ninja/?push="+ferdigNinjaId,
            "view":"https://obs.ninja/?view="+ferdigNinjaId,
            "settings": "&webcam&quality=0&autostart"
        }
        with open("jsonFiles/spillere/obsninja/"+str(id)+".json","w") as f:
            json.dump(obsNinjaInfo, f)
        spillereMedObsNinjaLink.append(id)

spillerListe = hentJson("jsonFiles/spillerListe.json")
teliaMastersTeamliste = hentJson("jsonFiles/production/teams.json")
spillereMedObsNinjaLink = hentJson("jsonFiles/spillere/obsninja/oversikt.json")
#print(spillerListe)
teliaMastersLagliste = []
print("\n\n\n\n\n\n")
for teams in teliaMastersTeamliste:
    teliaMastersLagliste.append(teams["Contestant"])
    print(teams["Contestant"]["name"])
    for lagspiller in teams["ContestantMember"]:
        createObsNinjaLinkWithGamernoInfo(lagspiller["id"],lagspiller["nickname"],lagspiller["country_iso"],lagspiller["gameaccount"])
        spillerToAdd ={
            "navn": lagspiller["name"],
            "lolIngame": lagspiller["gameaccount"],
            "id": "TM"+lagspiller["id"],
            "gamernoBilde":""
        }
        spillerListe.append(spillerToAdd)
print("LAGER TEAMS I PROGRAM" +"\n"*4)
for teams in teliaMastersTeamliste:
    print(teams)
    #print(teams["Contestant"]["name"])
    generatedId = requests.get("http://localhost:5000/lag/create/"+teams["Contestant"]["name"]).text
    #print(generatedId.text)

    lagInfo = hentJson("jsonFiles/lag/"+generatedId+".json")
    lagInfo["kallenavn"] = "TM_"+teams["Contestant"]["name"]
    lagInfo["tag"] = teams["Contestant"]["shortname"]
    lagInfo["bilde"] = teams["Contestant"]["name"]+"_logo.png"
    for i,lagspiller in enumerate(teams["ContestantMember"]):
        lagInfo["spillere"][i]["navn"] = lagspiller["name"]
        lagInfo["spillere"][i]["id"] = "TM"+lagspiller["id"]
        lagInfo["spillere"][i]["spillerBilde"] = ""
        lagInfo["spillere"][i]["ingameNavn"] = lagspiller["gameaccount"]
        if(i >4):
            break
    with open("jsonFiles/lag/"+generatedId+".json","w") as f:
        json.dump(lagInfo, f)
    #/lag/<id>/save
with open("jsonFiles/spillere/obsninja/oversikt.json","w") as f:
    json.dump(spillereMedObsNinjaLink, f)
with open("jsonFiles/spillerListe.json","w") as f:
    json.dump(spillerListe, f)
