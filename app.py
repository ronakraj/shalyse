import dash
from dash import dcc
from dash import html
import numpy as np


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
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Index", className="menu-title"),
                        dcc.Dropdown(
                            id="index-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
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
        ),
        html.Div(
            children=[
                html.P(children="⚠️", className="header-emoji"),
                html.P(
                    children="Disclaimer: Results from this simulator should not "
                    "be taken as financial advice. Past performance is not "
                    "a reliable indicator of future performance. Every individual"
                    " situation is different and you should consult a qualified "
                    "financial planner and/or tax accountant.",
                    className="header-description",
                ),
            ],
            className="warning",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)