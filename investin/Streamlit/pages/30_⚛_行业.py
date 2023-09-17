import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
page_config()

timezone = 'UTC'
data_path = '{data_dir}/spot/stock_spot_global_primary.csv'.format(data_dir=data_dir)
translated_industry = '{data_dir}/static/translation.xlsx'.format(data_dir=data_dir)

df = pd.read_csv(data_path,encoding = 'utf-8')
trans_df = pd.read_excel(open(translated_industry, 'rb'),sheet_name='industry_trans')
market_df = pd.read_excel(open(translated_industry, 'rb'),sheet_name='market_trans')

df = df.merge(trans_df, on = 'industry').merge(market_df, on = 'market').fillna("")



def plot_plate(industry):
    if industry in ['消费','金融']:
        path=[px.Constant("industry"),'plate','市场']
        dfi = df[df['大行业'].isin([industry]) & (~df['一级行业'].isin(['商业服务','经销商']))]

    elif industry in ['汽车','制药']:
        path=[px.Constant(industry),'二级行业','plate','市场','description']
        dfi = df[df['一级行业'].isin([industry])]

    else:
        path=[px.Constant(industry),'plate','市场','description']
        if industry in ['石油']:
            dfi = df[df['一级行业'].isin(['能源'])]
            dfi = dfi[~dfi['二级行业'].isin(['煤炭'])]  
        else:        
            dfi = df[df['二级行业'].isin([industry])]


    dfi = dfi[dfi['market_cap_USD'] > dfi['market_cap_USD'].quantile(.75) ]
    fig = treemap(dfi, 
                    path=path,  
                    values='market_cap_USD',
                    color='change', 
                    range_color = 8,
                    custom_data=['change','name','market_cap_USD','close','市场','Traded_USD'],
                    hovertemplate= "%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:d}亿<br>成交额=%{customdata[5]:.2f}亿"                  
                    )               
    return fig



update_at(data_path, timezone)


st.radio(
    "",
    key="industry",
    options=['金融','消费','半导体','汽车','计算机设备','电力设备','机械加工设备','制药','石油','煤炭','钢'],
    horizontal=True
)



# Plot!
fig = plot_plate(st.session_state.industry)
st.plotly_chart(fig, use_container_width=True)

