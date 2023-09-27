import requests
import pandas as pd
from investin.Utils.config import data_dir
from investin.Utils.DataLoader.common.EM import fetch_spot_em


class StockSpotUS():
    def __init__(self):
        self.read_dir = data_dir +'/static/EM/US/us_stocks.xlsx'
        self.write_dir = data_dir + '/spot/stock_spot_us.csv'
        
    def fetch(self):
        temp_df = fetch_spot_em(market='US')       
        return temp_df
    
    def clean(self, temp_df):
        stock_custom_industry = pd.read_excel(open(self.read_dir, 'rb'),sheet_name='us_stocks_industry')
        df = temp_df.merge(stock_custom_industry,how='left',on=['证券代码'])
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
                print('Start fetching US stock data')
                temp_df = self.fetch()
                clean_df = self.clean(temp_df)
                self.update(clean_df)
                print('Data updated')
                break
            except Exception as e:
                attempts += 1
                print('errors occur, retrying {attempts} times'.format(attempts=attempts))