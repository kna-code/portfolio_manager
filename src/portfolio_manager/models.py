class Holding:
    def __init__(self, account_number = None, investment_name = None, symbol = None, shares = None, share_price = None, total_value = None):
        self.account_number = account_number
        self.investment_name = investment_name
        self.symbol = symbol
        self.shares = shares
        self.share_price = share_price
        self.total_value = total_value

    def __str__(self):
         return f"account_number={self.investment_name}, investment_name={self.investment_name}, symbol={self.symbol}, shares={self.shares}, share_price={self.share_price}, total_value={self.total_value}"


class Account:
    def __init__(self, account_number = None):
        self.account_number = account_number
        self.target_allocations = []
        self.holdings = []

    def __str__(self):
         return f"account_number={self.account_number}, target_allocations={len(self.target_allocations)}, holdings={len(self.holdings)}"


class Allocation:
    def __init__(self, account_name=None, account_number=None, category=None, target_percentage=None, investment_name=None, symbol=None):
        self.account_name = account_name
        self.account_number = account_number
        self.category = category
        self.target_percentage = target_percentage
        self.investment_name = investment_name
        self.symbol = symbol

    def __str__(self):
         return f"account_name={self.account_name}, account_number={self.account_number}, category={self.category}, target_percentage={self.target_percentage}, category={self.category}, investment_name={self.investment_name}, symbol={self.symbol}"


class Reallocation():
    def __init__(self, account_name=None, account_number=None, category=None, target_percentage=None, investment_name=None, symbol=None):
            self.account_name = account_name
            self.account_number = account_number
            self.category = category
            self.target_percentage = target_percentage
            self.investment_name = investment_name
            self.symbol = symbol
            self.current_percentage = None
            self.current_value = None
            self.target_value = None
            self.trade_value = None
            self.trade_action = None
            self.trade_quantity = None
            self.diff_percentage = None
            self.diff_value = None

    def __str__(self):
         return f"account_number={self.account_number}, symbol={self.symbol}, current_value={self.current_value}, target_value={self.target_value}, current_percentage={self.current_percentage}, target_percentage={self.target_percentage}, trade_action={self.trade_action}, trade_quantity={self.trade_quantity}"
