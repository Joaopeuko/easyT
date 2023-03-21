from dotenv import load_dotenv
from supportLibEasyT.log_manager import LogManager

from easyT.platforms import NoPlatformFound
from easyT.platforms import Platforms


def get_initialize(log: LogManager, platform: str or Platforms):
    """
    This function return the class that ensure the platform are working properly.

    If it is connected on the internet, and if the symbol that you are trying to use exists or was not mistyped.

    Args:
        log:
            The log receives a log handler to be able to log the information

        platform:
            It is the platform that the information will be returned.

    Returns:
        The class or Error message:
        It returns the right class that will be used or an error message in case it was not found

    """
    log.logger.info("get_initialize called")
    platforms = Platforms()

    if platform == platforms.BINANCE_SPOT:
        log.logger.info(f"It is returning the platform {platforms.BINANCE_SPOT}.")

        load_dotenv()
        from binanceSpotEasyT.initialization import Initialize

        return Initialize()

    elif platform == platforms.METATRADER5:
        log.logger.info(f"It is returning the platform {platforms.METATRADER5}.")

        from metatrader5EasyT.initialization import Initialize

        return Initialize()

    else:
        log.logger.error(
            f"The {platform} was not found, you can only use these options {platforms.__dict__.keys()}"
            f"of type Platform or the values {platforms.__dict__.values()} of type string, "
            f"both are acceptable."
        )

        raise NoPlatformFound
