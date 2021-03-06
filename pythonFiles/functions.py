import ssl
import base64
import requests
#processes the riot lockfile
import os.path
from os import path
import time

def getInstallationPath():
    if(path.exists("settings.txt")):
        infile = open("settings.txt","r")
        settings = []
        for line in infile:

            settings.append(line.rstrip("\n"))
        return settings
    else:
        print("ERROR:")
        print("Cannot find settings.txt ")
        print("\n\n Please restart the program to fix issues")
        print("if you continue to have issues, open CMD and type webSocketer.exe in this folder, and copy the logOutput and send it to me.")
        input("\n\n\n\nPress a button to exit")
        exit()
def getRiotLock():
    #infile = open("C:\Riot Games\League of Legends\lockfile")
    pathFile = getInstallationPath()[0]
    if(path.exists(pathFile)):

        infile = open(pathFile)
        for line in infile:
            liste = line.split(":")
        return  liste
    else:
        print("ERROR:")
        print("Cannot find lockfile:")
        print("Check if the LoL-client is launched or if you have the right settings")
        print("\n\n Please restart the program to fix issues")
        print("if you continue to have issues, open CMD and type webSocketer.exe in this folder, and copy the logOutput and send it to me.")
        input("\n\n\n\nPress a button to exit")
        exit()
#returns the encoded _authorizationString for use in headers
def getAuthorizationString(liste):
    strRiotKey = "riot:" + liste[3]
    strRiotKey = strRiotKey.encode("utf-8")
    nyString = base64.b64encode(strRiotKey)
    nyStringDecoded = nyString.decode("utf-8")
    print(nyStringDecoded)
    return nyStringDecoded

#returns a dictionary with the championNames and ID's
def makeDictForChampionId():#makes a dictionary for championids and champion names
    championIDDict = {}
    championJson = requests.get(getInstallationPath()[1]).json()
    championData = championJson["data"]
    championFor = championData.items()
    for champion in championFor:
        championIDDict[int(champion[1]["key"])] = champion[1]["id"] #Gir Navn
    return championIDDict

#returns a dictionary with the summonerspellNames and ID's
def makeDictForSummonerSpell():
    championIDDict = {}
    championJson = requests.get(getInstallationPath()[2]).json()
    championData = championJson["data"]
    championFor = championData.items()
    for champion in championFor:
        championIDDict[int(champion[1]["key"])] = champion[1]["id"]
    return championIDDict

#returns an ssl context
def getSslContext():

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    print(ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT))
    ssl_context.check_hostname = False
    print(ssl_context.check_hostname)
    ssl_context.verify_mode = ssl.CERT_NONE
    print(ssl_context.verify_mode)
    print(ssl.CERT_NONE)
    return ssl_context


def checkPassword():
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
            if((passordSjekk == "Thinked") or passordSjekk =="Caster" or passordSjekk == "thinked" or passordSjekk == "caster"):
                print("Password is correct")
                break
            else:
                print("Password is wrong, type '' or ' ' or 'exit' to exit the program, or type passord again")
            passordSjekk = input("Type password: ")