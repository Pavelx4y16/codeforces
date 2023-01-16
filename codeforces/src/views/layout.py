from dash import html, dcc

from codeforces.src.database.data_classes import SortFields
from codeforces.src.utils.dash_utils import ComponentIds
from codeforces.src.views.admin_panel import create_admin_panel

layout = html.Div(children=[
    html.Div(
        dcc.Tabs(id=ComponentIds.TABS.value, value='гомель', children=[
            dcc.Tab(label='Гомель', value='гомель', className="tabStyle"),
            dcc.Tab(label='Мозырь', value='мозырь', className="tabStyle"),
            dcc.Tab(label='Светлогорск', value='светлогорск', className="tabStyle"),
            dcc.Tab(label='Гомельская область', value='область', className="tabStyle")
        ], parent_className="tabzStyle", className="tabzConteiner")),
    html.Div(children=[
        html.Div(children=[html.Button('Изменить кол-во выводимых столбцов',
                                       id=ComponentIds.VIEW_LAST_ROUND_ATTRIBUTES_BUTTON.value,
                                       n_clicks=0, className='SbuttonStyle')
        ], className='insider'),
        html.Div(children=[
            dcc.RadioItems(
                id=ComponentIds.SORT_MENU.value,
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
            html.Button('Изменить вывод учебных заведений', id=ComponentIds.VIEW_SCHOOL_ATTRIBUTES_BUTTON.value, n_clicks=0, className='SbuttonStyle')
        ], className='insider'),
        html.Div(children=[
            html.Div(dcc.Input(id=ComponentIds.PASSWORD_INPUT.value, type='text', placeholder="Ключ(для админа)".format('text')),
                     className="inputStyle"),
            html.Button('Ввод', id=ComponentIds.PASSWORD_BUTTON.value, n_clicks=0, className='buttonStyle')
        ], className='insider')
    ], className='style1'),
    create_admin_panel(visible=False),
    html.Div(
        children=[
            html.Div(id=ComponentIds.TAB_CONTENT.value)
        ],
        className='divStyle')],
    id=ComponentIds.LAYOUT.value)
