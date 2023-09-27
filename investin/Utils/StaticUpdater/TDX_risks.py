import pandas as pd
import requests
import json
from tqdm import tqdm
import os
import warnings
warnings.filterwarnings('ignore')
try:
    from investin.Utils.config import data_dir
except:
    data_dir = 'investin/data'
 
save_path = data_dir + '/static/TDX/TDX_risks.csv'
initiated = os.path.exists(save_path)   
    
headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6,zh-TW;q=0.5,nl;q=0.4',
'cache-control': 'no-cache',
'cookie': '_ga=GA1.1.542530460.1664195503; taotieDeviceId=18379c82-1f06-dbb5-4d30-f609f1c37f2b; Hm_lvt_5a36d47aea259294d4ceb6ccbb2fa0d9=1664195504,1664315393,1665521616,1666255342; Hm_lpvt_5a36d47aea259294d4ceb6ccbb2fa0d9=1666255989; _ga_297ZV00D16=GS1.1.1666255340.10.1.1666256055.0.0.0',
'pragma': 'no-cache',
'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'cross-site',
'upgrade-insecure-requests': '1' ,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def get_fetched_list():
    fetched_list = list(pd.read_csv(save_path)['证券代码']) if initiated else []
    return fetched_list  

# get stock list
def get_stock_list():
    data_path = '{data_dir}/spot/stock_spot_china_a.csv'.format(data_dir=data_dir)
    df = pd.read_csv(data_path,encoding = 'utf-8')
    df = df[~df['最新价'].isnull()]
    stock_list = df['证券代码'].tolist()
    fetched_list = get_fetched_list()
    stock_list = [i for i in stock_list if i not in fetched_list]
    return stock_list



def get_stock_risk(code):
    url = 'http://page3.tdx.com.cn:7615/site/pcwebcall_static/bxb/json/' + str(code[:6]) + '.json'
    r= requests.get(url , headers = headers)
    if r.ok:
        json_o = json.loads(r.text)
        stock_name = json_o['name']
        num_risks = json_o['num']
        
        all_risks = pd.DataFrame(json_o['data']).explode('rows')['rows'].apply(pd.Series).fillna('')
        l1 = all_risks[all_risks['commonlxid'].astype(str) == '[]']
        l2 = all_risks[all_risks['commonlxid'].astype(str) != '[]'].explode('commonlxid')['commonlxid'].apply(pd.Series).fillna('')
        if 'fs' in l1.columns: 
            col_list = ['id','lx','fs','trig','trigyy']
            score =  int( 100 - pd.to_numeric(all_risks.fs).sum())    
        else: 
            col_list = ['id','lx','trig']
            score =  100
        if 'trigyy' in l2.columns: 
            col_list2 = ['id','lx','fs','trig','trigyy']  
        else: 
            col_list2 = ['id','lx','fs','trig']
        l1 = l1[col_list]    
        l2 = l2[col_list2]
        risk_table = pd.concat([l1,l2]).sort_values('id').sort_index()
        risk_table = risk_table.join(pd.DataFrame(json_o['data'])['name'])
        risk_table['cat_id'] = risk_table.index


        rs = risk_table [risk_table['trig'] == 1]
        rs['name'] = stock_name
        if 'trigyy' in rs.columns:
            rs = rs.groupby(['name']).agg({'lx': ';'.join , 'trigyy' :  ';'.join}).reset_index(level=0)
        else:
            rs = rs.groupby(['name']).agg({'lx': ';'.join}).reset_index(level=0)
        rs['score'] = score
        rs['num_risks'] = num_risks
        rs['code'] = code
        if len(rs) == 0:
            rs = pd.DataFrame([{'code': code,'name': stock_name, 'score': score,'lx': None, 'trigyy': None, 'num_risks': None }])
        else:
            pass
        rs = rs.rename({'code': '证券代码', 'name': '证券名称', 'lx': '风险项', 'score':'风险评分','trigyy':'风险详情', 'num_risks':'风险项数量'}, axis=1) 
        rs = rs[['证券代码', '证券名称', '风险评分', '风险项', '风险项数量','风险详情']]
        rs['证券名称'] = rs['证券名称'].str.replace(' ','').str.replace('Ａ','A')
        return rs
    else:
        # print(code + ' unsuccessful')
        pass

def update_result(df):
    header = False
    df.to_csv(save_path, mode='a',index = False, header=header, encoding = 'utf-8') 


# http://page3.tdx.com.cn:7615/site/pcwebcall_static/bxb/bxb.html?code=600089&color=0

def run():
    print("获取股票Risk...") 
    stock_list = get_stock_list()
    for code in tqdm(stock_list):
        df = get_stock_risk(code)
        update_result(df)
    
def main():
    attempts = 0
    while attempts < 2:
        try:
            run()
            break
        except Exception as e:
            print(e)
            attempts += 1
            print('errors occur, retrying {attempts} times'.format(attempts=attempts))


if __name__ == '__main__':
    
    main()






# 风险类别表格
# rt = risk_table[['cat_id','name','id','lx','fs']].reset_index()
# all_risk_table['fs'] = pd.to_numeric(all_risk_table['fs']).dropna().astype(str)
# #aa = all_risk_table[['cat_id','name', 'id', 'lx', 'fs' ]].groupby(['cat_id','name', 'id', 'lx']).agg({'fs':  lambda x: ','.join(pd.Series.unique(x)) }).reset_index()
# aa = all_risk_table[['cat_id','name', 'id', 'lx', 'fs' ]].groupby(['cat_id','name', 'id', 'lx']).max(['fs']).reset_index()
# mm = aa.merge(rt, on = ['cat_id', 'name', 'id', 'lx'])
# mm['fs_x'] = mm['fs_x'].str.replace(',0','')
# mm[['cat_id','name','id','lx','fs_x']].to_csv('risk_cat.csv', index =False, encoding = 'utf-8')
