import pandas as pd
from investin.Utils.config import data_dir
from investin.Utils.DataLoader.common.EM import fetch_spot_em
import numpy as np
import math

def remove_suffix(name):
    suffix = [' plc',' inc',' Inc',' Ltd',' Holdings',' Corp']
    for i in suffix:
        name = name.split(i)[0]
    return name


class StockSpotUS():
    def __init__(self):
        self.read_dir = data_dir +'/static/EM/US/us_stocks.xlsx'
        self.write_dir = data_dir + '/spot/stock_spot_us.csv'
        
    def fetch(self):
        temp_df = fetch_spot_em(market='US')       
        return temp_df
    
    def clean(self, temp_df):
        stock_custom_industry = pd.read_excel(open(self.read_dir, 'rb'),sheet_name='us_stocks_industry').drop(columns = '证券名称')
        df = temp_df.merge(stock_custom_industry,how='left',on=['证券代码'])
        df['证券名称'] = df['证券名称'].apply(remove_suffix)
        df = df[~df['涨跌幅'].isnull()]
        df = df[~df['三级行业'].isnull()]
        df = df[~df['总市值'].isnull()]
        return df
    
    def update(self, df): 
        df['异动值'] = df['成交额'] * df['涨跌幅'].abs() * np.log10( (math.e - 1) * df['涨跌幅'].abs() + 1) / (np.log(df['总市值'] + 1) + 1)  
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