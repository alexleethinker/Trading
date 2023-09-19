import requests

url = 'http://www.iwencai.com/gateway/urp/v7/landing/getDataList'

query_string = '所属概念 公司亮点 所属同花顺行业 所属指数类'
page = 2

condition = []
condition_1 = {
        'score': 0.0,
        'chunkedResult': '_&_'.join(query_string.split(' ')),
        'opName': 'and',
        'opProperty': '',
        'sonSize': 4,
        'relatedSize': '0',
        "logid":"d624c935ac7e617d9d45ef70fd4d5ca8"
        }
condition.append(condition_1)

for i in query_string.split(' '):
#     i = i.replace('指数','指数类')
    dic = {
        'dateText': '',
        'indexName': i,
        'indexProperties': [],
        'child_node': i,
        'ci': True,
        'type': 'index',
        'indexPropertiesMap': {},
        'reportType': 'null',
        'ciChunk': i,
        'createBy': 'preCache',
        'uiText': i,
        'valueType': '_' + i,
        'domain': 'abs_股票领域',
        'sonSize': 0,
        'dateList': [],
        "order":0
        }
    condition.append(dic)
condition = str(condition).replace("'", '"').replace(' ','')

[{"chunkedResult":"所属概念 _&_公司亮点 _&_所属同花顺行业 _&_所属指数类",
  "opName":"and",
  "opProperty":"",
  "sonSize":2,
  "relatedSize":0},
 {"reportType":"null",
  "indexName":"美股@所属概念",
  "indexProperties":[],
  "valueType":"_美股所属概念",
  "domain":"abs_美股领域",
  "uiText":"所属概念","sonSize":0,"queryText":"所属概念","relatedSize":0,"source":"new_parser","type":"index","indexPropertiesMap":{}},
 {"reportType":"null","indexName":"美股@所属指数类","indexProperties":[],"valueType":"_美股所属指数","domain":"abs_美股领域","uiText":"所属指数类","sonSize":0,"queryText":"所属指数类","relatedSize":0,"source":"new_parser","type":"index","indexPropertiesMap":{}}]

payload = {
    "question": query_string,
    "page": page,
    "perpage": 100,
    "source": "Ths_iwencai_Xuangu",
    'urp_sort_way': 'desc',
    'urp_sort_index': '最新涨跌幅',
    'addheaderindexes': '',
    'codelist': '',
    'indexnamelimit': '',
    'ret': 'json_all',
    'urp_use_sort': '1',
    'user_id': 'Ths_iwencai_Xuangu_4glx5h91g41h0ubj83v3rzq67526qfyg',
    'uuids[0]': '24087',
    'query_type': 'stock', #hkstock,usstock
    'comp_id': '6836372',
    'business_cat': 'soniu',
    'uuid': '24087',
#    以下为每次变化
#     'date_range[0]': '20230610',
#     'iwc_token': '0ac9529816863435305771116',
#     'sessionid': '9f98f2743c41f01ae1e20f42ce38d2a1',
#     'logid': '9f98f2743c41f01ae1e20f42ce38d2a1',
    'condition': str(condition).replace("'", '"').replace(' ','')
}

# logid: bed82184e5b2b3ed0989f4be3e23617f
# sessionid: bed82184e5b2b3ed0989f4be3e23617f
# date_range[0]: 20230920
# iwc_token: 0ac952b216951587657128344

    
cookies = {
    "WafStatus":'0',
    "ta_random_userid":'anro5tt7uu',
    "cid":'e77a8079986b06e6a9a46e614cf7eee21659209895',
    "ComputerID":'e77a8079986b06e6a9a46e614cf7eee21659209895',
    "other_uid":'Ths_iwencai_Xuangu_x25492z942nd2ag2aqbfqwh7m852m7vi',
    "ttype":'WEB',
    "wencai_pc_version":'1',
    "user_status":'0',
    "user":'MDpteF81NzA2NjI2NTU6Ok5vbmU6NTAwOjU4MDY2MjY1NTo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA6MTY6Ojo1NzA2NjI2NTU6MTY4NjMyMTg1NTo6OjE2MTQ4OTgzMjA6NjA0ODAwOjA6MTk0Yzg1NGMxMzdlYzY1ZmY1NTcxNjIzMWU2YzA2MGZkOmRlZmF1bHRfNDow',
    "userid":'570662655',
    "u_name":'mx_570662655',
    "escapename":'mx_570662655',
    "ticket":'106f915b0a9985030a58c2151f69d9b8',
    "utk":'86be216097cbd990b074d0a691f39d39',
#     'THSSESSID':'210fbd845858470fd3dcc8c227',
#     "PHPSESSID":'i1jarg6eiikd16j6ajcjuqhb7j1a88je',
#     "v":'A1hilGtTiE5eR6Q8zbqmwNg1KY3vQa3eHoyRWZLcpY9GCvSzOlGMW261YLTh',
}


headers = {
    'Accept':'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6,zh-TW;q=0.5,nl;q=0.4',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Content-Length':'2221',
    'Content-Type':'application/x-www-form-urlencoded',
#     'Hexin-V':'A1hilGtTiE5eR6Q8zbqmwNg1KY3vQa3eHoyRWZLcpY9GCvSzOlGMW261YLTh',
    'Host':'www.iwencai.com',
    'Origin':'http://www.iwencai.com',
    'Pragma':'no-cache',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}



r = requests.post(url, data = payload, cookies = cookies, headers = headers)

import json
import pandas as pd
df = pd.DataFrame(r.json()['answer']['components'][0]['data']['datas'])
df