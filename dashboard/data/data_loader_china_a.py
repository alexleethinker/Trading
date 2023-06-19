import requests
import pandas as pd


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


def stock_spot_a():
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
        'fs': 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23',
        'fields': 'f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
        '_': '1631107510188',
    }

    r = requests.get(url, params=params, timeout=10)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = range(1, len(temp_df)+1)
    temp_df.columns = [
        '序号',
        '最新价',
        '涨跌幅',
        '涨跌额',
        '成交量',
        '成交额',
        '振幅',
        '换手率',
        '市盈率-动态',
        '量比',
        '_',
        '代码',
        '_',
        '名称',
        '最高',
        '最低',
        '今开',
        '昨收',
        '总市值',
        '流通市值',
        '_',
        '市净率',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
    ]

    temp_df = temp_df[[
        '代码',
        '名称',
        '最新价',
        '总市值',
        '流通市值',
        '涨跌幅',
        '涨跌额',
        '成交量',
        '成交额',
        '振幅',
        '最高',
        '最低',
        '今开',
        '昨收',
        '量比',
        '换手率',
        '市盈率-动态',
        '市净率',
    ]]
    temp_df['证券代码'] = temp_df['代码'].apply(market_suffix)
    temp_df['证券名称'] = temp_df['名称'].str.replace(' ','').str.replace('Ａ','A')
    temp_df['流通市值'] = (pd.to_numeric(temp_df['流通市值'], errors="coerce")/100000000).round(1).fillna('') 
    temp_df['总市值'] = (pd.to_numeric(temp_df['总市值'], errors="coerce")/100000000).round(1).fillna('') 
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors="coerce")
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors="coerce")
    temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'], errors="coerce")
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'], errors="coerce")
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'], errors="coerce")
    temp_df['振幅'] = pd.to_numeric(temp_df['振幅'], errors="coerce")
    temp_df['最高'] = pd.to_numeric(temp_df['最高'], errors="coerce")
    temp_df['最低'] = pd.to_numeric(temp_df['最低'], errors="coerce")
    temp_df['今开'] = pd.to_numeric(temp_df['今开'], errors="coerce")
    temp_df['量比'] = pd.to_numeric(temp_df['量比'], errors="coerce")
    temp_df['换手率'] = pd.to_numeric(temp_df['换手率'], errors="coerce")
    temp_df = temp_df[['证券代码','证券名称','流通市值','总市值','最新价', '涨跌幅']]

    stock_custom_industry = pd.read_excel(open(data_path +'/static/a_stocks.xlsx', 'rb'),sheet_name='a_stocks').drop(['股票简称'], axis=1)
    df = temp_df.merge(stock_custom_industry,how='left',on=['证券代码'])
    df = df[~df['一级行业'].isnull()]
    df = df[~df['涨跌幅'].isnull()]
    return df

def update_spot_data_a():   
    import os
    home_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    global data_path
    data_path = home_path + '/data/'

    try:
        spot = stock_spot_a()
        spot.to_csv( data_path + '/spot/stock_spot_china_a.csv', index = False, encoding = 'utf-8')
    except:
        pass



if __name__ == "__main__":

    print('Started data loader')
    update_spot_data_a()