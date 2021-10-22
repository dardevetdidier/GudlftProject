import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def get_club_list(email):
    club_list = [club for club in clubs if club['email'] == email]
    return club_list


def get_club_by_email(club_list):
    if club_list:
        return club_list[0]
    else:
        return None


def get_club_by_name(name):
    club_list = [c for c in clubs if c['name'] == name]
    print(club_list)
    if club_list:
        return club_list[0]
    else:
        return None


def get_competition_by_name(name):
    competition = [c for c in competitions if c['name'] == name]
    if competition:
        return competition[0]
    else:
        return None


def deducts_club_points(club_points, places):
    club_points = int(club_points) - places
    return club_points


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club_list = [club for club in clubs if club['email'] == request.form['email']]
    print(club_list)
    if club_list:
        club = club_list[0]
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Sorry, that email was not found.")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])

    if places_required > int(club['points']):
        flash(f"You cannot book more than {club['points']} points.")
        return render_template('booking.html', club=club, competition=competition)

    club['points'] = int(club['points']) - places_required
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)