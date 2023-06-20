import requests
import json
import pandas as pd
from lxml import etree
from zhconv import convert


def translate(string):
    return convert(string, 'zh-cn')

def format_code(code):
    code = code.replace('.HK','')
    code = '{:0>5}'.format(code)
    return code


def get_token():
    url_o='https://sc.hkex.com.hk/TuniS/www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=zh-HK'
    r = requests.get(url_o)
    token = etree.HTML(r.text).xpath('//*[contains(text(), "Base64-AES-Encrypted-Token")]')[0].text.split(';')[3].split()[1].replace('"','')
    return token


def get_industry_df():
    r = requests.get('https://static03.hket.com/data-lake/p/industry/industry-data.json', timeout=10)
    df = pd.DataFrame(json.loads(r.text))
    df['一级行业'] = df['industry'].apply(translate).str.replace('电讯','科技').str.replace('资讯科技','科技')
    df['二级行业'] = df['business'].apply(translate)
    df['三级行业'] = df['child-business'].apply(translate)
    df['证券名称'] = df['name'].apply(translate)
    df['证券代码'] = df['stock-id']
    df['总市值'] = df['market-cap']
    return df

def get_hkex_df():
    token = get_token()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
    url = 'https://www1.hkex.com.hk/hkexwidget/data/getequityfilter?lang=chi&token='+token+'&sort=5&order=0&all=1&qid=NULL&callback=NULL'

    res = requests.get(url, headers=headers, timeout=10)
    hkex_df = pd.DataFrame(json.loads(res.text.replace('NULL(','').replace(')',''))['data']['stocklist'])
    hkex_df['证券代码'] = hkex_df['ric'].apply(format_code)
    hkex_df['涨跌幅'] = pd.to_numeric(hkex_df['pc'], errors="coerce")
    return hkex_df



def update_spot_data_hk():  
    import os
    home_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    global data_path
    data_path = home_path + '/data'
 
    try:
        hk_industry_df = get_industry_df()
        hkex_df = get_hkex_df()

        df = hk_industry_df.merge(hkex_df, on = '证券代码', how = 'inner')
        df = df[~df['一级行业'].isnull()]
        df['总市值'] = (df['总市值']/100000000).round(1).fillna(0) 
        df = df[~df['涨跌幅'].isnull()]
        df = df[df['总市值'] > 0]

        df.to_csv( data_path + '/spot/stock_spot_hk.csv', index = False, encoding = 'utf-8')
    except:
        pass




if __name__ == "__main__":

    print('Started data loader')
    update_spot_data_hk()