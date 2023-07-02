import talib
import pandas as pd
print(talib.get_function_groups().keys())

data_df = pd.read_csv(r"E:\PythonCodes\StockAnalysis\Data\IndianStocks_IntradayData\ADANIENT_day_data.csv")
data_df['CDL3INSIDE'] = talib.CDL3INSIDE(data_df['open'], data_df['high'], data_df['low'], data_df['close'])
print(data_df['CDL3INSIDE'].value_counts())
print(data_df[data_df['CDL3INSIDE'] == 100]['date'])
