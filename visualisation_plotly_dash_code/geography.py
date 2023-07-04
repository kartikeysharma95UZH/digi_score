import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

# Read the dataset into a pandas DataFrame
data = pd.read_csv('locations_100.csv')

# Calculate the average digital score for each country
average_scores = data.groupby('country')['digital_score'].mean().reset_index()

# Sort the average_scores DataFrame in descending order
average_scores = average_scores.sort_values('digital_score', ascending=False)

# Set up the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H1('Average Digital Score by Country')),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(
                                        id='average-score-chart',
                                        figure=px.choropleth(
                                            average_scores,
                                            locations='country',
                                            locationmode='country names',
                                            color='digital_score',
                                            color_continuous_scale='blues',
                                            labels={'digital_score': 'Average Digital Score'},
                                            title='Average Digital Score by Country',
                                        ).update_geos(
                                            scope='world',
                                            projection=dict(type='natural earth'),
                                            showcountries=True,
                                            showcoastlines=True,
                                            lataxis=dict(range=[-60, 90]),
                                            lonaxis=dict(range=[-180, 180])
                                        ),
                                        style={'height': '600px'}
                                    ),
                                    width=18
                                ),
                                dbc.Col(
                                    dcc.Graph(
                                        id='country-bar-chart',
                                        config={'displayModeBar': False},
                                        style={'height': '400px', 'width': '150%'}
                                    )
                                ),
                            ]
                        ),
                        dbc.Row(
                            dbc.Col(
                                dcc.Graph(
                                    id='average-score-bar-chart',
                                    figure=px.bar(
                                        average_scores,
                                        x='country',
                                        y='digital_score',
                                        title='Average Digital Score by Country (Descending Order)',
                                        labels={'country': 'Country', 'digital_score': 'Average Digital Score'},
                                        color='digital_score',
                                        color_continuous_scale='blues',
                                        orientation='v'
                                    ).update_layout(showlegend=False),
                                    style={'height': '700px', 'width': '150%'}
                                )
                            )
                        ),
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    id='selected-country-website-info',
                                    style={'padding': '10px', 'font-weight': 'bold'}
                                )
                            )
                        )
                    ]
                ),
            ]
        ),
    ],
    className='mt-4',
    style={'width': '100%'}
)


# Callback function for updating the bar chart based on the selected country
@app.callback(
    dash.dependencies.Output('country-bar-chart', 'figure'),
    dash.dependencies.Input('average-score-chart', 'clickData')
)
def update_country_bar_chart(click_data):
    if click_data is not None:
        selected_country = click_data['points'][0]['location']
        filtered_data = data[data['country'] == selected_country]
        bar_chart_figure = px.bar(
            filtered_data,
            x='digital_score',
            y='Website',
            orientation='h',
            title=f'Digital Score Distribution - {selected_country}',
            labels={'digital_score': 'Digital Score', 'Website': 'Website'}
        )
        return bar_chart_figure
    else:
        return px.bar()


# Callback function for displaying website information when clicking on bars
@app.callback(
    dash.dependencies.Output('selected-country-website-info', 'children'),
    dash.dependencies.Input('country-bar-chart', 'clickData')
)
def display_website_info(click_data):
    if click_data is not None:
        selected_country = click_data['points'][0]['y']
        filtered_data = data[data['country'] == selected_country]
        websites = filtered_data['Website'].tolist()
        website_info = html.Ul([html.Li(website) for website in websites])
        return website_info
    else:
        return ''


# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True, port = 8053)


# import pandas as pd
# import plotly.express as px
# import dash
# from dash import dcc
# from dash import html
# import dash_bootstrap_components as dbc

# # Read the dataset into a pandas DataFrame
# data = pd.read_csv('locations_100.csv')

# # Calculate the average digital score for each country
# average_scores = data.groupby('country')['digital_score'].mean().reset_index()

# # Sort the average_scores DataFrame in descending order
# average_scores = average_scores.sort_values('digital_score', ascending=False)

# # Set up the Dash application
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# # Define app layout
# app.layout = dbc.Container(
#     [
#         dbc.Card(
#             [
#                 dbc.CardHeader(html.H1('Average Digital Score by Country')),
#                 dbc.CardBody(
#                     [
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     dcc.Graph(
#                                         id='average-score-chart',
#                                         figure=px.choropleth(
#                                             average_scores,
#                                             locations='country',
#                                             locationmode='country names',
#                                             color='digital_score',
#                                             color_continuous_scale='blues',
#                                             labels={'digital_score': 'Average Digital Score'},
#                                             title='Average Digital Score by Country',
#                                         ).update_geos(
#                                             scope='world',
#                                             projection=dict(type='natural earth'),
#                                             showcountries=True,
#                                             showcoastlines=True,
#                                             lataxis=dict(range=[-60, 90]),
#                                             lonaxis=dict(range=[-180, 180])
#                                         ),
#                                         style={'height': '600px'}  # Set the height of the graph
#                                     ),
#                                     width=16
#                                 ),
#                                 dbc.Col(
#                                     dcc.Dropdown(
#                                         id='country-dropdown',
#                                         options=[{'label': country, 'value': country} for country in average_scores['country']],
#                                         value=average_scores['country'].iloc[0],
#                                         style={'width': '100%'}
#                                     ),
#                                     width=6
#                                 ),
#                             ]
#                         ),
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     dcc.Graph(
#                                         id='country-bar-chart',
#                                         config={'displayModeBar': False},
#                                         style={'height': '500px', 'width': '100%'}  # Set the size of the graph
#                                     )
#                                 ),
#                                 dbc.Col(
#                                     dcc.Graph(
#                                         id='average-score-bar-chart',
#                                         figure=px.bar(
#                                             average_scores,
#                                             x='country',
#                                             y='digital_score',
#                                             title='Average Digital Score by Country (Descending Order)',
#                                             labels={'country': 'Country', 'digital_score': 'Average Digital Score'},
#                                             color='digital_score',
#                                             color_continuous_scale='blues',
#                                             orientation='v'
#                                         ).update_layout(showlegend=False),
#                                         style={'height': '500px', 'width': '120%'}  # Set the size of the graph
#                                     )
#                                 )
#                             ]
#                         )
#                     ]
#                 ),
#             ]
#         ),
#     ],
#     className='mt-4',
#     style={'width': '100%'}
# )


# # Callback function for updating the bar chart based on the selected country
# @app.callback(
#     dash.dependencies.Output('country-bar-chart', 'figure'),
#     dash.dependencies.Input('country-dropdown', 'value')
# )
# def update_country_bar_chart(selected_country):
#     filtered_data = data[data['country'] == selected_country]
#     bar_chart_figure = px.bar(
#         filtered_data,
#         x='digital_score',
#         y='Website',
#         orientation='h',
#         title=f'Digital Score Distribution - {selected_country}',
#         labels={'digital_score': 'Digital Score', 'Website': 'Website'}
#     )
#     return bar_chart_figure


# # Run the Dash application
# if __name__ == '__main__':
#     app.run_server(debug=True)

