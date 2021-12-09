import json
from flask import Flask, render_template, request, redirect, flash, url_for, session
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'projet_unit_test'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary(): # 
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        if club in clubs:
            return render_template('welcome.html',club = club, competitions = competitions), 200
    except:
        flash("Sorry, this email doesn't exist !")
        return render_template('index.html'), 403

@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        thisClub = [c for c in clubs if c['name'] == club][0]
        thisCompetition = [c for c in competitions if c['name'] == competition][0]
        if thisClub and thisCompetition:
            color = ('success', 'danger disabled')[int(datetime.timestamp(datetime.strptime(thisCompetition['date'], "%Y-%m-%d %H:%M:%S"))) <= int(datetime.timestamp(datetime.now()))]
            return render_template('booking.html',club = thisClub, competition = thisCompetition, color = color)
    except:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club = club, competitions = competitions), 400


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])

        if int(club["points"]) < (placesRequired*3):
            flash("Not enought points !")
            codeError = 403

        elif int(placesRequired) <= 0:
            flash('Invalid amount of requiered places')
            codeError = 403

        elif (placesRequired) > int(competition["numberOfPlaces"]):
            flash("Not enought places available !")
            codeError = 403

        elif int(placesRequired) > 12:
            flash('Too many places requiered')
            codeError = 403

        elif int(datetime.timestamp(datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S"))) <= int(datetime.timestamp(datetime.now())):
            flash('Old date, booking impossible !')
            codeError = 403

        elif int(club["points"]) > 0:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - (placesRequired*3)
            flash('Great-booking complete!')
            codeError = 200
            
    except:
        flash("Something went wrong-please try again")
        codeError = 403

    return render_template('welcome.html', club = club, competitions = competitions), codeError


# TODO: Add route for points display
@app.route('/pointsDiplay')
def pointsDiplay():
    return render_template('dashboard.html', clubs = clubs)


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash("You're now disconnected")
    return redirect(url_for('index')), 302


# fixed
if __name__ == '__main__':
    app.run(debug=True)