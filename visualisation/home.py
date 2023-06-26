import pandas as pd
import plotly.graph_objects as go
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output

# Sample data (replace with your actual data)
data = {
    'Website': ['example1', 'example2', 'example3', 'example4', 'example5', 'example6', 'example7', 'example8', 'example9', 'example10'],
    'digital_score': [0.94, 0.45, 0.64, 0.96, 0.92, 0.83, 0.76, 0.67, 0.73, 0.97]
}
df = pd.DataFrame(data)

# Count websites in different score ranges
bad_score_count = len(df[df['digital_score'] < 0.5])
average_score_count = len(df[(df['digital_score'] >= 0.5) & (df['digital_score'] < 0.85)])
good_score_count = len(df[df['digital_score'] >= 0.85])

# Set threshold values
threshold_poor = 0.5
threshold_average = 0.85

# Create bar charts
fig = go.Figure(data=[
    go.Bar(name='Poor Websites', x=['Score Range'], y=[bad_score_count], marker_color='red'),
    go.Bar(name='Average Websites', x=['Score Range'], y=[average_score_count], marker_color='yellow'),
    go.Bar(name='Good Websites', x=['Score Range'], y=[good_score_count], marker_color='green')
])

# Set layout
fig.update_layout(title='Website Status by Score Range', barmode='group')

# Define color map for table rows
color_map = {
    'Poor Websites': 'red',
    'Average Websites': 'yellow',
    'Good Websites': 'green'
}

def create_home_layout(selected_websites):
    layout = html.Div([
        html.H1("Website Status"),
        dcc.Graph(id='status-graph', figure=fig),
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

    return layout

@app.callback(
    Output('status-graph', 'figure'),
    Input('website-dropdown-home', 'value')
)
def update_home_graph(selected_websites):
    # Update graph based on selected websites (if required)
    return fig
