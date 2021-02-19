import json
from pythonFiles.f_functions import hentJson

dataBaseDict = hentJson("database")

while True:
    compareString = input("Skriv inn navn på spiller: ")
    print(len(dataBaseDict))
    for player in dataBaseDict:
        if(player["user"]["name"].lower() == (compareString).lower()):
            print(player)
            break
    print("Spiller ikke funnet")