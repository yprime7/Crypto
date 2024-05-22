# region imports
import math
from typing import List
from AlgorithmImports import *
# endregion

class HipsterFluorescentPinkMule(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 7, 30)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.symbol = self.AddEquity("BTCUSD", Resolution.Daily).Symbol
        self.dataset_symbol = self.AddData(RegalyticsRegulatoryArticles, "REG").Symbol
        self.SetBenchmark(self.symbol)
        
        self.lookback = 5
        self.momentum = self.MOMP("BTCUSD", self.lookback, Resolution.Daily)
        history = self.History(self.symbol, self.lookback, Resolution.Daily)
        for bar in history.itertuples():
            self.momentum.Update(bar.Index[1], bar.close)
        
    def OnData(self, slice: Slice) -> None:
        if not slice.ContainsKey(self.dataset_symbol):
            return
        crypto_news = False
        articles = slice[self.dataset_symbol]
        for article in articles:
            if any(word in article.Title for word in ["crypto", "blockchain", "crypto-friendly","bitcoin etf","ethereum", "cryptocurrency adoption", "blockchain adoption", "institutional crypto", "crypto legal framework", "crypto policy", "cryptocurrency approval", "crypto market"]) or any(word in article.Summary for word in ["crypto", "blockchain", "crypto-friendly","bitcoin etf","ethereum", "cryptocurrency adoption", "blockchain adoption", "institutional crypto", "crypto legal framework", "crypto policy", "cryptocurrency approval", "crypto market"]):
                crypto_news = True
                self.last_crypto_news = self.Time
        if crypto_news and not self.Portfolio[self.symbol].IsLong and self.momentum.Current.Value > 0:
            self.SetHoldings(self.symbol, 1)
        elif not crypto_news and not self.Portfolio[self.symbol].IsShort and self.momentum.Current.Value < 0:
            self.SetHoldings(self.symbol, -0.5)
