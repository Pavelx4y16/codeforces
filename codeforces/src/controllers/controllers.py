from dash.dependencies import Input, Output, State
from dash import ctx

import settings
from codeforces.src.codeforces_api.api import CodeForcesApi
from codeforces.src.database.data_base import DbClient
from codeforces.src.database.data_classes import Student
from codeforces.src.utils.dash_utils import show_panel, hide_panel, ComponentIds
from codeforces.src.views.city_table import create_students_table

db_client = DbClient(url=settings.cities_path)
codeforces_client = CodeForcesApi()


def register_callbacks(app):
    # attach Progress Bar for 'Update Contests' button
    codeforces_client.attach(app.layout[ComponentIds.UPDATE_CONTESTS_PROGRESS_BAR.value])

    @app.callback(Output(component_id=ComponentIds.UPDATE_CONTESTS_PROGRESS_BAR.value, component_property='value'),
                  Input(component_id=ComponentIds.UPDATE_CONTESTS_INTERVAL.value, component_property='n_intervals'),
                  Input(component_id=ComponentIds.UPDATE_CONTESTS_BUTTON.value, component_property='n_clicks'),
                  prevent_initial_call=True)
    def work_with_update_student_contests_progress_bar(*args, **kwargs):
        trigger_id = ComponentIds(ctx.triggered_id)

        if trigger_id is ComponentIds.UPDATE_CONTESTS_BUTTON:
            return 0

        return app.layout[ComponentIds.UPDATE_CONTESTS_PROGRESS_BAR.value].value

    @app.callback(Output(component_id=ComponentIds.UPDATE_CONTESTS_PROGRESS_BAR.value, component_property='style'),
                  Output(component_id=ComponentIds.UPDATE_CONTESTS_INTERVAL.value, component_property='disabled'),
                  Output(component_id=ComponentIds.UPDATE_CONTESTS_CONFIRM_DIALOG.value, component_property='displayed'),
                  Input(component_id=ComponentIds.UPDATE_CONTESTS_PROGRESS_BAR.value, component_property='value'),
                  State(component_id=ComponentIds.UPDATE_CONTESTS_PROGRESS_BAR.value, component_property='max'),
                  Input(component_id=ComponentIds.UPDATE_CONTESTS_BUTTON.value, component_property='n_clicks'),
                  Input(component_id=ComponentIds.UPDATE_CONTESTS_CONFIRM_DIALOG.value, component_property='submit_n_clicks'),
                  Input(component_id=ComponentIds.UPDATE_CONTESTS_CONFIRM_DIALOG.value, component_property='cancel_n_clicks'),
                  prevent_initial_call=True)
    def enable_update_student_contests_progress_bar(progress_bar_value, progress_bar_max_value, *args, **kwargs):
        trigger_id = ComponentIds(ctx.triggered_id)
        if trigger_id is ComponentIds.UPDATE_CONTESTS_BUTTON:
            return show_panel(), False, False
        elif trigger_id is ComponentIds.UPDATE_CONTESTS_PROGRESS_BAR:
            work_is_finished = progress_bar_value == progress_bar_max_value

            return show_panel(), work_is_finished, work_is_finished

        return hide_panel(), True, False

    @app.callback(Output(component_id=ComponentIds.ADMIN_PANEL.value, component_property='style'),
                  State(ComponentIds.PASSWORD_INPUT.value, 'value'),
                  Input(ComponentIds.PASSWORD_BUTTON.value, 'n_clicks'),
                  prevent_initial_call=True)
    def show_admin_panel(password, *args, **kwargs):
        if password == open('getpass.txt').read():
            return show_panel()
        return hide_panel()

    @app.callback(Output(component_id=ComponentIds.ADD_STUDENT_PANEL.value, component_property='style'),
                  Output(component_id=ComponentIds.REMOVE_STUDENT_PANEL.value, component_property='style'),
                  [Input(ComponentIds.TABS.value, 'value')],
                  prevent_initial_call=True)
    def show_city_dependend_functionality(tab_name):
        style = hide_panel() if tab_name == "область" else show_panel()

        return style, style

    @app.callback(Output(component_id=ComponentIds.ADD_STUDENT_BUTTON.value, component_property='disabled'),
                  [Input(component_id=ComponentIds.NICK_INPUT.value, component_property='value')])
    def show_add_button(nick_name):
        return not nick_name

    @app.callback(Output(component_id=ComponentIds.REMOVE_STUDENT_BUTTON.value, component_property='disabled'),
                  [Input(component_id=ComponentIds.REMOVE_NICK_INPUT.value, component_property='value')])
    def show_remove_button(nick_name):
        return not nick_name

    @app.callback(Output(ComponentIds.TAB_CONTENT.value, 'children'),
                  Input(ComponentIds.TABS.value, 'value'),
                  Input(ComponentIds.SORT_MENU.value, 'value'),
                  State(ComponentIds.NICK_INPUT.value, 'value'),
                  State(ComponentIds.FIO_INPUT.value, 'value'),
                  State(ComponentIds.GRADE_INPUT.value, 'value'),
                  State(ComponentIds.SCHOOL_INPUT.value, 'value'),
                  State(ComponentIds.REMOVE_NICK_INPUT.value, 'value'),
                  Input(ComponentIds.ADD_STUDENT_BUTTON.value, 'n_clicks'),
                  Input(ComponentIds.REMOVE_STUDENT_BUTTON.value, 'n_clicks'),
                  Input(ComponentIds.VIEW_SCHOOL_ATTRIBUTES_BUTTON.value, 'n_clicks'),
                  Input(ComponentIds.VIEW_LAST_ROUND_ATTRIBUTES_BUTTON.value, 'n_clicks'),
                  Input(ComponentIds.UPDATE_CONTESTS_BUTTON.value, 'n_clicks'),
                  Input(ComponentIds.GRADES_UP_BUTTON.value, 'n_clicks'),
                  Input(ComponentIds.GRADES_DOWN_BUTTON.value, 'n_clicks'),
                  Input(ComponentIds.REMOVE_GRADUATED_BUTTON.value, 'n_clicks'))
    def process_tab_operations(tab_name, sort_kind, nick_name, fio, grade, school_name, remove_nick_name,
                               *args, **kwargs):
        if ctx.triggered_id:
            trigger_id = ComponentIds(ctx.triggered_id)
            if trigger_id is ComponentIds.ADD_STUDENT_BUTTON:
                add_student(tab_name, nick_name, fio, grade, school_name)
            elif trigger_id is ComponentIds.REMOVE_STUDENT_BUTTON:
                remove_student(tab_name, remove_nick_name)
            elif trigger_id is ComponentIds.VIEW_SCHOOL_ATTRIBUTES_BUTTON:
                change_school_view()
            elif trigger_id is ComponentIds.VIEW_LAST_ROUND_ATTRIBUTES_BUTTON:
                change_last_round_view()
            elif trigger_id is ComponentIds.UPDATE_CONTESTS_BUTTON:
                update_contests(tab_name)
            elif trigger_id is ComponentIds.GRADES_UP_BUTTON:
                to_next_grade()
            elif trigger_id is ComponentIds.GRADES_DOWN_BUTTON:
                to_previous_grade()
            elif trigger_id is ComponentIds.REMOVE_GRADUATED_BUTTON:
                remove_graduated_students(tab_name)

        return create_students_table(db_client=db_client, current_tab=tab_name, sort_kind=sort_kind)


def add_student(tab_name, nick_name, fio, grade, school_name):
    user_info = codeforces_client.get_user_info(nick_name)
    db_client.add_student(tab_name, nick_name, fio, grade, school_name, user_info)


def remove_student(tab_name, nick_name):
    db_client.remove_student(tab_name, nick_name)


def change_school_view():
    Student.view_school_attributes = not Student.view_school_attributes


def change_last_round_view():
    Student.view_last_round_attributes = not Student.view_last_round_attributes


def update_contests(tab_name):
    students = db_client.students if tab_name == "область" else db_client.cities[tab_name]
    users_contests_info = codeforces_client.get_users_contests(students)
    db_client.update_users_contests(users_contests_info, students)


def to_next_grade():
    db_client.to_next_grade()


def to_previous_grade():
    db_client.to_prev_grade()


def remove_graduated_students(tab_name):
    if tab_name == "область":
        tab_name = None
    db_client.remove_graduated_students(tab_name)


