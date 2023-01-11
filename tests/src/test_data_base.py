def test_add_student(db_client, codeforces_client):
    nick_name = "Pavelx4y16"
    city_name = "гомель"

    students_number = len(db_client.cities[city_name])
    user_info = codeforces_client.get_user_info(nick_name)[0]
    db_client.add_student(city_name=city_name, nick_name=nick_name, fio=None,
                          grade=None, school_name=None, user_info=user_info)

    assert len(db_client.cities[city_name]) == students_number + 1

