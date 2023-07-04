import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc

# app = dash.Dash(

# )


# # Sample data (replace with your actual data)
# data = {
#     "Website": [
#         "example1",
#         "example2",
#         "example3",
#         "example4",
#         "example5",
#         "example6",
#         "example7",
#         "example8",
#         "example9",
#         "example10",
#     ],
#     "multilingual": ["yes", "no", "no", "no", "yes", "no", "yes", "yes", "yes", "yes"],
#     "attachments": [12, 0, 1, 22, 56, 23, 32, 8, 18, 23],
#     "payment": ["yes", "no", "no", "no", "yes", "yes", "no", "yes", "yes", "no"],
#     "formulare": ["yes", "yes", "yes", "yes", "no", "no", "yes", "no", "no", "yes"],
#     "contact_info": ["yes", "yes", "yes", "yes", "yes", "no", "no", "yes", "no", "yes"],
#     "chatbot": ["no", "no", "yes", "no", "yes", "no", "no", "no", "yes", "no"],
#     "socialmedia": ["yes", "yes", "no", "yes", "yes", "yes", "yes", "no", "yes", "yes"],
#     "digital_score": [0.94, 0.75, 0.64, 0.96, 0.92, 0.83, 0.76, 0.67, 0.73, 0.97],
# }
# df = pd.DataFrame(data)
df = pd.read_csv("zhaw_websites - Sheet3.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = px.bar(
    df,
    x="Website",
    y="date",
    title="Digital Scores",
)

# fig.update_traces(mode="markers+lines")

# fig.update_layout(
#     hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell")
# )
# 
app.layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader("Digital Scores", style={"align": "centre"}),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        list(df["date"].unique()),
                                        id="date-input",
                                        placeholder="Select the date of scraping",
                                        value=df["date"].unique().max(),
                                    ),
                                    style={
                                        "marginTop": " 10px",
                                        "marginBottom": "10px",
                                        "marginLeft": "430px",
                                    },
                                    width=3,
                                ),
                                dcc.Graph(id="digital-scores", figure=fig),
                                dbc.Col(
                                    [
                                        html.Div(id="website-count"),
                                    ],
                                    style={"align": "right"},
                                ),
                                dbc.Row(
                                    dcc.RangeSlider(
                                        id="score-slider",
                                        min=df["digital_score"].min(),
                                        max=df["digital_score"].max(),
                                        marks={
                                            score: str(score)
                                            for score in df["digital_score"]
                                        },
                                        value=[
                                            df["digital_score"].min(),
                                            df["digital_score"].max(),
                                        ],
                                    ),
                                    style={
                                        "marginTop": " 10px",
                                        "marginBottom": "10px",
                                    },
                                ),
                                dbc.Row(
                                    dcc.Dropdown(
                                        list(df["Website"].unique()), id="website-input"
                                    ),
                                    style={
                                        "marginTop": " 10px",
                                        "marginBottom": "10px",
                                    },
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Search",
                                        id="search-button",
                                        n_clicks=0,
                                        size="sm",
                                        color="info",
                                    ),
                                    style={
                                        "marginTop": " 10px",
                                        "marginBottom": "10px",
                                    },
                                    width=2,
                                ),
                                dbc.Row(
                                    html.Div(
                                        id="individual-scores-container"  # Placeholder for the individual scores graphs
                                    ),
                                    style={
                                        "marginTop": " 10px",
                                        "marginBottom": "10px",
                                    },
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
        # html.H3("Digital Scores", style={'align': 'centre'}),
        # dcc.Graph(
        #     id='digital-scores',
        #     figure=px.bar(df, x='Website', y='digital_score', title="Digital Scores")
        # ),
        # html.Div(id="website-filter-count"),
    ]
)


@app.callback(
    Output("digital-scores", "figure"),
    Output("website-count", "children"),
    Input("score-slider", "value"),
    State("website-input", "value"),
    State("search-button", "n_clicks"),
    Input("date-input", "value")  # Added state for date input NEW
)
def update_digital_scores(slider_range, website_name, n_clicks, selected_date): #NEW

    test_df = df[df["date"] == selected_date] #NEW

    filtered_data = test_df[
        (test_df["digital_score"] >= slider_range[0])
        & (test_df["digital_score"] <= slider_range[1])
    ]
    if website_name:
        filtered_data = filtered_data[
            filtered_data["Website"].str.contains(website_name, case=False)
        ]
    # if selected_date: #added NEW
    #     filtered_data = filtered_data[
    #         filtered_data["date"] == selected_date
    #     ]

    count_msg = f"There are a total of {len(filtered_data)} between Digital score range of { slider_range[0]} and { slider_range[1]}"

    fig = px.bar(filtered_data, x="Website", y="digital_score", title="Digital Scores")
    return fig, count_msg


@app.callback(
    Output(
        "individual-scores-container", "children"
    ),  # Update children property of the placeholder div
    Input("digital-scores", "clickData"),
)
def update_individual_scores(click_data):
    if click_data is None:
        return []

    selected_website = click_data["points"][0]["x"]
    website_data = df[df["Website"] == selected_website]
    individual_scores = website_data.iloc[
        :, 1:-1
    ]  # Exclude the website and digital_score columns

    fig = go.Figure()

    for column in individual_scores:
        value = individual_scores[column].values[0]
        color = (
            "green"
            if value == "yes" or (column == "attachments" and value > 0)
            else "red"
        )

        fig.add_trace(
            go.Bar(
                x=[column],
                y=[1],  # Dummy value to create a bar
                marker=dict(color=color),
                showlegend=False, # NEW
                name=column, # NEW
            )
        )

    fig.update_layout(
        title=f"Individual Scores for {selected_website}",
        xaxis_title="Categories",
        yaxis_title="",
        barmode="group",
        showlegend=True, # NEW
    )

    return [dcc.Graph(figure=fig)]


if __name__ == "__main__":
    app.run_server(debug=True, port = 8051)
