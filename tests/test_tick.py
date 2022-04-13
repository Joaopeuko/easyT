import pytest
from unittest.mock import patch
from easyT.tick import get_tick
from easyT.platforms import NoPlatformFound


class TestTick:
    @patch('supportLibEasyT.log_manager.LogManager')
    def test_get_tick(self, mock_logger):
        result = get_tick(log=mock_logger, platform='binance-spot', symbol='btcusdt')
        from binanceSpotEasyT.tick import Tick as Binance
        assert isinstance(result, Binance)

        result = get_tick(log=mock_logger, platform='metatrader5', symbol='eurusd')
        from metatrader5EasyT.tick import Tick as Metatrader
        assert isinstance(result, Metatrader)

        with pytest.raises(NoPlatformFound):
            get_tick(log=mock_logger, platform='wrong platform', symbol='eurusd')

