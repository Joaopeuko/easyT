import argparse


def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--file_name", type=str, action="store", default="demo")

    return vars(parser.parse_args())


def main():
    file_name = get_arguments()["file_name"]

    with open(f"{file_name}.py", "w") as file:
        file.write(
            """from easyT.manager import Manager
from easyT.platforms import Platforms

symbol = 'EURUSD'
platform = Platforms().METATRADER5

manager = Manager()
manager.set_platform(platform=platform)

initialize = manager.get_initialize()

initialize.initialize_platform()
initialize.initialize_symbol()

timeframe = manager.get_timeframe()

tick = manager.get_tick(symbol=symbol)
rates = manager.get_rates(count=20, symbol=symbol, timeframe=timeframe.ONE_MINUTE)
trade = manager.get_trade(symbol=symbol, lot=0.01, stop_loss=0.00003, take_profit=0.00003)

manager.set_trading_time(time_trade_start='00:05',
                         time_trade_stop='23:40',
                         time_position_close='23:55')
while True:
    manager.supervise()

    buy = (

        # Write the buy logic here!
        # Example:
        # It buys if the price is higher than the 20 candles average
        # You can set the timeframe here in the code above:
        # rates = manager.get_rates(count=20, symbol=symbol, timeframe=timeframe.ONE_MINUTE)
        tick.ask > rates.open.mean()

    )

    sell = (

        # Write sell the buy logic here!
        # Example:
        # It sells if the price is higher than the 20 candles average
        # You can set the timeframe here in the code above:
        # rates = manager.get_rates(count=20, symbol=symbol, timeframe=timeframe.ONE_MINUTE)
        tick.bid < rates.open.mean()

    )

    trade.position_open(buy, sell)
    """
        )
