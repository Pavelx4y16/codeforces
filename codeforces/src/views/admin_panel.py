from dash import html, dcc
from codeforces.src.utils.daq_utils import GraduatedBar

from codeforces.src.utils.dash_utils import show_panel, hide_panel, ComponentIds
from codeforces.src.utils.utils import Delays


def create_add_student_panel():
    return html.Div(children=[html.Div(dcc.Input(id=ComponentIds.NICK_INPUT.value, type='text', placeholder="Ник"),
                                       className="ninputStyle"),
                              html.Div(dcc.Input(id=ComponentIds.FIO_INPUT.value, type='text', placeholder="Фамилия и имя"),
                                       className="inputStyle"),
                              html.Div(dcc.Input(id=ComponentIds.GRADE_INPUT.value,
                                                 type='number', min=0, max=11,
                                                 placeholder="Класс (целое число)",
                                                 className="ninputStyle")),
                              html.Div(dcc.Input(id=ComponentIds.SCHOOL_INPUT.value, type='text', placeholder="Учебное заведение"),
                                       className="inputStyle"),
                              html.Button('Добавить учащегося', id=ComponentIds.ADD_STUDENT_BUTTON.value, className='buttonStyle')
                              ],
                    className='insider', id=ComponentIds.ADD_STUDENT_PANEL.value)


def create_remove_student_panel():
    return html.Div(children=[
                html.Div(dcc.Input(id=ComponentIds.REMOVE_NICK_INPUT.value, type='text', placeholder="Никнейм".format('text')),
                         className="inputStyle"),
                html.Button('Удалить учащегося', id=ComponentIds.REMOVE_STUDENT_BUTTON.value, className='buttonStyle')
            ], className='insider', id=ComponentIds.REMOVE_STUDENT_PANEL.value)


def create_update_contests_panel():
    return html.Div(children=[
                html.Button('Обновить раунды', id=ComponentIds.UPDATE_CONTESTS_BUTTON.value, className='buttonStyle'),
                html.Div(id='container-button-timestamp'),
                GraduatedBar(id=ComponentIds.UPDATE_CONTESTS_PROGRESS_BAR.value,
                             label="Updating Contests...",
                             showCurrentValue=True,
                             min=0, max=100, value=0,
                             style=hide_panel()),
                dcc.ConfirmDialog(id=ComponentIds.UPDATE_CONTESTS_CONFIRM_DIALOG.value, message="Contests Updated!!!"),
                dcc.Interval(ComponentIds.UPDATE_CONTESTS_INTERVAL.value,
                             interval=(Delays.CODE_FORCES.value+1)*1000, disabled=True)
            ])


def create_update_grades_panel(id_, display_value):
    return html.Div(children=[html.Button(display_value, id=id_, className='SbuttonStyle')],
                    style={'display': "inline-block"})


def create_remove_graduated_students_panel():
    return html.Div(children=[html.Button('Удалить выпускников', id=ComponentIds.REMOVE_GRADUATED_BUTTON.value,
                                          className='SbuttonStyle')],
                    style={'display': "inline-block"})


def create_admin_panel(visible=True):
    return html.Div(id=ComponentIds.ADMIN_PANEL.value,
                    children=[create_add_student_panel(),
                              create_remove_student_panel(),
                              create_update_contests_panel(),
                              create_update_grades_panel(id_=ComponentIds.GRADES_UP_BUTTON.value, display_value="+ класс"),
                              create_update_grades_panel(id_=ComponentIds.GRADES_DOWN_BUTTON.value, display_value="- класс"),
                              create_remove_graduated_students_panel()],
                    style=show_panel() if visible else hide_panel())
