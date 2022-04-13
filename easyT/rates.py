from supportLibEasyT.log_manager import LogManager

from easyT.platforms import Platforms
from easyT.platforms import NoPlatformFound


def get_rates(log: LogManager, platform: str, count: int, symbol: str, timeframe):
    """
    The function get_rates is used to select which rates will be used taking in consideration the platform.

    The Rates class is responsible to retrieve a certain amount of previous data.

    Args:
         log:
            The log receives a log handler to be able to log the information

        platform:
            It is the platform that the information will be returned.

        symbol:
            The symbol you want to retrieve previous data.

        timeframe (TimeFrame):
            The timeframe you want information, like 1 minute, 5 minute, 1 week.

        count:
            It is the amount of information in the past you want. If your time frame is 5 minutes and your count is 4,
            it will return 4 values containing time, open, high, low, close, tick_volume information of this past 4
            candlesticks.

    Returns:
        The class or Error message:
            It returns the right class that will be used or an error message in case it was not found


    """
    log.logger.info('get_rates called')
    platforms = Platforms()

    if platform == platforms.BINANCE_SPOT:

        log.logger.info(f'It is returning the platform {platforms.BINANCE_SPOT}.')

        from binanceSpotEasyT.rates import Rates
        return Rates(count=count, symbol=symbol, timeframe=timeframe)

    elif platform == platforms.METATRADER5:

        log.logger.info(f'It is returning the platform {platforms.METATRADER5}.')

        from metatrader5EasyT.rates import Rates
        return Rates(count=count, symbol=symbol, timeframe=timeframe)

    else:
        log.logger.error(f'The {platform} was not found, you can only use these options {platforms.__dict__.keys()}'
                         f'of type Platform or the values {platforms.__dict__.values()} of type string, '
                         f'both are acceptable.')

        raise NoPlatformFound
