import os
import plotly
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from TechnicalAnalysis.moving_average_compution import simple_moving_average, exponential_moving_average, moving_average_converge_divergence
from TechnicalAnalysis.adx_computation import adx_run
from TechnicalAnalysis.rsi_indicator import rsi, bollinger_bonds
import pdb


def plot_technical_graphs(input_df, short_window=20, longer_window=50, adx_window=14):
    mva_shorter, mva_longer, mva_cross_over = simple_moving_average(input_df, short_window, longer_window)
    emva_shorter, emva_longer, ewmva_cross_over = exponential_moving_average(input_df, short_window, longer_window)
    adx_data = adx_run(input_df, adx_window)
    macd_emva = moving_average_converge_divergence(input_df, short_window=12, longer_window=26, signal_period=9)
    rsi_data = rsi(input_df, window_size=14)
    bb_upper, bb_lower = bollinger_bonds(input_df, window_size=20)

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True)
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
                                name=f"emva_{short_window}"), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=emva_longer,
                                mode="lines",
                                name=f"emva_{longer_window}"), row=1, col=1)
    """
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=emva_longer,
                                # mode="lines",
                                name=f"bb_upper"), row=1, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=emva_shorter,
                                mode="lines",
                                # fill='tonexty',
                                name=f"bb_lower"), row=1, col=1)
    """
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=adx_data,
                                mode="lines",
                                name="ADX"), row=2, col=1)
    fig.append_trace(go.Bar(x=input_df['date'],
                            y=macd_emva,
                            marker_line_width = 0,
                            name="MACD"), row=2, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=rsi_data,
                                mode="lines",
                                name="RSI"), row=3, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=mva_cross_over.replace(0, None),
                                mode="markers",
                                name="MACrossOver"), row=4, col=1)
    fig.append_trace(go.Scatter(x=input_df['date'],
                                y=ewmva_cross_over.replace(0, None),
                                mode="markers",
                                name="EMACrossOver"), row=4, col=1)

    fig['layout']['yaxis1'].update(domain=[0.5, 1])
    fig['layout']['yaxis2'].update(domain=[0.3, 0.4])
    fig['layout']['yaxis3'].update(domain=[0.2, 0.3])
    fig['layout']['yaxis4'].update(domain=[0, 0.1])
    fig.update_layout(autosize=False, width=1600, height=800, xaxis_rangeslider_visible=False)
    return fig.to_json()
