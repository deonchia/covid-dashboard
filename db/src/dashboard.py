import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

from import_data import get_data

external_stylesheets = [
    {
    "href": 'http://fonts.googleapis.com/css?family=Lato&subset=latin,latin-ext',
    "rel": 'stylesheet', 
    "style": "text/css"
    }]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
df = pd.read_json(get_data()).sort_values("pr_date")
fig = px.line(df, x="pr_date", y="count_of_case", color='age_group',
            labels={"pr_date":"PR Date", "count_of_case":"Case Count"},
            )

app.layout = html.Div(
    children=[
        html.Div(children=[
            html.Br(),
            html.Br(),
            html.H1(children='Where is COVID?',
                    className="header-title"),
            html.Div(children="A simple dashboard on Singapore's Covid-19 situation based on data.gov", 
                    className="header-description")
        ], className="header"),

        html.Div(
            children=dcc.Graph(
                id='graph',
                figure=fig
            )
        )
])

# if __name__ == '__main__':
#     app.run_server(debug=True)