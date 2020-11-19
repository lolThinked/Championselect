from flask import Flask, render_template, jsonify, url_for, send_from_directory
import json
import os
import requests
app = Flask(__name__)

def hentJson(navn):
    with open("jsonFiles/" + navn + ".json", "r") as f:
        minInfo = json.load(f)
    return minInfo

@app.route("/")
def home():
    return render_template("homePage.html")

@app.route("/champselect")
def champselect():
    return render_template("champselect.html")

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
    return render_template("champselectStatistics.html")

@app.route("/statistics/player/<gamerId>")
def statisticsPlayerId(gamerId):
    brukerData = hentPerBrukerData(gamerId)
    #print(brukerData)
    return jsonify(brukerData)

@app.route("/statistics/standings")
def statisticsStandings():
    return render_template("standings.html")

@app.route("/statistics/standings/json")
def statisticsStandingsJson():
    standings = hentJson("tableStanding")
    return jsonify(standings)

@app.route("/statistics/json")
def statisticsJson():
    jsonFile = hentJson("database")
    return jsonify(jsonFile)

@app.route("/champselect/json")
def champselectJson():
    jsonFile = hentJson("minInfo")
    return jsonify(jsonFile)

@app.route("/champselect/timer")
def champselectTimer():
    jsonFile = hentJson("timer")
    return jsonify(jsonFile)
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
    app.run(host='0.0.0.0',port=5000)
    #app.run(debug=True)
    #threading.Thread(target=app.run).start()
##############                   For Compiling Only               ###########################
