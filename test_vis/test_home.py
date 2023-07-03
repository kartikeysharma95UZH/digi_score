import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from dash import dash_table
import dash_bootstrap_components as dbc

THRESHOLD_POOR = 0.5
THRESHOLD_AVERAGE = 0.85

color_map = {
    "Poor Websites": "red",
    "Average Websites": "yellow",
    "Good Websites": "green",
}


# Sample data (replace with your actual data)
# data = {
#     'Website': ['example1', 'example2', 'example3', 'example4', 'example5', 'example6', 'example7', 'example8', 'example9', 'example10'],
#     'digital_score': [0.94, 0.45, 0.64, 0.96, 0.92, 0.83, 0.76, 0.67, 0.73, 0.97]
# }
# df = pd.DataFrame(data)

df_data = pd.read_csv("zhaw_websites - Sheet3.csv")

# Set threshold values


# Create bar charts

# Define color map for table rows


# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader("Website Status"),
                # html.H1(""),
                dbc.CardBody(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                list(df_data["date"].unique()),
                                id="date-input",
                                placeholder="Select the date of scraping",
                                value=df_data["date"].unique().max(),
                            ),
                            style={
                                "marginTop": " 10px",
                                "marginBottom": "10px",
                                "marginLeft": "430px",
                            },
                            width=3,
                        ),
                        dcc.Graph(id="status-graph"),
                        html.H2("Website Count by Category and Thresholds"),
                        dbc.Col(
                            dash_table.DataTable(
                                id="status-table",
                                columns=[
                                    {"name": "Category", "id": "Category"},
                                    {"name": "Threshold", "id": "Threshold"},
                                    {"name": "Count", "id": "Count"},
                                ],
                                style_cell={'textAlign': 'center'},
                                style_data_conditional=[
                                    {
                                        "if": {"row_index": 0},
                                        "backgroundColor": color_map["Poor Websites"],
                                    },
                                    {
                                        "if": {"row_index": 1},
                                        "backgroundColor": color_map[
                                            "Average Websites"
                                        ],
                                    },
                                    {
                                        "if": {"row_index": 2},
                                        "backgroundColor": color_map["Good Websites"],
                                    },
                                ],
                            ),
                            width=5,
                            style={"marginLeft": "330px"}
                        ),
                    ]
                ),
            ]
        )
    ]
)


@app.callback(
    Output("status-graph", "figure"),
    Output("status-table", "data"),
    Input("date-input", "value"),
)
def subset_data(date_selected):
    # print(date_selected, type(date_selected), ÷÷)
    df = df_data[df_data["date"] == date_selected]
    # Count websites in different score ranges
    bad_score_count = len(df[df["digital_score"] < THRESHOLD_POOR])
    average_score_count = len(
        df[
            (df["digital_score"] >= THRESHOLD_POOR)
            & (df["digital_score"] < THRESHOLD_AVERAGE)
        ]
    )
    good_score_count = len(df[df["digital_score"] >= THRESHOLD_AVERAGE])

    fig = go.Figure(
        data=[
            go.Bar(
                name="Poor Websites",
                x=["Score Range"],
                y=[bad_score_count],
                marker_color="red",
            ),
            go.Bar(
                name="Average Websites",
                x=["Score Range"],
                y=[average_score_count],
                marker_color="yellow",
            ),
            go.Bar(
                name="Good Websites",
                x=["Score Range"],
                y=[good_score_count],
                marker_color="green",
            ),
        ]
    )

    # Set layout
    fig.update_layout(title="Website Status by Score Range", barmode="group")

    data = [
        {
            "Category": "Poor Websites",
            "Threshold": f"Below {THRESHOLD_POOR}",
            "Count": bad_score_count,
        },
        {
            "Category": "Average Websites",
            "Threshold": f"{THRESHOLD_POOR} - {THRESHOLD_AVERAGE}",
            "Count": average_score_count,
        },
        {
            "Category": "Good Websites",
            "Threshold": f"Above {THRESHOLD_AVERAGE}",
            "Count": good_score_count,
        },
    ]

    return fig, data


if __name__ == "__main__":
    app.run_server(debug=True, port = 8052)
