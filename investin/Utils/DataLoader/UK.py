import pandas as pd
from investin.Utils.config import data_dir
from investin.Utils.DataLoader.common.EM import fetch_spot_em
import numpy as np
import math


def remove_suffix(name):
    suffix = [' PLC',' ORD',' HOLDINGS',' GROUP']
    for i in suffix:
        name = name.split(i)[0]
    return name




class StockSpotUK():
    def __init__(self):
        # self.read_dir = data_dir +'/static/EM/US/uk_stocks.xlsx'
        self.write_dir = data_dir + '/spot/stock_spot_uk.csv'
        
    def fetch(self):
        temp_df = fetch_spot_em(market='UK') 
        return temp_df
    
    def clean(self, temp_df):
        global_df = pd.read_csv( data_dir + '/spot/stock_spot_global_all.csv',low_memory=False)[['证券代码','market','一级行业','二级行业','三级行业']]
        uk_df = global_df[global_df['market'] == 'uk']
        df = temp_df.merge(uk_df,how='left',on=['证券代码'])
        df['证券名称'] = df['证券名称'].apply(remove_suffix)
        df = df[~df['涨跌幅'].isnull()]
        df = df[~df['三级行业'].isnull()]
        df = df[~df['总市值'].isnull()]
        df['成交额'] = df['成交额'] /100
        df['总市值'] = df['总市值'] /100
        return df
    
    def update(self, df):   
        # df['异动值'] = df['成交额'] * df['涨跌幅'].abs() * np.log10( (math.e - 1) * df['涨跌幅'].abs() + 1) / (np.log(df['总市值'] + 1) + 1)
        df['异动值'] = df['成交额'] * np.maximum(df['涨跌幅'].abs(), df['振幅']) * np.log10( (math.e - 1) * np.maximum(df['涨跌幅'].abs(), df['振幅']) + 1) / (np.log(df['总市值'] + 1) + 1) 
        df.to_csv( self.write_dir, index = False, encoding = 'utf-8')

    def run(self):
        attempts = 0
        while attempts < 3:
            try:
                print('Start fetching UK stock data')
                temp_df = self.fetch()
                clean_df = self.clean(temp_df)
                self.update(clean_df)
                print('Data updated')
                break
            except Exception as e:
                attempts += 1
                print('errors occur, retrying {attempts} times'.format(attempts=attempts))