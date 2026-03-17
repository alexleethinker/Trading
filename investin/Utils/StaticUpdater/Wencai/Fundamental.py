import pywencai
import pandas as pd
try:
    from investin.Utils.config import data_dir
except:
    data_dir = 'investin/data'
    


controller_dict ={
'中华人民共和国':'',
'集团有限公司':'',
'股份有限公司':'',
'有限责任公司':'',
'有限公司':'',
'股份':'',
'集团公司':'',
'(集团)':'',
'集团':'',
'国务院国有资产监督管理委员会':'国资委',
'国有资产监督管理委员会':'国资委',
'国务院国有资产管理委员会':'国资委',
'国有资产管理委员会':'国资委',
'国有资产监督管理局':'国资委',
'国有资产管理局':'国资委',
'国有资产监督管理和金融工作局':'国资委',
'国有资产管理办公室':'国资办',
'国有资产监督管理办公室':'国资办',
'国有资产监督管理局':'国资办',
'国有(集体)资产监督管理办公室':'国资办',
'国有(集体)资产管理办公室':'国资办',
'市人民政府':'市',
'市政府':'市',
'省人民政府':'省',
'省政府':'省',
'区人民政府':'区',
}

def get_GJD_position():
    query = '国家队持股'
    loop = True
    query_type = 'stock'
    df = pywencai.get(query=query,loop = loop, log = True, query_type = query_type)
    df.columns = [x.split('[')[0] for x in df.columns.tolist()]
    df = df[['股票代码','机构本期持股占流通股比例明细','持股机构名称明细']]#.rename(columns={"股票代码":"证券代码"})
    df.columns = ['股票代码','国家队持股比例','国家队机构名称']
    
    GJD_dict={
    '国家集成电路产业投资基金股份有限公司':'大基金一期',
    '国家集成电路产业投资基金二期股份有限公司':'大基金二期',
    '中国证券金融股份有限公司':'证金公司'
    }
    def clean_GJD(x):
        if '中央汇金' in x:
            x = '中央汇金'
        elif '基本养老保险' in x:
            x = '社保基金'
        else:
            for i in GJD_dict:
                x = x.replace(i,GJD_dict[i])
        return x   
    
    df['国家队机构名称'] = df['国家队机构名称'].apply(clean_GJD).fillna('')
    df = df.groupby(by='股票代码').agg({
                                        '国家队机构名称': ', '.join,
                                        '国家队持股比例': lambda x: sum(x)
                                        }).reset_index().reset_index()
    return df


def get_basic_info():
    query = '所属概念 公司亮点 所属同花顺行业 所属指数类 机构持股比例 企业性质'
    loop = True
    query_type = 'stock'
    df = pywencai.get(query=query,loop = loop, log = True, query_type = query_type)
    df.columns = [x.split('[')[0] for x in df.columns.tolist()]

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
    
    def clean_controller(x):
        try:
            for i in controller_dict:
                x = x.replace(i,controller_dict[i])
        except:
            pass
        return x    
    
    df['所属概念'] = df['所属概念'].apply(clean_concepts)
    df['沪深指数'] = df['所属指数类'].apply(clean_index)

    df = df[['股票代码','股票简称','所属同花顺行业','沪深指数','公司亮点','所属概念','机构持股占流通股比例','最终控制人持股比例','企业性质','最终控制人类型','最终控制人']].rename(columns={"股票代码":"证券代码"})
  
    def drop_duplicates(x):
        try:
            x = ','.join(set(x.split('||')))
        except:
            pass
        return x
        
    df['最终控制人类型'] = df['最终控制人类型'].apply(drop_duplicates)
    df['最终控制人'] = df['最终控制人'].apply(drop_duplicates).apply(clean_controller)
    df['控制人'] = ''
    df.loc[df['最终控制人类型'].isin(['个人','境外','个人,境外']), '控制人'] = df.loc[df['最终控制人类型'].isin(['个人','境外','个人,境外']), '最终控制人类型']
    df.loc[~df['最终控制人类型'].isin(['个人','境外','个人,境外']), '控制人'] = df.loc[~df['最终控制人类型'].isin(['个人','境外','个人,境外']), '最终控制人']

    a_stock_info = pd.read_excel(open(data_dir + '/static/EM/China/a_stocks.xlsx', 'rb'),sheet_name='a_stocks_info')
    a_stock_info = a_stock_info[['证券代码','三级行业','二级行业','一级行业','主营产品','投资逻辑']]

    GJD_df = get_GJD_position().rename(columns={"股票代码":"证券代码"})
    df = df.merge(a_stock_info, how = 'left', on=['证券代码']).merge(GJD_df, how = 'left', on=['证券代码'])

    df['机构持股占流通股比例'] = pd.to_numeric(df['机构持股占流通股比例'], errors="coerce").round(2)
    df['最终控制人持股比例'] = pd.to_numeric(df['最终控制人持股比例'], errors="coerce").round(2)
    df['国家队持股比例'] = pd.to_numeric(df['国家队持股比例'], errors="coerce").round(2).fillna('')
    df['国家队机构名称'] = df['国家队机构名称'].fillna('')
    df = df.drop(columns = 'index')
    df.to_csv(data_dir + '/static/EM/China/a_stock_details.csv', index = False)


if __name__ == '__main__':
    get_basic_info()


