import dash

from codeforces.src.controllers.controllers import register_callbacks
from codeforces.src.views.layout import layout
from dash import html, dcc
from dash.dependencies import Input, Output, State

import settings
from codeforces.src.codeforces_api.api import CodeForcesApi
from codeforces.src.database.data_base import DbClient
from codeforces.src.database.data_classes import Student, SortFields

username = 'user'

app = dash.Dash(__name__)
app.layout = layout
register_callbacks(app)


# @app.callback(Output('cities-tabs-content', 'children'),
#               [Input('cities-tabs', 'value'),
#                Input('add-student-button', 'n_clicks'),
#                Input('remove-student-button', 'n_clicks'),
#                Input('educ-view-button', 'n_clicks'),
#                Input('columns-veiw-button', 'n_clicks'),
#                Input('update-table-button', 'n_clicks'),
#                Input('to-next-grade-button', 'n_clicks'),
#                Input('sort-menu', 'value'),
#                Input('to-prev-grade-button', 'n_clicks'),
#                Input('remove-students-button', 'n_clicks')]
#     , [State('nickname', 'value'),
#        State('add-fio', 'value'),
#        State('grade', 'value'),
#        State('educ', 'value'),
#        State('remove-nickname', 'value')]
#               )
# def render_content(tab, btn1, btn2, btn3, btn4, btn5, btn6, sort_menu, btn7, btn8, nick_name, add_fio, grade, educ,
#                    remove_nickname):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     global username
#     # if (username == 'admin') and ('add-student' in changed_id):
#     #     user_info = codeforces_client.get_user_info(nick_name)
#     #     db_client.add_student(tab, nick_name, add_fio, grade, educ, user_info)
#     if (username == 'admin') and ('remove-student-button' in changed_id):
#         db_client.remove_student(tab, remove_nickname)
#     elif 'educ-view-button' in changed_id:
#         school_view_change()
#     elif 'columns-veiw' in changed_id:
#         last_round_view_change()
#     elif (username == 'admin') and ('update-table-button' in changed_id):
#         students = db_client.students if tab == "область" else db_client.cities[tab]
#         users_contests_info = codeforces_client.get_users_contests(students)
#         db_client.update_users_contests(users_contests_info, students)
#     elif (username == 'admin') and ('to-next-grade-button' in changed_id):
#         db_client.to_next_grade()
#     elif (username == 'admin') and ('to-prev-grade-button' in changed_id):
#         db_client.to_prev_grade()
#     elif (username == 'admin') and ('remove-students-button' in changed_id):
#         db_client.remove_graduated_students()
#     table = create_table(tab, sort_menu)
#     return table


if __name__ == '__main__':
    # with DbClient(url=settings.cities_path) as db_client:
    #     codeforces_client = CodeForcesApi()
    app.run_server(debug=True)
