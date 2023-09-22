import pandas as pd


def Categorize_Concept_ths():
    
    # 所有概念group
    global all_concepts_grouped_ths
    global industry_concepts_grouped_ths
    global events_concepts_grouped_ths
    global trading_concepts_grouped_ths

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


def Categorize_Concept_em():

    global all_concepts_grouped_em
    global industry_concepts_grouped_em
    global events_concepts_grouped_em
    global trading_concepts_grouped_em

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






read_route = './ungrouped_data/'
save_route = './grouped_data/'

concepts_ths = pd.read_csv('./行业概念/ths_概念.csv',encoding="gbk")
concepts_em = pd.read_csv('./行业概念/em_概念.csv',encoding="gbk") # 经过优化后的概念列表

all_stocks_industry_ths = pd.read_csv('./ungrouped_data/all_stocks_industry_ths.csv',encoding="gbk",encoding_errors='ignore',converters = {u'代码':str})
#print(all_stocks_industry_ths)
all_stocks_concepts_ths = pd.read_csv('./ungrouped_data/all_stocks_concepts_ths_ungrouped.csv',encoding="gbk",encoding_errors='ignore',converters = {u'代码':str})
all_stocks_concepts_em  = pd.read_csv('./ungrouped_data/all_stocks_concepts_em_ungrouped.csv' ,encoding="gbk",encoding_errors='ignore',converters = {u'代码':str})

ts_stocks_info = pd.read_csv('./ungrouped_data/ts_stocks_info.csv',encoding="gbk",encoding_errors='ignore',converters = {u'代码':str})
stock_zcfz_em  = pd.read_csv('./ungrouped_data/balance_sheet.csv',encoding="gbk",encoding_errors='ignore',converters = {u'股票代码':str})
stock_lrb_em   = pd.read_csv('./ungrouped_data/revenue.csv',encoding="gbk",encoding_errors='ignore',converters = {u'股票代码':str})


Categorize_Concept_ths()
Categorize_Concept_em()

# # merge 行业和所有概念信息
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

all_stocks_info.to_csv( save_route + 'all_stocks_info.csv')


all_stocks_info_main = all_stocks_info[['代码','名称_x','流通市值','市盈率','行业名称_ths','概念名称_ths','行业概念_ths','事件概念_ths','交易概念_ths', \
                                    '概念名称_em','行业概念_em','事件概念_em','交易概念_em','公司介绍','营业范围','主营业务','注册资本','省份','城市', \
                                    '净利润','净利润同比','营业总收入','营业总收入同比','资产负债率','股东权益合计']]
all_stocks_info_main.to_csv( save_route + '股票行业概念信息.csv')