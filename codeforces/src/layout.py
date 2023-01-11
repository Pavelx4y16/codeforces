from dash import html, dcc

from codeforces.src.database.data_classes import Student, SortFields

layout = html.Div(children=[
    html.Div(
        dcc.Tabs(id='cities-tabs', value='гомель', children=[
            dcc.Tab(label='Гомель', value='гомель', className="tabStyle"),
            dcc.Tab(label='Мозырь', value='мозырь', className="tabStyle"),
            dcc.Tab(label='Светлогорск', value='светлогорск', className="tabStyle"),
            dcc.Tab(label='Гомельская область', value='область', className="tabStyle")
        ], parent_className="tabzStyle", className="tabzConteiner")),
    html.Div(children=[
        html.Div(children=[
            html.Button('Изменить кол-во выводимых столбцов', id='columns-veiw-button', n_clicks=0,
                        className='SbuttonStyle')
        ], className='insider'),
        html.Div(children=[
            dcc.RadioItems(
                id="sort-menu",
                options=[
                    {'label': 'Сортировать по рейтингу', 'value': SortFields.RATING.value},
                    {'label': 'Сортировать по ФИО', 'value': SortFields.FIO.value},
                    {'label': 'Сортировать по классу', 'value': SortFields.GRADE.value},
                    {'label': 'Сортировать по дате последнего участия', 'value': SortFields.DATE.value}
                ],
                value='rating'
            )
        ]),
        html.Div(children=[
            html.Button('Изменить вывод учебных заведений', id='educ-view-button', n_clicks=0, className='SbuttonStyle')
        ], className='insider'),
        html.Div(children=[
            html.Div(dcc.Input(id='admin-input', type='text', placeholder="Ключ(для админа)".format('text')),
                     className="inputStyle"),
            html.Button('Ввод', id='admin-button', n_clicks=0, className='buttonStyle')
        ], className='insider')
    ], className='style1'),
    html.Div(id='admin-panel', children=[
        html.Div(children=[
            html.Div(dcc.Input(id='nickname', type='text', placeholder="Ник".format('text')), className="ninputStyle"),
            html.Div(dcc.Input(id='add-fio', type='text', placeholder="Фамилия и имя".format('text')),
                     className="inputStyle"),
            html.Div(dcc.Input(id='grade', type='text', placeholder="Класс".format('text'), className="ninputStyle")),
            html.Div(dcc.Input(id='educ', type='text', placeholder="Учебное заведение(Без запятых)".format('text')),
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
        html.Tr(),
        html.Div(children=[
            html.Button('Удалить выпускников', id='remove-students-button', n_clicks=0, className='SbuttonStyle')
        ], style={'display': 'none'})
    ], className="style1"),
    html.Div(
        children=[
            html.Div(id='cities-tabs-content')
        ],
        className='divStyle')]
    , id='layout')
