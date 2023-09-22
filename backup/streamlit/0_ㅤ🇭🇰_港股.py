import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
page_config()


title = '港股-HKD'
timezone = 'Asia/Shanghai'
data_path = '{data_dir}/spot/stock_spot_hk.csv'.format(data_dir=data_dir)


df = pd.read_csv(data_path,encoding = 'utf-8')
df['证券代码'] = df['证券代码'].astype(str)
df = df[df['证券代码'].str[:1] != '8']
df = df[df['总市值'] > df['总市值'].quantile(.85) ]



fig_block = treemap(df, 
                 path=[px.Constant(title),'一级行业','二级行业','三级行业'], 
                 values='总市值', 
                 color='涨跌幅', 
                 range_color = 4, 
                 custom_data=['涨跌幅','总市值','成交额'],
                 hovertemplate= "%{label}<br>%{customdata[0]:.2f}%<br>总市值=%{customdata[1]:d}亿"
                )
fig = treemap(df, 
                 path=[px.Constant(title),'一级行业','二级行业','证券名称'], 
                 values='总市值', 
                 color='涨跌幅', 
                 range_color = 8, 
                 custom_data=['涨跌幅','证券代码','总市值','最新价','am','am_u'],
                 hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.2f}  (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:d}亿<br>成交额=%{customdata[4]:d}%{customdata[5]}"
                )



update_at(data_path, timezone)

tab1, tab2 = st.tabs(["板块概览", "个股详情"])
with tab1:
    st.plotly_chart(fig_block, use_container_width=True)
with tab2:
    st.plotly_chart(fig, use_container_width=True)