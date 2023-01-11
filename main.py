import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

import settings
from codeforces.src.codeforces_api.api import CodeForcesApi
from codeforces.src.database.data_base import DbClient
from codeforces.src.database.data_classes import Student, SortFields
from codeforces.src.layout import layout

username = 'user'

app = dash.Dash(__name__)
app.layout = layout


def last_round_view_change():
    Student.view_last_round_attributes = not Student.view_last_round_attributes


def school_view_change():
    Student.view_school_attributes = not Student.view_school_attributes


def create_table(current_tab, sort_menu):
    if current_tab == "область":
        students = db_client.students
        Student.view_city_name = True
    else:
        Student.view_city_name = False
        students = db_client.cities[current_tab.lower()]

    reverse = sort_menu != SortFields.FIO.value
    students.sort(key=Student.sort_map[SortFields(sort_menu)], reverse=reverse)

    return html.Table([
                html.Thead(
                    html.Tr([html.Th(header) for header in Student.display_headers()])
                ),
                html.Tbody([
                    html.Tr([html.Td(attr) for attr in student.display()]) for student in students
                ])
    ], className="tableStyle")


'''
def create_backup():
    cities = ['гомель.csv', 'мозырь.csv', 'светлогорск.csv']
    cities_backup = ['гомель_backup.csv', 'мозырь_backup.csv', 'светлогорск_backup.csv']
    for i in range(3):
        cdf = pd.read_csv(cities[i])
        cdf.to_csv(cities_backup[i])

def goto_backup():
    cities = ['гомель.csv', 'мозырь.csv', 'светлогорск.csv']
    cities_backup = ['гомель_backup.csv', 'мозырь_backup.csv', 'светлогорск_backup.csv']
    for i in range(3):
        cdf = pd.read_csv(cities_backup[i])
        cdf.to_csv(cities[i])
'''


@app.callback(Output('cities-tabs-content', 'children'),
              [Input('cities-tabs', 'value'),
               Input('add-student-button', 'n_clicks'),
               Input('remove-student-button', 'n_clicks'),
               Input('educ-view-button', 'n_clicks'),
               Input('columns-veiw-button', 'n_clicks'),
               Input('update-table-button', 'n_clicks'),
               Input('to-next-grade-button', 'n_clicks'),
               Input('sort-menu', 'value'),
               Input('to-prev-grade-button', 'n_clicks'),
               Input('remove-students-button', 'n_clicks')]
    , [State('nickname', 'value'),
       State('add-fio', 'value'),
       State('grade', 'value'),
       State('educ', 'value'),
       State('remove-nickname', 'value')]
              )
def render_content(tab, btn1, btn2, btn3, btn4, btn5, btn6, sort_menu, btn7, btn8, nick_name, add_fio, grade, educ,
                   remove_nickname):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    global username
    if (username == 'admin') and ('add-student' in changed_id):
        user_info = codeforces_client.get_user_info(nick_name)
        db_client.add_student(tab, nick_name, add_fio, grade, educ, user_info)
    elif (username == 'admin') and ('remove-student-button' in changed_id):
        db_client.remove_student(tab, remove_nickname)
    elif 'educ-view-button' in changed_id:
        school_view_change()
    elif 'columns-veiw' in changed_id:
        last_round_view_change()
    elif (username == 'admin') and ('update-table-button' in changed_id):
        users_contests_info = codeforces_client.get_users_contests(db_client.students)
        db_client.update_users_contests(users_contests_info)
    elif (username == 'admin') and ('to-next-grade-button' in changed_id):
        db_client.to_next_grade()
    elif (username == 'admin') and ('to-prev-grade-button' in changed_id):
        db_client.to_prev_grade()
    elif (username == 'admin') and ('remove-students-button' in changed_id):
        db_client.remove_graduated_students()
    table = create_table(tab, sort_menu)
    return table


@app.callback(Output('admin-panel', 'children'),
              [Input('admin-button', 'n_clicks')],
              [State('admin-input', 'value')])
def show_admin_panel(button, val):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    keyword = open('getpass.txt').read()
    if ('admin-button' in changed_id) and (val == keyword):
        global username
        if username == 'user':
            username = 'admin'
            return [html.Div(children=[
                html.Div(dcc.Input(id='nickname', type='text', placeholder="Ник".format('text')),
                         className="ninputStyle"),
                html.Div(dcc.Input(id='add-fio', type='text', placeholder="Фамилия и имя".format('text')),
                         className="inputStyle"),
                html.Div(
                    dcc.Input(id='grade', type='text', placeholder="Класс".format('text'), className="ninputStyle")),
                html.Div(dcc.Input(id='educ', type='text', placeholder="Учебное заведение".format('text')),
                         className="inputStyle"),
                html.Button('Добавить учащегося', id='add-student-button', n_clicks=0, className='buttonStyle')
            ], className='insider'),
                html.Div(children=[
                    html.Div(dcc.Input(id='remove-nickname', type='text', placeholder="Никнейм".format('text')),
                             className="inputStyle"),
                    html.Button('Удалить учащегося', id='remove-student-button', n_clicks=0, className='buttonStyle')
                ], className='insider'),
                html.Div(children=[
                    html.Button('Обновить раунды', id='update-table-button', n_clicks=0, className='buttonStyle'),
                    html.Div(id='container-button-timestamp')
                ]),
                html.Div(children=[
                    html.Button('+ класс', id='to-next-grade-button', n_clicks=0, className='SbuttonStyle')
                ]),
                html.Div(children=[
                    html.Button('- класс', id='to-prev-grade-button', n_clicks=0, className='SbuttonStyle')
                ]),
                html.Tr(),
                html.Div(children=[
                    html.Button('Удалить выпускников', id='remove-students-button', n_clicks=0,
                                className='SbuttonStyle')
                ])
            ]
        username = 'user'
    return [html.Div(children=[
        html.Div(dcc.Input(id='nickname', type='text', placeholder="Ник".format('text')), className="ninputStyle"),
        html.Div(dcc.Input(id='add-fio', type='text', placeholder="Фамилия и имя".format('text')),
                 className="inputStyle"),
        html.Div(dcc.Input(id='grade', type='text', placeholder="Класс".format('text'), className="ninputStyle")),
        html.Div(dcc.Input(id='educ', type='text', placeholder="Учебное заведение".format('text')),
                 className="inputStyle"),
        html.Button('Добавить учащегося', id='add-student-button', n_clicks=0, className='buttonStyle')
    ], className='insider', style={'display': 'none'}),
        html.Div(children=[
            html.Div(dcc.Input(id='remove-nickname', type='text', placeholder="Никнейм".format('text')),
                     className="inputStyle"),
            html.Button('Удалить учащегося', id='remove-student-button', n_clicks=0, className='buttonStyle')
        ], className='insider', style={'display': 'none'}),
        html.Div(children=[
            html.Button('Обновить раунды', id='update-table-button', n_clicks=0, className='buttonStyle'),
            html.Div(id='container-button-timestamp')
        ], style={'display': 'none'}),
        html.Div(children=[
            html.Button('+ класс', id='to-next-grade-button', n_clicks=0, className='SbuttonStyle')
        ], style={'display': 'none'}),
        html.Div(children=[
            html.Button('- класс', id='to-prev-grade-button', n_clicks=0, className='SbuttonStyle')
        ], style={'display': 'none'}),
        html.Div(children=[
            html.Button('Удалить выпускников', id='remove-students-button', n_clicks=0, className='SbuttonStyle')
        ], style={'display': 'none'})
    ]


if __name__ == '__main__':
    with DbClient(url=settings.cities_path) as db_client:
        codeforces_client = CodeForcesApi()
        app.run_server(debug=True)
