import json
import os
def hentInnLagoversikt():
    with open("jsonFiles/lag/oversikt.json", "r") as f:
        if os.stat("jsonFiles/lag/oversikt.json").st_size != 0:
            return json.load(f)
        else:
            return {}