import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

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
    'digital_score': [0.94, 0.45, 0.64, 0.96, 0.92, 0.83, 0.76, 0.67, 0.73, 0.97]
}
df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Digital Scores"),
    dcc.Graph(
        id='digital-scores',
        figure=px.bar(df, x='Website', y='digital_score', title="Digital Scores")
    ),
    dcc.Dropdown(
        id='website-dropdown',
        options=[{'label': f"{website} ({score})", 'value': website} for website, score in zip(df['Website'], df['digital_score'])],
        value=[df['Website'][0]],  # Set the default value to the first website
        multi=True  # Allow multiple selections
    ),
    html.Div(
        id="individual-scores-container"  # Placeholder for the individual scores graphs
    )
])

@app.callback(
    Output('digital-scores', 'figure'),
    Input('website-dropdown', 'value')
)
def update_digital_scores(selected_websites):
    selected_data = df[df['Website'].isin(selected_websites)]

    fig = px.bar(selected_data, x='Website', y='digital_score', title="Digital Scores")
    return fig

def create_page1_layout():
    layout = app.layout
    return layout

def update_individual_scores(selected_websites):
    graphs = []
    
    for website in selected_websites:
        website_data = df[df["Website"] == website]
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
            title=f"Individual Scores for {website}",
            xaxis_title="Categories",
            yaxis_title="",
            barmode="group",
        )
        graphs.append(dcc.Graph(figure=fig))

    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)
