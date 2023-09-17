import requests
import pandas as pd
import json
from datetime import datetime
import hashlib

def get_headers(url):
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


def get_xetr_prices():
    num = '1100'
    payload = '{"indices":[],"regions":[],"countries":[],"sectors":[],"types":[],"forms":[],"segments":[],"markets":[],"stockExchanges":["XETR"],"lang":"en","offset":0,"limit":'+num+',"sorting":"TURNOVER","sortOrder":"DESC"}'
    url = 'https://api.boerse-frankfurt.de/v1/search/equity_search'
    headers = get_headers(url)
    r = requests.post(url, data = payload, headers = headers, timeout = 30).text

    df = pd.json_normalize(json.loads(r)['data']) 
    df = df[['isin','slug','name.originalValue','name.translations.others','name.translations.en','overview.lastPrice','changeToPrevDay','turnover','marketCapitalisation','overview.dateTimeLastPrice']]
    return df

# 备用
def get_xetr_master_data(isin):
    url = 'https://api.boerse-frankfurt.de/v1/data/equity_master_data?isin={isin}'.format(isin=isin)
    payload = 'isin={isin}'.format(isin=isin)
    headers = get_headers(url)
    r = requests.get(url, data = payload, headers = headers, timeout = 10).text
    df = pd.json_normalize(json.loads(r)) 
    return df



def update_spot_xetr():   
    import os
    home_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    global data_path
    data_path = home_path + '/data'

    try:
        xetr_df = get_xetr_prices()
        degiro_df = pd.read_csv( data_path + '/static/xetr_degiro.csv') 
        df = degiro_df.merge(xetr_df, how = 'left', on = ['isin'])
        df.to_csv( data_path + '/spot/stock_spot_xetra.csv', index = False, encoding = 'utf-8')
        
        print('Data updated')
    except Exception as e:
        print(e)
        update_spot_xetr()


if __name__ == "__main__":

    print('Started data loader')
    update_spot_xetr()