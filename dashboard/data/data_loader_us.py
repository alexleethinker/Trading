import requests
import pandas as pd

def stock_spot_us():
    url = 'http://40.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'pn': '1',
        'pz': '15000',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:105,m:106,m:107',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152',
        '_': '1631107510188',
    }

    r = requests.get(url, params=params, timeout=10)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.columns = [
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "_",
        "成交额",
        "_",
        "_",
        "_",
        "_",
        "_",
        "简称",
        "编码",
        "名称",
        "最高价",
        "最低价",
        "开盘价",
        "昨收价",
        "总市值",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "市盈率",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df.reset_index(inplace=True)
    temp_df["index"] = range(1, len(temp_df) + 1)
    temp_df.rename(columns={"index": "序号"}, inplace=True)
    temp_df["证券代码"] = temp_df["简称"]
    temp_df = temp_df[
        [
            "证券代码",
            "名称",
            "最新价",
            "涨跌额",
            "涨跌幅",
            "开盘价",
            "最高价",
            "最低价",
            "昨收价",
            '成交额',
            "总市值",
            "市盈率",
#             "代码",
        ]
    ]
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"], errors="coerce")
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"], errors="coerce")
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"], errors="coerce")
    temp_df["开盘价"] = pd.to_numeric(temp_df["开盘价"], errors="coerce")
    temp_df["最高价"] = pd.to_numeric(temp_df["最高价"], errors="coerce")
    temp_df["最低价"] = pd.to_numeric(temp_df["最低价"], errors="coerce")
    temp_df["昨收价"] = pd.to_numeric(temp_df["昨收价"], errors="coerce")
    temp_df["总市值"] = pd.to_numeric(temp_df["总市值"], errors="coerce")
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"], errors="coerce")
    temp_df["市盈率"] = pd.to_numeric(temp_df["市盈率"], errors="coerce")    

    stock_custom_industry = pd.read_excel(open(data_path +'/static/us_stocks.xlsx', 'rb'),sheet_name='us_stocks_industry')
    df = temp_df.merge(stock_custom_industry,how='left',on=['证券代码'])
    df = df[~df['涨跌幅'].isnull()]
    df = df[~df['三级行业'].isnull()]
    df = df[~df['总市值'].isnull()]
    df['总市值'] = (df['总市值']/100000000).round(2)
    df['成交额'] = (df['成交额']/100000000).round(2)
    return df


def update_spot_data_us():   
    import os
    home_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    global data_path
    data_path = home_path + '/data'
    
    try:
        spot = stock_spot_us()
        spot.to_csv( data_path + '/spot/stock_spot_us.csv', index = False, encoding = 'utf-8')
        print('Data updated')
    except:
        update_spot_data_us()


if __name__ == "__main__":

    print('Started data loader')
    
    update_spot_data_us()
