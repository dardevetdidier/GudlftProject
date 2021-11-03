import datetime

from server import get_club_list, get_club_by_email, get_club_by_name, get_competition_by_name, deducts_club_points, \
    places_required_absolute_value, places_required_is_digit, format_competition_date, competition_is_over, \
    competition_is_full


def test_get_club_list_should_return_a_list_of_one_club_with_valid_email():
    """
        Checks if get_club_list function does not return an empty list when a valid email is passed as parameter.
    """
    email = 'john@simplylift.co'
    assert get_club_list(email) != []


def test_get_club_list_should_return_an_empty_list_of_club_with_invalid_email():
    """
        Checks if get_club_list function returns an empty list when an invalid email is passed as parameter.
    """
    email = 'test@test.com'
    expected_value = []
    assert get_club_list(email) == expected_value


def test_should_return_a_club_with_not_empty_list_of_club():
    """
        Checks if the club email returned by get_club_by_email function is the correct email
    """
    email = 'john@simplylift.co'
    assert get_club_by_email(get_club_list(email))["email"] == email


def test_should_return_none_if_list_of_club_is_empty():
    """
        Checks if get_club_by_email function return none if list of clubs is empty.
    """
    email = ""
    expected_value = None
    assert get_club_by_email(get_club_list(email)) == expected_value


def test_should_return_a_club_with_valid_name():
    """
        checks if get_club_by_name function returns the right club by checking its email which must
        correspond to the club whose name was entered as a parameter to the function.
    """
    name = 'Iron Temple'
    club = get_club_by_name(name)
    expected_value = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }
    assert club == expected_value


def test_should_return_none_with_invalid_name():
    """
        Checks if get_club_by_name function returns None if the club name entered as parameter doesn't match with
        any names of clubs.
    """
    name = 'test name'
    club = get_club_by_name(name)
    expected_value = None
    assert club == expected_value


def test_should_return_competition_name_with_valid_name():
    """
       Checks if get_competition_by_name function returns the correct competition
       by checking if names are corresponding.
    """
    name = 'Spring Festival'
    competition = get_competition_by_name(name)
    print(f"competition = {competition}")
    expected_value = "Spring Festival"
    assert competition['name'] == expected_value


def test_get_competition_by_name_should_return_none_with_invalid_name():
    """
        Checks if get_competition_by_name function returns None if
        name entered as parameter does not match any of the names in the competition list.
    """
    name = 'test name'
    competition = get_competition_by_name(name)
    expected_value = None
    assert competition == expected_value


def test_should_deduct_points_club():
    """
        Checks if deducts_club_points function deduts the right numbers of points to total points of the club.
    """
    club_points = "12"
    places = 3
    expected_value = 3
    assert deducts_club_points(club_points, places) == expected_value


def test_negative_places_required_should_return_absolute_value():
    """
    Checks if 'places_required_absolute_value' function returns absolute value of the number of places required is a
    negative number.
    """
    places_required = -5
    expected_value = 5
    assert places_required_absolute_value(places_required) == expected_value


def test_positive_places_required_return_positive_value():
    """
    Checks if 'places_required_absolute_value' function returns the number entered by the user if its a positive number.
    """
    places_required = 5
    expected_value = 5
    assert places_required_absolute_value(places_required) == expected_value


def test_places_required_is_digit_should_return_false_if_not_digit():
    """If the user enters a non digit value, expected 'places_required_is_digit' returns False"""
    places_required = "abc"
    expected_value = False
    assert places_required_is_digit(places_required) == expected_value


def test_places_required_should_return_true_if_is_digit():
    """If the user enters a digit value, expected 'places_required_is_digit' returns True"""
    places_required = "5"
    expected_value = True
    assert places_required_is_digit(places_required) == expected_value


def test_return_date_with_datetime_format():
    """Checks if the date of the competition is converted in datetime type."""
    comp_date = "2020-03-27 10:00:00"
    competition_date = format_competition_date(comp_date)
    assert isinstance(competition_date, datetime.datetime)


def test_return_true_if_competition_is_over():
    """Checks if competition_is_over function returns True if date is past"""
    competition = {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
    }
    assert competition_is_over(competition) is True


def test_return_false_if_competition_is_not_over():
    """Checks if competition_is_over function returns False if date is not past"""
    competition = {
        "name": "Spring Festival",
        "date": "2022-08-12 12:30:00",
        "numberOfPlaces": "25"
    }
    assert competition_is_over(competition) is False


def test_should_return_true_if_competition_is_full():
    """Checks if competition_is_full function returns True if number of places is equal to zero"""
    competition = {
        "name": "Test Competition",
        "date": "2022-08-12 12:30:00",
        "numberOfPlaces": "0"
    }
    assert competition_is_full(competition) is True


def test_should_return_false_if_competition_is_not_full():
    """Checks if competition_is_full function returns False if number of places is not equal to zero"""
    competition = {
        "name": "Test Competition",
        "date": "2022-08-12 12:30:00",
        "numberOfPlaces": "15"
    }
    assert competition_is_full(competition) is False

