import pandas as pd
from investin.Utils.config import data_dir
from investin.Utils.DataLoader.common.EM import fetch_spot_em
import numpy as np
import math


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


class StockSpotChinaA():
    def __init__(self) -> None:
        # self.read_dir = data_dir +'/static/EM/China/a_stocks.xlsx'  
        self.read_dir = data_dir + '/static/EM/China/a_stock_details.csv'
        self.PE_values_dir = data_dir +'/static/EM/China/a_stock_PE_values.csv'
        self.write_dir = data_dir + '/spot/stock_spot_china_a.csv'

    def fetch(self):
        temp_df = fetch_spot_em(market='China')
        temp_df = temp_df.drop_duplicates(subset=['证券代码'])
        return temp_df
        

    def clean(self, temp_df):
        stock_custom_industry = pd.read_csv(self.read_dir).drop(['股票简称'], axis=1)
        temp_df['证券代码'] = temp_df['证券代码'].apply(market_suffix)
        temp_df['证券名称'] = temp_df['证券名称'].str.replace(' ','').str.replace('Ａ','A')
        df = temp_df.merge(stock_custom_industry,how='left',on=['证券代码'])
        PE_values = pd.read_csv(self.PE_values_dir)[['证券代码','分红比例','商誉占比','扣非PEG','扣非市赚率']]
        df = df.merge(PE_values,how='left',on=['证券代码'])
        df = df[~df['一级行业'].isnull()]
        df = df[~df['涨跌幅'].isnull()]     	 
        return df
    
    def update(self, df):  
        # df['异动值'] = df['成交额'] * df['涨跌幅'].abs() * np.log10( (math.e - 1) * df['涨跌幅'].abs() + 1) / (np.log(df['流通市值'] + 1) + 1) 
        df['异动值'] = df['成交额'] * np.maximum(df['涨跌幅'].abs(), df['振幅']) * np.log10( (math.e - 1) * np.maximum(df['涨跌幅'].abs(), df['振幅']) + 1) / (np.log(df['流通市值'] + 1) + 1) 
        df.to_csv( self.write_dir, index = False, encoding = 'utf-8')

    def run(self):
        attempts = 0
        while attempts < 3:
            try:
                print('Start fetching China A stock data')
                temp_df = self.fetch()
                print('Start cleaning data')
                clean_df = self.clean(temp_df)
                self.update(clean_df)
                print('Data updated')
                break
            except Exception as e:
                attempts += 1
                print(e)
                print('errors occur, retrying {attempts} times'.format(attempts=attempts))          

