import pytest
from server import app, POINTS_PER_PLACE


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2022-10-22 13:30:00",
            "numberOfPlaces": "0"
        },
        {
            "name": "Test Competition",
            "date": "2020-08-27 12:00:00",
            "numberOfPlaces": "15"
        },
        {
            "name": "Star Competition",
            "date": "2022-10-22 13:30:00",
            "numberOfPlaces": "20"
        }
    ]


@pytest.fixture
def competition(competitions):
    return competitions[0]


@pytest.fixture
def competition_over(competitions):
    return competitions[2]


@pytest.fixture
def competition_full(competitions):
    return competitions[1]


@pytest.fixture
def club():
    return {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    }


def get_response(client, places, competition, club):
    """A response of post request at the route purchasePlaces

    :param client:
        FlaskClient: Client used to test request
    :param places:
        str: Number of booking places
    :param competition:
        str: The name of the competition
    :param club:
        str: The name of the club
    :return:
        response_class object: response of request, used to get the string representation of the response body.
    """
    return client.post('/purchasePlaces',
                       data={"places": places,
                             "competition": competition,
                             "club": club},
                       follow_redirects=True)


# ERROR 1 --> OK
def test_show_summary_displays_error_message_with_bad_email(client):
    email = "test@test.co"
    response = client.post('/showSummary',
                           data={"email": email},
                           follow_redirects=True)
    expected_flash_message = b"Sorry, that email was not found."
    assert response.status_code == 200
    assert expected_flash_message in response.data


# BUG 2 / BUG 6 --> OK
def test_purchase_places_cannot_use_more_than_their_allowed_points(client, competition, club):
    allowed_points = int(club['points'])
    places = str(allowed_points + 1)
    print(places)

    response = get_response(client, places, competition['name'], club['name'])
    print(response.data)
    expected_message = b"You exceed the number of allowed booking places. Try again"

    assert response.status_code == 200
    assert expected_message in response.data


def test_purchase_places_reddeem_points_deducted_from_points_clubs(client, competition, club):
    club_points = club['points']
    places = "2"
    points_by_place = POINTS_PER_PLACE
    response = get_response(client, places, competition["name"], club["name"])
    available_points_str = f"Points available: {int(club_points) - (points_by_place * int(places))}"
    expected_available_points = bytes(available_points_str, 'utf-8')
    assert response.status_code == 200
    assert expected_available_points in response.data


# BUG 3 --> OK
def test_purchase_places_cannot_book_more_than_12_places(client, competition, club):
    places = "13"
    response = get_response(client, places, competition['name'], club["name"])
    expected_message = b"You exceed the number of allowed booking places. Try again."
    assert response.status_code == 200
    assert expected_message in response.data


def test_book_should_display_max_booking_places_message(client, competition, club):
    response = client.get(f'/book/{competition["name"]}/{club["name"]}')
    expected_message = b"Max booking places per club: 12"
    assert expected_message in response.data


def test_purchase_places_should_display_message_if_booking_more_than_available(client, competition, club):
    competition_places = competition['numberOfPlaces']
    places = str(int(competition_places) + 1)
    response = get_response(client, places, competition['name'], club['name'])
    expected_message = b"You exceed the number of allowed booking places. Try again."
    assert response.status_code == 200
    assert expected_message in response.data


# BUG 5 --> OK

def test_booking_past_competition_is_impossible(client, competition, club):
    response = client.get(f'/book/{competition["name"]}/{club["name"]}')
    expected_message = b"Booking impossible. Competition is over."
    assert response.status_code == 200
    assert expected_message in response.data


#  FEATURE 7 --> OK

def test_pointsboard_endpoint_exists(client):
    response = client.get("/pointsBoard")
    assert response.status_code == 200


def test_should_diplay_points_board(client, club):
    response = client.get('/pointsBoard')
    expected_display = f"<td>{club['name']}</td>"

    assert response.status_code == 200
    assert expected_display in response.data.decode()


# COMPETITION IS FULL

def test_book_should_display_if_competition_is_full(client, competition_full, club):
    response = client.get(f'/book/{competition_full["name"]}/{club["name"]}')
    expected_message = b"Competition is full."

    assert expected_message in response.data
