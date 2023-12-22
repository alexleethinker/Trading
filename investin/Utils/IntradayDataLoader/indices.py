import requests
import json
import pandas as pd
from investin.Utils.config import data_dir

read_path = f'{data_dir}/static/EM/Indices/indices.csv'

def get_index(secid):
    write_path = f'{data_dir}/intraday/indices/{secid}.json'
    url = 'https://push2his.eastmoney.com/api/qt/stock/trends2/get'
    params = {
        'secid': secid,
        'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58',
        'ut': 'e1e6871893c6386c5ff6967026016627',
        'iscr': '0',
    }
    r = requests.get(url, params=params, timeout=10)
    data_json = r.json()['data']
    with open(write_path, 'w', encoding='utf-8') as f:
        json.dump(data_json, f)
      
def run(secid):
    attempts = 0
    while attempts < 3:
        try:
            print(f'Start fetching {secid} data')
            get_index(secid)
            break
        except Exception as e:
            attempts += 1
            print(e)
            print('errors occur, retrying {attempts} times'.format(attempts=attempts))  
            

def indices_intraday():
    indices_df = pd.read_csv(read_path,encoding = 'utf-8')
    for i, row in indices_df.iterrows():
        run(row['indices'])

def indices_intraday_china():
    indices_df = pd.read_csv(read_path,encoding = 'utf-8')
    indices_df = indices_df[indices_df['region'].isin(['中国'])]
    for i, row in indices_df.iterrows():
        run(row['indices'])

def indices_intraday_hk():
    indices_df = pd.read_csv(read_path,encoding = 'utf-8')
    indices_df = indices_df[indices_df['region'].isin(['香港'])]
    for i, row in indices_df.iterrows():
        run(row['indices'])

def indices_intraday_apac():
    indices_df = pd.read_csv(read_path,encoding = 'utf-8')
    indices_df = indices_df[indices_df['region'].isin(['亚太'])]
    for i, row in indices_df.iterrows():
        run(row['indices'])
        
def indices_intraday_india():
    indices_df = pd.read_csv(read_path,encoding = 'utf-8')
    indices_df = indices_df[indices_df['region'].isin(['印度'])]
    for i, row in indices_df.iterrows():
        run(row['indices'])

def indices_intraday_US():
    indices_df = pd.read_csv(read_path,encoding = 'utf-8')
    indices_df = indices_df[indices_df['region'].isin(['美国'])]
    for i, row in indices_df.iterrows():
        run(row['indices'])

def indices_intraday_europe():
    indices_df = pd.read_csv(read_path,encoding = 'utf-8')
    indices_df = indices_df[indices_df['region'].isin(['欧洲'])]
    for i, row in indices_df.iterrows():
        run(row['indices'])    



if __name__ == '__main__':
    
    
    indices_intraday_apac()