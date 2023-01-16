import dash

from codeforces.src.controllers.controllers import register_callbacks
from codeforces.src.views.layout import layout

app = dash.Dash(__name__)
app.layout = layout
register_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True)
