import requests
import pandas as pd
import json
import os
from bs4 import BeautifulSoup
from tqdm import tqdm
try:
    from investin.Utils.config import data_dir
except:
    data_dir = 'investin/data'
    
save_path = data_dir + '/static/TradingView/isin.csv'
initiated = os.path.exists(save_path)


def get_primay_symbol_list():
    data_path = '{data_dir}/spot/stock_spot_global_primary.csv'.format(data_dir=data_dir)
    df = pd.read_csv(data_path,encoding = 'utf-8', low_memory=False)
    df = df.sort_values(by='market_cap_USD', ascending=False)
    symbol_list = list(df[df['is_primary'] == True]['full_symbol'].str.replace(':','-'))
    return symbol_list

def get_isin(symbol_string):
    url = 'https://www.tradingview.com/symbols/{symbol_string}/?route_range=full'.format(symbol_string = symbol_string)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    html = requests.get(url, headers = headers, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script", type="application/prs.init-data+json")
    symbol_dict = list(json.loads(scripts[2].text).values())[0]['data']['symbol']
    try:
        df = pd.DataFrame(list(json.loads(scripts[2].text).values())[0]['data']['related_symbols']['stocks']['data'])
    except:
        df = pd.DataFrame()
    df['primary_symbol'] = symbol_dict['pro_symbol']
    df['ticker_title'] = symbol_dict['ticker_title']
    return df

def get_fetched_list():
    fetched_list = list(pd.read_csv(save_path)['primary_symbol'].str.replace(':','-').unique()) if initiated else []
    return fetched_list

def update_result(df):
    header = False
    df.to_csv(save_path, mode='a',index = False, header=header, encoding = 'utf-8')
    

def run():
    fetched_list = get_fetched_list()
    primary_symbol_list = get_primay_symbol_list()
    symbol_list = [i for i in primary_symbol_list if i not in fetched_list]

    for symbol_string in tqdm(symbol_list):
        df = get_isin(symbol_string)
        update_result(df)


def main():
    attempts = 0
    while attempts < 10:
        try:
            run()
            break
        except:
            attempts += 1
            print('errors occur, retrying {attempts} times'.format(attempts=attempts))

if __name__ == '__main__':
    
    main()