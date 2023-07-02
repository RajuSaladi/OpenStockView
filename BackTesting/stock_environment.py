import pdb
import pandas as pd

class StockEnvironment:

    def __init__(self):
        self.fund_value = 0
        self.trade_book = 0
        self.positions = 0
        self.trade_count = 0
        self.trade_df = pd.DataFrame(columns=['FundValue', 'TradeBook', 'Position', 'TradeVerdict'])
        self.complete_trade = {}

    def get_stock_value(self, current_stock_price):
        return current_stock_price * self.positions

    def trade_analysis(self):
        trade_df = self.trade_df.reset_index(drop=False, inplace=False)
        trade_df['year'] = pd.to_datetime(trade_df['index']).apply(lambda x: x.year)
        prev_value = 0
        output_dict = {}
        for this_year in trade_df['year'].unique():
            output_dict[this_year] = {}
            this_df = trade_df[trade_df['year'] == this_year]
            this_row = this_df.iloc[-1]
            this_value = this_row['FundValue'] + this_row['TradeBook']
            if prev_value:
                output_dict[this_year]["YoY"] = (this_value - prev_value)/prev_value
            else:
                output_dict[this_year]["YoY"] = 0
            prev_value = this_value
            output_dict[this_year].update(self.trade_stats(this_df))
        return pd.DataFrame(output_dict)

    def trade_stats(self, input_trade_df):
        output_dict = {}
        output_dict['SuccessTrades'] = input_trade_df[input_trade_df['TradeVerdict'] > 0]['TradeVerdict'].sum()
        output_dict['FailureTrades'] = -1* input_trade_df[input_trade_df['TradeVerdict'] < 0]['TradeVerdict'].sum()
        output_dict['SuccessRatio'] = output_dict['SuccessTrades']/(output_dict['SuccessTrades'] + output_dict['FailureTrades'])
        output_dict['FailureRatio'] = output_dict['FailureTrades']/(output_dict['SuccessTrades'] + output_dict['FailureTrades'])
        return output_dict


    def get_trade_performance_summary(self):
        output_dict = {}
        output_dict['Profit'] = self.get_profit()
        output_dict['NoOfTrades'] = self.trade_count
        output_dict['TradeInfo'] = self.trade_df
        output_dict['TradeSummary'] = self.trade_analysis()
        output_dict.update(self.trade_stats(self.trade_df))
        return output_dict

    def get_profit(self):
        return self.fund_value + self.trade_book

    def run(self, input_row):
        success_trade = 0
        traded_positions = 0
        current_stock_price, strategy_move, date_index = input_row['stock_price'], input_row['decision'], input_row.name
        if strategy_move == "BUY":
            traded_positions = 1
            self.fund_value = self.fund_value - current_stock_price
            self.positions = self.positions + traded_positions
            self.trade_count = self.trade_count + 1
            trade_mode = True
        elif strategy_move == "SELL":
            traded_positions = self.positions
            self.fund_value = self.fund_value + (traded_positions * current_stock_price)
            self.positions = 0
            self.trade_count = self.trade_count + 1
            trade_mode = True
        self.trade_book = self.get_stock_value(current_stock_price)
        if traded_positions != 0:
            self.complete_trade[strategy_move] = self.complete_trade.get(strategy_move, 0) + (traded_positions * current_stock_price)
            if len(self.complete_trade.keys()) == 2:
                net_trade = self.complete_trade["SELL"] - self.complete_trade["BUY"]
                if net_trade > 0:
                    success_trade = traded_positions
                else:
                    success_trade = -1 * traded_positions
                self.complete_trade = {}
            self.trade_df.loc[date_index] = [self.fund_value, self.trade_book, self.positions, success_trade]
