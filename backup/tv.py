import pandas as pd
import requests
import json

def fetch_global_prices():
    country = 'global'
    markets = '["america","argentina","australia","austria","bahrain","bangladesh","belgium","brazil","canada","chile","china","colombia","cyprus","czech","denmark","egypt","estonia","finland","france","germany","greece","hongkong","hungary","iceland","india","indonesia","israel","italy","japan","kenya","kuwait","latvia","lithuania","luxembourg","malaysia","mexico","morocco","netherlands","newzealand","nigeria","norway","pakistan","peru","philippines","poland","portugal","qatar","romania","russia","ksa","serbia","singapore","slovakia","rsa","korea","spain","srilanka","sweden","switzerland","taiwan","thailand","tunisia","turkey","uae","uk","venezuela","vietnam"]'
    columns = '["isin","name","description","logoid","type","close","currency","change","Value.Traded","market_cap_basic","fundamental_currency_code","sector","industry","market","is_primary","exchange","country"]'
    payload = '{"columns":'+ columns +',"filter":[{"left":"typespecs","operation":"has_none_of","right":["etn","etf"]}],"ignore_unknown_fields":false,"price_conversion":{"to_currency":"usd"},"range":[0,80000],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"markets":' + markets + '}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    url = 'https://scanner.tradingview.com/' + country + '/scan'
    r = requests.post(url, headers = headers, data = payload, timeout=10).text
    df_data = pd.DataFrame(json.loads(r)['data'])['d']
    df_data = pd.DataFrame(df_data.tolist(), index = df_data.index, columns = json.loads(columns))
    df_s    = pd.DataFrame(json.loads(r)['data'])['s']
    df_s    = pd.DataFrame(df_s.tolist(), index = df_s.index, columns = ['full_symbol'])
    df = pd.concat([df_s, df_data], axis=1)
    return df


df = fetch_global_prices()
df.to_csv('tv.csv',index = False)