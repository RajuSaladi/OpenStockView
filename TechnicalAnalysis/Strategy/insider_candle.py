import os
import pdb
import pandas as pd


BUY = 'BUY'
SELL = 'SELL'
HOLD = 'HOLD'

class InsiderCandle:

    def __init__(self):
        self.prev_candle = None
        self.strategy_flag = False

    def check_strategy(self, current_candle):
        pdb.set_trace()
        if self.prev_candle is None:
            self.strategy_flag = False
        elif current_candle['low'] > self.prev_candle['low']:
            if current_candle['high'] < self.prev_candle['high']:
                self.strategy_flag = True
                print('strategy_flag', self.strategy_flag)
            print("-"*100)
            print("Current Price", current_candle)
            print("prev_candle Price", self.prev_candle)
        else:
            self.strategy_flag = False


    def decide(self, current_candle):
        decision = HOLD
        if self.strategy_flag:
            if current_candle['high'] > self.prev_candle['high']:
                decision =  BUY
            elif current_candle['low'] < self.prev_candle['low']:
                decision =  SELL
        return decision

    def run(self, current_candle):
        decision = self.decide(current_candle)
        self.check_strategy(current_candle)
        self.prev_candle = current_candle
        return decision


if __name__ == "__main__":

    strategyCheck = InsiderCandle()
    data_df = pd.read_csv(r"E:\PythonCodes\StockAnalysis\Data\IndianStocks_IntradayData\NIFTY BANK_5minute_data.csv")
    data_df['insider_candle'] = data_df.apply(lambda x: strategyCheck.run(x), axis=1)
    print(data_df['insider_candle'].value_counts())
