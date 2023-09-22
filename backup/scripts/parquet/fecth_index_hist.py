import akshare as ak
import pandas as pd
import os
home_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from tqdm import tqdm

indices = {
    'sh000001':'上证指数',
    'sz399001':'深证成指',
    'sh000300':'沪深300',
    'sh000688':'科创50',
    'sh000016':'上证50',
    'sh000852':'中证1000'
}

for index in tqdm(indices):
    index_daily = ak.stock_zh_index_daily_em(symbol=index)
    index_daily.to_parquet( home_path + '/market_data/index/daily/' + index + '.parquet', index = False)