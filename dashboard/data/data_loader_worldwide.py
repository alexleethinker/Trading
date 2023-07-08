import requests
import pandas as pd
import json


def check_plate(market):
    fvey = ['america','canada']
    eur = ['uk','belgium','france','germany','italy','luxembourg','netherlands','portugal','spain','switzerland','cyprus','greece']
    n_eur = ['iceland','denmark','finland','norway','sweden']
    china = ['china','hongkong']
    east_asia = ['japan','korea','taiwan','australia','newzealand']
    latin_america = ['argentina','brazil','chile','colombia','mexico','peru','venezuela']
    middle_east = ['bahrain','egypt','israel','kuwait','qatar','turkey','uae','ksa']
    africa = ['kenya','morocco','nigeria','tunisia','rsa']
    asan = ['indonesia','malaysia','philippines','singapore','thailand','vietnam']
    indian = ['india','pakistan','srilanka']
    east_eur = ['russia','lithuania','latvia','estonia','serbia','hungary','romania','poland','slovakia']    
    
    if market in fvey:
        market = '北美'
    elif market in (eur + n_eur):
        market = '欧洲'
#     elif market in east_eur:
#         market = 'East Europe'
    elif market in china:
        market = '中国'
    elif market in east_asia:
        market = '亚太'
    elif market in latin_america :
        market = '拉丁美洲'
    elif market in middle_east + africa + east_eur:
        market = '中东/非/东欧'
    elif market in indian:
        market = '南亚'
    elif market in asan:
        market = '东盟'
    else:
        market = 'Rest'
    return market



def get_USD_forex_table():
    url = 'https://scanner.tradingview.com/forex/scan'
    payload = '{"columns":["currency_logoid","base_currency_logoid","name","description","update_mode","type","typespecs","close","pricescale","minmov","fractional","minmove2","currency","change","change_abs","bid","ask","high","low","Recommend.All"],"ignore_unknown_fields":false,"options":{"lang":"en"},"range":[0,2000],"sort":{"sortBy":"name","sortOrder":"asc","nullsFirst":false},"preset":"forex_rates_all"}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}

    r = requests.post(url, headers = headers, data = payload, timeout=10).text
    forex_df = pd.DataFrame(json.loads(r)['data'])['d']
    forex_df = pd.DataFrame(forex_df.tolist(), index = forex_df.index)
    USD_forex_table = forex_df[(forex_df[12] == 'USD')][[2,3,7]]
    USD_forex_table['currency_id'] =  USD_forex_table[2].str.replace('USD','').str.replace('GBP','GBX')
    USD_forex_table['name'] =  USD_forex_table[3].str.replace(' / U.S. DOLLAR','')
    USD_forex_table['forex_rate'] =  USD_forex_table[7]
    USD_forex_table = USD_forex_table.reset_index(inplace = False)[['currency_id','forex_rate']]
#     USD_forex_table = USD_forex_table.append({'currency_id':'USD','forex_rate':1}, ignore_index=True)
    USD_forex_table = pd.concat([USD_forex_table, pd.DataFrame({'currency_id':['USD'],'forex_rate':[1]})], ignore_index=True)

    
    USD_forex_table.loc[USD_forex_table['currency_id'].isin(['GBX']), 'forex_rate'] = USD_forex_table[USD_forex_table['currency_id'].isin(['GBX'])]['forex_rate']/100 
    return USD_forex_table

def fetch_global_data():
    
    country = 'global'
    columns = '["name","description","type","close","currency","change","Value.Traded","market_cap_basic","fundamental_currency_code","sector","industry","market","is_primary","exchange","country"]'
    payload = '{"columns":'+ columns +',"filter":[{"left":"typespecs","operation":"has_none_of","right":["etn","etf"]}],"ignore_unknown_fields":false,"price_conversion":{"to_currency":"usd"},"range":[0,90000],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"},"markets":["america","argentina","australia","bahrain","belgium","brazil","canada","chile","china","colombia","cyprus","denmark","egypt","estonia","finland","france","germany","greece","hongkong","hungary","iceland","india","indonesia","israel","italy","japan","kenya","kuwait","latvia","lithuania","luxembourg","malaysia","mexico","morocco","netherlands","newzealand","nigeria","norway","pakistan","peru","philippines","poland","portugal","qatar","romania","russia","ksa","serbia","singapore","slovakia","rsa","korea","spain","srilanka","sweden","switzerland","taiwan","thailand","tunisia","turkey","uae","uk","venezuela","vietnam"]}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
    
    url = 'https://scanner.tradingview.com/' + country + '/scan'
    r = requests.post(url, headers = headers, data = payload, timeout=10).text
    df = pd.DataFrame(json.loads(r)['data'])['d']
    df = pd.DataFrame(df.tolist(), index = df.index, columns = json.loads(columns))
    
    USD_forex_table = get_USD_forex_table()
    df = df.merge(USD_forex_table,left_on='currency', right_on = 'currency_id')
    
    df['market_cap_USD'] = (df['market_cap_basic']/100000000).fillna(0)
    df = df[df['market_cap_USD'] > 0]
    
    df['Traded_USD'] = (df['Value.Traded']* df['forex_rate']/100000000).fillna(0)
    df = df[df['Value.Traded'] > 0.01]
    
    df['turnover_rate'] = (df['Traded_USD'] / df['market_cap_USD']).round(4)
    
    df['plate'] = df['market'].apply(check_plate)
    df = df[~df['change'].isnull()]
    df = df[~df['industry'].isnull()]
    df = df[~df['sector'].isnull()]
    df = df[~df['market_cap_basic'].isnull()]
    
    return df



def update_spot_data_global():   

    import os
    home_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    global data_path
    data_path = home_path + '/data'
   
    try:
        df = fetch_global_data()
        df.to_csv( data_path + '/spot/stock_spot_global_all.csv', index = False, encoding = 'utf-8')

        a_df = df[( ((df['is_primary'] == True) & (df['type'] == 'stock')) | \
            ((df['is_primary'] == True) & (df['type'] == 'dr') & (df['market'].isin(['netherlands','america']))) | \
            ((df['name'].isin(['PHIA','DSM'])) & (df['market'].isin(['netherlands']))) | \
            ((df['name'].isin(['STLAM'])) & (df['market'].isin(['italy'])))    ) & \
            (~df['exchange'].isin(['OTC']))   &   (~df['name'].isin(['BRKB'])) ]
        a_df.to_csv( data_path + '/spot/stock_spot_global_primary.csv', index = False, encoding = 'utf-8')

    except:
        pass


if __name__ == "__main__":

    print('Started data loader')
    update_spot_data_global()