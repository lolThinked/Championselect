import json
import os
def hentInnLagoversikt():
    with open("jsonFiles/lag/oversikt.json", "r") as f:
        if os.stat("jsonFiles/lag/oversikt.json").st_size != 0:
            return json.load(f)
        else:
            return {}

def hentInnKampoversikt():
    if os.path.exists("jsonFiles/kamper/oversikt.json"):
        if os.stat("jsonFiles/kamper/oversikt.json").st_size !=0:
            with open("jsonFiles/kamper/oversikt.json","r") as f:
                return json.load(f)
        else:
            return []
    else:
        with open("jsonFiles/kamper/oversikt.json", "w") as f:
            tempDict = []
            json.dump(tempDict, f)
            return []


def lastInnCurrentKamp():
    with open("jsonFiles/kamper/currentKamp.json", "r") as f:
        return json.load(f)