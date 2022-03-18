import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

from import_data import get_data

"""
A module to display the dashboard based on the data pulled from the get_data() 
method and prepares the app and the server, courtesy of Dash.
The dashboard is based on the CSS stylesheet located in assets/style.css. 
"""


external_stylesheets = [
    {
    "href": 'http://fonts.googleapis.com/css?family=Lato&subset=latin,latin-ext',
    "rel": 'stylesheet', 
    "style": "text/css"
    }
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
df = pd.read_json(get_data()).sort_values("pr_date")

# Line to load local dataset to troubleshoot CSS layout
# with open("../../sg_covid.json") as r:
#     df = pd.read_json(r).sort_values("pr_date")

fig = px.line(df, x="pr_date", y="count_of_case", color='age_group',
            labels={"pr_date":"Date", "count_of_case":"Case Count"},
            category_orders={"age_group": sorted(df.age_group.unique())}
            )

fig.update_layout(
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        title="Age Group")
    )

app.layout = html.Div(
    children=[
        html.Div(children=[
            html.Br(),
            html.H1(children='Everybody asks who has COVID-19, but nobody asks how is COVID-19',
                    className="header-title"),
            html.Div(children="A simple dashboard on Singapore's Covid-19 situation", 
                    className="header-description")
        ], className="header"),

        html.Div(
            children=dcc.Graph(
                id='graph',
                figure=fig,
                style={'height': '80vh'}
            )
        ),

        html.Div(children=[
            html.Div(children="Data obtained from data.gov.sg",
                    className="footer-description"),
            html.Div(children="Deon Chia, 2022", 
                    className="footer-description")
            ], className="footer")
        
])

if __name__ == '__main__':
    app.run_server(debug=True)