###############################################################
# Stock Price Data Retriever
# From Yahoo Finance
###############################################################

import yfinance as yf
import json
import os
import pandas as pd

class Retriever:
    def __init__(self, ticker, period="max"):
        self.ticker = ticker
        self.period = period
        self.csv_fp = self.ticker + ".csv"
        self.json_fp = self.ticker + ".csv"
        self.data, self.info = self.get_ticker_data(\
            self.ticker, self.period, self.csv_fp, self.json_fp)

    def get_ticker_data(self, ticker, period, csv_fp, json_fp):
        # Check if data for ticker exists already
        if not os.path.isfile(ticker + ".csv"):
            # Retrieve price data for specified time period 
            # (default 1 day interval) and save to csv.
            hist = yf.download(ticker, period=period)
            hist.to_csv(csv_fp)

            if not os.path.isfile(ticker + ".json"):
                # Retrieve ticker info and save to json.
                stock = yf.Ticker(ticker)
                with open(json_fp, "w") as f:
                    json.dump(stock.info, f, ensure_ascii=False, indent=4)

        # Save ticker data into dictionary
        data = pd.read_csv(csv_fp)
        data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
        data.sort_values("Date", inplace=True)
        
        return data, stock.info
