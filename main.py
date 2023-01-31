import dash
import dash_bootstrap_components.themes

from codeforces.src.controllers.controllers import register_callbacks
from codeforces.src.views.layout import layout

app = dash.Dash(__name__, title="CodeForces", update_title="Working, don't press any button...")
app.layout = layout
register_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=False)
