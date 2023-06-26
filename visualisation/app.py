import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from home import create_home_layout, update_home_graph

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='website-dropdown-home',
        options=[
            {'label': 'Website 1', 'value': 'website1'},
            {'label': 'Website 2', 'value': 'website2'},
            {'label': 'Website 3', 'value': 'website3'}
        ],
        value=[]
    ),
    html.Div(id='home-container')
])

@app.callback(
    Output('home-container', 'children'),
    Input('website-dropdown-home', 'value')
)
def update_home_layout(selected_websites):
    return create_home_layout(selected_websites)

if __name__ == '__main__':
    app.run_server(debug=True)
