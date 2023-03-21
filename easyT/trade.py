from dotenv import load_dotenv
from supportLibEasyT.log_manager import LogManager

from easyT.platforms import NoPlatformFound
from easyT.platforms import Platforms


def get_trade(
    log: LogManager,
    platform,
    symbol: str,
    lot: float,
    stop_loss: float,
    take_profit: float,
):
    """
    This function return the class that responsible is responsible to handle all the trade requests

    It is allowed to have only one position at time per symbol, right now it is not possible to open a position and
    increase the size of it or to open opposite position. Open an open position will close the other direction one.

    Args:
         log:
            The log receives a log handler to be able to log the information

        platform:
            It is the platform that the information will be returned.

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
        The class or Error message:
        It returns the right class that will be used or an error message in case it was not found

    """
    log.logger.info("get_trade called")
    platforms = Platforms()

    if platform == platforms.BINANCE_SPOT:
        log.logger.info(f"It is returning the platform {platforms.BINANCE_SPOT}.")

        load_dotenv()
        from binanceSpotEasyT.trade import Trade

        return Trade(symbol, lot, stop_loss, take_profit)

    elif platform == platforms.METATRADER5:
        log.logger.info(f"It is returning the platform {platforms.METATRADER5}.")

        from metatrader5EasyT.trade import Trade

        return Trade(symbol, lot, stop_loss, take_profit)

    else:
        log.logger.error(
            f"The {platform} was not found, you can only use these options {platforms.__dict__.keys()}"
            f"of type Platform or the values {platforms.__dict__.values()} of type string, "
            f"both are acceptable."
        )

        raise NoPlatformFound
