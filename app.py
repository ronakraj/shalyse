import dash
from dash import dcc
from dash import html
import pandas as pd

data = pd.read_csv("asx.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Shalyse: Open Source Share Analysis"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="💰", className="header-emoji"),
                html.H1(
                    children="Shalyse",
                    className="header-title",
                ),
                html.P(
                    children="An open-source tool to simulate your investment "
                    " strategies over historical data. ",
                    className="header-description",
                ),
                html.P(
                    children="Created by RonakrajGosalia.",
                    className="header-description",
                )
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["Date"],
                                    "y": data["Adj Close"],
                                    "type": "lines",
                                    "hovertemplate": "$%{y:.2f}<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": "Index Value over Time",
                                "yaxis": {
                                    "tickprefix": "$"
                                },
                                "coloraway": ["#17B897"],
                            },
                        },
                        className="card",
                    ),
                )
            ],
            className="wrapper",
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)