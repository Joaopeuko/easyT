import pytest
from dateutil.parser import parse
from easyT.manager import Manager
from binanceSpotEasyT.tick import Tick
from binanceSpotEasyT.rates import Rates
from binanceSpotEasyT.trade import Trade
from easyT.manager import ClassNotInvoked
from binanceSpotEasyT.timeframe import TimeFrame
from binanceSpotEasyT.initialization import Initialize


class TestTrade:

    def test_set_platform(self):
        manager = Manager()
        manager.set_platform('binance-spot')

        assert manager.platform == 'binance-spot'

        manager = Manager()
        manager.set_platform('metatrader5')

        assert manager.platform == 'metatrader5'

    def test_allowed_to_trade(self):
        manager = Manager()
        manager.set_platform('binance-spot')

        with pytest.raises(ClassNotInvoked):
            manager.allowed_to_trade()

        manager.get_trade('btcusdt', 0.01, 0.00, 0.00)
        assert manager.allowed_to_trade() is False

        manager.trade._trade_allowed = True

        assert manager.allowed_to_trade() is True

    def test_trading_time(self):
        manager = Manager()
        manager.set_platform('binance-spot')

        assert manager.time_trade_start is None
        assert manager.time_trade_stop is None
        assert manager.time_position_close is None

        time_start = '09:00'
        time_stop = '17:23'
        time_close = '17:45'

        manager.set_trading_time(time_start, time_stop, time_close)

        assert manager.time_trade_start == time_start
        assert manager.time_trade_stop == time_stop
        assert manager.time_position_close == time_close

    def test_get_initialize(self):
        manager = Manager()
        manager.set_platform('binance-spot')
        initialize = manager.get_initialize()

        assert isinstance(initialize, Initialize)

    def test_get_rates(self):
        manager = Manager()
        manager.set_platform('binance-spot')
        rates = manager.get_rates(20, 'btcusdt', '1m')

        assert isinstance(rates, Rates)

    def test_get_tick(self):
        manager = Manager()
        manager.set_platform('binance-spot')
        tick = manager.get_tick('btcusdt')

        assert isinstance(tick, Tick)

    def test_get_timeframe(self):
        manager = Manager()
        manager.set_platform('binance-spot')
        timeframe = manager.get_timeframe()

        assert isinstance(timeframe, TimeFrame)

    def test_get_trade(self):
        manager = Manager()
        manager.set_platform('binance-spot')
        trade = manager.get_trade('btcusdt', 0.01, 0.00, 0.00)

        assert isinstance(trade, Trade)

    def test_supervise(self):
        manager = Manager()
        manager.set_platform('binance-spot')
        manager.get_tick('btcusdt')

        assert manager.time is None
        manager.supervise()
        assert manager.time is not None

        manager.get_rates(20, 'btcusdt', '1m')
        assert manager.rates.time is None
        manager.supervise()
        assert manager.rates.time is not None

    def test_time(self):
        manager = Manager()
        manager.set_platform('binance-spot')
        manager.get_trade('btcusdt', 0.01, 0.00, 0.00)
        manager.get_tick('btcusdt')

        result = manager.allowed_to_trade()
        manager.set_trading_time('10:00', '12:00', '13:00')
        assert result is False
        manager.time = parse('11:00')
        manager._supervise_trading_time()
        result = manager.allowed_to_trade()
        assert result is True

