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
    id = "ticker-filter",
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
    className = "dropdown",
    clearable = False,       
)
topup_freq_opts = dcc.Dropdown(
    id = "topup-freq",
    options = [
        {"label": "Daily", "value": 1},
        {"label": "Weekly", "value": 7},
        {"label": "Fortnightly", "value": 14},
        {"label": "Monthly", "value": 30},
        {"label": "Every 2 Months", "value": 60},
        {"label": "Every 6 Months", "value": 183},
        {"label": "Yearly", "value": 365},
        ],
    value = shalyse.scenario['period'],
    className = "dropdown",
    clearable = False,       
)

horizon_opts = dcc.Slider(
    id="hori-opts",
    min = 1,
    max = int(shalyse.info['years'] / 2),
    marks = {i: "{}".format(i) for i in range(1, 
        int(shalyse.info['years'] / 2))},
    value = shalyse.scenario['horizon'], 
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
                html.H1(children="Your strategy",
                className="menu-title"),
            ],
            className="menu",
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
                    children=[
                        html.Div("Initial investment: (" + 
                                 shalyse.info['currency'] + ")", 
                                 className="menu-title"),
                        dcc.Input(id="initial-invest", 
                                  type="number", 
                                  value = shalyse.scenario['initial'],
                                  placeholder=shalyse.info['currency'], 
                                  debounce=True,
                                  style={"width": "192px", "height": "48px", 
                                         "font-size": "20px"}),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div("Regular contribution: (" + 
                                 shalyse.info['currency'] + ")", 
                                 className="menu-title"),
                        dcc.Input(id="topup-contr", type="number", 
                                  placeholder=shalyse.info['currency'], 
                                  value = shalyse.scenario['topup'],
                                  debounce=True,
                                  style={"width": "192px", "height": "48px", 
                                         "font-size": "20px"}),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div("Number of years:", 
                                 className="menu-title"),
                        horizon_opts,
                    ],
                ),
                html.Div(
                    children=[
                        html.Div("Contribution frequency:", 
                                 className="menu-title"),
                        topup_freq_opts,
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(children="Result",
                        className="header-title"),
                        html.P(children="Expected: " + 
                               shalyse.stats['median']['display'],
                               className="header-description"),
                        html.P(children="Absolute worst case: " + 
                               shalyse.stats['min']['display'],
                               className="header-description"),
                        html.P(children="Worst case: " + 
                               shalyse.stats['-1std']['display'],
                               className="header-description"),
                        html.P(children="Best case: " + 
                               shalyse.stats['+1std']['display'],
                               className="header-description"),
                        html.P(children="Absolute best case: " + 
                               shalyse.stats['max']['display'],
                               className="header-description"),
                    ],
                    className="card",
                ),
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
    [Input("ticker-filter", "value"),
    Input("initial-invest", "value"),
    Input("hori-opts", "value"),
    Input("topup-contr", "value"),
    Input("topup-freq", "value")],
    [State("model-chart", "figure"),
    State("price-chart", "figure")],
)

def update_charts(ticker, init, horizon, topup, topfreq, model_fig, price_fig):
    global shalyse

    # Retrieve current model and price charts
    model_fig=go.Figure(model_fig)
    price_fig=go.Figure(price_fig)

    scenario = {
        'initial': init,      
        'topup': topup,        
        'period': topfreq, 
        'horizon': horizon 
        }

    # Current ticker and simulation scenario
    rerun_sim = False
    next_ticker = shalyse.ticker
    next_scenario = shalyse.scenario

    if ticker != shalyse.ticker:
        next_ticker = ticker
        # New ticker, so will need to rerun simulation
        rerun_sim = True

    if scenario != shalyse.scenario:
        next_scenario = scenario
        # Retrieved a new scenario so run simulation again
        rerun_sim = True

    if rerun_sim:
        shalyse = Shalyse(ticker=next_ticker, scenario=next_scenario)

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