import akshare as ak
import pandas as pd


def market_suffix(code):
    if code[:1] == '6':
        code = code + '.SH'
    elif code[:1] in ['0','3']:
        code = code + '.SZ'
    elif code[:1] in ['8','4']:
        code = code + '.BJ'
    else:
        pass
    return code


spot = ak.stock_zh_a_spot_em()
# spot = spot[~spot['最新价'].isnull()]

spot['股票代码'] = spot['代码'].apply(market_suffix)
spot['股票简称'] = spot['名称'].str.replace(' ','').str.replace('Ａ','A')
spot['流通市值'] = (pd.to_numeric(spot['流通市值'])/100000000).round(1).fillna('') 
spot['总市值'] = (pd.to_numeric(spot['总市值'])/100000000).round(1).fillna('') 
spot = spot[['股票代码','股票简称','流通市值','总市值','最新价', '涨跌幅']]
spot.to_csv('spot_prices.csv', index = False, encoding = 'utf-8')
