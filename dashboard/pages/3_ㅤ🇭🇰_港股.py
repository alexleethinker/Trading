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



data_path = './data/spot/stock_spot_hk.csv'

df = pd.read_csv(data_path,encoding = 'utf-8')
df['证券代码'] = df['证券代码'].astype(str)


fig = px.treemap(df, 
                 path=[px.Constant("全部"),'一级行业','二级行业','三级行业','证券名称'],  # 指定层次结构，每一个层次都应该是category型的变量
                 values='总市值', # 需要聚合的列名
                 color='涨跌幅', 
                 custom_data=['涨跌幅','证券代码','总市值','最新价'],
                 range_color = [-8, 8], # 色彩范围最大最小值
                 hover_data= {'涨跌幅':':.2',
                             '总市值':':.1f'}, # 鼠标悬浮显示数据的格式
                 color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                #  height = 900,
                #  width = 1600,
                 color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                )
fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
fig.update_coloraxes(showscale=False)
fig.update_traces(marker_line_width = 0.5,marker_line_color="white")
fig.update_traces(textposition='middle center', 
                  textinfo='label', 
                  textfont = dict(color='white'),
                  texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>",
                  hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.2f}  (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:d}亿")







fig2 = px.treemap(df, 
                 path=[px.Constant("全部"),'一级行业','二级行业','三级行业'],  # 指定层次结构，每一个层次都应该是category型的变量
                 values='总市值', # 需要聚合的列名
                 color='涨跌幅', 
                 custom_data=['涨跌幅','总市值',],
                 range_color = [-4, 4], # 色彩范围最大最小值
                 hover_data= {'涨跌幅':':.2',
                             '总市值':':.1f'}, # 鼠标悬浮显示数据的格式
                 color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                #  height = 900,
                #  width = 1600,
                 color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                )
fig2.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
fig2.update_coloraxes(showscale=False)
fig2.update_traces(marker_line_width = 0.5,marker_line_color="white")
fig2.update_traces(textposition='middle center', 
                  textinfo='label', 
                  textfont = dict(color='white'),
                  texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>",
                  hovertemplate= "%{label}<br>%{customdata[0]:.2f}%<br>总市值=%{customdata[1]:d}亿")



import os 
from datetime import datetime
import pytz

st.text('Last updated: ' + datetime.fromtimestamp(os.path.getmtime(data_path)).astimezone(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'))
# Plot!


tab1, tab2 = st.tabs(["板块概览", "个股详情"])
with tab1:
    st.plotly_chart(fig2, use_container_width=True, theme = 'streamlit')
with tab2:
    st.plotly_chart(fig, use_container_width=True, theme = 'streamlit')