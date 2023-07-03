import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc

# Sample data (replace with your actual data)
df = pd.read_csv("zhaw_websites - Sheet3.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader("Digital Scores", style={"align": "centre"}),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dcc.Graph(
                                    id="digital-scores",
                                    figure=px.bar(
                                        df,
                                        x="Website",
                                        y="digital_score",
                                        title="Digital Scores",
                                    ),
                                ),
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
                                        list(df["Website"].values),
                                        id="website-input"
                                    ),
                                    style={
                                        "marginTop": " 10px",
                                        "marginBottom": "10px",
                                    },
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Search", id="search-button", n_clicks=0, size = "sm", color='info'
                                    ),
                                    style={
                                        "marginTop": " 10px",
                                        "marginBottom": "10px",
                                    },
                                    width=2
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
)
def update_digital_scores(slider_range, website_name, n_clicks):
    filtered_data = df[
        (df["digital_score"] >= slider_range[0])
        & (df["digital_score"] <= slider_range[1])
    ]
    if website_name:
        filtered_data = filtered_data[
            filtered_data["Website"].str.contains(website_name, case=False)
        ]

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
                showlegend=True,
            )
        )

    fig.update_layout(
        title=f"Individual Scores for {selected_website}",
        xaxis_title="Categories",
        yaxis_title="",
        barmode="group",
    )

    return [dcc.Graph(figure=fig)]


if __name__ == "__main__":
    app.run_server(debug=True)
