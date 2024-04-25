import pytest
from portfolio_manager.portfolio import Portfolio
from portfolio_manager.models import Account, Allocation, Holding
from pathlib import Path

def test_portfolio_import_target_allocations():
    file_path = "tests/data/target_allocations.csv"
    
    p = Portfolio()
    p.import_target_allocations(file_path)

    assert len(p.accounts) == 3
    assert len(p.accounts[1].target_allocations) == 1
    assert len(p.accounts[2].target_allocations) == 6
    assert len(p.accounts[3].target_allocations) == 6

def test_portfolio_import_holdings():
    vanguard_holdings_file_path = "tests/data/OfxDownload.csv"
  
    p = Portfolio()
    p.import_holdings("Vanguard", vanguard_holdings_file_path)

    assert len(p.accounts) == 3
    assert len(p.accounts[1].holdings) == 3
    assert len(p.accounts[2].holdings) == 7
    assert len(p.accounts[3].holdings) == 7


def test_portfolio_load_target_allocations():
    file_path = "tests/data/target_allocations.csv"
    
    target_allocations = Portfolio.load_target_allocations(file_path)

    assert len(target_allocations) == 13
    for a in target_allocations:
        #print(a)
        assert a.account_name is not None
        assert a.account_number is not None
        assert a.category is not None
        assert a.target_percentage > 0
        assert a.investment_name is not None
        assert a.symbol is not None
        
def test_portfolio_calcuate_rebalance_trades():
    a = Account()
    a.target_allocations.append(Allocation(symbol="A", target_percentage=0.25))
    a.target_allocations.append(Allocation(symbol="B", target_percentage=0.25))
    a.target_allocations.append(Allocation(symbol="C", target_percentage=0.50))
    a.holdings.append(Holding(symbol="A", share_price=100, shares=5, total_value=500))
    a.holdings.append(Holding(symbol="B", share_price=50, shares=2, total_value=100))
    a.holdings.append(Holding(symbol="C", share_price=200, shares=2, total_value=400))

    realloc = Portfolio.calcuate_rebalance_trades(a)
    #for ra in realloc:
    #    print(ra)
    assert len(realloc) == 3

    assert realloc[0].symbol == "A"
    assert realloc[0].current_percentage == 0.5
    assert realloc[0].target_percentage == 0.25
    assert realloc[0].current_value == 500
    assert realloc[0].target_value == 250
    assert realloc[0].trade_action == "SELL"
    assert realloc[0].trade_quantity == -2.5

    assert realloc[1].symbol == "B"
    assert realloc[1].current_percentage == 0.1
    assert realloc[1].target_percentage == 0.25
    assert realloc[1].current_value == 100
    assert realloc[1].target_value == 250
    assert realloc[1].trade_action == "BUY"
    assert realloc[1].trade_quantity == 3

    assert realloc[2].symbol == "C"
    assert realloc[2].current_percentage == 0.4
    assert realloc[2].target_percentage == 0.50
    assert realloc[2].current_value == 400
    assert realloc[2].target_value == 500
    assert realloc[2].trade_action == "BUY"
    assert realloc[2].trade_quantity == 0.5


def test_portfolio_rebalance():
    allocations_file_path = "tests/data/target_allocations.csv"
    vanguard_holdings_file_path = "tests/data/OfxDownload.csv"
    output_path = "tests/output/test_realloc.csv"
    
    p = Portfolio()
    p.import_target_allocations(allocations_file_path)
    p.import_holdings("Vanguard", vanguard_holdings_file_path)
    p.rebalance(output_path)

    file_contents = Path(output_path).read_text()
    lines = file_contents.split('\n')
    assert lines[11] == "\"Account: 2 (Account2): $4,970.30\""
    assert lines[12] == "Category,Investment Name,Symbol,Target Percentage,Current Percentage,Diff Percentage,Target Value,Current Value,Diff Value,Trade Action,Trade Quantity"
    assert lines[13] == "Equities-US-Large,Vanguard S&P 500 ETF,VOO,30.00%,27.94%,-2.06%,\"$1,491.09\",\"$1,388.85\",\"$-102.24\",BUY,\"0.22\""