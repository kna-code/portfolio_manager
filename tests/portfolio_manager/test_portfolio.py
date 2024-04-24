import pytest
from portfolio_manager.portfolio import Portfolio
from portfolio_manager.models import Account, Allocation, Holding

def test_import_target_allocations():
    file_path = "tests/data/target_allocations.csv"
    
    p = Portfolio()
    p.import_target_allocations(file_path)

    assert len(p.accounts) == 3
    assert len(p.accounts[1].target_allocations) == 6
    assert len(p.accounts[2].target_allocations) == 6
    assert len(p.accounts[3].target_allocations) == 1


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

