import pytest


def test_get_method(codeforces_client):

    urls = ["user.rating?handle=Pavelx4y16",
            "user.info?handles=Pavelx4y16"]
    data = [codeforces_client._get(url) for url in urls]

    assert len(data) == 2


def test_get_contests(codeforces_client):
    data = codeforces_client.get_user_contests("Pavelx4y16")

    assert len(data) == 5


def test_get_user_info(codeforces_client):
    user_info = codeforces_client.get_user_info("Pavelx4y16")

    assert user_info['rank'] == "специалист"
    assert user_info['rating'] >= 1000


@pytest.mark.skip(reason="this test takes to long time")
def test_get_users_info(codeforces_client, db_client):
    students = db_client.students
    users_info = list(codeforces_client.get_users_info(students))

    total = len(students)
    assert len(users_info) == total

    failed = len([user_info for user_info in users_info if user_info is None])
    print(f"Failure percentage: {failed / total}")  # failures may be here because of non-existing nick_names


@pytest.mark.skip(reason="this test takes to long time")
def test_get_users_contests(codeforces_client, db_client):
    students = db_client.students
    users_contests = list(codeforces_client.get_users_contests(students))

    total = len(students)
    assert len(users_contests) == total

    failed = len([user_info for user_info in users_contests if user_info is None])
    print(f"Failure percentage: {failed / total}")  # failures may be here because of non-existing nick_names
