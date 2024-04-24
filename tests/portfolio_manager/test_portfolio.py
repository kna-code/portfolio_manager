import pytest
from portfolio_manager.portfolio import Portfolio

def test_portfolio_load_target_allocations():
    filePath = "tests/data/target_allocations.csv"
    
    p = Portfolio()
    p.load_target_allocations(filePath)

    assert len(p.target_allocations) == 13
    for a in p.target_allocations:
        print(a)
        assert a.account_name is not None
        assert a.account_number is not None
        assert a.category is not None
        assert a.target_percentage > 0
        assert a.investment_name is not None
        assert a.investment_symbol is not None