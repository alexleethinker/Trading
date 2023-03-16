import akshare as ak

stock_hsgt_stock_statistics_em_df = ak.stock_hsgt_stock_statistics_em(symbol="北向持股", start_date="20230313", end_date="20230314")
stock_hsgt_stock_statistics_em_df.to_csv('north.csv')