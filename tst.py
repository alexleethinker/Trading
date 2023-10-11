from investin.Utils.HistoryDataLoader.common.stock import stock_zh_a_hist
from investin.Utils.DataLoader.common.EM import fetch_spot_em
from tqdm import tqdm
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
from investin.Utils.config import data_dir
import pandas as pd

save_dir = f'{data_dir}/history/stock/china.h5'
today = datetime.today().strftime('%Y%m%d')

# stock_daily = stock_zh_a_hist(symbol='600089', period='daily', adjust="hfq")

def market_suffix(code):
    if code[:1] == '6':
        code = code + '.SH'
    elif code[:1] in ['0','3']:
        code = code + '.SZ'
    elif code[:1] in ['8','4']:
        code = code + '.BJ'
    else:
        pass
    return code

print("获取股票代码列表...")
stock_list = fetch_spot_em(market='China')['证券代码']


store = pd.HDFStore(save_dir, mode='a')
print("更新股票历史行情...")
def fetch_hist(stock):
    with pool_sema:
        try:
            df = stock_zh_a_hist(symbol = stock, period='daily', adjust="hfq")
            df['日期'] = pd.to_datetime(df['日期'])
            df = df.set_index(['日期'])
            try:
                updates = df.loc[df.index.difference(store[market_suffix(stock)].index)]
            except:
                updates = df
            store.append(market_suffix(stock), updates)
        except:
            print( stock + " failed")
        pool_sema.release()



import threading
threads = []

max_connections = 10  # 定义最大线程数
pool_sema = threading.BoundedSemaphore(max_connections) # 或使用Semaphore方法

with tqdm(total=stock_list.shape[0]) as pbar:
    for stock in stock_list:
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
        