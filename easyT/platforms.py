from supportLibEasyT import log_manager


class NoPlatformFound(BaseException):
    """ No platform was found, ensure that there is no mistype and that the platform is right."""


class Platforms:
    """
    This class contains all the platforms allowed in this project!

    """
    def __init__(self):

        self.BINANCE_SPOT = 'binance-spot'
        self.METATRADER5 = 'metatrader5'
