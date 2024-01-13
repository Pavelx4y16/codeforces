from unittest.mock import Mock

import pytest


def test_get_method(codeforces_client):

    urls = ["api/user.rating?handle=Pavelx4y16",
            "api/user.info?handles=Pavelx4y16"]
    data = [codeforces_client._get(url) for url in urls]

    assert len(data) == 2


def test_get_user_contests(codeforces_client):
    student = Mock()
    student.nick_name = "Pavelx4y16"
    data = codeforces_client.get_user_contests(student)

    assert data


def test_get_user_contests_with_old_nick_name(codeforces_client):
    student = Mock()
    student.nick_name = "-kirito-"
    data = codeforces_client.get_user_contests(student)

    assert data
    assert student.nick_name == "k1r1t0"


def test_get_user_info(codeforces_client):
    user_info = codeforces_client.get_user_info("Pavelx4y16")

    assert user_info['rank'] == "специалист"
    assert user_info['rating'] >= 1000


@pytest.mark.skip(reason="this test takes to long time")
def test_get_users_info(codeforces_client, db_client):
    students = db_client.students
    total = len({student.nick_name for student in students})
    users_info = codeforces_client.get_users_info(students).values()

    assert len(users_info) == total

    failed = len([user_info for user_info in users_info if user_info is None])
    print(f"Failure percentage: {failed / total}")  # failures may be here because of non-existing nick_names


@pytest.mark.skip(reason="this test takes to long time")
def test_get_users_contests(codeforces_client, db_client):
    students = db_client.students
    # todo: why not just len(students) ???
    total = len({student.nick_name for student in students})
    users_contests = codeforces_client.get_users_contests(students).values()

    assert len(users_contests) == total

    failed = len([user_info for user_info in users_contests if user_info is None])
    print(f"Failure percentage: {failed / total}")  # failures may be here because of non-existing nick_names


def test_update_nick_name(codeforces_client):
    # old nick_name is '-kirito-'
    updated_nick_name = codeforces_client.update_nick_name(nick_name="-kirito-")
    assert updated_nick_name == "k1r1t0"

    # if the function is run on actual (not old) nick_name
    updated_nick_name = codeforces_client.update_nick_name(nick_name="k1r1t0")
    assert updated_nick_name == "k1r1t0"
