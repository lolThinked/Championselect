# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, url_for, send_from_directory, redirect, request
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from pythonFiles.f_functions import hentInnLagoversikt, hentInnKampoversikt, lastInnCurrentKamp, hentInnSpillerOversikt, hentJson, hentLag, hentInstillinger
from operator import itemgetter
from flask_socketio import SocketIO, send, emit
import subprocess

import uuid
import json
import os
import requests
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

login= LoginManager(app)
login.login_view = "login"

false = False
true = True

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


from pythonFiles.models import User

print("Laster inn filer")
'''
kampoversiktjson = [
    {
        "spill":"League of Legends",
        "tid": "01.02.2021",

    }
]
'''
gamerNoDatabase = hentJson("database")
lagoversiktjson = hentInnLagoversikt()
kampoversiktjson = hentInnKampoversikt()
casterPlayerOfTheGameJson = hentJson("production/casterPlayerOfTheGame")

global currentKampjson

currentKampjson = lastInnCurrentKamp()

#print(currentKampjson)

kameraOversiktJson = hentJson("production/playerCamOverview")
spillerListe = hentInnSpillerOversikt()
homePageLinkerJson = hentJson("homepageLinker")
settings = hentInstillinger()
livecontrolJson = hentJson("production/livecontrol")
playerToFocusJson = hentJson("production/playerToFocus")
#print(currentKamp)
def getOversikt():
    return lagoversiktjson
def oppdaterOversikt(tempOversikt):
    lagoversiktjson = tempOversikt



     
showHideQueue = {
    "ingame":[
        {
            "commandName":"",
            "action":"action",
            "data":"data"
        }
    ],
    "pregame":[

    ]

}

@socketio.on('message')
def handle_message(data):
    print(data)
    #print('received message: ' + data)
    send(data)


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@socketio.on("champSelectUpdate")
def handleChampSelectUpdate(data):
    socketio.emit("updateChampionSelecBrowser", data)
    print(data)
@socketio.on("playerNameUpdateFromWebsocket")
def updatePlayerNamesInBrowser(data):
    socketio.emit("updatePlayerNamesInBrowser", data)
    print("UPDATED PLAYERNAMES")

@socketio.on("clearChampSelectWebsocket")
def clearChampionSelect(data):
    print("CLEARING CHAMPIONSELECT")
    socketio.emit("clearChampionSelect", data)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

def hentCurrentKamp():
    return currentKampjson

def lagNyCurrentKamp():
    currentKamps = lagCustomLagoversikt()[0]
    currentKamps["lag1"]["score"] = 0
    currentKamps["lag2"]["score"] = 0
    lag1AllowedCameras = [1,1,1,1,1]
    lag2AllowedCameras = [1,1,1,1,1]
    currentKamps["allowedCameras"] = {"team1":lag1AllowedCameras, "team2":lag2AllowedCameras}
    with open("jsonFiles/kamper/currentKamp.json", "w") as f:
        json.dump(currentKamps, f)
    global currentKampjson
    currentKampjson = currentKamps

@app.route("/")
def home():
    return render_template("interface/homePage.html", user=current_user, current_user=current_user, linker=homePageLinkerJson)

@app.route("/kampeditor")
def kampeditor():
    alleLag = hentAlleLag()
    #print(alleLag)
    customKampOversikt = lagCustomLagoversikt()
    return render_template("interface/kampeditor.html", user=current_user, kamper=customKampOversikt, lagoversikt=alleLag)

@app.route("/kampeditor/create", methods=["POST"])
def createUpdateKamp():
    inData = eval(request.data)
    lagEllerRedigerKamp(inData)
    #print(inData)
    print("LAGER KAMP- FLASK")
    return "200"

@app.route("/kampeditor/swapside", methods=["POST"])
def kampSwapside():
    inData = eval(request.data)
    kampID = inData["id"]
    for x in range(len(kampoversiktjson)):
        riktigKamp = kampoversiktjson[x]
        if(riktigKamp["kampID"] == kampID):
            midlertidig = riktigKamp["lag1ID"]
            riktigKamp["lag1ID"] = riktigKamp["lag2ID"]
            riktigKamp["lag2ID"] = midlertidig

             
@app.route("/kampeditor/delete", methods=["POST"])
def deleteKamp():
    indata = eval(request.data)
    kampId = indata["id"]
    for x in range(len(kampoversiktjson)):
        if(kampoversiktjson[x]["kampID"] == kampId):
            print(kampoversiktjson[x])
            kampoversiktjson.pop(x)
            with open("jsonFiles/kamper/oversikt.json","w") as f:
                json.dump(kampoversiktjson, f)
            return "Deleted"
    
    
@app.route("/lagoversikt")
def lagoversikt():
    alleLag = hentAlleLag()
    print(alleLag)
    return render_template("interface/lagoversikt.html", user=current_user, lagoversikt = alleLag)

@app.route("/currentKamp")
def currentKamp():
    customKampoversikt = lagCustomLagoversikt()
    return jsonify(customKampoversikt[0])

@app.route("/kampoversikt")
def kampoversikt():
    alleLag = hentAlleLag()
    #Pass Lag in kampoversikt
    customKampoversikt = lagCustomLagoversikt()
    return render_template("stream/kampoversikt.html", user=current_user, kamper=customKampoversikt, lagoversikt=alleLag)

@app.route("/lag/create/<navn>")
def createLag(navn):
    tempID = str(uuid.uuid4())
    opdaterLagoversikt(navn, tempID)
    lagNyttLag(navn, tempID)
    return str(tempID)
    # redirect("/lagoversikt")
    # redirect("/lag/")
    #redirect(url_for('editlag', id=tempID))

@app.route("/lag/<id>", methods=["POST"])
def lag(id):
    #laget = hentLag(id)
    indata = eval(request.data)
    opdaterLag(indata, id)
    return 200

@app.route("/lag/<id>/edit")
def editLag(id):
    print("HIT")
    laget = hentLag(id)
    if laget == False:
        return "LAGET FINNES IKKE"
    else:
        print(laget)
        return render_template("interface/lageditor.html", user=current_user, lag=laget, alleSpillere=spillerListe)
@app.route("/lag/<id>/save", methods=["POST"])
def lagreLag(id):
    print("\n\n\n REQUEST")
    print(request)
    indata = request.data
    indata = eval(request.data)
    print(indata)
    with open("jsonFiles/lag/"+id+".json", "w") as f:
        json.dump(indata, f)
    print("saved - " + id)
    return "Saved"

@app.route("/lag/<id>/delete")
def deleteLag(id):
    copiedDict = getOversikt().copy()
    if(os.path.exists("jsonFiles/lag/"+id+".json")):
        os.remove("jsonFiles/lag/"+id+".json")
    del copiedDict[id]
    #Lagrer oversikten som json
    lagreLagoversikt(copiedDict)
    oppdaterOversikt(copiedDict)
    return "Deleted"

    
@app.route("/spillere/oversikt")
def spillerOversikt():
    return render_template("interface/spillerOversikt.html", spillere = spillerListe)

@app.route("/spillere/<id>/stream")
def spillerTilStream(id):
    spiller = None
    for spillerLOOP in gamerNoDatabase:
        if spillerLOOP["user"]["id"] == int(id):
            print(spillerLOOP["user"]["id"])
            spiller = spillerLOOP
            break
    if(spiller == None):
        for spillerListeIteration in spillerListe:
            if spillerListeIteration["id"] == int(id):
                print(spillerListeIteration)
                for spillerLOOP in gamerNoDatabase:
                    if spillerLOOP["user"]["name"] == spillerListeIteration["navn"] or spillerLOOP["summonerName"] == spillerListeIteration["lolIngame"]:
                        print(spillerLOOP["user"]["id"])
                        spiller = spillerLOOP
                        break
                break

    return render_template("stream/spiller.html", spiller=spiller)

@app.route("/spillere/json/<id>")
def spillerJson(id):
    spiller = None
    for spillerLOOP in gamerNoDatabase:
        if spillerLOOP["user"]["id"] == int(id):
            print(spillerLOOP["user"]["id"])
            spiller = spillerLOOP
            break
    return jsonify(spiller)
@app.route("/production/spiller/id", methods=["POST"])
def getSpillerJson():
    indata = eval(request.data)
    spillerId = indata["id"]
    spiller = None
    for spillerLOOP in gamerNoDatabase:
        if spillerLOOP["user"]["id"] == int(spillerId):
            print(spillerLOOP["user"]["id"])
            spiller = spillerLOOP
            break
    return jsonify(spiller)
    


@app.route("/caster/dashboard")
def casterDashboard():
    #print("CASTER DASHBOARD")
    #print(hentCurrentKamp())
    #print(currentKampjson)
    return render_template("caster/dashboard.html", alleLag=hentAlleLag(), kamp = currentKampjson, livecontrol = livecontrolJson)

@app.route("/caster/ingame")
def casterIngame():
    return render_template("interface/ingameController.html", kamp = currentKampjson, spillerToFocus=playerToFocusJson, alleSpillere=spillerListe, livecontrol = livecontrolJson)

@app.route("/production/playeroftheGameControl")
def playerOfTheGameControl():
    return render_template("interface/playerOfTheGameControl.html", alleSpillere=spillerListe, casters =casterPlayerOfTheGameJson)

@app.route("/stream/view/playerOfTheGame")
def viewPlayerOfTheGameStream():
    return render_template("stream/viewPlayerOfTheGame.html", casters =casterPlayerOfTheGameJson)

@app.route("/production/playeroftheGameControl/update", methods=["POST"])
def updatePlayerOfTheGameControl():
    indata = eval(request.data)
    global casterPlayerOfTheGameJson
    casterPlayerOfTheGameJson  =indata
    with open("jsonFiles/production/casterPlayerOfTheGame.json","w") as f:
        json.dump(casterPlayerOfTheGameJson, f)
    return "200"


@app.route("/production/livecontrol/view")
@app.route("/production/livecontrol")
def viewLiveControl():
    return render_template("production/livecontrol.html", livecontrol = livecontrolJson)


@app.route("/production/livecontrol/scene/<sceneName>", methods=["GET", "POST"])
def livecontrolSpesificScene(sceneName):
    global livecontrolJson
    if request.method == "GET":
        for category in livecontrolJson:
            for scene in  livecontrolJson[category]:
                if scene == sceneName:
                    return jsonify(livecontrolJson[category][scene])
        #return jsonify(livecontrolJson[sceneName])
    elif request.method =="POST":
        indata = eval(request.data)
        livecontrolJson[sceneName] = indata
        return "200"

@app.route("/production/livecontrolModule/obs")
def livecontrolModuleObs():
    return render_template("production/_modulelivecontrol.html", livecontrol = livecontrolJson)
@app.route("/production/livecontrol/json")
def getLivecontrolJson():
    return jsonify(livecontrolJson)

@app.route("/production/livecontrol/update", methods=["POST"])
def updateLiveControl():
    indata = eval(request.data)
    global livecontrolJson
    livecontrolJson = indata
    print(livecontrolJson)
    socketio.emit("livecontrolupdate", livecontrolJson)
    with open("jsonFiles/production/livecontrol.json", "w") as f:
        json.dump(livecontrolJson, f)
    return "200"

@app.route("/test/ninjaStream")
def viewTestNinjaStream():
    return render_template("testNinja.html")

@app.route("/stream/ingame/playerCams")
def playerCamStreamView():
    return render_template("stream/ingamePlayercams.html", kamp = currentKampjson, kameraOversikt = kameraOversiktJson, liveControlInfo = livecontrolJson)

@app.route("/production/playerCamOverview/json")
def playerCamOverviewJson():
    return jsonify(kameraOversiktJson)
    
@app.route("/production/playerCamOverview/json/update", methods=["POST"])
def playerCamOverviewJsonUPDATE():
    inputData = eval(request.data)
    global kameraOversiktJson
    kameraOversiktJson = inputData
    with open("jsonFiles/production/playerCamOverview.json", "w") as f:
        json.dump(kameraOversiktJson, f)
    return "KampoverSIKT TRUE"

@app.route("/stream/currentkamp")
def streamCurrentKamp():
    return render_template("stream/currentKamp.html", kamp = currentKampjson)

@app.route("/currentKamp/getKamp")
def getCurrentKamp():
    return jsonify(currentKamp)


##### BAKGROUNDS ########

@app.route("/stream/background/animation")
def backgroundAnimation1():
    return render_template("stream/backgroundAnimation.html")
#print(currentKampjson)

@app.route("/stream/background/movingGradient")
def backgroundMovingGradient():
    return render_template("stream/background/movingGradient.html")


@app.route("/stream/upcomingGamesSmall")
def upcomingGamesSmall():
    print(kampoversiktjson)
    customKampoversikt = lagCustomLagoversikt()
    return render_template("stream/upcomingGamesSmall.html", kamper = customKampoversikt)

@app.route("/currentKamp/update", methods=["POST"])
def updateCurrentKamp():
    #print(currentKampjson)
    global currentKampjson
    #print("CURRENT KAMP")
    #print(currentKampjson)
    indata = eval(request.data)
    #print(currentKampjson)
    currentKampjson = indata
    with open("jsonFiles/kamper/currentKamp.json","w") as f:
        json.dump(indata, f)
    print("\n"*10)
    print(currentKampjson)
    return "SUCCESS"

@app.route("/currentKamp/newFromID", methods=["POST"])
def newCurrentMatchPost():
    indata = eval(request.data)
    alleLag = hentAlleLag()
    if (len(indata["id"]) <3):
        kamper = kampoversiktjson.copy()
        kamp = kamper[0]
    else:
        kamp=""
        for kamper in kampoversiktjson:
            if kamper["kampID"] == indata["id"]:
                kamp = kamper
                break
    #print(kampoversiktjson)
    for lag in alleLag:
                if lag["id"] == kamp["lag1ID"]:
                    kamp["lag1"] = lag
                if lag["id"] == kamp["lag2ID"]:
                    kamp["lag2"] = lag
    kamp["lag1"]["score"] = 0
    kamp["lag2"]["score"] = 0
    lag1AllowedCameras = [1,1,1,1,1]
    lag2AllowedCameras = [1,1,1,1,1]
    #kamp[""]
    kamp["allowedCameras"] = {"team1":lag1AllowedCameras, "team2":lag2AllowedCameras}
    global currentKampjson
    currentKampjson = kamp
    lagKameraOversiktJson(currentKampjson)
    print(kamp)
    #print("TEST")
    #lagNyCurrentKamp()
    return "Success"


@app.route("/production/inputStreams/nonedivided")
def inputStreamsNoneDivided():
    return render_template("modules/_fullTeamStreamCamsForSplitting.html", kamp = currentKampjson,kameraOversikt = kameraOversiktJson)
@app.route("/production/streamslinks")
def streamLinksHtml():
    return render_template("modules/_streamLinks.html",kamp = currentKampjson,kameraOversikt = kameraOversiktJson)
@app.route("/production/ingamePlayerCamsWithDelay/")
def ingamePlayerCamsWithDelay():
    return render_template("stream/ingamePlayercamsServerStreamed.html")



#CLEAN JSON DATA REQUESTS
@app.route("/production/jsonData/currentKampJson",methods=["GET"])
def getJsonDataCurrentKampJson():
    return jsonify(currentKampjson)



@app.route("/caster/choosePlayerToFocus")
def viewChoosePlayerToFocus():
    return render_template("interface/choosePlayerToFocus.html", alleSpillere=spillerListe, spillerToFocus=playerToFocusJson)

@app.route("/caster/choosePlayerToFocus/json")
def viewChoosePlayerToFocusJson():
    return jsonify(playerToFocusJson)

@app.route("/caster/choosePlayerToFocus/update", methods=["POST"])
def updateChoosePlayerToFocus():
    indata = eval(request.data)
    global playerToFocusJson
    playerToFocusJson = indata
    with open("jsonFiles/production/playerToFocus.json", "w") as f:
        json.dump(indata, f)
    return "200"

@app.route("/production/twitterMatchImage/<id>")
def twitterMatchImage(id):
    kamptilSide = None
    for kamp in kampoversiktjson:
        if kamp["kampID"] == id:
            kamptilSide = kamp
            break
    return render_template("production/twitterMatchImage.html", kamp = kamptilSide)
@app.route("/production/makeTwitterImage", methods=["POST"])
def makeTwitterImage():
    indata = eval(request.data)
    stringForTwitter = "seleniumScreenshotter.exe" + indata["id"]
    #subprocess.run(['seleniumScreenshotter.exe', indata["id"]])
    os.system("start seleniumScreenshotter.exe "+indata["id"])
    #os.system("exit")
    return "200"

@app.route("/stream/currentMatchPreview")
def currentMatchPreviewStream():
    return render_template("stream/currentMatchPreview.html", kamp=currentKampjson)

@app.route("/stream/ingameOverlay")
def ingameOverlay():
    return render_template("stream/ingameOverlay.html", kamp = currentKampjson)
@app.route("/stream/roster")
def streamRoster():
    return render_template("stream/roster.html", kamp = currentKampjson)

@app.route("/championselectOverlay")
def championselectOverlay():
    print(currentKampjson)
    return render_template("stream/championselectOverlay.html", kamp = currentKampjson)
@app.route("/champselectOld")
def champselectOld():
    return render_template("champselectOld.html", settings=settings)

@app.route("/champselect")
def champselect():
    return render_template("stream/champselect.html", settings=settings)
@app.route("/lobby")
def lobby():
    return render_template("lobby.html")

@app.route("/lobby/json")
def lobbyJson():
    return jsonify(hentJson("lobbyData"))
@app.route("/lobby/timer")
def lobbyTimer():
    return jsonify(hentJson("lobbyTimer"))

@app.route("/champselect2")
def champselect2():
    return render_template("champselect2.html")

@app.route("/champselect/statistics")
def champselectStatistics():
    return render_template("stream/champselectStatistics.html")

@app.route("/statistics/player/<gamerId>")
def statisticsPlayerId(gamerId):
    brukerData = hentPerBrukerData(gamerId)
    #print(brukerData)
    return jsonify(brukerData)

@app.route("/statistics/standings")
def statisticsStandings():
    return render_template("standings.html")
@app.route("/stream/tabell")
def streamTabell():
    providedTabell = None
    if currentKampjson["liga"] == "Telialigaen":
        providedTabell = hentJson("tableStanding")
    else:
        providedTabell = hentJson("TESStanding")
    return render_template("stream/tabell.html", tabell = providedTabell)

@app.route("/statistics/standings/json")
def statisticsStandingsJson():
    print(currentKampjson)
    if(currentKampjson != None):
        if(currentKampjson["liga"] == "Telia Esport Series"):
            #print(currentKampjson["liga"])
            standings = hentJson("TESStanding")
        else:
            #print("Ikke Den nei")
            standings = hentJson("tableStanding")
            #print(standings)
    else:
        standings = hentJson("tableStanding")
    return jsonify(standings)

@app.route("/statistics/json")
def statisticsJson():
    jsonFile = hentJson("database")
    return jsonify(jsonFile)

@app.route("/championselect/websocketUpdate", methods=["POST"])
def updateChampionselectDataFromWebsocketRequest():
    #indata = eval(request.data)
    indata = json.loads(request.data)
    print(indata)
    return "200"

@app.route("/champselect/json")
def champselectJson():
    jsonFile = hentJson("minInfo")
    return jsonify(jsonFile)

@app.route("/champselect/timer")
def champselectTimer():
    jsonFile = hentJson("timer")
    return jsonify(jsonFile)



@app.route("/settings")
def viewSettings():
    return render_template("interface/settings.html", settings=settings)
@app.route("/settings/update", methods=["POST"])
def updateSettings():
    global settings
    settings = eval(request.data)
    with open("jsonFiles/settings.json","w") as f:
        json.dump(settings, f)
    return "200"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

def opdaterLagoversikt(navn, tempID):
    print(lagoversiktjson)
    #lagoversikt["liste"].append([tempID,navn])
    lagoversiktjson[tempID] = navn
    with open("jsonFiles/lag/oversikt.json","w") as f:
        json.dump(lagoversiktjson, f)
    print("OPPDATERT LAGOVERSIKT")

def lagreLagoversikt(oversikt):
    with open("jsonFiles/lag/oversikt.json", "w") as f:
        json.dump(oversikt, f)

def lagEllerRedigerKamp(jsonObject):
    if(jsonObject["kampID"] ==""):
        kampID = str(uuid.uuid4())
        print("UUID")
        jsonObject["kampID"] = kampID
    else:
        kampID = jsonObject["kampID"]
        print("JSON")
    # print("\n"*3)
    # print(jsonObject)
    # print(kampID)
    # print("\n"*3)
    kampoversiktjson.append(jsonObject)
    kampoversiktjson.sort(key = lambda x: (x["dato"], x["tid"]))
    #print(kampoversiktjson)
    with open("jsonFiles/kamper/oversikt.json", "w") as f:
        json.dump(kampoversiktjson, f)
    print("LAGER KAMP- FUNC")

def lagNyttLag(navn, tempID):
    tempDict = {
        "navn": navn,
        "id":tempID,
        "bilde":navn+"_logo.png",
        "tag":"",
        "spill":"",
        "spillere":[
            {
                "rolle":"top",
                "navn":"",
                "spill":"lol"
            },
            {
                "rolle":"jgl",
                "navn":"",
                "spill":"lol"
            },
            {
                "rolle":"mid",
                "navn":"",
                "spill":"lol"
            },
            {
                "rolle":"adc",
                "navn":"",
                "spill":"lol"
            },
            {
                "rolle":"sup",
                "navn":"",
                "spill":"lol"
            },
            {
                "rolle":"chc",
                "navn":"",
                "spill":"lol"
            }
        ]
    }
    with open("jsonFiles/lag/"+tempID+".json","w") as f:
        json.dump(tempDict, f)
    print("LAGET LAG")
def opdaterLag(indata, id):
    with open("jsonFiles/lag/"+id+".json","w") as f:
        json.dump(indata, f)
    opdaterLagoversikt(indata["navn"], id)
    print("OPPDATERT LAG")

def hentAlleLag():
    totalDict = []
    for lag in lagoversiktjson:
        hentetLag = hentLag(lag)
        if(hentetLag != False):
            totalDict.append(hentetLag)  
    return totalDict

def lagCustomLagoversikt():
    alleLag = hentAlleLag()
    print("\n\nKAMPOVERSIKT")
    #print(kampoversiktjson)
    customKampoversikt = kampoversiktjson.copy()
    #customKampoversikt = dict(kampoversiktjson)
    for kamp in customKampoversikt:
            for lag in alleLag:
                if lag["id"] == kamp["lag1ID"]:
                    kamp["lag1"] = lag
                if lag["id"] == kamp["lag2ID"]:
                    kamp["lag2"] = lag
    #print("\n\n\n\n")
    #print(customKampoversikt)
    #print("\n\n\n\n\n")
    #print("\nKAMPOVERSIKT\n")
    #print(kampoversiktjson)
    return customKampoversikt


def lagKameraOversiktJson(currentKamp):
    #Takes in current kamp
    # Creates an overview of all the kameralinks
    global kameraOversiktJson
    lag1Liste = []
    lag2Liste = []
    for player in currentKamp["lag1"]["spillere"]:
        tempID = player["id"]
        if(tempID!=""):
            print(tempID)
            lag1Liste.append(hentKameraLinkerMedId(tempID))
    kameraOversiktJson["lag1"] = lag1Liste
    for player in currentKamp["lag2"]["spillere"]:
        print(player)
        tempID = player["id"]
        if(tempID!=""):
            print(tempID)
            lag2Liste.append(hentKameraLinkerMedId(tempID))
    kameraOversiktJson["lag2"] = lag2Liste
    print(len(lag1Liste), len(lag2Liste))
    for i, spiller in enumerate(kameraOversiktJson["lag1"]):
        spiller["nginxLink"] = "/cam/test"+str(i)+"/index.m3u8"


    for i,spiller in enumerate(kameraOversiktJson["lag2"]):
        spiller["nginxLink"] = "/cam/test"+str(i+8)+"/index.m3u8"
    print(kameraOversiktJson)
    with open("jsonFiles/production/playerCamOverview.json", "w") as f:
        json.dump(kameraOversiktJson, f)
    
def hentKameraLinkerMedId(id):
    if(id == ""):
        return 
    #id = str(id)
    obsNinjaLink = ("spillere/obsninja/"+str(id)+"")
    print(obsNinjaLink)
    return hentJson(obsNinjaLink)
#lagNyCurrentKamp()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
def hentPerBrukerData(bruker = 44513):
    response1 = requests.get(
        "https://www.gamer.no/api/v1/users/"+str(bruker)+"/lolstats",
        headers={"Authorization": "04d8d48c80dfc8f5a1eae4b459ba9253c4ff46caa2ef2cfc2fbea87f4d185ab5"}).json()["response"]
    #print(response1)    
    return response1
#hentPerBrukerData()
##############                   For Compiling Only               ###########################
if __name__ =='__main__':
    
    #app.run(host='0.0.0.0',port=5000, threaded=True)
    socketio.run(app, host='0.0.0.0', port=5000)
    #app.run(debug=True)
    #threading.Thread(target=app.run).start()
##############                   For Compiling Only               ###########################
