from dash import html, dcc

from codeforces.src.utils.dash_utils import show_panel, hide_panel, ComponentIds


def create_add_student_panel():
    return html.Div(children=[html.Div(dcc.Input(id=ComponentIds.NICK_INPUT.value, type='text', placeholder="Ник".format('text')),
                                       className="ninputStyle"),
                              html.Div(dcc.Input(id=ComponentIds.FIO_INPUT.value, type='text', placeholder="Фамилия и имя".format('text')),
                                       className="inputStyle"),
                              html.Div(dcc.Input(id=ComponentIds.GRADE_INPUT.value, type='text', placeholder="Класс".format('text'),
                                                 className="ninputStyle")),
                              html.Div(dcc.Input(id=ComponentIds.SCHOOL_INPUT.value, type='text', placeholder="Учебное заведение".format('text')),
                                       className="inputStyle"),
                              html.Button('Добавить учащегося', id=ComponentIds.ADD_STUDENT_BUTTON.value, className='buttonStyle')
                              ],
                    className='insider')


def create_remove_student_panel():
    return html.Div(children=[
                html.Div(dcc.Input(id=ComponentIds.REMOVE_NICK_INPUT.value, type='text', placeholder="Никнейм".format('text')),
                         className="inputStyle"),
                html.Button('Удалить учащегося', id=ComponentIds.REMOVE_STUDENT_BUTTON.value, className='buttonStyle')
            ], className='insider')


def create_update_contests_panel():
    return html.Div(children=[
                html.Button('Обновить раунды', id=ComponentIds.UPDATE_CONTESTS_BUTTON.value, className='buttonStyle'),
                html.Div(id='container-button-timestamp')
            ])


def create_update_grades_panel(id_, display_value):
    return html.Div(children=[html.Button(display_value, id=id_, className='SbuttonStyle')])


def create_remove_graduated_students_panel():
    return html.Div(children=[html.Button('Удалить выпускников', id=ComponentIds.REMOVE_GRADUATED_BUTTON.value,
                                          className='SbuttonStyle')])


def create_admin_panel(visible=True):
    return html.Div(id=ComponentIds.ADMIN_PANEL.value,
                    children=[create_add_student_panel(),
                              create_remove_student_panel(),
                              create_update_contests_panel(),
                              create_update_grades_panel(id_=ComponentIds.GRADES_UP_BUTTON.value, display_value="+ класс"),
                              create_update_grades_panel(id_=ComponentIds.GRADES_DOWN_BUTTON.value, display_value="- класс"),
                              create_remove_graduated_students_panel()],
                    style=show_panel() if visible else hide_panel())
