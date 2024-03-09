import pywencai
import pandas as pd
try:
    from investin.Utils.config import data_dir
except:
    data_dir = 'investin/data'
    
    
# query = '所属概念 公司亮点 所属同花顺行业 所属指数类'
query = '行业 概念 市值'
loop = True
query_type = 'hkstock'

'''
stock	股票
zhishu	指数
fund	基金
hkstock	港股
usstock	美股
threeboard	新三板
conbond	可转债
insurance	保险
futures	期货
lccp	理财
foreign_exchange	外汇
'''

r = pywencai.get(query=query,loop = loop, log = True, query_type = query_type)
# r = pd.read_csv('a_stock_details.csv', encoding="utf-8")



index_selected_list = ['上证50','沪深300','中证500','中证1000','中证2000']
ignored_list = ['上证180','上证380','深证100','深证200','深证700']
concepts_list = pd.read_csv(data_dir + '/static/Wencai/concepts_checklist.csv',encoding="utf-8")
industry_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['行业','产品','业务','行业+']) & concepts_list['active']==1 ]['概念名称'].values.tolist()
events_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['事件','改革','政策']) & concepts_list['active']==1]['概念名称'].values.tolist()
master_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['知名企业','国企体系']) & concepts_list['active']==1]['概念名称'].values.tolist()
exclude_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['交易'])]['概念名称'].values.tolist()


def clean_index(cell):
    cell = str(cell)
    cell = ','.join(set(cell.split(';')).intersection(index_selected_list))
    return cell

def clean_concepts(cell):
    cell = str(cell)
    cell = ','.join(set(cell.split(';')).difference(exclude_concepts_list))
    cell = cell.replace('概念股','').replace('概念','').replace('[US]','').replace('[HK]','')
    return cell
    
# r['所属概念'] = r['所属概念'].apply(clean_concepts)
# r['沪深指数'] = r['所属指数类'].apply(clean_index)



# r = r[['股票代码','股票简称','所属同花顺行业','沪深指数','公司亮点','所属概念']]
r.to_csv('hk_stock_details.csv', index = False)