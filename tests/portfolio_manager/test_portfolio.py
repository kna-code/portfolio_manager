import pytest
from portfolio_manager.portfolio import Portfolio

def test_portfolio_load_target_allocations():
    filePath = "tests/data/target_allocations.csv"
    
    p = Portfolio()
    p.load_target_allocations(filePath)

    assert len(p.target_allocations) == 15
    for allocation in p.target_allocations:
        assert allocation.account_name is not None
        assert allocation.account_number is not None
        assert allocation.category is not None
        assert allocation.target_percentage is not None
        assert allocation.investment_name is not None
        assert allocation.investment_symbol is not None