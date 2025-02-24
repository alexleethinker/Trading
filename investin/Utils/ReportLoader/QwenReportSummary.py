import requests
import pandas as pd
from tqdm import tqdm
from requests_html import HTMLSession
from datetime import datetime, timedelta
from langchain.llms import Ollama
import warnings
warnings.filterwarnings("ignore")
try:
    from investin.Utils.config import data_dir
except:
    data_dir = 'investin/data'
tqdm.pandas() 

mappings = {
    '能源': [['国金证券'], ['石油行业','煤炭行业','采掘行业','燃气']],
    '有色金属': [['国金证券','华福证券'], ['有色金属','小金属','能源金属','贵金属']],
    '钢铁': [['华福证券'], ['钢铁行业','煤炭行业']],
    '化工': [['国金证券','国海证券'], ['化学制品','化纤行业','化学原料', '化肥行业', '塑料制品','橡胶制品', '非金属材料']],  
    
    '电力': [['国金证券'],['公用事业','电力行业','环保行业']], 
    '电力设备': [['国金证券','华福证券'], ['光伏设备','电池','风电设备','电网设备', '电源设备']], 
    
    '房地产': [['国金证券'],['房地产开发','房地产服务']], 
    '建材': [['国投证券','国信证券'], ['水泥建材','装修建材','玻璃玻纤']], 
    '建筑': [['国投证券'], ['工程建设','装修装饰']],  
    
    '金融': [['国金证券','华福证券'], ['银行', '证券','多元金融','保险']],
    '汽车': [['国金证券','华福证券'], ['汽车服务','汽车整车', '汽车零部件','交运设备']],
    '机械': [['国金证券'], ['专用设备', '通用设备','仪器仪表','工程机械']],
    '家电': [['国金证券','华福证券'], ['家电行业']],
    '电子': [['国金证券','华福证券'],['半导体', '消费电子','电子元件', '光学光电子','电子化学品']],
    
    '科技': [['国金证券','华福证券'], ['计算机设备',  '游戏', '通信设备', '通信服务', '互联网服务','软件开发','文化传媒']],
    '医药': [['国金证券','华福证券'], ['生物制品','医疗器械', '化学制药','医药商业','医疗服务','中药']],
    '食品饮料': [['国金证券','华福证券'], ['酿酒行业','食品饮料']],
    '农牧饲渔': [['国金证券'], ['农牧饲渔']],
    '轻工制造': [['华安证券','上海证券'], ['纺织服装', '家用轻工','造纸印刷', '包装材料']],
    '商贸零售': [['上海证券'], [ '商业百货', '美容护理', '珠宝首饰']],
    '社会服务': [['万联证券'], ['旅游酒店','教育','专业服务']], 
    '交通运输': [['国金证券','华福证券'], ['航运港口','航空机场', '物流行业','铁路公路']],
    
    '军工': [['中航证券'],['航天航空', '船舶制造']],
    
}



today = datetime.today()
lastweek_start = today - timedelta(days=today.weekday()+1)


def fetch_reports(page, beginTime, endTime):
    url = 'https://reportapi.eastmoney.com/report/list'
    payload ={
        'industryCode': '*',
        'pageSize': '100',
        'industry': '*',
        'rating': '*',
        'ratingChange': '*',
        'beginTime': beginTime.strftime("%Y-%m-%d"),
        'endTime': endTime.strftime("%Y-%m-%d"),
        'pageNo': str(page),
        'qType': '1'
    }

    r = requests.get(url, params = payload)
    total_page = r.json()['TotalPage']
    return r, total_page


def prepare_query_df():
    total_df = pd.DataFrame()
    _, total_page = fetch_reports(1, lastweek_start, today)

    for page in tqdm(range(1,total_page+1)):
        r, _ = fetch_reports(page, lastweek_start, today)
        df = pd.DataFrame(r.json()['data'])[['title','orgSName','publishDate','infoCode','industryCode','industryName','emRatingValue','researcher']]
        df['publishDate'] = pd.to_datetime(df['publishDate']).dt.date.astype(str)
        total_df = pd.concat([total_df,df])

    total_df.loc[total_df['title'].str.contains('能源周'), 'industryName'] = '石油行业'
    df = pd.DataFrame(mappings).T
    def format_title(x):
        try:
            if len(x.split('：')) > 1:
                x = ':'.join(x.split('：')[1:])
            else:
                x = x.split('：')[-1]
        except:
            pass   
        return x
        
    df['title'] = '' 
    df['infoCode'] = ''

    def fetch_highlight(infocode_list):
        highlight_list = []
        for infocode in infocode_list:
            url = f'https://data.eastmoney.com/report/zw_industry.jshtml?infocode={infocode}'
            session = HTMLSession()  
            r = session.get(url)  
            highlight = r.html.find('div.ctx-content')[0].text.replace('\n','').split('风险提示')[0]
            highlight_list.append(highlight)
            # pdf_link = list(r.html.find('a.pdf-link')[0].links)[0]
        return highlight_list
    #使用tqdm进度条
    # 
    
    for i, row in df.iterrows():
        tmp = total_df[total_df['orgSName'].isin(row[0]) & total_df['industryName'].isin(row[1])]
        tmp['title'] = tmp['title'].apply(format_title)
        df.at[i, 'title'] = (tmp['publishDate'] + ' || ' + tmp['title']).to_list()
        df.at[i, 'infoCode'] = tmp['infoCode'].to_list()
    df['highlight'] = df['infoCode'].progress_map(fetch_highlight)
    df['title'] = df['title'].apply(lambda x: ','.join(x))
    df = df.dropna(subset=['title'])
    return df




def make_query(highlight_list):
    num = len(highlight_list)
    query = f'你是一名资深的投资顾问, 请分析以下{num}篇券商行业研报的摘要内容，然后总结行业的发展现状，并简述投资机会：'#, 并详细地列出推荐标的及理由：'
    for i in highlight_list:
        query = query + f'摘要{highlight_list.index(i)+1}：{i}'
    return query

# def ask_qwen(query):
#     api_key = 'sk-7397a9299d73435cb10290493bddee4e'
#     url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
#     headers = {'Content-Type': 'application/json',
#                'Authorization':f'Bearer {api_key}'}
#     body = {
#         'model': 'qwen-long',
#         "input": {
#             "messages": [
#                 {"role": "system","content": "You are an experienced investment manager."},
#                 {"role": "user","content": query}
#             ]
#         },
#         "parameters": {"result_format": "message"}
#     }
#     response = requests.post(url, headers=headers, json=body)
#     try:
#         answer = response.json()['output']['choices'][0]['message']['content']
#     except:
#         answer = response.json()
#     return answer


# from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
# from sparkai.core.messages import ChatMessage

# def ask_sparkai(query):
#     #星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
#     SPARKAI_URL = 'wss://spark-api.xf-yun.com/v1.1/chat'	
#     #星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
#     SPARKAI_APP_ID = 'ac7278af'
#     SPARKAI_API_SECRET = 'OWZiZDc4NzQyZDQ4YzY3MTcyYzIyMDhm'
#     SPARKAI_API_KEY = 'c53eca48af4d20082ab4346499f00ae3'
#     #星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
#     SPARKAI_DOMAIN = 'lite'
#     spark = ChatSparkLLM(
#         spark_api_url=SPARKAI_URL,
#         spark_app_id=SPARKAI_APP_ID,
#         spark_api_key=SPARKAI_API_KEY,
#         spark_api_secret=SPARKAI_API_SECRET,
#         spark_llm_domain=SPARKAI_DOMAIN,
#         streaming=False,
#     )
#     messages = [ChatMessage(
#         role="user",
#         content= query
#     )]
#     handler = ChunkPrintHandler()
#     a = spark.generate([messages], callbacks=[handler])
#     print(a)


def ask_deepseek(query):
    llm = Ollama(model="deepseek-r1:1.5b")
    answer = llm.invoke(query)
    return answer


def generate_weekly_qwen_report():
    df = prepare_query_df()
    qwen_df = df[['title','highlight']].rename(columns = {'title':'标题','highlight':'摘要'})
    qwen_df['千问读研报'] = qwen_df['摘要'].apply(make_query).progress_map(ask_deepseek)
    qwen_df[['标题','千问读研报']].to_csv(data_dir + '/spot/Qwen_weekly_reports.csv', index =  True)



if __name__ == '__main__':
    generate_weekly_qwen_report()
