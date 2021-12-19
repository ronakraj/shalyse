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

max_mark = int(shalyse.info['years'] / 2)
new_marks = range(1, max_mark, max(int(max_mark / 10), 1))
hori_opts_marks = {}
for mark in new_marks:
    hori_opts_marks[int(mark)] = str(mark)
horizon_opts = dcc.Slider(
    id = "hori-opts",
    min = 1,
    max = max_mark,
    marks = hori_opts_marks,
    value = shalyse.scenario['horizon'], 
)

result_text = {
    "median": shalyse.stats['median']['display'],
    "min": shalyse.stats['min']['display'],
    "-1std": shalyse.stats['-1std']['display'],
    "+1std": shalyse.stats['+1std']['display'],
    "max": shalyse.stats['max']['display'],
}

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
                        html.Div(id = "init-invest-title",
                                 className = "menu-title"),
                        dcc.Input(id = "initial-invest", 
                                  type = "number", 
                                  value = shalyse.scenario['initial'],
                                  placeholder = shalyse.info['currency'], 
                                  debounce = True,
                                  style = {"width": "192px", "height": "48px", 
                                         "font-size": "20px"}),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(id = "topup-title",
                                 className = "menu-title"),
                        dcc.Input(id = "topup-contr", type="number", 
                                  placeholder = shalyse.info['currency'], 
                                  value = shalyse.scenario['topup'],
                                  debounce = True,
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
                        html.P(id = "expected-field",
                               className="header-description"),
                        html.P(id = "min-field",
                               className="header-description"),
                        html.P(id = "worst-field",
                               className="header-description"),
                        html.P(id = "best-field",
                               className="header-description"),
                        html.P(id = "max-field",
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
    Output("price-chart", "figure"),
    Output("init-invest-title", "children"),
    Output("topup-title", "children"),
    Output("hori-opts", "max"),
    Output("hori-opts", "marks"),
    Output("expected-field", "children"),
    Output("min-field", "children"),
    Output("worst-field", "children"),
    Output("best-field", "children"),
    Output("max-field", "children"),],
    [Input("ticker-filter", "value"),
    Input("initial-invest", "value"),
    Input("hori-opts", "value"),
    Input("topup-contr", "value"),
    Input("topup-freq", "value")],
    [State("model-chart", "figure"),
    State("price-chart", "figure"),],
)

def update_charts(ticker, init, horizon, topup, topfreq, model_fig, price_fig):
    global shalyse

    # Retrieve current model and price charts
    model_fig = go.Figure(model_fig)
    price_fig = go.Figure(price_fig)

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

    # Update all text fields
    init_invest_title = "Initial investment: (" + shalyse.info['currency'] + ")"
    topup_title = "Regular contribution: (" +  shalyse.info['currency'] + ")"

    # Update horizon slider
    hori_opts_max = int(shalyse.info['years'] / 2)
    max_mark = int(shalyse.info['years'] / 2)
    new_marks = range(1, max_mark, max(int(max_mark / 10), 1))
    hori_opts_marks = {}
    for mark in new_marks:
        hori_opts_marks[int(mark)] = str(mark)
    
    # Update all result text fields
    expected_field = "Expected: " + shalyse.stats['median']['display']
    worst_worst_field = "Worst case: " + \
        shalyse.stats['min']['display']
    worst_field = "Expected min: " + shalyse.stats['-1std']['display']
    best_field = "Expected max: " + shalyse.stats['+1std']['display']
    best_best_field = "Best case: " + shalyse.stats['max']['display']

    return model_fig, price_fig, init_invest_title, topup_title, \
        hori_opts_max, hori_opts_marks, expected_field, worst_worst_field, \
        worst_field, best_field, best_best_field

if __name__ == "__main__":
    app.run_server(debug=True)