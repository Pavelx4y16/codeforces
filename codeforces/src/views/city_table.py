from dash import html

from codeforces.src.database.data_base import DbClient
from codeforces.src.database.data_classes import Student, SortFields, StudentFields


def create_students_table(db_client: DbClient, current_tab, sort_kind):
    if current_tab == "область":
        students = db_client.students
        Student.view_city_name = True
    else:
        Student.view_city_name = False
        students = db_client.cities[current_tab.lower()]

    reverse = sort_kind != SortFields.FIO.value
    students.sort(key=Student.sort_map[SortFields(sort_kind)], reverse=reverse)

    return html.Table([
                html.Thead(
                    html.Tr([html.Th(header) for header in Student.display_headers()])
                ),
                html.Tbody([
                    html.Tr([html.Td(column_value, className=f"columnName{column_name.name.capitalize()}")
                                    for column_name, column_value in student.display().items()])
                                        for student in students
                ])
    ], className="tableStyle")
