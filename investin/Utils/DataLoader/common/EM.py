import requests
import pandas as pd


em_fields = {
    'f2':'最新价',
    'f3':'涨跌幅',
    'f6':'成交额',
    'f8':'换手率',
    'f12':'证券代码',
    'f14':'证券名称',
    'f20':'总市值',
    'f21':'流通市值',
}
fields = [ i for i in em_fields]
fields = ','.join(fields)


def fetch_spot_em(market):
    
    if market == 'China':
        pz = '6000'
        fs = 'm:0 t:6,m:0 t:13,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048'
    elif market == 'HK':
        pz = '5000'
        fs = 'm:128 t:3,m:128 t:4,m:128 t:1,m:128 t:2'
    elif market == 'US':
        pz = '15000'
        fs = 'm:105,m:106,m:107'       
    elif market == 'UK':
        pz = '10000'
        fs = 'm:155 t:1,m:155 t:2,m:155 t:3,m:156 t:1,m:156 t:2,m:156 t:5,m:156 t:6,m:156 t:7,m:156 t:8'       
    else:
        raise('Market not support')
    
    url = 'http://40.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'pn': '1',
        'pz': pz,
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': fs,
        'fields': fields,
        '_': '1631107510188',
    }

    r = requests.get(url, params=params, timeout=10)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df = temp_df.rename(columns = em_fields)

    temp_df['流通市值'] = (pd.to_numeric(temp_df['流通市值'], errors="coerce")/100000000).round(2).fillna(0) 
    temp_df['总市值'] = (pd.to_numeric(temp_df['总市值'], errors="coerce")/100000000).round(2).fillna(0) 
    temp_df['成交额'] = (pd.to_numeric(temp_df['成交额'], errors="coerce")/100000000).round(2).fillna(0) 
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors="coerce")
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors="coerce")
    temp_df['换手率'] = pd.to_numeric(temp_df['换手率'], errors="coerce")
    temp_df = temp_df[['证券代码','证券名称','流通市值','总市值','最新价', '涨跌幅','成交额','换手率']]
    
    temp_df = temp_df[temp_df['流通市值'] > 0]
    temp_df = temp_df[temp_df['总市值'] > 0]
    temp_df = temp_df[temp_df['成交额'] > 0]
    return temp_df



if __name__ == '__main__':
    df = fetch_spot_em(market='China')
    print(df)