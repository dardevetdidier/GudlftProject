from server import get_club_list, get_club_by_email, get_club_by_name, get_competition_by_name, deducts_club_points


# ERROR 1
# def test_should_return_a_list_of_one_club_with_valid_email():
#     email = 'john@simplylift.co'
#     expected_value = [{
#         "name":"Simply Lift",
#         "email":"john@simplylift.co",
#         "points":"13"
#     }]
#     assert get_club_list(email) == expected_value
#
#
# def test_should_return_an_empty_list_of_club_with_invalid_email():
#     email = 'test@test.com'
#     expected_value = []
#     assert get_club_list(email) == expected_value
#
#
# def test_should_return_a_club_with_not_empty_list_of_club():
#     email = 'john@simplylift.co'
#     expected_value = {
#         "name": "Simply Lift",
#         "email": "john@simplylift.co",
#         "points": "13"
#     }
#     assert get_club_by_email(get_club_list(email)) == expected_value
#
#
# def test_should_return_none_if_list_of_club_is_empty():
#     email = []
#     expected_value = None
#     assert get_club_by_email(get_club_list(email)) == expected_value


def test_should_return_a_club_with_valid_name():
    name = 'Iron Temple'
    club = get_club_by_name(name)
    expected_value = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }
    assert club == expected_value


def test_should_return_none_with_invalid_name():
    name = 'test name'
    club = get_club_by_name(name)
    expected_value = None
    assert club == expected_value


def test_should_return_a_competition_with_valid_name():
    name = 'Spring Festival'
    competition = get_competition_by_name(name)
    print(f"competition = {competition}")
    expected_value = {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": 20
        }
    assert competition == expected_value


def test_get_competition_by_name_should_return_none_with_invalid_name():
    name = 'test name'
    competition = get_competition_by_name(name)

    expected_value = None
    assert competition == expected_value


def test_should_deduct_points_club():
    club_points = "12"
    places = 5
    expected_value = 7
    assert deducts_club_points(club_points, places) == expected_value

