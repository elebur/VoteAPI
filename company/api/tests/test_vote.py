def test_retrieve_without_votes():
    assert 1 == 2


def test_retrieve_with_positive_votes():
    assert 1 == 2


def test_retrieve_with_negative_votes():
    assert 1 == 2


def test_retrieve_on_the_day_without_menus():
    assert 1 == 2


def test_vote():
    assert 1 == 2


def test_vote_multiple_times():
    assert 1 == 2


def test_vote_set_like_then_dislike_for_same_menu():
    assert 1 == 2


def test_vote_by_with_existing_user_id():
    assert 1 == 2


def test_with_someone_else_employee_id():
    """
    When user#1 using their JWT token, but in the
    body they send another employee ID (e.g. user#1 sends ID of the user#2)
    """
    assert 1 == 2
