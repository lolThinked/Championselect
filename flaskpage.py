from flask import Flask, render_template, jsonify, url_for, send_from_directory, redirect, request
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from pythonFiles.f_functions import hentInnLagoversikt
import uuid
import json
import os
import requests
app = Flask(__name__)

login= LoginManager(app)
login.login_view = "login"
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


from pythonFiles.models import User

print("Laster inn filer")
kampoversikt = [
    {
        "spill":"League of Legends",
        "tid": "01.02.2021",

    }
]
lagoversiktjson = hentInnLagoversikt()
'''
lagoversikt = {
    "Nordavind":{
        "tag":"NVD",
        "bilde":"Nordavind_logo.png",
        "LoL":{
            "top":"",
            "jgl":"Sharp",
            "mid":"Erixen",
            "adc":"Chrisberg",
            "sup":"Touch",
            "subs":[],
            "coach":""
        }
    }
}
'''


def hentJson(navn):
    with open("jsonFiles/" + navn + ".json", "r") as f:
        return json.load(f)
     
def hentLag(id):
    with open("jsonFiles/lag/"+id+".json", "r") as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("interface/homePage.html", user=current_user, current_user=current_user)

@app.route("/kampeditor")
def kampeditor():
    return render_template("interface/kampeditor.html", user=current_user, kamper=kampoversikt)
    
@app.route("/lagoversikt")
def lagoversikt():
    alleLag = hentAlleLag()
    return render_template("interface/lagoversikt.html", user=current_user, lagoversikt = alleLag)

@app.route("/kampoversikt")
def kampoversikt():
    return render_template("stream/kampoversikt.html", user=current_user, kamper=kampoversikt)

@app.route("/lag/create/<navn>")
def createLag(navn):
    tempID = str(uuid.uuid4())
    opdaterLagoversikt(navn, tempID)
    lagNyttLag(navn, tempID)
    return id
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
    print(laget)
    return render_template("interface/lageditor.html", user=current_user, lag=laget)

@app.route("/lag/<id>/delete")
def deleteLag(id):
    if(os.path.exists("jsonFiles/lag/"+id+".json")):
        os.remove("jsonFiles/lag/"+id+".json")
    del lagoversiktjson[id]
    lagreLagoversikt()
    return "Deleted"

    






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

def lagreLagoversikt():
    with open("jsonFiles/lag/oversikt.json", "w") as f:
        json.dump(lagoversiktjson, f)

def lagNyttLag(navn, tempID):
    tempDict = {
        "navn": navn,
        "id":tempID,
        "bilde":navn+"_logo.png",
        "tag":"",
        "spill":"",
        "spillere":[]
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
        totalDict.append(hentetLag)  
    return totalDict





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
