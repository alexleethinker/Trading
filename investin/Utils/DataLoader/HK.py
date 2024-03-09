import requests
import json
import pandas as pd
from lxml import etree
from zhconv import convert
from investin.Utils.DataLoader.common.EM import fetch_spot_em
from investin.Utils.config import data_dir
import numpy as np
import math


def translate(string):
    return convert(string, 'zh-cn')

def format_code(code):
    code = code.replace('.HK','')
    code = '{:0>5}'.format(code)
    return code



class StockSpotHK():
    def __init__(self) -> None:
        pass

    def fetch(self):
        temp_df = fetch_spot_em(market='HK')        
        return temp_df









class StockSpotHKEX():
    def __init__(self) -> None:
        self.read_dir = data_dir +'/static/EM/HK/hk_details.csv'
        # self.write_dir = data_dir + '/spot/stock_spot_uk.csv'

    def get_industry_df(self):
        r = requests.get('https://static03.hket.com/data-lake/p/industry/industry-data.json', timeout=10)
        df = pd.DataFrame(json.loads(r.text))
        df['一级行业'] = df['industry'].fillna('').apply(translate).str.replace('电讯','科技').str.replace('资讯科技','科技')
        df['二级行业'] = df['business'].fillna('').apply(translate)
        df['三级行业'] = df['child-business'].fillna('软件开发').apply(translate)
        df['证券名称'] = df['name'].fillna('').apply(translate)
        df['证券代码'] = df['stock-id']
        df['总市值'] = df['market-cap']
        return df

    def _get_hkex_token(self):
        url_o='https://sc.hkex.com.hk/TuniS/www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=zh-HK'
        r = requests.get(url_o)
        token = etree.HTML(r.text).xpath('//*[contains(text(), "Base64-AES-Encrypted-Token")]')[0].text.split(';')[3].split()[1].replace('"','') # type: ignore
        return token

    def get_hkex_df(self):
        token = self._get_hkex_token()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        url = 'https://www1.hkex.com.hk/hkexwidget/data/getequityfilter?lang=chi&token='+token+'&sort=5&order=0&all=1&qid=NULL&callback=NULL'
        res = requests.get(url, headers=headers, timeout=10)
        hkex_df = pd.DataFrame(json.loads(res.text.replace('NULL(','').replace(')',''))['data']['stocklist'])
        hkex_df['证券代码'] = hkex_df['ric'].apply(format_code)
        hkex_df['涨跌幅'] = pd.to_numeric(hkex_df['pc'], errors="coerce")
        return hkex_df

    def clean(self, df):       
        df = df[~df['一级行业'].isnull()]
        df['总市值'] = (df['总市值']/100000000).round(1).fillna(0) 
        df['最新价'] = df['ls']
        df['证券代码'] = df['证券代码'] + '.HK'
        df = df[~df['涨跌幅'].isnull()]
        df = df[df['总市值'] > 0]
        
        df['am_u'] = df['am_u'].str.replace('B','1000000000').str.replace('M','1000000').str.replace('K','1000')
        df["am"] = pd.to_numeric(df["am"], errors="coerce")
        df["am_u"] = pd.to_numeric(df["am_u"], errors="coerce")
        df['成交额'] = ((df['am'] * df['am_u'])/100000000).round(1).fillna(0) 
        return df

    def update(self, df):
        stock_concepts = pd.read_csv(self.read_dir).drop(['证券名称','港股@总市值'], axis=1)
        df = df.merge(stock_concepts,how='left',left_on=['ric'], right_on = ['股票代码'])
        df['异动值'] = df['成交额'] * df['涨跌幅'].abs() * np.log10( (math.e - 1) * df['涨跌幅'].abs() + 1) / (np.log(df['总市值'] + 1) + 1)
        df.to_csv( data_dir + '/spot/stock_spot_hk.csv', index = False, encoding = 'utf-8')

    def run(self):
        attempts = 0
        while attempts < 3:
            try:
                print('Start fetching HK stock data')
                hk_industry_df = self.get_industry_df()
                hkex_df = self.get_hkex_df()
                df = hk_industry_df.merge(hkex_df, on = '证券代码', how = 'inner')
                df = self.clean(df)
                self.update(df)
                print('Data updated')
                break
            except Exception as e:
                attempts += 1
                print(e)
                print('errors occur, retrying {attempts} times'.format(attempts=attempts))          
