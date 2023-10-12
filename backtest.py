from investin.Backtest.DataSource import HDFDataSource
from investin.Backtest.Strategy import buy_low_sell_high_rsi
from pybroker import Strategy


data_source = HDFDataSource()
strategy = Strategy(data_source, '6/1/2021', '12/1/2021')
strategy.add_execution(buy_low_sell_high_rsi, ['600089.SH', '000520.SZ', '688521.SH'])
result = strategy.backtest()




print(result.orders)