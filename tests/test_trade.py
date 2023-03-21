from unittest.mock import patch

import MetaTrader5
import pytest

from easyT.platforms import NoPlatformFound
from easyT.trade import get_trade


class TestTrade:
    @patch.object(MetaTrader5, "positions_get")
    @patch.object(MetaTrader5, "symbol_info")
    @patch("supportLibEasyT.log_manager.LogManager")
    def test_get_trade(self, mock_logger, mock_symbol_info, mock_position_get):
        mock_symbol_info.return_value.trade_tick_size = 1e-05

        result = get_trade(
            log=mock_logger,
            platform="binance-spot",
            symbol="btcusdt",
            lot=0.01,
            stop_loss=0.00,
            take_profit=0.00,
        )
        from binanceSpotEasyT.trade import Trade as Binance

        assert isinstance(result, Binance)

        result = get_trade(
            log=mock_logger,
            platform="metatrader5",
            symbol="eurusd",
            lot=0.01,
            stop_loss=0.00,
            take_profit=0.00,
        )
        from metatrader5EasyT.trade import Trade as Metatrader

        assert isinstance(result, Metatrader)

        with pytest.raises(NoPlatformFound):
            get_trade(
                log=mock_logger,
                platform="wrong platform",
                symbol="eurusd",
                lot=0.01,
                stop_loss=0.00,
                take_profit=0.00,
            )
