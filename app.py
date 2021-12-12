import dash
from dash import dcc
from dash import html
import numpy as np
from simulator import Shalyse
import plotly.express as px
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go

# Global parameters
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
shalyse = Shalyse()

# Scenario inputs
ticker_opts = dcc.Dropdown(
        id="ticker-filter",
        options = [
            {"label": "S&P/ASX 200", "value": "^AXJO"},
            {"label": "S&P 500", "value": "^GSPC"},
            {"label": "NASDAQ 100", "value": "^NDX"},
            {"label": "FTSE 100", "value": "^FTSE"},
            {"label": "Hang Seng", "value": "^HSI"},
            {"label": "ASX All Ords", "value": "^AORD"},
            {"label": "Dow Jones", "value": "^DJI"},
            ],
        value = "^AXJO",
        className="dropdown",
        clearable=False,       
    )

# Application visualisation
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
                    children="An open-source tool to simulate investment "
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
                        html.Div("Index", className="menu-title"),
                        ticker_opts,
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="model-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                )
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.P(children="⚠️", className="header-emoji"),
                html.P(
                    children="Disclaimer: Results from this simulator should "
                    "not be taken as financial advice. Past performance is not "
                    "a reliable indicator of future performance. Every "
                    "individual situation is different and you should consult "
                    "a qualified financial planner and/or tax accountant.",
                    className="header-description",
                ),
            ],
            className="warning",
        ),
    ]
)

# Handle callback from interface
@app.callback(
    [Output("model-chart", "figure"),
    Output("price-chart", "figure")],
    [Input("ticker-filter", "value")],
    [State("model-chart", "figure"),
    State("price-chart", "figure")],
)

def update_charts(ticker, model_fig, price_fig):
    global shalyse

    # Retrive current model and price charts
    model_fig=go.Figure(model_fig)
    price_fig=go.Figure(price_fig)

    if ticker != shalyse.ticker:
        # Retrieved new ticker ID so run simulation again
        shalyse = Shalyse(ticker)

    # Update model output
    model_fig = px.histogram(x=shalyse.total_profit,
        marginal="box",
        nbins=30,
        histnorm="probability",
    )
    model_fig.update_layout(
        title_text="Expected Profit After " + \
            str(shalyse.scenario['horizon']) + " Years",
        title_x=0.5,
        xaxis_title_text=shalyse.info['currency'],
        yaxis_title_text="Probability",
    )

    price_fig = px.line(
        x=shalyse.data['Date'], 
        y=shalyse.data['Adj Close'], 
        log_y=True,
        render_mode="SVG")
    price_fig.update_layout(
        title_text=shalyse.info["shortName"],
        title_x=0.5,
        xaxis_title_text="Date",
        yaxis_title_text= shalyse.info["currency"]
    )

    return model_fig, price_fig

if __name__ == "__main__":
    app.run_server(debug=True)