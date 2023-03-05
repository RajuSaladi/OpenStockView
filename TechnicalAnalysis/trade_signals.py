
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