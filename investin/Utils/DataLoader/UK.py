import requests
import pandas as pd
from investin.Utils.config import data_dir


class StockSpotUK():
    def __init__(self):
        # self.read_dir = data_dir +'/static/EM/US/uk_stocks.xlsx'
        self.write_dir = data_dir + '/spot/stock_spot_uk.csv'
        
    def fetch(self):
        url = 'http://40.push2.eastmoney.com/api/qt/clist/get'
        params = {
            'pn': '1',
            'pz': '10000',
            'po': '1',
            'np': '1',
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': '2',
            'invt': '2',
            'fid': 'f3',
            'fs': 'm:155 t:1,m:155 t:2,m:155 t:3,m:156 t:1,m:156 t:2,m:156 t:5,m:156 t:6,m:156 t:7,m:156 t:8',
            'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152',
            '_': '1631107510188',
        }

        r = requests.get(url, params=params, timeout=10)
        data_json = r.json()
        temp_df = pd.DataFrame(data_json['data']['diff'])
        temp_df.columns = [
            "_",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "_",
            "_",
            "_",
            "_",
            "证券代码",
            "编码",
            "名称",
            "最高价",
            "最低价",
            "开盘价",
            "昨收价",
            "总市值",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
            "_",
        ]
        temp_df.reset_index(inplace=True)
        temp_df["index"] = range(1, len(temp_df) + 1)
        temp_df.rename(columns={"index": "序号"}, inplace=True)
        temp_df = temp_df[
            [
                "证券代码",
                "名称",
                "最新价",
                "涨跌额",
                "涨跌幅",
                "开盘价",
                "最高价",
                "最低价",
                "昨收价",
                '成交额',
                "总市值",
            ]
        ]
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
        temp_df["开盘价"] = pd.to_numeric(temp_df["开盘价"], errors="coerce")
        temp_df["最高价"] = pd.to_numeric(temp_df["最高价"], errors="coerce")
        temp_df["最低价"] = pd.to_numeric(temp_df["最低价"], errors="coerce")
        temp_df["昨收价"] = pd.to_numeric(temp_df["昨收价"], errors="coerce")
        temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
        return temp_df
    
    def clean(self, temp_df):
        global_df = pd.read_csv( data_dir + '/spot/stock_spot_global_all.csv',low_memory=False)[['name','market','一级行业','二级行业','三级行业']]
        uk_df = global_df[global_df['market'] == 'uk']
        df = temp_df.merge(uk_df,how='left',left_on=['证券代码'], right_on=['name'])
        df = df[~df['涨跌幅'].isnull()]
        df = df[~df['三级行业'].isnull()]
        df = df[~df['总市值'].isnull()]
        df['总市值'] = (df['总市值']/10000000000).round(2)
        df['成交额'] = (df['成交额']/10000000000).round(2)
        df =df.rename(columns={"名称": "证券名称"})
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