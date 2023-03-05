from TechnicalAnalysis.trade_signals import CrossOverTrader


crossOverTrade = CrossOverTrader()

def simple_moving_average(input_df, short_window=20, longer_window=50):
    
    mva_shorter = input_df['close'].rolling(window=short_window).mean()
    mva_longer = input_df['close'].rolling(window=longer_window).mean()
    mva_diff = mva_shorter - mva_longer
    # input_df['crossover'] = np.sign(crossover).diff().ne(0)
    mva_cross_over = mva_diff.apply(lambda x: crossOverTrade.decide(x))
    return mva_shorter, mva_longer, mva_cross_over

def exponential_moving_average(input_df, short_window=20, longer_window=50):
    emva_shorter = input_df['close'].ewm(span=short_window, adjust=False).mean()
    emva_longer = input_df['close'].ewm(span=longer_window, adjust=False).mean()
    ewm_diff = emva_shorter - emva_longer
    ewmva_cross_over = ewm_diff.apply(lambda x: crossOverTrade.decide(x))
    return emva_shorter, emva_longer, ewmva_cross_over

def moving_average_converge_divergence(input_df, short_window=12, longer_window=26, signal_period=9):
    emva_shorter = input_df['close'].ewm(span=short_window, adjust=False).mean()
    emva_longer = input_df['close'].ewm(span=longer_window, adjust=False).mean()
    macd = emva_shorter - emva_longer
    macd_emva = macd.ewm(span=signal_period, adjust=False).mean()
    return macd - macd_emva
