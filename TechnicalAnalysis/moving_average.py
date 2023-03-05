import os
import plotly
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class CrossOverTrader:
    
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
    crossOverTrade = CrossOverTrader()
    mva_shorter = input_df['close'].rolling(window=short_window).mean()
    mva_longer = input_df['close'].rolling(window=longer_window).mean()
    mva_diff = mva_shorter - mva_longer
    # input_df['crossover'] = np.sign(crossover).diff().ne(0)
    mva_cross_over = mva_diff.apply(lambda x: crossOverTrade.decide(x))

    emva_shorter = input_df['close'].ewm(span=short_window, adjust=False).mean()
    emva_longer = input_df['close'].ewm(span=longer_window, adjust=False).mean()
    ewm_diff = emva_shorter - emva_longer
    ewmva_cross_over = ewm_diff.apply(lambda x: crossOverTrade.decide(x))

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)
    # fig.update_layout(xaxis_rangeslider_visible=True)
    fig.append_trace(go.Candlestick(x=input_df['date'],
                                    open=input_df['open'],
                                    high=input_df['high'],
                                    low=input_df['low'],
                                    close=input_df['close']
                                ), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=mva_shorter,
                                mode="lines",
                                name=f"mva_{short_window}"), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=mva_longer,
                                mode="lines",
                                name=f"mva_{longer_window}"), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=emva_shorter,
                                mode="lines",
                                name=f"mva_{short_window}"), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=emva_longer,
                                mode="lines",
                                name=f"mva_{longer_window}"), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=mva_cross_over.replace(0, None),
                                mode="markers",
                                name="MovingAverageCrossOverSignal"), row=2, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=ewmva_cross_over.replace(0, None),
                                mode="markers",
                                name="ExpMovingAverageCrossOverSignal"), row=3, col=1)
    fig.update_layout(autosize=False, width=1600, height=800, xaxis_rangeslider_visible=False)
    fig['layout']['yaxis1'].update(domain=[0, 0.7])
    fig['layout']['yaxis2'].update(domain=[0.8, 0.9])
    fig['layout']['yaxis3'].update(domain=[0.9, 1])
    return fig.to_json()
