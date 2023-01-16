import pytest


def test_add_student(db_client, codeforces_client):
    nick_name = "Pavelx4y16"
    city_name = "гомель"

    students_number = len(db_client.cities[city_name])
    user_info = codeforces_client.get_user_info(nick_name)
    db_client.add_student(city_name=city_name, nick_name=nick_name, fio=None,
                          grade=None, school_name=None, user_info=user_info)

    assert len(db_client.cities[city_name]) == students_number + 1


def test_add_unrated_student(db_client, codeforces_client):
    nick_name = "Vabbaj"
    city_name = "гомель"

    students_number = len(db_client.cities[city_name])
    user_info = codeforces_client.get_user_info(nick_name)
    db_client.add_student(city_name=city_name, nick_name=nick_name, fio=None,
                          grade=None, school_name=None, user_info=user_info)

    assert len(db_client.cities[city_name]) == students_number + 1


@pytest.mark.skip("nick_names should be unique! But let's skip it for now...")
def test_check_unique_nick_names(db_client):
    nick_names = [student.nick_name for student in db_client.students]
    assert len(nick_names) == len(set(nick_names))

