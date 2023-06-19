import streamlit as st
st.set_page_config(layout= 'wide')
import pandas as pd
import plotly.express as px

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



data_path = './csv/stock_spot.csv'

df = pd.read_csv(data_path,encoding = 'utf-8')

fig = px.treemap(df, 
                 path=['一级行业','二级行业','三级行业'],  # 指定层次结构，每一个层次都应该是category型的变量
                 values='流通市值', # 需要聚合的列名
                 color='涨跌幅', 
                 custom_data=['涨跌幅','流通市值'],
                 range_color = [-4, 4], # 色彩范围最大最小值
                 hover_data= {'涨跌幅':':.2',
                             '流通市值':':.1f'}, # 鼠标悬浮显示数据的格式
                 color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                 height = 500,
                #  width = 1600,
                 color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                )
fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
fig.update_coloraxes(showscale=False)
fig.update_traces(textposition='middle center', 
                  textinfo='label', 
                  textfont = dict(color='white'),
                  texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>",
                  hovertemplate= "%{label}<br>涨跌幅=%{customdata[0]:.2f}%<br>流通市值=%{customdata[1]:d}") # 显示企业名称和市值，字体24

import os 
from datetime import datetime
import pytz

st.text('Last updated: ' + datetime.fromtimestamp(os.path.getmtime(data_path)).astimezone(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'))
# Plot!
st.plotly_chart(fig, use_container_width=True)




fig2 = px.treemap(df, 
                 path=['一级行业','二级行业','三级行业','股票简称',],  # 指定层次结构，每一个层次都应该是category型的变量
                 values='流通市值', # 需要聚合的列名
                 color='涨跌幅', 
                 custom_data=['涨跌幅','流通市值','所属同花顺行业','公司亮点','最新价','股票代码'],
                 range_color = [-8, 8], # 色彩范围最大最小值
                 hover_data= {'涨跌幅':':.2',
                             '流通市值':':.1f'}, # 鼠标悬浮显示数据的格式
                 color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                 height = 500,
                #  width = 1600,
                 color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                )
fig2.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
fig2.update_coloraxes(showscale=False)
fig2.update_traces(textposition='middle center', 
                  textinfo='label', 
                  textfont = dict(color='white'),
                  texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>",
                  hovertemplate= "%{customdata[5]}<br>%{label}<br>%{customdata[4]:.2f}  (%{customdata[0]:.2f}%)<br>流通市值=%{customdata[1]:d}亿<br>%{customdata[2]}<br>%{customdata[3]}<br>") # 显示企业名称和市值，字体24

    # hovertemplate="<br>".join([
    #     "ColX: %{x}",
    #     "ColY: %{y}",
    #     "Col1: %{customdata[0]}",
    #     "Col2: %{customdata[1]}",
    #     "Col3: %{customdata[2]}",
    # ])
st.plotly_chart(fig2, use_container_width=True)
