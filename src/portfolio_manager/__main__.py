from portfolio_manager.portfolio import Portfolio
import argparse
from datetime import datetime
import os

def get_args():
    """"""
    parser = argparse.ArgumentParser(
        description="An investment portfolio rebalencing tool",
        epilog="This is where you might put example usage",
    )

    parser.add_argument("-targets_csv", action="store", required=True, help="Target allocations CSV file") 
    parser.add_argument("-vanguard_csv", action="store", required=True, help="Vanguard holdings CSV file")
    parser.add_argument("-output", action="store", required=True, help="Output file path")

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    p = Portfolio()
    p.import_target_allocations(args["targets_csv"])
    p.import_holdings("Vanguard", args["vanguard_csv"])
    p.rebalance(args["output"])