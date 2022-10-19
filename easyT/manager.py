from datetime import datetime

from easyT.tick import get_tick
from dateutil.parser import parse
from easyT.rates import get_rates
from easyT.trade import get_trade
from easyT.platforms import Platforms
from supportLibEasyT import log_manager
from easyT.timeframe import get_timeframe
from easyT.initialization import get_initialize


class ClassNotInvoked(BaseException):
    """ Raise this error when the class is called but not invoked first!"""


class Manager:
    def __init__(self):

        self._log = log_manager.LogManager('easyt')
        self._log.logger.info('Logger Initialized in Manager')

        self.platform = None
        self.timeframe = None

        self.initialize = None

        # set rates
        self.rates = None

        # set tick
        self.tick = None

        # set trading class
        self.trade = None

        # time management
        self.time = None
        self.time_trade_start = None
        self.time_trade_stop = None
        self.time_position_close = None

    def allowed_to_trade(self) -> bool:
        """
        This function return the information if your algotrading is allowed to trade or not, it is controled by the
        manager class.

        Returns:
            It returns True or False, True if your algotrading is allowed to trade or False if not.

        Raises:
            ClassNotInvoked():
                The error occur when it tries tro return the trade._trade_allowed information before the trade
                be invoked, call the get_trade() first.

        Examples:

            >>> from easyT.manager import Manager
            >>> symbol = 'BTCUSDT'
            >>> manager = Manager()
            >>> manager.set_platform('binance-spot')
            'binance-spot'
            >>> # The Trade class need to be invoked to test the allowed_to_trade(), if it was not done, an error will
            >>> # occur
            >>> manager.allowed_to_trade()
            easyT.manager.ClassNotInvoked
            >>> manager.get_trade(symbol=symbol, lot=0.01, stop_loss=0.00, take_profit=0.00)
            <binanceSpotEasyT.trade.Trade object>
            >>> manager.allowed_to_trade()
            False


        """
        self._log.logger.info(f'allowed_to_trade called')
        if self.trade is None:
            self._log.logger.error(f'allowed_to_trade was called but trade class was not invoked,'
                                   f' call get_trade first!')
            raise ClassNotInvoked

        else:
            return self.trade._trade_allowed

    def set_platform(self, platform: str or Platforms) -> None:
        """
        This function is used to set the platform to the manager, the platform will be used for many functions
        to know witch class to return and more.

        Args:
             platform:
                It can be of type Platforms, or it can be a string. It is up to you to decide. The class Platform was
                created to reduce the errors possibilities when writing the correct name of the platform.

        Returns:
             It returns None, but it saves the platform in an attribute.

        Examples:

            >>> from easyT.manager import Manager
            >>> symbol = 'BTCUSDT'
            >>> manager = Manager()
            >>> manager.set_platform('binance-spot')
            'binance-spot'


        """
        self._log.logger.info(f'Setting platform to {platform}')

        self.platform = platform
        return self.platform

    def set_trading_time(self, time_trade_start: str, time_trade_stop: str, time_position_close: str):
        """
        This function is responsible to set the trading time, when the time is in between the start and stop,
        trade is alowed, when in between in stop and position close, it is allowed to have a position opened, but it can
        not open a new one anymore.

        After the position close, it closes the position.

        Please, pay attention to the string time format, it uses a 24h format.

        Args:
            time_trade_start:
                The time that the algotrading can starts to trade.
            time_trade_stop:
                The time that the algotrading stops to open position.
            time_position_close:
                The time the algotrading closes opened position.

        Returns:
            It updates the atributes in constructors, returns None

        Examples:

            >>> from easyT.manager import Manager
            >>> symbol = 'BTCUSDT'
            >>> manager = Manager()
            >>> manager.set_trading_time(time_trade_start='09:00', time_trade_stop='17:30', time_position_close='17:45')

        """
        self._log.logger.info(f'set_trading_time for the times:'
                              f'Start: {time_trade_start}, '
                              f'Stop: {time_trade_stop}, '
                              f'Close Position {time_position_close}')

        self.time_trade_start = time_trade_start
        self.time_trade_stop = time_trade_stop
        self.time_position_close = time_position_close

    def get_initialize(self):
        """
        This function will use the platform attribute to return the correct class between the options in the Class
        Platforms.

        Returns:
            It returns the class already invoked.

        Examples:

            >>> from easyT.manager import Manager
            >>> symbol = 'BTCUSDT'
            >>> manager = Manager()
            >>> manager.set_platform('binance-spot')
            'binance-spot'
            >>> manager.get_initialize()
            <binanceSpotEasyT.initialization.Initialize object>

        """
        self._log.logger.info(f'Get Initialize()')
        self.initialize = get_initialize(self._log, self.platform)
        return self.initialize

    def get_rates(self, count: int, symbol: str, timeframe: str or int):
        """
        This function will use the platform attribute to return the correct class between the options in the Class
        Platforms.

        Args:
            symbol:
                The symbol you want to retrieve previous data.

            timeframe (TimeFrame):
                The timeframe you want information, like 1 minute, 5 minute, 1 week.

            count:
                It is the amount of information in the past you want. If your time frame is 5 minutes and your count is 4,
                it will return 4 values containing time, open, high, low, close, tick_volume information of this past 4
                candlesticks.

        Returns:
            It returns the class already invoked.

        Examples:

            >>> from easyT.manager import Manager
            >>> symbol = 'BTCUSDT'
            >>> manager = Manager()
            >>> manager.set_platform('binance-spot')
            'binance-spot'
            >>> manager.get_initialize()
            <binanceSpotEasyT.initialization.Initialize object>
            >>> manager.get_rates(symbol=symbol, count=20, timeframe='1m')
            <binanceSpotEasyT.rates.Rates object>

        """

        self._log.logger.info(f'Get Rates()')
        self.rates = get_rates(self._log, self.platform, count=count, symbol=symbol, timeframe=timeframe)
        self.rates.update_rates()
        return self.rates

    def get_tick(self, symbol: str):
        """
        This function will use the platform attribute to return the correct class between the options in the Class
        Platforms.

        Args:
            symbol:
                It is the symbol you want information about. You can have information about time, bid, ask, last, volume.

        Returns:
            It returns the class already invoked.

        Examples:

            >>> from easyT.manager import Manager
            >>> symbol = 'BTCUSDT'
            >>> manager = Manager()
            >>> manager.set_platform('binance-spot')
            'binance-spot'
            >>> manager.get_initialize()
            <binanceSpotEasyT.initialization.Initialize object>
            >>> manager.get_tick(symbol=symbol)
            <binanceSpotEasyT.tick.Tick object>

        """
        self._log.logger.info(f'Get Tick()')
        self.tick = get_tick(self._log, self.platform, symbol.upper())
        self.tick.get_new_tick()
        return self.tick

    def get_timeframe(self):
        """
        This function will use the platform attribute to return the correct class between the options in the Class
        Platforms.

        Returns:
            It returns the class already invoked.

        Examples:

            >>> from easyT.manager import Manager
            >>> symbol = 'BTCUSDT'
            >>> manager = Manager()
            >>> manager.set_platform('binance-spot')
            'binance-spot'
            >>> manager.get_initialize()
            <binanceSpotEasyT.initialization.Initialize object>
            >>> manager.get_timeframe()
            <binanceSpotEasyT.timeframe.TimeFrame object>

        """
        self._log.logger.info(f'Get TimeFrame()')
        return get_timeframe(self._log, self.platform)

    def get_trade(self, symbol, lot, stop_loss, take_profit):
        """
        This function will use the platform attribute to return the correct class between the options in the Class
        Platforms.

        Args:
            symbol:
                It is the symbol you want to open or close or check if already have an operation opened.

            lot:
                It is how many shares you want to trade, many symbols allow fractions and others requires a
                certain amount. It can be 0.01, 100.0, 1000.0, 10000.0.

            stop_loss:
                It is how much you accept to lose. Example: If you buy a share for US$10.00, and you accept to lose US$1.00
                you set this variable at 1.00, you will be out of the operation at US$9.00 (sometimes more, somtime less,
                the US$9.00 is the trigger). Keep in mind that some symbols has different points metrics, US$1.00 sometimes
                can be 1000 points.

            take_profit:
                It is how much you accept to win. Example: If you buy a share for US$10.00, and you accept to win US$1.00
                you set this variable at 1.00, you will be out of the operation at US$11.00 (sometimes more, somtime less,
                the US$11.00 is the trigger). Keep in mind that some symbols has different points metrics, US$1.00 sometimes
                can be 1000 points.

        Returns:
            It returns the class already invoked.

        Examples:

            >>> from easyT.manager import Manager
            >>> symbol = 'BTCUSDT'
            >>> manager = Manager()
            >>> manager.set_platform('binance-spot')
            'binance-spot'
            >>> manager.get_initialize()
            <binanceSpotEasyT.initialization.Initialize object>
            >>> manager.get_trade(symbol=symbol, lot=0.01, stop_loss=0.00, take_profit=0.00)
            <binanceSpotEasyT.trade.Trade object>

        """
        self._log.logger.info(f'Getting Trade()')
        self.trade = get_trade(self._log, self.platform, symbol, lot, stop_loss, take_profit)
        return self.trade

    def supervise(self):
        """
        These functions should be calling inside the while True looping, it is responsible to updates information like
        if the AlgoTrading is allowed to trade, if it needs to close the position, and to update the tick
        and the rates' information.

        Returns:
            It updates attribute values.

       Examples:

            >>> from easyT.manager import Manager
            >>> symbol = 'BTCUSDT'
            >>> manager = Manager()
            >>> manager.set_platform('binance-spot')
            'binance-spot'
            >>> manager.get_initialize()
            <binanceSpotEasyT.initialization.Initialize object>
            >>> # It is important to know that the supervise needs the time set.
            >>> manager.supervise()
            TypeError: '<=' not supported between instances of 'datetime.datetime' and 'NoneType'
            >>> manager.set_trading_time(time_trade_start='09:00', time_trade_stop='17:30', time_position_close='17:45')
            >>> # It is important to know that it do not only need the trading time, but also, it needs the Tick() class
            >>> # to retrieve the time!
            >>> manager.get_tick(symbol=symbol)
            <binanceSpotEasyT.tick.Tick object>
            >>> manager.supervise()

        """
        self._supervise_updates()

        self.time = datetime.fromtimestamp(self.tick.time)

        self._supervise_trading_time()

    def _supervise_trading_time(self):
        """
        It checks the trading time window to see if the algotrading is allowed to trade or if it should close
        opened position.

        There is no need to inform this information, but keep in mid the Algotrading might not work as expected.

        Returns:
            It updates the trade class, informing if it is allowed to trade or not, and, close position if the
            time passed a determined time that you set to have position opened.

        """
        if self.trade is not None:
            if self.time_trade_start and self.time_trade_stop:
                self.trade._trade_allowed = parse(self.time_trade_start) <= self.time <= parse(self.time_trade_stop)

            if self.time_position_close is not None:
                if self.time > parse(self.time_position_close):
                    self.trade.position_close()

    def _supervise_updates(self):
        """
        This class call the updates for Tick and Rates if they exist, that mean, there are NOT None!

        Returns:
            It updates the Tick and Rates if possible.

        """

        if self.tick is not None:
            self.tick.get_new_tick()

        if self.rates is not None:
            self.rates.update_rates()
