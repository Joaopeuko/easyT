from supportLibEasyT.log_manager import LogManager

from easyT.platforms import NoPlatformFound
from easyT.platforms import Platforms


def get_tick(log: LogManager, platform, symbol: str):
    """
    This function return the class that responsible to retrieve every tick information.

    Tick class is the responsible to retrieve every tick information.

    Args:
         log:
            The log receives a log handler to be able to log the information

        platform:
            It is the platform that the information will be returned.

        symbol:
         It is the symbol you want information about. You can have information about time, bid, ask, last, volume.

    Returns:
        The class or Error message:
        It returns the right class that will be used or an error message in case it was not found

    """
    log.logger.info("get_tick called")
    platforms = Platforms()

    if platform == platforms.BINANCE_SPOT:
        log.logger.info(f"It is returning the platform {platforms.BINANCE_SPOT}.")

        from binanceSpotEasyT.tick import Tick

        return Tick(symbol)

    elif platform == platforms.METATRADER5:
        log.logger.info(f"It is returning the platform {platforms.METATRADER5}.")

        from metatrader5EasyT.tick import Tick

        return Tick(symbol)

    else:
        log.logger.error(
            f"The {platform} was not found, you can only use these options {platforms.__dict__.keys()}"
            f"of type Platform or the values {platforms.__dict__.values()} of type string, "
            f"both are acceptable."
        )

        raise NoPlatformFound
