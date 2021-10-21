from server import get_club_list, get_club_by_email


def test_should_return_a_list_of_one_club_with_valid_email():
    email = 'john@simplylift.co'
    expected_value = [{
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    }]
    assert get_club_list(email) == expected_value


def test_should_return_an_empty_list_of_club_with_invalid_email():
    email = 'test@test.com'
    expected_value = []
    assert get_club_list(email) == expected_value


def test_should_return_a_club_with_not_empty_list_of_club():
    email = 'john@simplylift.co'
    expected_value = {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }
    assert get_club_by_email(get_club_list(email)) == expected_value


def test_should_return_none_if_list_of_club_is_empty():
    email = []
    expected_value = None
    assert get_club_by_email(get_club_list(email)) == expected_value
