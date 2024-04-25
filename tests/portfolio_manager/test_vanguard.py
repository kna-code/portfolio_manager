import pytest
from portfolio_manager.vanguard import Vanguard

def test_vanguard_load_holdings():
    filePath = "tests/data/OfxDownload.csv"

    holdings = Vanguard.load_holdings(filePath)

    assert len(holdings) == 17
    for h in holdings:
        #print(h)
        assert h.account_number is not None
        assert h.investment_name is not None
        assert h.symbol is not None
        assert h.shares is not None
        assert h.share_price is not None
        assert h.total_value is not None