import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
page_config()

title = 'A股-RMB'
timezone = 'Asia/Shanghai'
data_path = '{data_dir}/spot/stock_spot_china_a.csv'.format(data_dir=data_dir)
update_at(data_path, timezone)

df = pd.read_csv(data_path,encoding = 'utf-8')
df = df[df['成交额'] > df['成交额'].quantile(.5) ]

fig_block = treemap(df, 
                 path=[px.Constant(title),'一级行业','二级行业','三级行业'],
                 values='流通市值', 
                 color='涨跌幅', 
                 range_color = 4, 
                 custom_data=['涨跌幅','流通市值'],
                 hovertemplate= "%{label}<br>涨跌幅=%{customdata[0]:.2f}%<br>流通市值=%{customdata[1]:d}亿"
                )

fig = treemap(df, 
                path=[px.Constant(title),'一级行业','二级行业','三级行业','证券名称'], 
                values='流通市值', 
                color='涨跌幅', 
                range_color = 8, 
                custom_data=['涨跌幅','流通市值','所属同花顺行业','投资逻辑','最新价','证券代码','主营产品','成交额'],
                hovertemplate= "%{customdata[5]}<br>%{label}<br>%{customdata[4]:.2f}  (%{customdata[0]:.2f}%)<br>流通市值=%{customdata[1]:d}亿<br>成交额=%{customdata[7]:.2f}亿<br>%{customdata[2]}<br>主营产品：%{customdata[6]}<br>%{customdata[3]}<br>"
                )


tab1, tab2 = st.tabs(["板块概览", "个股详情"])
with tab1:
    st.plotly_chart(fig_block, use_container_width=True)
with tab2:
    st.plotly_chart(fig, use_container_width=True)