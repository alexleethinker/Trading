import pandas as pd
import pybroker
from pybroker.data import DataSource


data_dir='investin/data'


class HDFDataSource(DataSource):

    def __init__(self):
        super().__init__()
        pybroker.register_columns('换手率')

    def _fetch_data(self, symbols, start_date, end_date, _timeframe, _adjust):
        store = pd.HDFStore(f'{data_dir}/history/stock/china.h5','r')        
        df = pd.DataFrame()
        for symbol in symbols:
            dfi = store[symbol]
            dfi.reset_index(inplace=True)
            dfi['symbol'] = symbol
            df = pd.concat([df, dfi], ignore_index=True)
        df = df.rename(columns= {'日期':'date','开盘':'open','收盘':'close','最高':'high','最低':'low'})
        df['date'] = pd.to_datetime(df['date'])
        store.close()
        return df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    