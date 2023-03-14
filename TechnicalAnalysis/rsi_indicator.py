import pandas as pd

# Reference:
#   1. https://stackoverflow.com/questions/57006437/calculate-rsi-indicator-from-pandas-dataframe
#   2. https://github.com/peerchemist/finta/blob/master/finta/finta.py

def rsi(input_df, window_size=14):
    return input_df["close"].diff(1).mask(input_df["close"].diff(1) < 0, 0).ewm(alpha=1/window_size, adjust=False).mean().div(input_df["close"].diff(1).mask(input_df["close"].diff(1) > 0, -0.0).abs().ewm(alpha=1/window_size, adjust=False).mean()).add(1).rdiv(100).rsub(100)

def bollinger_bonds(input_df, window_size=20):
    tp_data = (input_df['close'] + input_df['low'] + input_df['high'])/3
    tp_std_data = tp_data.rolling(window_size).std(ddof=0)
    tp_mean_data = tp_data.rolling(window_size).mean()
    return (tp_mean_data + 2*tp_std_data), (tp_mean_data - 2*tp_std_data)
