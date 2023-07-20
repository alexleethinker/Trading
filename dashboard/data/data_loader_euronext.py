import requests
import pandas as pd
import json
import lxml.html


def update_euronext_price():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6,zh-TW;q=0.5,nl;q=0.4',
        'Content-Length': '2291',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'visid_incap_2784265=Fa+2QpF1RPOGRvczqZc9doviJWQAAAAAQUIPAAAAAABjdMOtC35OE9i9CqTY6Cs2; visid_incap_2784297=IPdkiUKKRA+fEgAlrkIyCVKnXGQAAAAAQUIPAAAAAAD/LtpK/6LgeAblpwLuLmiM; visid_incap_2691598=U/NqsPS3TyqhlTHgSGGNYlanXGQAAAAAQUIPAAAAAAAB5o04iL2AMEYmxUNQzY1t; visid_incap_2790185=BQi+PIrxRGGpulC7+EtSq+prhGQAAAAAQUIPAAAAAACbCqPEY30BuR/7dsPteOrP; cookie-agreed-version=1.0.1; cookie-agreed-categories=[%22necessary%22%2C%22performance%22]; cookie-agreed=2; _ga_PMEFBR6CSF=GS1.1.1689803565.1.0.1689803571.0.0.0; _gat_UA-46900155-5=1; _gid=GA1.2.49211915.1689843268; incap_ses_766_2784297=vT2CboPeeX4rXYEr6mGhCkb2uGQAAAAA+NpC7RU0E/aohDIZ19IgGg==; _gcl_au=1.1.1158013361.1689843272; _ga_5H9XW5KEHP=GS1.1.1689843263.2.1.1689843272.0.0.0; _ga_WYRYLMR662=GS1.1.1689843263.2.1.1689843273.0.0.0; _ga=GA1.2.838838868.1689546998; _hjSessionUser_1305322=eyJpZCI6ImVhODMxMWYzLWI5ZTgtNTE4Yi04NGU3LTg0YTMzNjdjMmI0MiIsImNyZWF0ZWQiOjE2ODk4NDMyNzMxNjcsImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjIncludedInSessionSample_1305322=0; _hjSession_1305322=eyJpZCI6IjIyODFkM2QxLTI2NmUtNGYyOS04OTU1LThmYWEwNGRhN2Y2ZiIsImNyZWF0ZWQiOjE2ODk4NDMyNzMxODYsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0',
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

    num = '1900'
    payload = 'draw=3&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={num}&search%5Bvalue%5D=&search%5Bregex%5D=false&args%5BtradedToday%5D=true&args%5BinitialLetter%5D=&iDisplayLength={num}&iDisplayStart=0&sSortDir_0=asc&sSortField=name'.format(num=num)
    # get all data
    # payload = 'draw=3&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={num}&search%5Bvalue%5D=&search%5Bregex%5D=false&args%5BinitialLetter%5D=&iDisplayLength={num}&iDisplayStart=0&sSortDir_0=asc&sSortField=name'.format(num=num)
    exchanges = 'XAMS,XPAR,XBRU,MTAA,XELI'
    # exchanges = 'dm_all_stock'
    url = 'https://live.euronext.com/en/pd_es/data/stocks?mics={exchanges}'.format(exchanges=exchanges)  
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

def update_spot_euronext():   
    import os
    home_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    global data_path
    data_path = home_path + '/data'

    try:
        euronext_df = update_euronext_price()
        global_df = pd.read_csv( data_path + '/spot/stock_spot_global_all.csv').drop(columns=['change','currency'])
        degiro_df = pd.read_csv( data_path + '/static/euronext_degiro.csv') 
        degiro_df = degiro_df.merge(global_df, how = 'left', left_on = ['symbol','market'], right_on = ['name','market'])
        df = degiro_df.merge(euronext_df, how = 'left', on = ['euronext_code'])
        df.to_csv( data_path + '/spot/stock_spot_euronext.csv', index = False, encoding = 'utf-8')
        
        print('Data updated')
    except Exception as e:
        print(e)
        update_spot_euronext()


if __name__ == "__main__":

    print('Started data loader')
    update_spot_euronext()
