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
    
    USD_forex_table['currency_id'] = USD_forex_table['currency_id'].str.replace('ZAR','ZAC').str.replace('ILS','ILA')
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

def correct_industry(df):
    correct_df = pd.read_csv(data_path + '/static/correct_industry.csv')

    tw_df = pd.read_csv(data_path + '/static/tw_all_securaties.csv').rename(columns={"有价证券代号": "code"})
    tw_df = tw_df[tw_df['产业别'].isin(['半导体业'])][['code']]
    data = {'correct_industry': 'Semiconductors', 'market': 'taiwan'}
    tw_df = tw_df.assign(**data)

    us_df = pd.read_excel(open(data_path +'/static/us_stocks.xlsx', 'rb'),sheet_name='us_stocks_industry').rename(columns={"证券代码": "code"})
    us_df = us_df[us_df['二级行业'].isin(['半导体'])][['code']]
    data = {'correct_industry': 'Semiconductors', 'market': 'america'}
    us_df = us_df.assign(**data)

    a_df = pd.read_excel(open(data_path +'/static/a_stocks.xlsx', 'rb'),sheet_name='a_stocks_info').rename(columns={"证券代码": "code",'二级行业':'correct_industry'})
    a_df = a_df[a_df['correct_industry'].isin(['半导体','光伏'])][['code','correct_industry']]
    a_df["code"] = a_df["code"].str[:6]
    a_df["correct_industry"] = a_df["correct_industry"].str.replace('半导体','Semiconductors').str.replace('光伏','Electrical Products')
    data = {'market': 'china'}
    a_df = a_df.assign(**data)

    correct_df = pd.concat([correct_df, tw_df, us_df, a_df], ignore_index=True).drop_duplicates(subset=['code', 'market'])

    df = df.merge(correct_df, how = 'left', left_on=['name','market'], right_on= ['code','market'])
    df.loc[~df['correct_industry'].isnull(), 'industry'] = df[~df['correct_industry'].isnull()]['correct_industry']
    # df = df.drop(columns = 'industry')
    # df = df.rename(columns={'correct_industry':'industry'}, inplace=True)
    # print('Data cleaned')
    return df


def translate_name(df):

    def format_hk_code(code):
        code = '{:0>5}'.format(code)
        return code
    df.loc[df['market'].isin(['hongkong']), 'name'] = df[df['market'].isin(['hongkong'])]['name'].apply(format_hk_code)

    tw_df = pd.read_csv(data_path + '/static/tw_all_securaties.csv').rename(columns={"有价证券代号": "证券代码","有价证券名称": "证券名称"})
    tw_df = tw_df[["证券代码","证券名称"]]
    tw_df['market'] = 'taiwan'

    sg_df = pd.read_csv(data_path + '/static/sg_stocks.csv').rename(columns={"交易代号": "证券代码"})
    sg_df = sg_df[["证券代码","证券名称"]]
    sg_df['market'] = 'singapore'

    hk_df = pd.read_csv(data_path + '/spot/stock_spot_hk.csv')
    hk_df = hk_df[["证券代码","证券名称"]]
    hk_df["证券代码"] = hk_df["证券代码"].str[:5]
    hk_df['market'] = 'hongkong'
    # print(hk_df)
    uk_df = pd.read_csv(data_path + '/static/uk_stocks.csv')
    uk_df = uk_df[["证券代码","证券名称"]]
    uk_df['market'] = 'uk'

    us_df = pd.read_excel(open(data_path +'/static/us_stocks.xlsx', 'rb'),sheet_name='us_stocks_industry')
    us_df = us_df[["证券代码","证券名称"]]
    us_df['market'] = 'america'   

    a_df = pd.read_excel(open(data_path +'/static/a_stocks.xlsx', 'rb'),sheet_name='a_stocks_info')
    a_df = a_df[["证券代码","股票简称"]].rename(columns={"股票简称": "证券名称"})
    a_df["证券代码"] = a_df["证券代码"].str[:6]
    a_df['market'] = 'china'  

    translate_df = pd.concat([tw_df, sg_df, hk_df, uk_df, us_df, a_df], ignore_index=True)

    df = df.merge(translate_df, how = 'left', left_on=['name','market'], right_on= ['证券代码','market'])
    df['en_description'] = df['description'] 
    df.loc[~df['证券名称'].isnull(), 'description'] = df[~df['证券名称'].isnull()]['证券名称']
    print('name translated')
    return df

def update_spot_data_global():   

    import os
    home_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    global data_path
    data_path = home_path + '/data'
   
    try:
        df = fetch_global_data()
        df = translate_name(df)
        df = correct_industry(df)
        
        df.to_csv( data_path + '/spot/stock_spot_global_all.csv', index = False, encoding = 'utf-8')

        a_df = df[( ((df['is_primary'] == True) & (df['type'] == 'stock')) | \
            ((df['is_primary'] == True) & (df['type'] == 'dr') & (df['market'].isin(['netherlands','america']))) | \
            ((df['name'].isin(['PHIA','DSM'])) & (df['market'].isin(['netherlands']))) | \
            ((df['name'].isin(['STLAM'])) & (df['market'].isin(['italy'])))    ) & \
            (~df['exchange'].isin(['OTC']))   &   (~df['name'].isin(['BRKB'])) ]
        a_df.to_csv( data_path + '/spot/stock_spot_global_primary.csv', index = False, encoding = 'utf-8')

    except Exception as e:
        print(e)


if __name__ == "__main__":

    print('Started data loader')
    update_spot_data_global()