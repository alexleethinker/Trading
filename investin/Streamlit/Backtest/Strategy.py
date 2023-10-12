
def buy_low_sell_high_rsi(ctx):
    pos = ctx.long_pos()
    if not pos and ctx.换手率[-1] < 0.8:
        ctx.buy_shares = 100
    elif pos and ctx.换手率[-1] > 3:
        ctx.sell_shares = pos.shares