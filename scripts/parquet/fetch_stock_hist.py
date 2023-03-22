import akshare as ak
import tushare as ts
pro = ts.pro_api('158ce95d6e799f55b8e8277aa1f6138fa71acf9c52df5ec667296fbc')
import os
home_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from tqdm import tqdm
from datetime import datetime

today = datetime.today().strftime('%Y%m%d')
period = "daily"
save_path = home_path + '/market_data/stock/' + period + '/'
if not os.path.exists(save_path):
   os.makedirs(save_path)

# # get stock list from east money
# print("获取股票代码列表...")
# spot = ak.stock_zh_a_spot_em()
# spot = spot[~spot['最新价'].isnull()]
# stocks_list = spot['代码'].tolist()

# for stock in tqdm(stocks_list):
#     stock_daily = ak.stock_zh_a_hist(symbol=stock, period=period, start_date="19910101", end_date=today, adjust="")
#     stock_daily.to_parquet( save_path + stock + '.parquet', index = False)

print("获取股票代码列表...")
stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,list_date')

print("更新股票历史行情...")


def fetch_hist(stock):
    with pool_sema:
        try:
            stock_daily = ak.stock_zh_a_hist(symbol=stock['symbol'], period=period, start_date=stock['list_date'], end_date=today, adjust="")
            stock_daily.to_parquet( save_path + stock['symbol'] + '.parquet', index = False)   
        except:
            print( stock['ts_code'] + " failed")
        pool_sema.release()
# for row, stock in tqdm(stock_list.iterrows(),  total=stock_list.shape[0]):
#     stock_daily = pro.daily(ts_code=stock['ts_code'], period=period, start_date=stock['list_date'], end_date=today, adjust="")
#     stock_daily.to_parquet( save_path + stock['symbol'] + '.parquet', index = False)


import threading
threads = []

max_connections = 2  # 定义最大线程数
pool_sema = threading.BoundedSemaphore(max_connections) # 或使用Semaphore方法

with tqdm(total=stock_list.shape[0]) as pbar:
    for row, stock in stock_list.iterrows():
        t = threading.Thread(target = fetch_hist, args = (stock,))
        threads.append(t)
    #print(threads)
    for t in threads:
        pool_sema.acquire()
        t.start()
        pbar.update(1)
    # 等待所有thread完成之后再执行之后的代码    
    for t in threads: 
        t.join()
        
