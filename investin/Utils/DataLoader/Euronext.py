import requests
import pandas as pd
import json
import lxml.html
from investin.Utils.config import data_dir


class StockSpotEuronext():
    def __init__(self) -> None:
        self.read_dir = data_dir + '/static/Europe/Euronext/euronext_degiro.csv'
        self.write_dir = data_dir + '/spot/stock_spot_euronext.csv'
        self.translate_dir = data_dir + '/static/TradingView/translations/translation.xlsx'

    def fetch_prices(self):
        num = '1900'
        payload = 'draw=3&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={num}&search%5Bvalue%5D=&search%5Bregex%5D=false&args%5BtradedToday%5D=true&args%5BinitialLetter%5D=&iDisplayLength={num}&iDisplayStart=0&sSortDir_0=asc&sSortField=name'.format(num=num)
        # get all data
        # payload = 'draw=3&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={num}&search%5Bvalue%5D=&search%5Bregex%5D=false&args%5BinitialLetter%5D=&iDisplayLength={num}&iDisplayStart=0&sSortDir_0=asc&sSortField=name'.format(num=num)
        exchanges = 'XAMS,XPAR,XBRU,MTAA,XELI'
        # exchanges = 'dm_all_stock'
        url = 'https://live.euronext.com/en/pd_es/data/stocks?mics={exchanges}'.format(exchanges=exchanges)  
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6,zh-TW;q=0.5,nl;q=0.4',
                'Content-Length': '2291',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'visid_incap_2784265=Fa+2QpF1RPOGRvczqZc9doviJWQAAAAAQUIPAAAAAABjdMOtC35OE9i9CqTY6Cs2; visid_incap_2784297=IPdkiUKKRA+fEgAlrkIyCVKnXGQAAAAAQUIPAAAAAAD/LtpK/6LgeAblpwLuLmiM; visid_incap_2691598=U/NqsPS3TyqhlTHgSGGNYlanXGQAAAAAQUIPAAAAAAAB5o04iL2AMEYmxUNQzY1t; visid_incap_2790185=BQi+PIrxRGGpulC7+EtSq+prhGQAAAAAQUIPAAAAAACbCqPEY30BuR/7dsPteOrP; cookie-agreed-version=1.0.1; cookie-agreed-categories=[%22necessary%22%2C%22performance%22]; cookie-agreed=2; _ga_PMEFBR6CSF=GS1.1.1691538410.1.1.1691540208.0.0.0; _hjFirstSeen=1; _gat_gtag_UA_46900155_5=1; incap_ses_766_2784297=ybsKVIQ5RAZ2fKfg7mGhCj3c0mQAAAAAco6m3Y4DoftpCspxky1MMA==; _ga_5H9XW5KEHP=GS1.1.1691540476.3.1.1691540540.0.0.0; _ga_WYRYLMR662=GS1.1.1691538404.6.1.1691540540.0.0.0',
                'Origin': 'https://live.euronext.com',
                'Referer': 'https://live.euronext.com/en/products/equities/list',
                'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"macOS"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'X-Requested-With': 'XMLHttpRequest'
                }
        r = requests.post(url,data=payload,headers = headers, timeout=30).text
        df = pd.DataFrame(json.loads(r)['aaData'])

        def extract_code(string):
            string = string.replace("<a href='/en/product/equities/",'').split('/')[0]
            return string

        df['code'] = df[1].apply(extract_code)

        def parse_html(string):
            try:
                html = lxml.html.fromstring(string)
                content = html.text_content()
            except:
                content = ''
            return content

        for i in df.columns:
            df[i] = df[i].apply(parse_html)

        columns = ['','name','ISIN','symbol','exchange_code','last_price','change','last_traded_at','close_price','trading_date','euronext_code']
        df.columns = columns    
        df[['trade_currency','last_price']] = df['last_price'].str.split(' ',expand=True)
        df = df[~df['change'].isnull()]
        df['change'] = df['change'].str.replace('%','')
        df['change'] = pd.to_numeric(df['change'], errors="coerce").fillna('0')
        df = df[['euronext_code','exchange_code','trade_currency','last_price','change','last_traded_at','close_price','trading_date']]
        return df

    def clean(self, euronext_df):
        global_df = pd.read_csv( data_dir + '/spot/stock_spot_global_all.csv',low_memory=False).drop(columns=['change','currency','证券名称'])
        # df = euronext_df.merge(global_df, how = 'left', left_on = ['symbol','market'], right_on = ['name','market'])
        degiro_df = pd.read_csv( self.read_dir) 
        degiro_df = degiro_df.merge(global_df, how = 'left', left_on = ['symbol','market'], right_on = ['name','market'])
        df = degiro_df.merge(euronext_df, how = 'left', on = ['euronext_code'])
        # replace names with translated names
        df.loc[~df['名称翻译'].isnull(), 'stock_name'] = df[~df['名称翻译'].isnull()]['名称翻译']
        df.loc[~df['dr_name'].isnull() & df['名称翻译'].isnull(), 'stock_name'] = df[~df['dr_name'].isnull() & df['名称翻译'].isnull()]['dr_name'] + ' SE'
        df['stock_name'] = df['stock_name'].str.replace('�','').str.replace(' SpA','').str.replace(' NV','')
        df = df.rename(columns={"stock_name": "证券名称"})
        return df
    
    def update(self, df):
        df.to_csv( self.write_dir , index = False, encoding = 'utf-8')

    def run(self):
        attempts = 0
        while attempts < 3:
            try:
                print('Start fetching Euronext data')
                euronext_df = self.fetch_prices()
                print('Start cleaning data')
                df = self.clean(euronext_df)
                self.update(df)
                print('Data updated')
                break
            except Exception as e:
                attempts += 1
                print('errors occur, retrying {attempts} times'.format(attempts=attempts))          

