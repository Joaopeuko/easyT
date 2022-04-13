import pytest
from unittest.mock import patch
from easyT.platforms import NoPlatformFound
from easyT.initialization import get_initialize


class TestInitialization:
    @patch('supportLibEasyT.log_manager.LogManager')
    def test_get_initialize(self, mock_logger):
        result = get_initialize(mock_logger, platform='binance-spot')
        from binanceSpotEasyT.initialization import Initialize as Binance
        assert isinstance(result, Binance)

        result = get_initialize(mock_logger, platform='metatrader5')
        from metatrader5EasyT.initialization import Initialize as Metatrader
        assert isinstance(result, Metatrader)

        with pytest.raises(NoPlatformFound):
            get_initialize(mock_logger, platform='wrong platform')

