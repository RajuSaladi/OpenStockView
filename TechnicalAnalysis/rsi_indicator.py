import pandas as pd

# Reference:
#   1. https://stackoverflow.com/questions/57006437/calculate-rsi-indicator-from-pandas-dataframe
#   2. https://github.com/peerchemist/finta/blob/master/finta/finta.py

def rsi(input_df, window_size=14):
    return input_df["close"].diff(1).mask(input_df["close"].diff(1) < 0, 0).ewm(alpha=1/window_size, adjust=False).mean().div(input_df["close"].diff(1).mask(input_df["close"].diff(1) > 0, -0.0).abs().ewm(alpha=1/window_size, adjust=False).mean()).add(1).rdiv(100).rsub(100)
