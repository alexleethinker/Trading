import wencai as wc
from wencai.core.session import Session
Session.headers.update({'Host':'www.iwencai.com'})
wc.set_variable(cn_col=True)
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
pd.set_option('display.max_colwidth', None)
import os
home_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

index_selected_list = ['上证50','上证150','上证180','上证380','沪深300','科创50','创业板50',\
                       '中证500','中证1000','创业300','深证100','深证200','深证700']
concepts_list = pd.read_csv(home_path + '/static/concepts_checklist.csv',encoding="utf-8")
industry_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['行业','产品','业务','行业+']) & concepts_list['active']==1 ]['概念名称'].values.tolist()
events_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['事件','改革','政策']) & concepts_list['active']==1]['概念名称'].values.tolist()
master_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['知名企业','国企体系']) & concepts_list['active']==1]['概念名称'].values.tolist()
exclude_concepts_list = concepts_list.loc[concepts_list['分类'].isin(['交易'])]['概念名称'].values.tolist()

wc_result = pd.DataFrame()

for i in range(1,52):
    print('page: '+ str(i))
    sr = wc.search('概念 主营 所属指数类 公司亮点',page =i).fillna('')
    sr['沪深指数'] = ''
    sr['行业概念'] = ''
    sr['事件概念'] = ''
    sr['体系概念'] = ''

    for row, l in sr.iterrows():
        # sr['主营产品名称'][row] = ','.join(l['主营产品名称'].split('||'))
        sr['沪深指数'][row] = ','.join(set(l['所属指数类'].split(';')).intersection(index_selected_list))
        sr['所属概念'][row] = ','.join(set(l['所属概念'].split(';')).difference(exclude_concepts_list))
        # sr['行业概念'][row] = ','.join(set(l['所属概念'].replace('概念股','').replace('概念','').split(';')).intersection(industry_concepts_list)).replace('金属','')
        # sr['事件概念'][row] = ','.join(set(l['所属概念'].replace('概念股','').replace('概念','').split(';')).intersection(events_concepts_list))
        # sr['体系概念'][row] = ','.join(set(l['所属概念'].replace('概念股','').replace('概念','').split(';')).intersection(master_concepts_list))

    sr['所属概念'] =   sr['所属概念'].str.replace('概念股','').str.replace('概念','')
    sr['流动市值'] = (pd.to_numeric(sr['a股市值(不含限售股)'])/100000000).round(1).fillna('')    
    
    wc_result = wc_result.append(sr)

wc_result[['股票代码','股票简称','流动市值','最新价','最新涨跌幅','所属同花顺行业','沪深指数','公司亮点','所属概念']]\
            .to_csv('wc_info.csv',index = False, encoding = 'utf-8')