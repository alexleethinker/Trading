import requests
import pandas as pd
import json
from datetime import datetime
import hashlib
from investin.Utils.config import data_dir



class StockSpotXetra():
    def __init__(self) -> None:
        self.read_dir = data_dir + '/static/Europe/Xetra/xetra_degiro.csv'
        self.xetra_master_dir = data_dir + '/static/Europe/Xetra/xetra_masterdata.csv'
        self.write_dir = data_dir + '/spot/stock_spot_xetra.csv'
        self.translate_dir = data_dir + '/static/TradingView/translations/translation.xlsx'
        
    def _get_headers(self, url):
        clientDate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z' 
        salt = 'w4ivc1ATTGta6njAZzMbkL3kJwxMfEAKDa3MNr'
        input = clientDate + url + salt
        client_traceid = hashlib.md5(input.encode()).hexdigest()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6,zh-TW;q=0.5,nl;q=0.4',
            'Cache-Control': 'no-cache',
            'Content-Length': '199',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': 'https://www.boerse-frankfurt.de',
            'Pragma': 'no-cache',
            'Referer': 'https://www.boerse-frankfurt.de/',
            'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            ###############################
            'Client-Date': clientDate,
            'X-Client-Traceid': client_traceid,
        #     'X-Security': '925b054c5fc80fe42bdea8e06a25a4a2'
            }
        return headers
    
    def fetch_xetra_prices(self):
        num = '1100'
        payload = '{"indices":[],"regions":[],"countries":[],"sectors":[],"types":[],"forms":[],"segments":[],"markets":[],"stockExchanges":["XETR"],"lang":"en","offset":0,"limit":'+num+',"sorting":"TURNOVER","sortOrder":"DESC"}'
        url = 'https://api.boerse-frankfurt.de/v1/search/equity_search'
        headers = self._get_headers(url)
        r = requests.post(url, data = payload, headers = headers, timeout = 30).text
        df = pd.json_normalize(json.loads(r)['data']) 
        df = df[['isin','slug','name.originalValue','name.translations.others','name.translations.en','overview.lastPrice','changeToPrevDay','turnover','marketCapitalisation','overview.dateTimeLastPrice']]
        return df
    
    # 备用
    # def _get_xetr_master_data(self, isin):
    #     url = 'https://api.boerse-frankfurt.de/v1/data/equity_master_data?isin={isin}'.format(isin=isin)
    #     payload = 'isin={isin}'.format(isin=isin)
    #     headers = self._get_headers(url)
    #     r = requests.get(url, data = payload, headers = headers, timeout = 10).text
    #     df = pd.json_normalize(json.loads(r)) 
    #     return df
    
    def clean(self, df):
        degiro_df = pd.read_csv( self.read_dir) 
        df = degiro_df.merge(df, how = 'left', on = ['isin'])
        return df
    
    def add_xetra_master(self, df):
        trans_df = pd.read_excel(open(self.translate_dir, 'rb'),sheet_name='industry_trans').drop(columns=['sector'])
        master_df = pd.read_csv(self.xetra_master_dir,encoding = 'utf-8')
        df = df.merge(trans_df, on = 'industry').merge(master_df , on = 'isin')
        df.loc[~df['名称翻译'].isnull(), 'name'] = df[~df['名称翻译'].isnull()]['名称翻译']
        df = df.rename(columns={"name": "证券名称"})
        return df
    
    def update(self, df):
        df.to_csv( self.write_dir, index = False, encoding = 'utf-8')

    def run(self):
        try:
            print('Start fetch Xetra stock prices')
            df = self.fetch_xetra_prices()
            df = self.clean(df)
            df = self.add_xetra_master(df)
            self.update(df)
            print('Data all updated')
        except Exception as e:
            print('Error occurs during data loading, retrying')
            self.run()  
