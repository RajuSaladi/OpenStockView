import os
import plotly
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class MovingAverageTrader:
    
    def __init__(self):
        self.prev_sign = 0 
        self.sell_position = 0
        self.buy_position = 0
        self.net_trade = 0

    def decide(self, input_data):
        trade_move = 0
        if input_data is None:
            self.prev_sign = 0
        elif input_data > 0:
            if self.prev_sign in [0, -1]:
                # print("Buy Sign")
                trade_move = 1
                self.buy_position += 1
            self.prev_sign = 1
        elif input_data < 0:
            if self.prev_sign in [0, 1]:
                # print("Sell Sign")
                trade_move = -1
                self.sell_position += 1
            self.prev_sign = -1
        else:
            trade_move = 0
            # Prevsign will remain same if diff is zero
        self.net_trade = self.buy_position - self.sell_position
        return trade_move


def plot_technical_graphs(input_df, short_window=20, longer_window=50):
    movAvgTrade = MovingAverageTrader()
    mva_shorter = input_df['close'].rolling(window=short_window).mean()
    mva_longer = input_df['close'].rolling(window=longer_window).mean()
    mva_diff = mva_shorter - mva_longer
    # input_df['crossover'] = np.sign(crossover).diff().ne(0)
    mva_diff.apply(lambda x: movAvgTrade.decide(x)).replace(0, None)

    fig = make_subplots(rows=2, cols=1)
    fig.update_layout(xaxis_rangeslider_visible=True)
    fig.append_trace(go.Candlestick(x=input_df['date'],
                                    open=input_df['open'],
                                    high=input_df['high'],
                                    low=input_df['low'],
                                    close=input_df['close']
                                ), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=mva_shorter,
                                mode="lines",
                                name="mva_20"), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=mva_longer,
                                mode="lines",
                                name="mva_50"), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=mva_diff.apply(lambda x: movAvgTrade.decide(x)).replace(0, None),
                                mode="markers",
                                name="Buy or Sell"), row=2, col=1)
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig.to_json()
