###############################################################
# Stock Price Data Getter
# From Yahoo Finance
###############################################################

import yfinance as yf
import json

ticker = "^AXJO"
period = "max"
csv_file = "asx.csv"
json_file = "asx.json"

# Retrieve price data for specified time period (default 1 day interval)
# and save to csv.
hist = yf.download(ticker, period=period)
hist.to_csv(csv_file)

# Retrieve ticker info and save to json.
stock = yf.Ticker(ticker)
with open(json_file, "w") as f:
    json.dump(stock.info, f, ensure_ascii=False, indent=4)