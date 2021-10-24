import datetime

from server import get_club_list, get_club_by_email, get_club_by_name, get_competition_by_name, deducts_club_points, \
    places_required_absolute_value, places_required_is_digit, format_competition_date, competition_is_over


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


# def test_should_return_a_club_with_valid_name():
#     name = 'Iron Temple'
#     club = get_club_by_name(name)
#     expected_value = {
#         "name": "Iron Temple",
#         "email": "admin@irontemple.com",
#         "points": "4"
#     }
#     assert club == expected_value
#
#
# def test_should_return_none_with_invalid_name():
#     name = 'test name'
#     club = get_club_by_name(name)
#     expected_value = None
#     assert club == expected_value
#
#
# def test_should_return_competition_name_with_valid_name():
#     name = 'Spring Festival'
#     competition = get_competition_by_name(name)
#     print(f"competition = {competition}")
#     expected_value = "Spring Festival"
#     assert competition['name'] == expected_value
#
#
# def test_get_competition_by_name_should_return_none_with_invalid_name():
#     name = 'test name'
#     competition = get_competition_by_name(name)
#
#     expected_value = None
#     assert competition == expected_value
#
#
# def test_should_deduct_points_club():
#     club_points = "12"
#     places = 5
#     expected_value = 7
#     assert deducts_club_points(club_points, places) == expected_value

# def test_negative_places_required_should_return_absolute_value():
#     places_required = -5
#     expected_value = 5
#     assert places_required_absolute_value(places_required) == expected_value
#
#
# def test_positive_places_required_return_positive_value():
#     places_required = 5
#     expected_value = 5
#     assert places_required_absolute_value(places_required) == expected_value
#
#
# def test_places_required_should_return_false_if_not_digit():
#     places_required = "abc"
#     expected_value = False
#     assert places_required_is_digit(places_required) == expected_value
#
#
# def test_places_required_should_return_true_if_is_digit():
#     places_required = "5"
#     expected_value = True
#     assert places_required_is_digit(places_required) == expected_value


# def test_return_date_with_datetime_format():
#     comp_date = "2020-03-27 10:00:00"
#     competition_date = format_competition_date(comp_date)
#     assert isinstance(competition_date, datetime.datetime)
#
#
# def test_return_true_if_competition_is_over():
#     competition = {
#             "name": "Spring Festival",
#             "date": "2020-03-27 10:00:00",
#             "numberOfPlaces": "25"
#     }
#
#     assert competition_is_over(competition) is True
#
#
# def test_return_false_if_competition_is_not_over():
#     competition = {
#         "name": "Spring Festival",
#         "date": "2022-08-12 12:30:00",
#         "numberOfPlaces": "25"
#     }
#     assert competition_is_over(competition) is False

