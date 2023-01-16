from dash.dependencies import Input, Output, State
from dash import ctx

import settings
from codeforces.src.codeforces_api.api import CodeForcesApi
from codeforces.src.database.data_base import DbClient
from codeforces.src.utils.dash_utils import show_panel, hide_panel, ComponentIds
from codeforces.src.views.city_table import create_students_table

db_client = DbClient(url=settings.cities_path)
codeforces_client = CodeForcesApi()


def register_callbacks(app):
    @app.callback(Output(component_id=ComponentIds.ADMIN_PANEL.value, component_property='style'),
                  [Input(ComponentIds.PASSWORD_BUTTON.value, 'n_clicks')], [State(ComponentIds.PASSWORD_INPUT.value, 'value')],
                  prevent_initial_call=True)
    def show_admin_panel(button, password):
        if password == open('getpass.txt').read():
            return show_panel()
        return hide_panel()

    @app.callback(Output(ComponentIds.TAB_CONTENT.value, 'children'),
                  [Input(ComponentIds.TABS.value, 'value'),
                   Input(ComponentIds.ADD_STUDENT_BUTTON.value, 'n_clicks'),
                   Input(ComponentIds.REMOVE_STUDENT_BUTTON.value, 'n_clicks'),
                   Input(ComponentIds.VIEW_SCHOOL_ATTRIBUTES_BUTTON.value, 'n_clicks'),
                   Input(ComponentIds.VIEW_LAST_ROUND_ATTRIBUTES_BUTTON.value, 'n_clicks'),
                   Input(ComponentIds.UPDATE_CONTESTS_BUTTON.value, 'n_clicks'),
                   Input(ComponentIds.GRADES_UP_BUTTON.value, 'n_clicks'),
                   Input(ComponentIds.GRADES_DOWN_BUTTON.value, 'n_clicks'),
                   Input(ComponentIds.REMOVE_GRADUATED_BUTTON.value, 'n_clicks'),
                   Input(ComponentIds.SORT_MENU.value, 'value')],
                  [State(ComponentIds.NICK_INPUT.value, 'value'),
                   State(ComponentIds.FIO_INPUT.value, 'value'),
                   State(ComponentIds.GRADE_INPUT.value, 'value'),
                   State(ComponentIds.SCHOOL_INPUT.value, 'value'),
                   State(ComponentIds.REMOVE_NICK_INPUT.value, 'value')])
    def process_tab_operations(tab_name,
                               add_student_button, remove_student_button, educ_view_button, columns_view_button,
                               update_contests_button, grades_up_button, grades_down_button,
                               remove_graduated_students_button,
                               sort_kind, nick_name, fio, grade, school_name, remove_nick_name):
        if ctx.triggered_id:
            trigger_id = ComponentIds(ctx.triggered_id)
            if trigger_id is ComponentIds.ADD_STUDENT_BUTTON:
                add_student(tab_name, sort_kind, nick_name, fio, grade, school_name)
            elif trigger_id is ComponentIds.REMOVE_STUDENT_BUTTON:
                pass
            elif trigger_id is ComponentIds.VIEW_SCHOOL_ATTRIBUTES_BUTTON:
                pass
            elif trigger_id is ComponentIds.VIEW_LAST_ROUND_ATTRIBUTES_BUTTON:
                pass
            elif trigger_id is ComponentIds.UPDATE_CONTESTS_BUTTON:
                pass
            elif trigger_id is ComponentIds.GRADES_UP_BUTTON:
                pass
            elif trigger_id is ComponentIds.GRADES_DOWN_BUTTON:
                pass
            elif trigger_id is ComponentIds.REMOVE_GRADUATED_BUTTON:
                pass

        return create_students_table(db_client=db_client, current_tab=tab_name, sort_kind=sort_kind)


def add_student(tab_name, sort_kind, nick_name, fio, grade, school_name):
    user_info = codeforces_client.get_user_info(nick_name)
    db_client.add_student(tab_name, nick_name, fio, grade, school_name, user_info)

    return create_students_table(db_client=db_client, current_tab=tab_name, sort_kind=sort_kind)

