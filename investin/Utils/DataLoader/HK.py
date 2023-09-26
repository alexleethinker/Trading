import requests
import json
import pandas as pd
from lxml import etree
from zhconv import convert

from investin.Utils.config import data_dir

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
        url = 'http://40.push2.eastmoney.com/api/qt/clist/get'
        params = {
            'pn': '1',
            'pz': '6000',
            'po': '1',
            'np': '1',
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': '2',
            'invt': '2',
            'fid': 'f3',
            'fs': 'm:128 t:3,m:128 t:4,m:128 t:1,m:128 t:2',
            'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152',
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
            "_",
            "总市值",
            "港股市值",
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
                "流通市值",
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
        temp_df["流通市值"] = pd.to_numeric(temp_df["流通市值"], errors="coerce")          
        return temp_df









class StockSpotHKEX():
    def __init__(self) -> None:
        pass

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
                print('errors occur, retrying {attempts} times'.format(attempts=attempts))          
