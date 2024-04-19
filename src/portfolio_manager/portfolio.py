import pandas as pd
from portfolio_manager.models import Allocation

class Portfolio:
    def __init__(self):
        self.target_allocations = []

    def load_target_allocations(self, filePath):
        
        self.target_allocations = []

        cols = ["AccountName", "AccountNumber", "Category", "TargetPercent", "InvestmentName", "InvestmentSymbol"]
        df = pd.read_csv(filePath, header=0, usecols=cols)
        for idx, row in df.iterrows():

            allocation = Allocation()
            allocation.account_name = row['AccountName']
            allocation.account_number = row['AccountNumber']
            allocation.category = row['Category']
            allocation.target_percentage = row['AccountNumber']
            allocation.investment_name = row['InvestmentName']
            allocation.investment_symbol = row['InvestmentSymbol']

            self.target_allocations.append(allocation)
