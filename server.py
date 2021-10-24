import json
from datetime import datetime

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


def places_required_absolute_value(places):
    if places < 0:
        return abs(places)
    else:
        return places


def places_required_is_digit(places):
    if not places.lstrip("-").isdigit():
        return False
    else:
        return True


def format_competition_date(comp_date):
    competition_date = datetime.strptime(comp_date, '%Y-%m-%d %H:%M:%S')
    return competition_date


def competition_is_over(competition):
    competition_date = format_competition_date(competition["date"])
    if competition_date < datetime.now():
        return True
    else:
        return False


def competition_is_full(competition):
    if competition["numberOfPlaces"] == "0":
        return True
    else:
        return False


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club_list = get_club_list(request.form['email'])
    print(club_list)
    if club_list:
        club = get_club_by_email(club_list)
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Sorry, that email was not found.")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = get_club_by_name(club)
    found_competition = get_competition_by_name(competition)

    format_competition_date(found_competition['date'])

    full_competition = competition_is_full(found_competition)

    if found_club and found_competition and full_competition:
        return render_template('welcome.html', club=found_club, competitions=competitions)

    if found_club and found_competition and not competition_is_over(found_competition):
        return render_template('booking.html', club=found_club, competition=found_competition)
    elif found_club and found_competition and competition_is_over(found_competition):
        flash("Booking impossible. Competition is over.")
        return render_template('welcome.html', club=found_club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = get_competition_by_name(request.form['competition'])
    club = get_club_by_name(request.form['club'])

    while not places_required_is_digit(request.form['places']):
        flash("You must enter a number")
        return render_template('booking.html', club=club, competition=competition)

    places_required = int(request.form['places'])
    places_required = places_required_absolute_value(places_required)

    if places_required > 12 or places_required > int(club['points']) or\
            places_required > int(competition['numberOfPlaces']):
        flash("You exceed the number of allowed booking places. Try again.")
        return render_template('booking.html', club=club, competition=competition)

    club['points'] = deducts_club_points(int(club['points']), places_required)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/pointsBoard')
def display_points_board():
    all_clubs = load_clubs()
    return render_template('points_board.html', clubs=all_clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)