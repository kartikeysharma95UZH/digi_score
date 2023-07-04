import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the CSV file
df = pd.read_csv("zhaw_websites - Sheet3.csv")

# Create Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div(
    [
        html.H1("Website Score Changes"),
        html.Div(
            [
                html.Label("Select Start Date:"),
                dcc.Dropdown(
                    id="start-date-dropdown",
                    options=[
                        {"label": date, "value": date}
                        for date in df["date"].unique()
                    ],
                    value=df["date"].min(),
                ),
            ],
            style={"width": "200px", "margin-bottom": "10px"},
        ),
        html.Div(
            [
                html.Label("Select End Date:"),
                dcc.Dropdown(
                    id="end-date-dropdown",
                    options=[
                        {"label": date, "value": date}
                        for date in df["date"].unique()
                    ],
                    value=df["date"].max(),
                ),
            ],
            style={"width": "200px", "margin-bottom": "10px"},
        ),
        dcc.Graph(id="bar-chart"),
    ],
    style={"width": "1500px", "margin": "auto"},
)

@app.callback(
    Output("bar-chart", "figure"),
    Input("start-date-dropdown", "value"),
    Input("end-date-dropdown", "value"),
)
def update_graph(start_date, end_date):
    # Filter the data based on selected dates
    df_filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # Calculate score changes across all websites
    comparison = df_filtered.groupby("Website")["digital_score"].last() - df_filtered.groupby("Website")["digital_score"].first()
    print("Comparison:")
    print(comparison)

    improved = comparison[comparison > 0].count()
    same = comparison[comparison == 0].count()
    decreased = comparison[comparison < 0].count()

    print("Improved count:", improved)
    print("Same count:", same)
    print("Decreased count:", decreased)

    # Create a dataframe for the visualization
    df_visualization = pd.DataFrame(
        {
            "Score Change": ["Improved", "Same", "Decreased"],
            "Count": [improved, same, decreased],
        }
    )

    # Create the bar chart
    fig = px.bar(
        df_visualization,
        x="Score Change",
        y="Count",
        labels={"Count": "Number of Websites", "Score Change": "Score Change"},
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )

    # Customize the chart layout
    fig.update_layout(
        title="Website Score Changes",
        xaxis=dict(title="Score Change"),
        yaxis=dict(title="Number of Websites"),
    )

    return fig

# @app.callback(
#     Output("bar-chart", "figure"),
#     Input("start-date-dropdown", "value"),
#     Input("end-date-dropdown", "value"),
# )
# def update_graph(start_date, end_date):
#     # Filter the data based on selected dates
#     df_filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

#     # Calculate score changes across all websites
#     comparison = df_filtered.groupby("Website")["digital_score"].last() - df_filtered.groupby("Website")["digital_score"].first()
#     improved = comparison[comparison > 0].count()
#     same = comparison[comparison == 0].count()
#     decreased = comparison[comparison < 0].count()

#     # Create a dataframe for the visualization
#     df_visualization = pd.DataFrame(
#         {
#             "Score Change": ["Improved", "Same", "Decreased"],
#             "Count": [improved, same, decreased],
#         }
#     )

#     # Create the bar chart
#     fig = px.bar(
#         df_visualization,
#         x="Score Change",
#         y="Count",
#         labels={"Count": "Number of Websites", "Score Change": "Score Change"},
#         color_discrete_sequence=px.colors.qualitative.Pastel,
#     )

#     # Customize the chart layout
#     fig.update_layout(
#         title="Website Score Changes",
#         xaxis=dict(title="Score Change"),
#         yaxis=dict(title="Number of Websites"),
#     )

#     return fig

if __name__ == "__main__":
    app.run_server(debug=True, port = 8053)
