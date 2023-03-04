import os
import numpy as np
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

class StatsCalculation:

    def __init__(self):
        self.reset()

    def reset(self):
        self.win_streak = 0
        self.lose_streak = 0

    def get_streaks(self, input_data):
        if input_data:
            self.win_streak += 1
            self.lose_streak = 0
        else:
            self.lose_streak += 1
            self.win_streak = 0
        return self.win_streak, self.lose_streak
    
    def timestamp_to_date(self, input_timestamp):
        return datetime.strftime(input_timestamp, "%d %B %Y")

    def maximum_info(self, input_df, column_name):
        return round(input_df[column_name].max(), 2), self.timestamp_to_date(input_df.loc[input_df[column_name].idxmax(), 'date'])

    def minimum_info(self, input_df, column_name):
        return round(input_df[column_name].min(), 2), self.timestamp_to_date(input_df.loc[input_df[column_name].idxmin(), 'date'])

    def mean_info(self, input_df, column_name):
        return round(input_df[column_name].mean(), 2)

    def median_info(self, input_df, column_name):
        return round(input_df[column_name].median(), 2)

    def max_streaks(self, input_df, column_name='win_streaks'):
        return round(input_df[column_name].max(), 2), self.timestamp_to_date(input_df.loc[input_df[column_name].idxmax(), 'date'])

    def get_stats(self, input_df, column_name='close'):
        output_dict = {}
        self.reset()
        temp = input_df["profit_flag"].apply(lambda x: self.get_streaks(x))
        input_df["win_streaks"] = temp.apply(lambda x: x[0])
        input_df["lose_streaks"] = temp.apply(lambda x: x[1])
        del temp
        output_dict['MinimumValue'], output_dict['MinimumValueDate'] = self.minimum_info(input_df, column_name)
        output_dict['MaximumValue'], output_dict['MaximumValueDate'] = self.maximum_info(input_df, column_name)
        output_dict['MeanValue'] = self.mean_info(input_df, column_name)
        output_dict['MedianValue'] = self.median_info(input_df, column_name)
        output_dict['MaxWinStreaks'], output_dict['MaxWinStreaksDate'] = self.max_streaks(input_df, "win_streaks")
        output_dict['MaxLoseStreaks'], output_dict['MaxLoseStreaksDate'] = self.max_streaks(input_df, "lose_streaks")
        return output_dict

statcalc = StatsCalculation()

def run(input_df):
    output_dict = {}
    input_df['date'] = pd.to_datetime(input_df['date'])
    input_df['year'] = input_df['date'].dt.year
    output_dict['year_wise'] = segment_run(input_df, segment_type='year')
    input_df['month'] = input_df['date'].dt.month_name()
    output_dict['month_wise'] = segment_run(input_df, segment_type='month')
    input_df['day'] = input_df['date'].dt.day
    input_df['week'] = input_df['date'].dt.isocalendar().week
    return [output_dict['year_wise'], output_dict['month_wise']], ['na', 'Yearwise Performance', 'Monthwise Performance']

def segment_run(input_df, segment_type):
    segment_dict = {}
    input_df['day_profit'] = input_df['close'].diff(1).fillna(0)
    for this_segment in input_df[segment_type].unique():
        this_segment_df = input_df[input_df[segment_type] == this_segment]
        this_segment_df["profit_flag"] = this_segment_df['day_profit'].apply(lambda x: int(x> 0))
        segment_dict[this_segment] = statcalc.get_stats(this_segment_df, 'close')
    return pd.DataFrame(segment_dict).to_html(classes=segment_type)
