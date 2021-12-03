import json
from flask import Flask, render_template, request, redirect, flash, url_for, session

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
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        if club in clubs:    
            return render_template('welcome.html',club=club,competitions=competitions)
    except:
        error = 'Sorry, this doesn\'t exist !'
        return render_template('index.html', error = error), 403


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',club = foundClub, competition = foundCompetition)
    except:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club = club, competitions = competitions), 400


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])

        if int(club["points"]) < (placesRequired * 3):
            flash("Not enought points !")
        elif placesRequired > int(competition["numberOfPlaces"]):
            flash("Not enought places availible !")
        elif int(placesRequired) >= 12:
            flash('Too many places requiered')
        elif int(club["points"]) > 0:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - (placesRequired *3)
            flash('Great-booking complete!')
    except Exception as error:
        flash("Something went wrong-please try again")
        print(error)
    return render_template('welcome.html', club=club, competitions=competitions), 403


# TODO: Add route for points display


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# fixed
if __name__ == '__main__':
    app.run(debug=True)