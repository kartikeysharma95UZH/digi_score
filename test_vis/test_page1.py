
import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

# Sample data (replace with your actual data)
data = {
    'Website': ['example1', 'example2', 'example3', 'example4', 'example5', 'example6', 'example7', 'example8', 'example9', 'example10'],
    'multilingual': ['yes', 'no', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'yes'],
    'attachments': [12, 0, 1, 22, 56, 23, 32, 8, 18, 23],
    'payment': ['yes', 'no', 'no', 'no', 'yes', 'yes', 'no', 'yes', 'yes', 'no'],
    'formulare': ['yes', 'yes', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'yes'],
    'contact_info': ['yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'yes'],
    'chatbot': ['no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no'],
    'socialmedia': ['yes', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'no', 'yes', 'yes'],
    'digital_score': [0.94, 0.75, 0.64, 0.96, 0.92, 0.83, 0.76, 0.67, 0.73, 0.97]
}
df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Digital Scores"),
    dcc.Graph(
        id='digital-scores',
        figure=px.bar(df, x='Website', y='digital_score', title="Digital Scores")
    ),
    dcc.RangeSlider(
        id='score-slider',
        min=df['digital_score'].min(),
        max=df['digital_score'].max(),
        marks={score: str(score) for score in df['digital_score']},
        value=[df['digital_score'].min(), df['digital_score'].max()],
    ),
    dcc.Input(
        id='website-input',
        type='text',
        placeholder='Enter website name...',
    ),
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(
        id="individual-scores-container"  # Placeholder for the individual scores graphs
    )
])

@app.callback(
    Output('digital-scores', 'figure'),
    Input('score-slider', 'value'),
    State('website-input', 'value'),
    State('search-button', 'n_clicks')
)
def update_digital_scores(slider_range, website_name, n_clicks):
    filtered_data = df[(df['digital_score'] >= slider_range[0]) & (df['digital_score'] <= slider_range[1])]
    if website_name:
        filtered_data = filtered_data[filtered_data['Website'].str.contains(website_name, case=False)]
    
    fig = px.bar(filtered_data, x='Website', y='digital_score', title="Digital Scores")
    return fig

@app.callback(
    Output("individual-scores-container", "children"),  # Update children property of the placeholder div
    Input("digital-scores", "clickData")
)
def update_individual_scores(click_data):
    if click_data is None:
        return []

    selected_website = click_data['points'][0]['x']
    website_data = df[df["Website"] == selected_website]
    individual_scores = website_data.iloc[:, 1:-1]  # Exclude the website and digital_score columns

    fig = go.Figure()

    for column in individual_scores:
        value = individual_scores[column].values[0]
        color = "green" if value == "yes" or (column == "attachments" and value > 0) else "red"

        fig.add_trace(
            go.Bar(
                x=[column],
                y=[1],  # Dummy value to create a bar
                marker=dict(color=color),
                showlegend=False,
            )
        )

    fig.update_layout(
        title=f"Individual Scores for {selected_website}",
        xaxis_title="Categories",
        yaxis_title="",
        barmode="group",
    )

    return [dcc.Graph(figure=fig)]


if __name__ == '__main__':
    app.run_server(debug=True)




# import dash
# from dash import dcc
# from dash import html
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from dash.dependencies import Input, Output

# # Sample data (replace with your actual data)
# data = {
#     'Website': ['example1', 'example2', 'example3', 'example4', 'example5', 'example6', 'example7', 'example8', 'example9', 'example10'],
#     'multilingual': ['yes', 'no', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'yes'],
#     'attachments': [12, 0, 1, 22, 56, 23, 32, 8, 18, 23],
#     'payment': ['yes', 'no', 'no', 'no', 'yes', 'yes', 'no', 'yes', 'yes', 'no'],
#     'formulare': ['yes', 'yes', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'yes'],
#     'contact_info': ['yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'yes'],
#     'chatbot': ['no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no'],
#     'socialmedia': ['yes', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'no', 'yes', 'yes'],
#     'digital_score': [0.94, 0.75, 0.64, 0.96, 0.92, 0.83, 0.76, 0.67, 0.73, 0.97]
# }
# df = pd.DataFrame(data)

# app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.H1("Digital Scores"),
#     dcc.Graph(
#         id='digital-scores',
#         figure=px.bar(df, x='Website', y='digital_score', title="Digital Scores")
#     ),
#     dcc.RangeSlider(
#         id='score-slider',
#         min=df['digital_score'].min(),
#         max=df['digital_score'].max(),
#         marks={score: str(score) for score in df['digital_score']},
#         value=[df['digital_score'].min(), df['digital_score'].max()],
#     ),
#     html.Div(
#         id="individual-scores-container"  # Placeholder for the individual scores graphs
#     )
# ])

# @app.callback(
#     Output('digital-scores', 'figure'),
#     Input('score-slider', 'value')
# )
# def update_digital_scores(slider_range):
#     filtered_data = df[(df['digital_score'] >= slider_range[0]) & (df['digital_score'] <= slider_range[1])]
    
#     fig = px.bar(filtered_data, x='Website', y='digital_score', title="Digital Scores")
#     return fig

# @app.callback(
#     Output("individual-scores-container", "children"),  # Update children property of the placeholder div
#     Input("digital-scores", "clickData")
# )
# def update_individual_scores(click_data):
#     if click_data is None:
#         return []

#     selected_website = click_data['points'][0]['x']
#     website_data = df[df["Website"] == selected_website]
#     individual_scores = website_data.iloc[:, 1:-1]  # Exclude the website and digital_score columns

#     fig = go.Figure()

#     for column in individual_scores:
#         value = individual_scores[column].values[0]
#         color = "green" if value == "yes" or (column == "attachments" and value > 0) else "red"

#         fig.add_trace(
#             go.Bar(
#                 x=[column],
#                 y=[1],  # Dummy value to create a bar
#                 marker=dict(color=color),
#                 showlegend=False,
#             )
#         )

#     fig.update_layout(
#         title=f"Individual Scores for {selected_website}",
#         xaxis_title="Categories",
#         yaxis_title="",
#         barmode="group",
#     )

#     return [dcc.Graph(figure=fig)]


# if __name__ == '__main__':
#     app.run_server(debug=True)

