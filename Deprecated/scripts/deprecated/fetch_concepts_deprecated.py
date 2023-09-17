import akshare as ak
import pandas as pd
import warnings
warnings.filterwarnings('ignore')



#待解决： 断点续传问题
# 获取同花顺概念信息

concepts_list = ak.stock_board_concept_name_ths()
concepts_list['概念名称'] = concepts_list['概念名称'].str.replace('概念股','').str.replace('概念','').str.replace(' ','')

# check concepts_list updates
# new_concepts = set(concepts_list['概念名称']).difference(concepts_checklist['概念名称'])
# out_concepts = set(concepts_checklist['概念名称']).difference(concepts_list['概念名称'])
# print( out_concepts )

global stock_concepts
stock_concepts = pd.DataFrame()


def get_concept_components(concept):
    global stock_concepts
    with pool_sema:
        print('正在获取同花顺概念成分股： ' + concept['概念名称'])
        stock_board_cons_df = ak.stock_board_cons_ths(symbol=concept['代码'])
        stock_board_cons_df['概念名称'] = concept['概念名称']
        stock_board_cons_df['概念代码'] = concept['代码']
        stock_concepts = stock_concepts.append(stock_board_cons_df)


import threading
threads = []

max_connections = 2  # 定义最大线程数
pool_sema = threading.BoundedSemaphore(max_connections) # 或使用Semaphore方法

for row, concept in concepts_list.iterrows():
    t = threading.Thread(target = get_concept_components, args = (concept,))
    threads.append(t)

#print(threads)

for t in threads: 
    t.start()

# 等待所有thread完成之后再执行之后的代码    
for t in threads: 
    t.join()




stock_concepts = stock_concepts.groupby(['代码','名称'])['概念名称'].apply(lambda x: ",".join \
                            (list(set(x.str.cat(sep=',').split(','))))).reset_index()

stock_concepts['行业概念'] = ''
stock_concepts['事件概念'] = ''
stock_concepts['交易概念'] = ''


# 将同花顺概念分为 “行业”，“事件”和“交易”三类
concepts_checklist = pd.read_csv('./static/concepts_checklist.csv',encoding="gbk") # list got from old iwencai api / more comple but outdate
industry_concepts_list = concepts_checklist.loc[concepts_checklist['分类'].isin(['行业'])]['概念名称'].values.tolist()
events_concepts_list = concepts_checklist.loc[concepts_checklist['分类'].isin(['事件','知名企业','农村','军工'])]['概念名称'].values.tolist()
trading_concepts_list = concepts_checklist.loc[concepts_checklist['分类'].isin(['交易'])]['概念名称','改革','国企体系'].values.tolist() # 区域missing


for row, l in stock_concepts.iterrows():
    stock_concepts['行业概念'][row] = ','.join(set(l['概念名称'].split(',')).intersection(industry_concepts_list))
    stock_concepts['事件概念'][row] = ','.join(set(l['概念名称'].split(',')).intersection(events_concepts_list))
    stock_concepts['交易概念'][row] = ','.join(set(l['概念名称'].split(',')).intersection(trading_concepts_list))



stock_concepts.to_csv( './static/stock_concepts.csv', encoding="gbk", index=0)