from pybroker import Strategy, StrategyConfig
from pybroker.ext.data import AKShare


def buy_low(ctx):
    # If shares were already purchased and are currently being held, then return.
    if ctx.long_pos():
        return
    # If the latest close price is less than the previous day's low price,
    # then place a buy order.
    if ctx.bars >= 2 and ctx.close[-1] < ctx.low[-2]:
        # Buy a number of shares that is equal to 25% the portfolio.
        ctx.buy_shares = ctx.calc_target_shares(0.25)
        # Set the limit price of the order.
        ctx.buy_limit_price = ctx.close[-1] - 0.01
        # Hold the position for 3 bars before liquidating (in this case, 3 days).
        ctx.hold_bars = 3

data_source = AKShare()
config = StrategyConfig(initial_cash=500_000)
strategy = Strategy(data_source, '6/1/2021', '12/1/2021', config)
strategy.add_execution(buy_low, ['600089.SH', '000520.SZ', '688521.SH'])
result = strategy.backtest()



# 8. 结果分析
print("=== 回测关键指标 ===")
print(f"总收益率: {result.metrics}")
# print(f"年化收益率: {result.metrics['annualized_return']:}%")
# print(f"最大回撤: {result.metrics['max_drawdown']}%")
# print(f"夏普比率: {result.metrics['sharpe_ratio']}")
# print(f"交易次数: {result.metrics['trade_count']}")