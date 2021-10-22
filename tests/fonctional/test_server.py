import pytest
from server import app, load_clubs, load_competitions


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def competition():
    return load_competitions()[0]['name']


@pytest.fixture
def club():
    return load_clubs()[0]['name']


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
# def test_show_summary_displays_error_message_with_bad_email(client):
#     email = "test@test.co"
#     response = client.post('/showSummary',
#                            data={"email": email},
#                            follow_redirects=True)
#     expected_flash_message = b"Sorry, that email was not found."
#     assert response.status_code == 200
#     assert expected_flash_message in response.data


# BUG 2 / BUG 6 --> OK
def test_purchase_places_cannot_use_more_than_their_allowed_points(client, competition, club):
    allowed_points = int(load_clubs()[0]['points'])
    places = str(allowed_points + 1)
    print(places)

    response = get_response(client, places, competition, club)
    print(response.data)
    message_str = f"You cannot book more than {str(allowed_points)} points."
    expected_message = bytes(message_str, 'utf-8')
    assert response.status_code == 200
    assert expected_message in response.data


def test_purchase_places_reddeem_points_deducted_from_points_clubs(client, competition, club):
    club_points = load_clubs()[0]['points']
    places = "5"

    response = get_response(client, places, competition, club)
    available_points_str = f"Points available: {int(club_points) - int(places)}"
    expected_available_points = bytes(available_points_str, 'utf-8')
    assert response.status_code == 200
    assert expected_available_points in response.data