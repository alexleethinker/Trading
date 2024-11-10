import pywencai
import pandas as pd
try:
    from investin.Utils.config import data_dir
except:
    data_dir = 'investin/data'
    

'''
query_type:
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
        
    df['所属概念'] = df['所属概念'].apply(clean_concepts)
    df['沪深指数'] = df['所属指数类'].apply(clean_index)

    df = df[['股票代码','股票简称','所属同花顺行业','沪深指数','公司亮点','所属概念','机构持股占流通股比例','最终控制人持股比例','企业性质','最终控制人类型','最终控制人']].rename(columns={"股票代码":"证券代码"})
  
    def drop_duplicates(x):
        try:
            l = ','.join(','.join(set(x.split('||'))))
            return l
        except:
            return x
        

    df['最终控制人类型'] = df['最终控制人类型'].apply(drop_duplicates)
    df['最终控制人'] = df['最终控制人'].apply(drop_duplicates)
    df['机构持股占流通股比例'] = pd.to_numeric(df['机构持股占流通股比例'], errors="coerce").round(2)
    df['最终控制人持股比例'] = pd.to_numeric(df['最终控制人持股比例'], errors="coerce").round(2)

    a_stock_info = pd.read_excel(open(data_dir + '/static/EM/China/a_stocks.xlsx', 'rb'),sheet_name='a_stocks_info')
    a_stock_info = a_stock_info[['证券代码','三级行业','二级行业','一级行业','主营产品','投资逻辑']]

    df = df.merge(a_stock_info, how = 'left', on=['证券代码'])
    df.to_csv('a_stock_details.csv', index = False)
'''
replace

类型：
中央国有企业  央企


控制人
中华人民共和国 -
集团有限公司 -
股份有限公司
有限责任公司
有限公司
股份
集团公司
(集团)
集团


国务院国有资产监督管理委员会 国资委
国有资产监督管理委员会 国资委
国务院国有资产管理委员会 国资委
国有资产管理委员会 国资委
国有资产监督管理局 国资委
国有资产管理局 国资委
国有资产监督管理和金融工作局 国资委

国有资产管理办公室 国资办
国有资产监督管理办公室 国资办
国有资产监督管理局 国资办
国有(集体)资产监督管理办公室 国资办
国有(集体)资产管理办公室 国资办

省人民政府 省
省政府 省
区人民政府 区




资产管理有限责任公司
投资有限责任公司

国家集成电路产业投资基金股份有限公司 大基金一期
国家集成电路产业投资基金二期股份有限公司 大基金二期
''' 

# get_basic_info()


# query = '国家队持股'
# loop = True
# query_type = 'stock'
# df = pywencai.get(query=query,loop = loop, log = True, query_type = query_type)
# df.columns = [x.split('[')[0] for x in df.columns.tolist()]
# df = df[['股票代码','股票简称','机构本期持股占流通股比例明细','持股机构名称明细']]#.rename(columns={"股票代码":"证券代码"})
# df.columns = ['股票代码','股票简称','国家队持股比例','国家队机构名称']

# # print(df)

# df.to_csv('GJD_details.csv', index = False)


def calculate_growth():
    query = 'PE 扣非PE PB 扣非ROE 扣非净利润同比增长率 每股分红 分红比例 销售净利率  销售毛利率 商誉占净资产比例 ROA  ROE EPS 股息率  总营收增长率 资产负债率'
    loop = True
    query_type = 'stock'
    r = pywencai.get(query=query,loop = loop, log = True, query_type = query_type)
    r.columns = [x.split('[')[0] for x in r.columns.tolist()]
    result = r[['股票代码','股票简称','市盈率(pe)','市盈率(pe,扣非ttm)','市净率(pb)','净资产收益率roe-扣除非经常损益','净资产收益率roe(加权,公布值)','总资产报酬率roa','股息率(股票获利率)','分红比例','销售毛利率','销售净利率','归属母公司股东的净利润-扣除非经常损益(同比增长率)','营业总收入(同比增长率)','商誉占净资产比例','资产负债率']]
    result.columns = ['股票代码','股票简称','PE','扣非PE','PB','扣非ROE','ROE','ROA','股息率','分红比例','毛利率','净利率','扣非净利润增速','营收增速','商誉占比','资产负债率']
    result = result.apply(pd.to_numeric, errors='ignore').rename(columns={"股票代码":"证券代码"})

    result['扣非PEG']  = (result['扣非PE'] / result['营收增速'])

    def dividend_correct(x):
        if x >= 0.5:
            n = 1
        elif x < 0.25:
            n = 2
        else:
            n = 0.5/x
        return n

    result['分红比例'] = result['分红比例'].fillna(0)
    result['扣非市赚率'] = result['扣非PE'] / result['扣非ROE'] * result['分红比例'].apply(dividend_correct)
    result['市赚率'] =result['PE'] / result['ROE'] * result['分红比例'].apply(dividend_correct)


    df = result.fillna('').apply(pd.to_numeric, errors='ignore').round(2).copy()

    # 市赚率
    # PE<0 ROE > 0, 亏损
    # 扣非PE<0 扣非ROE>0, 扣非亏损
    # ROE<0 资不抵债

    df.loc[(df['PE']< 0) & (df['ROE']<0),'市赚率'] = '亏损'
    df.loc[(df['PE']> 0) & (df['ROE']<0),'市赚率'] = '转盈'
    df.loc[(df['PE']< 0) & (df['ROE']>0),'市赚率'] = '转亏'

    df.loc[(df['扣非PE']< 0) & (df['扣非ROE']<0),'扣非市赚率'] = '扣非亏损'
    df.loc[(df['扣非PE']> 0) & (df['扣非ROE']<0),'扣非市赚率'] = '转盈'
    df.loc[(df['扣非PE']< 0) & (df['扣非ROE']>0),'扣非市赚率'] = '扣非转亏'
    df.loc[(df['扣非PE']> 0) & (df['扣非ROE']<0) & (df['PE']< 0),'扣非市赚率'] = '扣非亏损'

    df.loc[df['扣非PE']< 0,'扣非PEG'] = '扣非亏损'
    # 分红比例 < 0
    # PE 或 盈利增速 < 0
    df.to_csv(data_dir + '/static/Wencai/a_stock_PE_values.csv', index =False)

calculate_growth()