import requests
import pandas as pd
from investin.Utils.config import data_dir
from investin.Utils.DataLoader.common.EM import fetch_spot_em


class StockSpotUK():
    def __init__(self):
        # self.read_dir = data_dir +'/static/EM/US/uk_stocks.xlsx'
        self.write_dir = data_dir + '/spot/stock_spot_uk.csv'
        
    def fetch(self):
        temp_df = fetch_spot_em(market='UK') 
        return temp_df
    
    def clean(self, temp_df):
        global_df = pd.read_csv( data_dir + '/spot/stock_spot_global_all.csv',low_memory=False)[['name','market','一级行业','二级行业','三级行业']]
        uk_df = global_df[global_df['market'] == 'uk']
        df = temp_df.merge(uk_df,how='left',left_on=['证券代码'], right_on=['name'])
        df = df[~df['涨跌幅'].isnull()]
        df = df[~df['三级行业'].isnull()]
        df = df[~df['总市值'].isnull()]
        return df
    
    def update(self, df):   
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