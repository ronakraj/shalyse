###############################################################
# Stock Price Data Retriever
# From Yahoo Finance
###############################################################

import yfinance as yf
import json
import os
import pandas as pd

class Retriever:
    def __init__(self, ticker: str, period="max") -> None:
        """
        Main class for retrieving data from Yahoo Finance.
        """
        
        self.ticker = ticker
        self.period = period
        self.csv_fp = self.ticker + ".csv"
        self.json_fp = self.ticker + ".json"
        self.data, self.info = self._get_ticker_data(\
            self.ticker, self.period, self.csv_fp, self.json_fp)

    def _get_ticker_data(self, ticker: str, period: str, csv_fp: str, \
            json_fp: str) -> dict:
        """
        Yields information and all data from Yahoo Finance server for 
        provided ticker ID and stores these to json_fp and csv_fp files 
        respectively. Also returns both in dictionary format for use during
        runtime.
        """
        
        # Check if data for ticker exists already
        if not os.path.isfile(csv_fp):
            # Retrieve price data for specified time period 
            # (default 1 day interval) and save to csv.
            hist = yf.download(ticker, period=period)
            hist.to_csv(csv_fp)

            if not os.path.isfile(json_fp):
                # Retrieve ticker info and save to json.
                stock = yf.Ticker(ticker)
                with open(json_fp, "w") as f:
                    json.dump(stock.info, f, ensure_ascii=False, indent=4)

        # Store ticker data into dictionary for runtime
        data = pd.read_csv(csv_fp)
        data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
        data.sort_values("Date", inplace=True)

        # Store ticker information into dictionary for runtime
        with open(json_fp) as fp:
            info = json.load(fp)
        
        return data, info
