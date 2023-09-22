import akshare as ak

# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000300", period="daily", start_date="20220425", end_date='20221012', adjust="")
# print(stock_zh_a_hist_df)


stock_zh_index_daily_em_df = ak.stock_zh_index_daily_em(symbol="sh000300")
print(stock_zh_index_daily_em_df)