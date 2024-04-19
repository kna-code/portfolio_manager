class Holding:
    def __init__(self):
        self.investment_name = None
        self.symbol = None
        self.shares = None
        self.share_price = None
        self.total_value

class Account:
    def __init__(self):
        self.account_number = None
        self.holdings = []


class Allocation:
    def __init_(self):
        self.account_name = None
        self.account_number = None
        self.category = None
        self.target_percentage = None
        self.investment_name = None
        self.investment_symbol = None


class Reallocation(Allocation):
    def __init__(self):
            super.__init__(self)
            self.current_percentage = None
            self.current_value = None
            self.trade_value = None
            self.trade_action = None
            self.trade_quantity = None
            self.diff_percentage = None
            self.diff_value = None