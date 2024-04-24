class Holding:
    def __init__(self):
        self.account_number = None
        self.investment_name = None
        self.symbol = None
        self.shares = None
        self.share_price = None
        self.total_value = None

    def __str__(self):
         return f"account_number={self.investment_name}, investment_name={self.investment_name}, symbol={self.symbol}, shares={self.shares}, share_price={self.share_price}, total_value={self.total_value}"


class Account:
    def __init__(self):
        self.account_number = None
        self.holdings = []

    def __str__(self):
         return f"account_number={self.investment_name}, holdings={len(self.holdings)}"


class Allocation:
    def __init_(self):
        self.account_name = None
        self.account_number = None
        self.category = None
        self.target_percentage = None
        self.investment_name = None
        self.investment_symbol = None

    def __str__(self):
         return f"account_name={self.account_name}, account_number={self.account_number}, category={self.category}, target_percentage={self.target_percentage}, category={self.category}, investment_name={self.investment_name}, investment_symbol={self.investment_symbol}"


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