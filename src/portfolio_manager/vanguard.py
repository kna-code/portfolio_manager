from io import StringIO
import pandas as pd
from pathlib import Path
from portfolio_manager.models import Holding

class Vanguard:

    @staticmethod
    def load_holdings(file_path):

        holdings = []

        # Vanguard Account Download files contain two CSV data sets concatinated to each other.
        header_holdings = "Account Number,Investment Name,Symbol,Shares,Share Price,Total Value,"
        header_transactions = "Account Number,Trade Date,Settlement Date,Transaction Type,Transaction Description,Investment Name,Symbol,Shares,Share Price,Principal Amount,Commissions and Fees,Net Amount,Accrued Interest,Account Type"
        file_contents = Path(file_path).read_text()
        data_holdings = file_contents[0:file_contents.index(header_transactions)]

        cols = ["Account Number", "Investment Name", "Symbol", "Shares", "Share Price", "Total Value"]
        df = pd.read_csv(StringIO(data_holdings), header=0, usecols=cols)
        df.dropna(inplace=True) # Drop empty rows

        for idx, row in df.iterrows():

            holding = Holding()
            holding.account_number = row['Account Number']
            holding.investment_name = row['Investment Name']
            holding.symbol = row['Symbol']
            holding.shares = row['Shares']
            holding.share_price = row['Share Price']
            holding.total_value = row['Total Value']
            holdings.append(holding)

        return holdings