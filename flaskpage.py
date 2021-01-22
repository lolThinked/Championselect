from flask import Flask, render_template, jsonify, url_for, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
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
lagoversikt = {
    "Nordavind":{
        "tag":"NVD",
        "bilde":"nvd.png",
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



def hentJson(navn):
    with open("jsonFiles/" + navn + ".json", "r") as f:
        minInfo = json.load(f)
    return minInfo

@app.route("/")
def home():
    return render_template("homePage.html", user=current_user, current_user=current_user)

@app.route("/kampoversikt")
def kampeditor():
    return render_template("kampeditor.html", user=current_user, kamper=kampoversikt)
@app.route("/lagoversikt")
def lagoversikt():
    return render_template("lagoversikt.html", user=current_user, lagoversikt = lagoversikt)




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
