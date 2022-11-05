# 从同花顺，东方财富，tushare拉取数据并保存

import akshare as ak
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from datetime import date
today = date.today()

#同花顺概念列表需要到网站上爬取  http://q.10jqka.com.cn/gn/， 后续考虑写一个爬虫

#后续考虑自动化更新概念列表及概念名称统一
# ----------------------------同花顺----------------------
# 硅能源	碳化硅
# 共享单车	共享经济
# 债转股(AMC)	债转股
# 东数西算（算力）	东数西算

#东方财富网概念列表可以通过代码获得
# stock_board_concept_name_em_df = ak.stock_board_concept_name_em()[['板块名称','板块代码']]


def Fetch_Industry_ths():
    #获取股票同花顺行业信息
    industries_ths = pd.read_csv('./行业概念/ths_行业.csv',encoding="gbk")
    global all_stocks_industry_ths
    all_stocks_industry_ths = pd.DataFrame()
    for row, industry in industries_ths.iterrows():
        print('正在获取同花顺行业成分股： ' + industry['行业名称_ths'], str(row+1) + '/'+str(len(industries_ths)) )
        stock_board_cons_ths_df = ak.stock_board_cons_ths(symbol=industry['行业代码_ths'])
        stock_board_cons_ths_df['行业名称_ths'] = industry['行业名称_ths']
        stock_board_cons_ths_df['行业代码_ths'] = industry['行业代码_ths']
        all_stocks_industry_ths = all_stocks_industry_ths.append(stock_board_cons_ths_df)
    all_stocks_industry_ths.to_csv( save_route + 'all_stocks_industry_ths.csv', encoding="gbk", index=0)
    
    

def Fetch_Concept_ths():
    #待解决： 断点续传问题
    # 获取同花顺概念信息

    global concepts_ths
    global all_stocks_concepts_ths
    concepts_ths = pd.read_csv('./行业概念/ths_概念.csv',encoding="gbk")
    all_stocks_concepts_ths = pd.DataFrame()
    for row, concept in concepts_ths.iterrows():
        print('正在获取同花顺概念成分股： ' + concept['概念_ths'], str(row+1) + '/'+str(len(concepts_ths)))
        stock_board_cons_ths_df = ak.stock_board_cons_ths(symbol=concept['概念代码_ths'])
        stock_board_cons_ths_df['概念名称_ths'] = concept['概念_ths']
        stock_board_cons_ths_df['概念代码_ths'] = concept['概念代码_ths']
        all_stocks_concepts_ths = all_stocks_concepts_ths.append(stock_board_cons_ths_df)
    all_stocks_concepts_ths.to_csv( save_route + 'all_stocks_concepts_ths_ungrouped.csv', encoding="gbk", index=0)
    


def Fetch_Concept_em():
    # !!!后续：更新续传问题

    # 获取东方财富网概念信息
    global concepts_em
    global all_stocks_concepts_em

    concepts_em = pd.read_csv('./行业概念/em_概念.csv',encoding="gbk") # 经过优化后的概念列表

    concepts_original_em = ak.stock_board_concept_name_em()[['板块名称','板块代码']] # 东方财富原本的概念列表

    all_stocks_concepts_em = pd.DataFrame()
    for row, concept in concepts_em.iterrows():
        print('正在获取东方财富概念成分股： ' + concept['概念_em'], str(row+1) + '/'+str(len(concepts_em)) )
        stock_board_cons_em_df = ak.stock_board_concept_cons_em(symbol= \
                                concepts_original_em.loc[concepts_original_em['板块代码'] == concept['概念代码_em']]['板块名称'].values[0])
        stock_board_cons_em_df['概念名称_em'] = concept['概念_em']
        stock_board_cons_em_df['概念代码_em'] = concept['概念代码_em']
        all_stocks_concepts_em = all_stocks_concepts_em.append(stock_board_cons_em_df)
    all_stocks_concepts_em.to_csv( save_route + 'all_stocks_concepts_em_ungrouped.csv', encoding="gbk", index=0)   




# 通过tushare获取股票的省份和主营业务信息
def Fetch_Stock_info_Tushare():
    print('正在获取Tushare股票信息')

    global ts_stocks_info
    import tushare as ts
    pro = ts.pro_api('158ce95d6e799f55b8e8277aa1f6138fa71acf9c52df5ec667296fbc')
    ts_stocks_info = pro.stock_company( fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,city,employees,main_business,business_scope,introduction')

    ts_stocks_info['ts_code'] = ts_stocks_info['ts_code'].str.replace('.SZ','').str.replace('.SH','').str.replace('.BJ','')
    ts_stocks_info.columns = ['代码', '董事长', '总经理', '董事秘书', '注册资本', \
        '上市日期', '省份', '城市', '公司介绍', '营业范围', \
        '员工人数', '主营业务']
    
    ts_stocks_info.to_csv( save_route + 'ts_stocks_info.csv', encoding="gbk", index=0)

def Fetch_Financial_Data():
    print('正在获取资产负债表')
    # 所有股票的资产负债表
    global stock_zcfz_em
    try:
        stock_zcfz_em = ak.stock_zcfz_em(date=str(today.year)+"1231")
    except:
        try:
            stock_zcfz_em = ak.stock_zcfz_em(date=str(today.year)+"0930")
        except:
            try:
                stock_zcfz_em = ak.stock_zcfz_em(date=str(today.year)+"0630")
            except:
                stock_zcfz_em = ak.stock_zcfz_em(date=str(today.year)+"0331")

    # 所有股票的利润表
    global stock_lrb_em
    print('正在获取利润表')
    try:
        stock_lrb_em = ak.stock_lrb_em(date=str(today.year)+"1231")
    except:
        try:
            stock_lrb_em = ak.stock_lrb_em(date=str(today.year)+"0930")
        except:
            try:
                stock_lrb_em = ak.stock_lrb_em(date=str(today.year)+"0630")
            except:
                stock_lrb_em = ak.stock_lrb_em(date=str(today.year)+"0331")
    stock_zcfz_em.to_csv( save_route + 'balance_sheet.csv', encoding="gbk", index=0)
    stock_lrb_em.to_csv( save_route + 'revenue.csv', encoding="gbk", index=0)



if __name__=="__main__":


    save_route = './ungrouped_data/'

    import threading
    threads = []
    
    t = threading.Thread(target = Fetch_Industry_ths)
    threads.append(t)
    t = threading.Thread(target = Fetch_Concept_ths)
    threads.append(t)
    # t = threading.Thread(target = Fetch_Concept_em)
    # threads.append(t)
    t = threading.Thread(target = Fetch_Stock_info_Tushare)
    threads.append(t)
    # t = threading.Thread(target = Fetch_Financial_Data)
    # threads.append(t)
    print(threads)

    for t in threads: 
        t.start()

    # 等待所有thread完成之后再执行之后的代码    
    for t in threads: 
        t.join()


    save_grouped_route = './grouped_data/'
    # 所有概念group
    all_concepts_grouped_ths = all_stocks_concepts_ths.groupby(['代码','名称'])['概念名称_ths'].apply(lambda x: ",".join \
                                (list(set(x.str.cat(sep=',').split(','))))).reset_index()

    # 将同花顺概念分为 “行业”，“事件”和“交易”三类
    industry_concepts_list_ths = concepts_ths.loc[concepts_ths['概念种类'].isin(['行业'])]['概念_ths'].values.tolist()
    events_concepts_list_ths = concepts_ths.loc[concepts_ths['概念种类'].isin(['事件','区域','知名企业'])]['概念_ths'].values.tolist()
    trading_concepts_list_ths = concepts_ths.loc[concepts_ths['概念种类'].isin(['金融'])]['概念_ths'].values.tolist()

    # 三类概念分别group
    industry_concepts_grouped_ths = all_stocks_concepts_ths.loc[all_stocks_concepts_ths['概念名称_ths'].isin(industry_concepts_list_ths)].\
                                groupby(['代码','名称'])['概念名称_ths'].apply(lambda x: ",".join \
                                (list(set(x.str.cat(sep=',').split(','))))).reset_index().rename(columns={'概念名称_ths': '行业概念_ths'})

    events_concepts_grouped_ths = all_stocks_concepts_ths.loc[all_stocks_concepts_ths['概念名称_ths'].isin(events_concepts_list_ths)].\
                                groupby(['代码','名称'])['概念名称_ths'].apply(lambda x: ",".join \
                                (list(set(x.str.cat(sep=',').split(','))))).reset_index().rename(columns={'概念名称_ths': '事件概念_ths'})

    trading_concepts_grouped_ths = all_stocks_concepts_ths.loc[all_stocks_concepts_ths['概念名称_ths'].isin(trading_concepts_list_ths)].\
                                groupby(['代码','名称'])['概念名称_ths'].apply(lambda x: ",".join \
                                (list(set(x.str.cat(sep=',').split(','))))).reset_index().rename(columns={'概念名称_ths': '交易概念_ths'})
    
    all_stocks_info = all_stocks_industry_ths.merge(all_concepts_grouped_ths,how='outer',left_on=['代码','名称'],right_on=['代码','名称']) \
                                            .merge(industry_concepts_grouped_ths,how='outer',left_on=['代码','名称'],right_on=['代码','名称']) \
                                            .merge(events_concepts_grouped_ths,how='outer',left_on=['代码','名称'],right_on=['代码','名称']) \
                                            .merge(trading_concepts_grouped_ths,how='outer',left_on=['代码','名称'],right_on=['代码','名称'])



     #所有概念表格
    all_concepts_grouped_em = all_stocks_concepts_em.groupby(['代码','名称'])['概念名称_em'].apply(lambda x: ",".join \
                                (list(set(x.str.cat(sep=',').split(','))))).reset_index()
 
    #将东方财富概念分为 “行业”，“事件”和“交易”三类
    industry_concepts_list_em = concepts_em.loc[concepts_em['概念种类'].isin(['行业'])]['概念_em'].values.tolist()
    events_concepts_list_em = concepts_em.loc[concepts_em['概念种类'].isin(['事件','区域','知名企业'])]['概念_em'].values.tolist()
    trading_concepts_list_em = concepts_em.loc[concepts_em['概念种类'].isin(['金融'])]['概念_em'].values.tolist()

    #分别制作三类概念数据表格
    industry_concepts_grouped_em = all_stocks_concepts_em.loc[all_stocks_concepts_em['概念名称_em'].isin(industry_concepts_list_em)].\
                                groupby(['代码','名称'])['概念名称_em'].apply(lambda x: ",".join \
                                (list(set(x.str.cat(sep=',').split(','))))).reset_index().rename(columns={'概念名称_em': '行业概念_em'})

    events_concepts_grouped_em = all_stocks_concepts_em.loc[all_stocks_concepts_em['概念名称_em'].isin(events_concepts_list_em)].\
                                groupby(['代码','名称'])['概念名称_em'].apply(lambda x: ",".join \
                                (list(set(x.str.cat(sep=',').split(','))))).reset_index().rename(columns={'概念名称_em': '事件概念_em'})

    trading_concepts_grouped_em = all_stocks_concepts_em.loc[all_stocks_concepts_em['概念名称_em'].isin(trading_concepts_list_em)].\
                                groupby(['代码','名称'])['概念名称_em'].apply(lambda x: ",".join \
                                (list(set(x.str.cat(sep=',').split(','))))).reset_index().rename(columns={'概念名称_em': '交易概念_em'})

    


    all_stocks_info = all_stocks_industry_ths.merge(all_concepts_grouped_ths,how='outer',left_on=['代码','名称'],right_on=['代码','名称']) \
                                                .merge(industry_concepts_grouped_ths,how='outer',left_on=['代码','名称'],right_on=['代码','名称']) \
                                                .merge(events_concepts_grouped_ths,how='outer',left_on=['代码','名称'],right_on=['代码','名称']) \
                                                .merge(trading_concepts_grouped_ths,how='outer',left_on=['代码','名称'],right_on=['代码','名称']) \
                                                .merge(all_concepts_grouped_em,how='outer',left_on=['代码'],right_on=['代码']) \
                                                .merge(industry_concepts_grouped_em,how='outer',left_on=['代码'],right_on=['代码']) \
                                                .merge(events_concepts_grouped_em,how='outer',left_on=['代码'],right_on=['代码']) \
                                                .merge(trading_concepts_grouped_em,how='outer',left_on=['代码'],right_on=['代码']) \
                                                .merge(stock_lrb_em,how='outer',left_on=['代码','名称'],right_on=['股票代码','股票简称']) \
                                                .merge(stock_zcfz_em,how='outer',left_on=['代码','名称'],right_on=['股票代码','股票简称']) \
                                                .merge(ts_stocks_info,how='outer',left_on=['代码'],right_on=['代码']) 

    all_stocks_info.to_csv( save_grouped_route + 'all_stocks_info.csv')


    all_stocks_info_main = all_stocks_info[['代码','名称_x','流通市值','市盈率','行业名称_ths','概念名称_ths','行业概念_ths','事件概念_ths','交易概念_ths', \
                                        '概念名称_em','行业概念_em','事件概念_em','交易概念_em','公司介绍','营业范围','主营业务','注册资本','省份','城市', \
                                        '净利润','净利润同比','营业总收入','营业总收入同比','资产负债率','股东权益合计']]
    all_stocks_info_main.to_csv( save_grouped_route + '股票行业概念信息.csv')