from unittest.mock import patch

import pytest

from easyT.platforms import NoPlatformFound
from easyT.rates import get_rates


class TestRates:
    @patch("supportLibEasyT.log_manager.LogManager")
    def test_get_rates(self, mock_logger):
        result = get_rates(
            log=mock_logger,
            platform="binance-spot",
            count=20,
            symbol="btcusdt",
            timeframe="1m",
        )
        from binanceSpotEasyT.rates import Rates as Binance

        assert isinstance(result, Binance)

        result = get_rates(
            log=mock_logger,
            platform="metatrader5",
            count=20,
            symbol="eurusd",
            timeframe=1,
        )
        from metatrader5EasyT.rates import Rates as Metatrader

        assert isinstance(result, Metatrader)

        with pytest.raises(NoPlatformFound):
            get_rates(
                log=mock_logger,
                platform="wrong platform",
                count=20,
                symbol="eurusd",
                timeframe=1,
            )
