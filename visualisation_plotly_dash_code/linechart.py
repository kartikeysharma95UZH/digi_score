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
        html.H1("Website Digital Score Variation"),
        html.Div(
            [
                html.Label("Search Website:"),
                dcc.Dropdown(
                    id="website-search",
                    options=[
                        {"label": website, "value": website}
                        for website in df["Website"].unique()
                    ],
                    value="example1",
                    multi=True,
                    style={"width": "400px", "margin-bottom": "10px"},
                ),
            ],
            style={"margin-bottom": "10px"},
        ),
        dcc.Graph(id="line-chart"),
    ],
    style={"width": "1300px", "margin": "150px"},
)


@app.callback(
    Output("line-chart", "figure"),
    Input("website-search", "value"),
)
def update_line_chart(websites):
    if not websites:  # If no websites are selected, show an empty figure
        return px.line()

    # Convert the websites variable to a list if it's a string
    if isinstance(websites, str):
        websites = [websites]

    # Filter the data based on the selected websites
    df_filtered = df[df["Website"].isin(websites)]

    # Create the line chart
    fig = px.line(
        df_filtered,
        x="date",
        y="digital_score",
        color="Website",
        labels={"digital_score": "Digital Score", "date": "Date", "Website": "Website"},
        title="Digital Score Variation",
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port = 8052)
