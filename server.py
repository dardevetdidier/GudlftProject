import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for

POINTS_PER_PLACE = 3


def load_clubs():
    """
    Function used for testing app. Get all clubs contained in clubs.json file and return a list of clubs.
    :return: list: A list of clubs
    """
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    """
    Function used for testing app. Get all competitions contained in competitions.json file and return a list of
    competitions.
    :return: list: A list of competitions
    """
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def get_club_list(email):
    """
    Get a list of one club whose email matches the one entered by the user.
    If the email does not match, return an empty list.
    :param email: str: An email of a club
    :return: list: A list of one email
    """
    club_list = [club for club in clubs if club['email'] == email]
    return club_list


def get_club_by_email(club_list):
    """
    Function which get a list of one club as parameter and returns this club as dictionary.
    If club_list is empty, return None
    :param club_list: list: A list of club
    :return: dict: A club
    """
    if club_list:
        return club_list[0]
    else:
        return None


def get_club_by_name(name):
    """
    Returns a club if its name matches with the name of a club. Otherwise, returns None
    :param name: str: The name of a club
    :return: dict: A club
    """
    club_list = [c for c in clubs if c['name'] == name]
    if club_list:
        return club_list[0]
    else:
        return None


def get_competition_by_name(name):
    """
    Returns a competition if its name matches with the name of a competition. Otherwise returns None.
    :param name: str: The name of a competition
    :return: dict: A competition.
    """
    competition = [c for c in competitions if c['name'] == name]
    if competition:
        return competition[0]
    else:
        return None


def deducts_club_points(club_points, places, n=POINTS_PER_PLACE):
    """
    Deducts the number of booking places multiplyed by n
    :param club_points: int: Total of the points of the club
    :param places: int: The number of places booking by the club
    :param n: int: Points deducted per one booking place
    :return: int: TOtal points of the club after deduct.
    """
    club_points = int(club_points) - (n * places)
    return club_points


def places_required_absolute_value(places):
    """
    Checks if the number of book places entered by the user is a positive number.
    If it's a valid number returns this number.
    Otherwise returns the absolute value of this number
    :param places: int: The number of places
    :return: int: The absolute value of the number of places
    """
    if places < 0:
        return abs(places)
    else:
        return places


def places_required_is_digit(places):
    """
    Checks if the number of book places entered by the user is a number.
    :param places: str: The input of the user in number of places form.
    :return: Bool: True if 'places' is a number
    """
    if not places.lstrip("-").isdigit():
        return False
    else:
        return True


def format_competition_date(comp_date):
    """
    Transfom the date from string format to datetime format.
    :param comp_date: str: Competition date
    :return: datetime object : The date of the competition
    """
    competition_date = datetime.strptime(comp_date, '%Y-%m-%d %H:%M:%S')
    return competition_date


def competition_is_over(competition):
    """
    Checks if the date of the competition is earlier than the time of the execution of the function.
    :param competition: dict: A competition
    :return: Bool: True if the competition is over.
    """
    competition_date = format_competition_date(competition["date"])
    if competition_date < datetime.now():
        return True
    else:
        return False


def competition_is_full(competition):
    """
    Checks if competiton is full.
    :param competition: dict: A competition
    :return: Bool: True if the competition is full.
    """
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
    # Places required should be positive number
    places_required = places_required_absolute_value(places_required)

    if places_required > 12 or places_required * POINTS_PER_PLACE > int(club['points']) or \
            places_required > int(competition['numberOfPlaces']):
        flash("You exceed the number of allowed booking places. Try again.")
        return render_template('booking.html', club=club, competition=competition)

    club['points'] = deducts_club_points(int(club['points']), places_required)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/pointsBoard')
def display_points_board():
    all_clubs = clubs
    return render_template('points_board.html', clubs=all_clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
