import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir, get_args
from utils.figure import treemap
page_config()

import plotly.express as px
import numpy as np


a_stock = pd.read_csv(f'{data_dir}/spot/stock_spot_china_a.csv')[['证券代码','一级行业','二级行业','三级行业']]

@st.cache_data
def prepare_raw(source):
    df = pd.read_excel(f'{data_dir}/static/EM/China/{source}.xlsx') 
    df = df.dropna(subset = ['证券名称']).replace('——',np.nan).dropna(how = 'all').dropna(axis = 1, how = 'all').fillna(0)
    df.columns = [x.replace('\n[报告类型]合并报表\n[单位]元','').replace('\n[报告期]','').replace(source,'') for x in df.columns.tolist()]
    df.columns = [x.replace('年一季','0331').replace('年二季/中报','0630').replace('年三季','0930').replace('年年报','1231') for x in df.columns.tolist()]
    df = a_stock.merge(df, on = '证券代码', how= 'left').drop(columns = ['证券代码','证券名称'])
    return df

capex = prepare_raw('资本支出')
inventory = prepare_raw('存货')
income = prepare_raw('营业收入')



start_date = '2004-01-01'
industry_level = st.radio(
        "研究范围",
        key="level",
        options=['二级行业','三级行业'],
        horizontal=True,
        label_visibility='visible'
    )

col = st.columns([1,1,1])
with col[0]:
    level_1 = st.selectbox(
        "一级行业",
        ('金融','科技','资源','化工','建筑业','电力设备','交通运输','汽车','机械','可选消费','必需消费','生物医药','公共事业'))
with col[1]:
    level_2 = st.selectbox(
        "二级行业",
        tuple(a_stock[a_stock['一级行业'].isin([level_1])]['二级行业'].unique()))
with col[2]:
    if industry_level == '三级行业':
        level_3 = st.selectbox(
        "三级行业",
        tuple(a_stock[a_stock['二级行业'].isin([level_2])]['三级行业'].unique()))
    else:
        pass


industry_name = level_3 if industry_level == '三级行业' else level_2

def calculate_change(df):
    df = df[df[industry_level].isin([industry_name])].groupby([industry_level]).sum().T/100000000
    df.index = pd.to_datetime(df.index)
    df = df[(df.index > start_date)].sum(axis=1)
    df = ((df - df.shift(4)) / df.shift(4)).dropna(how='all')
    return df

capex_df = calculate_change(capex)
inventory_df = calculate_change(inventory)
income_df = calculate_change(income)
df = pd.concat([capex_df, inventory_df, income_df], axis=1).rename(columns={0: "资本支出", 1: "存货", 2:"营业收入"}).round(2)



historical_percentile = (inventory_df.tail(1)[0] - inventory_df.tail(40).min()) / (inventory_df.tail(40).max() - inventory_df.tail(40).min())

fig = px.line(df, color_discrete_sequence = ['red','yellow','lightgreen'], title = industry_name+'行业库存周期 - 历史分位值:'+ "{:.0%}".format(historical_percentile) ,
              labels={
                     "value": "同比增长率",
                     "index": "",
                     "variable": ""
                 },)
def fig_render(fig):
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'margin': dict(autoexpand=True,l=0,r=0,b=0),
        'showlegend': True
        })
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(zeroline = True, zerolinecolor = 'white', zerolinewidth = 0.5)
    return fig

fig =  fig_render(fig)
st.plotly_chart(fig, use_container_width=True)