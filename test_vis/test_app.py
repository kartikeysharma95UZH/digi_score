import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
from dash.dependencies import Input, Output

# Sample data (replace with your actual data)
data_home = {
    'Website': ['example1', 'example2', 'example3', 'example4', 'example5', 'example6', 'example7', 'example8', 'example9', 'example10'],
    'digital_score': [0.94, 0.45, 0.64, 0.96, 0.92, 0.83, 0.76, 0.67, 0.73, 0.97]
}
df_home = pd.DataFrame(data_home)

# Count websites in different score ranges
bad_score_count = len(df_home[df_home['digital_score'] < 0.5])
average_score_count = len(df_home[(df_home['digital_score'] >= 0.5) & (df_home['digital_score'] < 0.85)])
good_score_count = len(df_home[df_home['digital_score'] >= 0.85])

# Set threshold values
threshold_poor = 0.5
threshold_average = 0.85

# Create bar charts
fig_home = go.Figure(data=[
    go.Bar(name='Poor Websites', x=['Score Range'], y=[bad_score_count], marker_color='red'),
    go.Bar(name='Average Websites', x=['Score Range'], y=[average_score_count], marker_color='yellow'),
    go.Bar(name='Good Websites', x=['Score Range'], y=[good_score_count], marker_color='green')
])

# Set layout
fig_home.update_layout(title='Website Status by Score Range', barmode='group')

# Define color map for table rows
color_map = {
    'Poor Websites': 'red',
    'Average Websites': 'yellow',
    'Good Websites': 'green'
}

# Create Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    dcc.Tabs(id="tabs", value="tab-home", children=[
        dcc.Tab(label="Home", value="tab-home"),
        dcc.Tab(label="Page 1", value="tab-page1")
    ]),
    html.Div(id="tab-content")
])

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_content(tab):
    if tab == "tab-home":
        return html.Div([
            html.H1("Website Status"),
            dcc.Graph(id='status-graph', figure=fig_home),
            html.H2("Website Count by Category and Thresholds"),
            dash_table.DataTable(
                id='status-table',
                columns=[{"name": "Category", "id": "Category"}, {"name": "Threshold", "id": "Threshold"}, {"name": "Count", "id": "Count"}],
                data=[
                    {"Category": "Poor Websites", "Threshold": f"Below {threshold_poor}", "Count": bad_score_count},
                    {"Category": "Average Websites", "Threshold": f"{threshold_poor} - {threshold_average}", "Count": average_score_count},
                    {"Category": "Good Websites", "Threshold": f"Above {threshold_average}", "Count": good_score_count}
                ],
                style_data_conditional=[
                    {
                        'if': {'row_index': 0},
                        'backgroundColor': color_map['Poor Websites']
                    },
                    {
                        'if': {'row_index': 1},
                        'backgroundColor': color_map['Average Websites']
                    },
                    {
                        'if': {'row_index': 2},
                        'backgroundColor': color_map['Good Websites']
                    }
                ]
            )
        ])
    elif tab == "tab-page1":
        return dcc.Location(id='url-page1', href='/page1', refresh=True)

@app.callback(
    Output("url-page1", "pathname"),
    Input("status-graph", "clickData")
)
def navigate_to_page1(click_data):
    if click_data is not None:
        return '/page1'

if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)
