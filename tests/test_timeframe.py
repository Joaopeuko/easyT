from unittest.mock import patch

import pytest

from easyT.platforms import NoPlatformFound
from easyT.timeframe import get_timeframe


class TestTimeFrame:
    @patch("supportLibEasyT.log_manager.LogManager")
    def test_get_timeframe(self, mock_logger):
        result = get_timeframe(log=mock_logger, platform="binance-spot")
        from binanceSpotEasyT.timeframe import TimeFrame as Binance

        assert isinstance(result, Binance)

        result = get_timeframe(log=mock_logger, platform="metatrader5")
        from metatrader5EasyT.timeframe import TimeFrame as Metatrader

        assert isinstance(result, Metatrader)

        with pytest.raises(NoPlatformFound):
            get_timeframe(log=mock_logger, platform="wrong platform")
