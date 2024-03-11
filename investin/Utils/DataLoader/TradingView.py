import requests
import pandas as pd
import json
from investin.Utils.config import data_dir
import numpy as np
import math



def remove_suffix(name):
    suffix = [',',' PLC',' ORD',' HOLDINGS',' GROUP', ' plc',' inc',' Inc', ' INC',' Ltd',' Holdings',' Corp','ON NM']
    for i in suffix:
        name = str(name).split(i)[0]
    return name


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
    USD_forex_table['currency_id'] = USD_forex_table['currency_id'].str.replace('ZAR','ZAC').str.replace('ILS','ILA')
    USD_forex_table.loc[USD_forex_table['currency_id'].isin(['GBX','ZAC','ILA']), 'forex_rate'] = USD_forex_table[USD_forex_table['currency_id'].isin(['GBX','ZAC','ILA'])]['forex_rate']/100 
    return USD_forex_table



def check_plate(market):
    fvey = ['america','canada']
    eur = ['uk','belgium',"czech",'france','germany','italy','luxembourg','netherlands','portugal','spain','switzerland','cyprus','greece']
    n_eur = ['iceland','denmark','finland','norway','sweden']
    china = ['china','hongkong']
    east_asia = ['japan','korea','taiwan','australia','newzealand']
    latin_america = ['argentina','brazil','chile','colombia','mexico','peru','venezuela']
    middle_east = ['bahrain','egypt','israel','kuwait','qatar','turkey','uae','ksa']
    africa = ['kenya','morocco','nigeria','tunisia','rsa']
    asan = ['indonesia','malaysia','philippines','singapore','thailand','vietnam']
    indian = ["bangladesh",'india','pakistan','srilanka']
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
        market = '拉美'
    elif market in middle_east + africa + east_eur:
        market = '中东非'
    elif market in indian:
        market = '南亚'
    elif market in asan:
        market = '东盟'
    else:
        market = 'Rest'
    return market



class StockSpotTradingView():
    def __init__(self) -> None:
        self.hk_dir = data_dir + '/spot/stock_spot_hk.csv'
        self.us_dir = data_dir + '/static/EM/US/us_stocks.xlsx'
        self.a_dir  = data_dir + '/static/EM/China/a_stocks.xlsx'

        self.isin_dir = data_dir + '/static/TradingView/isin.csv'
        self.correct_ind = data_dir + '/static/TradingView/correct_industry.csv'
        self.tw_dir = data_dir + '/static/TradingView/tw_all_securaties.csv'
        self.sg_dir = data_dir + '/static/TradingView/sg_stocks.csv'
        self.uk_dir = data_dir + '/static/TradingView/uk_stocks.csv'

        self.translate_dir = data_dir + '/static/TradingView/translations/translation.xlsx'
        self.translate_name_dir = data_dir + '/static/TradingView/translations/stock_name_translation.csv'
        self.dr_name_dir = data_dir + '/static/TradingView/translations/dr_names.csv'

    def fetch_global_prices(self):
        country = 'global'
        markets = '["america","argentina","australia","austria","bahrain","bangladesh","belgium","brazil","canada","chile","china","colombia","cyprus","czech","denmark","egypt","estonia","finland","france","germany","greece","hongkong","hungary","iceland","india","indonesia","israel","italy","japan","kenya","kuwait","latvia","lithuania","luxembourg","malaysia","mexico","morocco","netherlands","newzealand","nigeria","norway","pakistan","peru","philippines","poland","portugal","qatar","romania","russia","ksa","serbia","singapore","slovakia","rsa","korea","spain","srilanka","sweden","switzerland","taiwan","thailand","tunisia","turkey","uae","uk","venezuela","vietnam"]'
        columns = '["name","description","logoid","type","close","currency","change","Value.Traded","market_cap_basic","fundamental_currency_code","sector","industry","market","is_primary","exchange","country"]'
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


    def add_isin(self,df):
        isin_df = pd.read_csv(self.isin_dir)[['fullname','isin','is_primary_listing','primary_symbol','ticker_title']]\
                                            .rename(columns={"fullname": "full_symbol"})
        df = df.merge(isin_df, how = 'left', on = 'full_symbol').rename(columns={"isin": "isin_tv"})
        df['ticker_title'] = df['ticker_title'].fillna('').apply(remove_suffix)
        return df
        
        
    def correct_industry(self, df):
        correct_df = pd.read_csv(self.correct_ind)

        tw_df = pd.read_csv(self.tw_dir).rename(columns={"有价证券代号": "code"})
        tw_df = tw_df[tw_df['产业别'].isin(['半导体业'])][['code']]
        data = {'correct_industry': 'Semiconductors', 'market': 'taiwan'}
        tw_df = tw_df.assign(**data)

        us_df = pd.read_excel(open(self.us_dir, 'rb'),sheet_name='us_stocks_industry').rename(columns={"证券代码": "code"})
        us_df = us_df[us_df['二级行业'].isin(['半导体'])][['code']]
        us_df['code'] = us_df['code'].str.replace('_','.')
        data = {'correct_industry': 'Semiconductors', 'market': 'america'}
        us_df = us_df.assign(**data)

        a_df = pd.read_excel(open(self.a_dir, 'rb'),sheet_name='a_stocks_info').rename(columns={"证券代码": "code",'二级行业':'correct_industry'})
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
        return df

    def translate_name(self, df):
        def format_korea_code(code):
            code = '{:0>6}'.format(code)
            return code
        def format_hk_code(code):
            code = '{:0>5}'.format(code)
            return code
        def format_jp_code(code):
            code = '{:0>4}'.format(code)
            return code

        
        df.loc[df['market'].isin(['hongkong']), 'name'] = df[df['market'].isin(['hongkong'])]['name'].apply(format_hk_code)

        tw_df = pd.read_csv(self.tw_dir).rename(columns={"有价证券代号": "证券代码","有价证券名称": "名称翻译"})
        tw_df = tw_df[["证券代码","名称翻译"]]
        tw_df['market'] = 'taiwan'

        sg_df = pd.read_csv(self.sg_dir).rename(columns={"交易代号": "证券代码","证券名称": "名称翻译"})
        sg_df = sg_df[["证券代码","名称翻译"]]
        sg_df['market'] = 'singapore'

        hk_df = pd.read_csv(self.hk_dir).rename(columns={"证券名称": "名称翻译"})
        hk_df = hk_df[["证券代码","名称翻译"]]
        hk_df["证券代码"] = hk_df["证券代码"].str[:5]
        hk_df['market'] = 'hongkong'

        uk_df = pd.read_csv(self.uk_dir).rename(columns={"证券名称": "名称翻译"})
        uk_df = uk_df[["证券代码","名称翻译"]]
        uk_df['market'] = 'uk'

        us_df = pd.read_excel(open(self.us_dir, 'rb'),sheet_name='us_stocks_industry').rename(columns={"证券名称": "名称翻译"})
        us_df = us_df[["证券代码","名称翻译"]]
        us_df['证券代码'] = us_df['证券代码'].str.replace('_','.')
        us_df['market'] = 'america' 
          
        a_df = pd.read_excel(open(self.a_dir, 'rb'),sheet_name='a_stocks_info')
        a_df = a_df[["证券代码","股票简称"]].rename(columns={"股票简称": "名称翻译"})
        a_df["证券代码"] = a_df["证券代码"].str[:6]
        a_df['market'] = 'china'  

        other_df = pd.read_csv(self.translate_name_dir)
        other_df.loc[other_df['market'].isin(['korea']), '证券代码'] = other_df[other_df['market'].isin(['korea'])]['证券代码'].apply(format_korea_code)   
        other_df.loc[other_df['market'].isin(['japan','ksa']), '证券代码'] = other_df[other_df['market'].isin(['japan','ksa'])]['证券代码'].apply(format_jp_code)   

        translate_df = pd.concat([tw_df, sg_df, hk_df, uk_df, us_df, a_df, other_df], ignore_index=True)

        df = df.rename(columns={"name": "证券代码"})
        df = df.merge(translate_df, how = 'left', on=['证券代码','market'])
        df['description'] = df['description'].str.replace(', S.A.','').str.replace(' S.A.','').str.replace(' LTD','').str.replace(' PLC','')\
                            .str.replace(' A/S','').str.replace(' OYJ','').str.replace(' AG NA','').str.replace(' SE NA','')\
                            .str.replace(' O.N.','').str.replace(' O N','').str.replace(' N.V.','')
        
        df['en_name'] = df['description'].apply(remove_suffix)
        df.loc[~df['名称翻译'].isnull(), 'description'] = df[~df['名称翻译'].isnull()]['名称翻译']
        
        dr_df = pd.read_csv(self.dr_name_dir)
        df = df.merge(dr_df, how = 'left', on=['logoid'])
        df.loc[~df['dr_name'].isnull() & df['名称翻译'].isnull(), 'description'] = df[~df['dr_name'].isnull() & df['名称翻译'].isnull()]['dr_name'] + '-X'
        df = df.rename(columns={"description": "证券名称",'change':'涨跌幅','close':'最新价'})
        df['证券名称'] = df['证券名称'].apply(remove_suffix)
        return df


    def translate_industry(self, df):
        # translated_industry = self.translation_dir
        trans_df = pd.read_excel(open(self.translate_dir, 'rb'),sheet_name='industry_trans').drop(columns = 'sector')
        market_df = pd.read_excel(open(self.translate_dir, 'rb'),sheet_name='market_trans')
        df = df.merge(trans_df, on = 'industry').merge(market_df, on = 'market')
        return df

    def clean(self, df):
        USD_forex_table = get_USD_forex_table()
        df = df.merge(USD_forex_table,left_on='currency', right_on = 'currency_id')
        
        df['总市值'] = (df['market_cap_basic']/100000000).fillna(0)
        df = df[df['总市值'] > 0]
        df['成交额'] = (df['Value.Traded']* df['forex_rate']/100000000).fillna(0)
        df = df[df['Value.Traded'] > 0]
        df['换手率'] = (df['成交额'] / df['总市值']).round(4)
        df['地区'] = df['market'].apply(check_plate)
        df = df[~df['change'].isnull()]
        df = df[~df['industry'].isnull()]
        df = df[~df['sector'].isnull()]
        df = df[~df['market_cap_basic'].isnull()]
        return df
    
    def update(self, df, mode = 'all'):
        df['异动值'] = df['成交额'] * df['涨跌幅'].abs() * np.log10( (math.e - 1) * df['涨跌幅'].abs() + 1) / (np.log(df['总市值'] + 1) + 1)

        if mode == 'all':
            df = df[~df['full_symbol'].isin(['OTC:CTTRF'])]
            df.to_csv( data_dir + '/spot/stock_spot_global_{mode}.csv'.format(mode=mode), index = False, encoding = 'utf-8')
            num = len(df)
            print(f'All markets with {num} symbols updated')
        elif mode == 'primary':
            primary_df = df[( ((df['is_primary'] == True) & (df['type'] == 'stock')) | \
                ((df['is_primary'] == True) & (df['type'] == 'dr') & (df['market'].isin(['netherlands','america']))) | \
                ((df['证券代码'].isin(['PHIA','DSM','ABN'])) & (df['market'].isin(['netherlands']))) | \
                ((df['证券代码'].isin(['STLAM'])) & (df['market'].isin(['italy'])))    ) & \
                (~df['exchange'].isin(['OTC']))  ]
            primary_df.to_csv( data_dir + '/spot/stock_spot_global_{mode}.csv'.format(mode=mode), index = False, encoding = 'utf-8')
            num = len(primary_df)
            print(f'Primary markets with {num} symbols updated')

    def run(self):

        attempts = 0
        while attempts < 3:
            try:
                print('Start fetching global stock prices')
                df = self.fetch_global_prices()
                df = self.clean(df)
                print('Start cleaning data')
                df = self.add_isin(df)
                df = self.correct_industry(df)
                print('translate names')
                df = self.translate_name(df)
                print('translate industries')
                df = self.translate_industry(df)
                self.update(df, mode = 'all')
                self.update(df, mode = 'primary')
                
                break
            except Exception as e:
                attempts += 1
                print('errors occur, retrying {attempts} times'.format(attempts=attempts))          


    