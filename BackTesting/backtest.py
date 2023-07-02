import os
import sys
import pdb
import pandas as pd
from collections import Counter
sys.path.insert(0, r"E:\PythonCodes\Docker\OpenStockView")
from TechnicalAnalysis.indicators import TA
from TechnicalAnalysis.trade_signals import CrossOverTrader
from BackTesting.stock_environment import StockEnvironment

AVAILABLE_TECHNICAL_INDICATORS = [k for k in TA.__dict__.keys() if k[0] not in "_"]
crossOverTrade = CrossOverTrader()

BUY = 1
HOLD = 0
SELL = -1
AGGREGATION_MAXVOTE='maxvote'
AGGREGATION_SUM = 'sum_all'


def run(input_df, input_strategies_list):
    output_list = []
    input_df.set_index('date', inplace=True)
    for i, this_strategy in enumerate(input_strategies_list):
        output_list.append(execute_strategy(input_df, this_strategy))
    trade_decision = aggregate_strategies(output_list, selection_mode=AGGREGATION_MAXVOTE)
    return evaluate_on_data(input_df, trade_decision)

def make_executable_indicator(indicator_info):
    output_indicator = indicator_info.get('indicator')
    if 'threshold' in indicator_info.keys():
        return indicator_info.get('threshold')
    output_indicator = output_indicator + "(input_df"
    for each_arg in indicator_info.get('arguments', []):
        output_indicator = output_indicator + ", " + each_arg
    output_indicator = output_indicator + ")"
    return output_indicator

def get_indicator_values(input_df, indicator_info):
    indicator = make_executable_indicator(indicator_info)
    print(f"executing {indicator}")
    return eval(indicator)

def opposite_move(input_strategy):
    if input_strategy == "BUY":
        return SELL
    elif input_strategy == "SELL":
        return BUY
    else:
        return HOLD

def execute_strategy(input_df, strategy_info):
    indicator1_info = strategy_info.get('indicator1_info')
    relation = strategy_info.get('relation')
    indicator2_info = strategy_info.get('indicator2_info')
    strategy_move = strategy_info.get('move_info')
    indicator1_values = get_indicator_values(input_df, indicator1_info)
    indicator2_values = get_indicator_values(input_df, indicator2_info)
    if relation == "CROSSOVER":
        indicator_diff = indicator1_values - indicator2_values 
        output_df = indicator_diff.apply(lambda x: strategy_move if(crossOverTrade.decide(x) == 1) else opposite_move(strategy_move) if(crossOverTrade.decide(x) == -1)  else HOLD)
    else:
        output_df = eval(f"indicator1_values {relation} indicator2_values")
    return output_df.apply(lambda x: strategy_move if x else "HOLD")

def get_max_vote_value(input_list):
    input_list = [x for x in input_list if x not in ["HOLD"]]
    if len(input_list):
        return Counter(input_list).most_common(1)[0][0]
    else:
        return "HOLD"

def aggregate_strategies(decision_info_list, selection_mode=AGGREGATION_MAXVOTE):
    agg_df = pd.concat([x for x in decision_info_list], axis=1)
    if selection_mode == AGGREGATION_MAXVOTE:
        return agg_df.apply(lambda x: get_max_vote_value(x), axis=1)
    elif selection_mode == AGGREGATION_SUM:
        return agg_df.apply(lambda x: x.sum(), axis=1)
    return agg_df

def evaluate_on_data(input_df, decision_df):
    stock_env = StockEnvironment()
    stock_df = pd.concat([input_df['close'], decision_df], axis=1)
    stock_df.columns = ['stock_price', 'decision']
    print(stock_df["decision"].value_counts())
    stock_df.apply(lambda x: stock_env.run(x), axis=1)
    return stock_env.get_trade_performance_summary()
