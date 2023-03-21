from supportLibEasyT.log_manager import LogManager

from easyT.platforms import NoPlatformFound
from easyT.platforms import Platforms


def get_timeframe(log: LogManager, platform):
    """
    This function return the class that responsible to hold the timeframe from different platform in a same structure.

    There are incompatibilities and different patterns in writing the timeframe between platforms.
    This class attend to reduce the chance of errors providing the same timeframe structure between platforms.

    Args:
         log:
            The log receives a log handler to be able to log the information

        platform:
            It is the platform that the information will be returned.

    Returns:
        The class or Error message:
        It returns the right class that will be used or an error message in case it was not found

    Examples:
        You can find an example of the TimeFrame usage in update_rates() function in Rates documentation

    """
    log.logger.info("get_timeframe called")
    platforms = Platforms()

    if platform == platforms.BINANCE_SPOT:
        log.logger.info(f"It is returning the platform {platforms.BINANCE_SPOT}.")

        from binanceSpotEasyT.timeframe import TimeFrame

        return TimeFrame()

    elif platform == platforms.METATRADER5:
        log.logger.info(f"It is returning the platform {platforms.METATRADER5}.")

        from metatrader5EasyT.timeframe import TimeFrame

        return TimeFrame()

    else:
        log.logger.error(
            f"The {platform} was not found, you can only use these options {platforms.__dict__.keys()}"
            f"of type Platform or the values {platforms.__dict__.values()} of type string, "
            f"both are acceptable."
        )

        raise NoPlatformFound
