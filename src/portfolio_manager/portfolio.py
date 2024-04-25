import pandas as pd
from portfolio_manager.models import Allocation, Account, Reallocation
from portfolio_manager.vanguard import Vanguard
from datetime import datetime
import os

class Portfolio:
    def __init__(self):
        self.accounts = dict()

    def import_target_allocations(self, file_path):
        target_allocations = Portfolio.load_target_allocations(file_path)
        for ta in target_allocations:
            if ta.account_number not in self.accounts:
                a = Account(account_number=ta.account_number, account_name=ta.account_name)
                self.accounts[a.account_number] = a
            
            self.accounts[ta.account_number].target_allocations.append(ta)

    def import_holdings(self, provider, file_path):
        holdings = Portfolio.load_holdings(provider, file_path)
        for h in holdings:
            if h.account_number not in self.accounts:
                a = Account(account_number=h.account_number)
                self.accounts[a.account_number] = a

            self.accounts[h.account_number].holdings.append(h)

    def rebalance(self, output_file_path):

        # Ensure the output directory exists
        dir_path = os.path.dirname(output_file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        accounts = sorted(self.accounts.values())

        # Generate the reallocation file
        with open(output_file_path, "w+") as file:
            file.write(f"Generated {datetime.now()}\n")

            for a in accounts:
                file.write(f"\n\n\"Account: {a.account_number} ({a.account_name}): ${a.total_value():,.2f}\"\n")
                file.write(
                    "Category,Investment Name,Symbol,Target Percentage,Current Percentage,Diff Percentage,Target Value,Current Value,Diff Value,Trade Action,Trade Quantity\n");

                reallocations = Portfolio.calcuate_rebalance_trades(a)
                for r in reallocations:
                    file.write(f"{r.category},"
                               f"{r.investment_name},"
                               f"{r.symbol},"
                               f"{r.target_percentage*100:.2f}%,"
                               f"{r.current_percentage*100:.2f}%,"
                               f"{r.diff_percentage*100:.2f}%,"
                               f"\"${r.target_value:,.2f}\","
                               f"\"${r.current_value:,.2f}\","                               
                               f"\"${r.diff_value:,.2f}\","
                               f"{r.trade_action},"
                               f"\"{r.trade_quantity:,.2f}\"\n")

                

    @staticmethod
    def load_target_allocations(file_path):
        
        target_allocations = []

        cols = ["AccountName", "AccountNumber", "Category", "TargetPercent", "InvestmentName", "Symbol"]
        df = pd.read_csv(file_path, header=0, usecols=cols)
        df.dropna(inplace=True) # Drop empty rows
        df["TargetPercent"] = df["TargetPercent"].str.rstrip("%").astype(float)/100 # Convert % to Float

        for idx, row in df.iterrows():

            allocation = Allocation()
            allocation.account_name = row['AccountName']
            allocation.account_number = int(row['AccountNumber'])
            allocation.category = row['Category']
            allocation.target_percentage = row['TargetPercent']
            allocation.investment_name = row['InvestmentName']
            allocation.symbol = row['Symbol']

            target_allocations.append(allocation)

        return target_allocations

    @staticmethod
    def load_holdings(provider, file_path):
        
        if provider == "Vanguard":
            return Vanguard.load_holdings(file_path)
        else:
            raise Exception(f"Provider {provider} is not supported")
        

    @staticmethod
    def calcuate_rebalance_trades(account):

        # Validate that we have 100% 
        total_allocation_percent = 0
        target_allocations_by_symbol = dict()
        for ta in account.target_allocations:
            total_allocation_percent += ta.target_percentage
            target_allocations_by_symbol[ta.symbol] = ta

        if total_allocation_percent != 1:
            raise Exception(f"Account {account.account_number}  total target allocations are {total_allocation_percent*100}% instead of 100%")
        
        # Calcuate the total value of all holdings
        total_value = 0
        holdings_by_symbol = dict()
        for h in account.holdings:
            total_value += h.total_value
            holdings_by_symbol[h.symbol] = h

        reallocations = []

        # Calcuate the new target holdings
        for ta in account.target_allocations:

            if ta.symbol not in holdings_by_symbol:
                raise Exception(f"Account {ta.account_number} {ta.symbol} exists in the Target Allocations, but not the existing holdings. This is not currently supported because we do not have the share price.")

            holding = holdings_by_symbol[ta.symbol]

            realloc = Reallocation()
            realloc.account_name = ta.account_name
            realloc.account_number = ta.account_number
            realloc.category = ta.category
            realloc.target_percentage = ta.target_percentage
            realloc.investment_name = ta.investment_name
            realloc.symbol = ta.symbol
            
            realloc.current_value = holding.total_value
            realloc.current_percentage = realloc.current_value / total_value
            realloc.target_value = total_value * ta.target_percentage

            realloc.diff_percentage = realloc.current_percentage - realloc.target_percentage
            realloc.diff_value = realloc.current_value - realloc.target_value
            realloc.trade_quantity = -realloc.diff_value / holding.share_price
            
            if realloc.trade_quantity > 0:
                realloc.trade_action = "BUY"
            elif realloc.trade_quantity < 0:
                realloc.trade_action = "SELL"
            else:    
                realloc.trade_action = "NONE"

            reallocations.append(realloc)

        # Zero out any holdings that are no longer in the target allocations
        for holding in account.holdings:
            if h.symbol not in target_allocations_by_symbol:
                
                realloc = Reallocation()
                realloc.account_name = "Unknown"
                realloc.account_number = h.account_number
                realloc.category = "Unknown"
                realloc.target_percentage = 0
                realloc.investment_name = holding.investment_name
                realloc.symbol = holding.symbol

                realloc.current_value = holding.total_value
                realloc.current_percentage = realloc.current_value / total_value
                realloc.target_value = 0

                realloc.diff_percentage = realloc.current_percentage - realloc.target_percentage
                realloc.diff_value = realloc.current_value - realloc.target_value
                realloc.trade_quantity = -holding.shares
                
                if realloc.trade_quantity > 0:
                    realloc.trade_action = "BUY"
                elif realloc.trade_quantity < 0:
                    realloc.trade_action = "SELL"
                else:    
                    realloc.trade_action = "NONE"

                reallocations.append(realloc)

        return reallocations

    
