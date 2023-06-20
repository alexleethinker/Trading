import streamlit as st
st.set_page_config(layout= 'wide')
import pandas as pd
import plotly.express as px

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
body {border-color: white; border-style: solid;}
footer {visibility: hidden;}
</style>

# """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



data_path = './data/spot/stock_spot_global_primary.csv'

df = pd.read_csv(data_path,encoding = 'utf-8')

fig = px.treemap(df, 
                 path=[px.Constant("世界"),'plate','market','sector','industry'],  # 指定层次结构，每一个层次都应该是category型的变量
#                  path=['plate','','sector','industry',],
                 values='market_cap_USD', # 需要聚合的列名
                 color='change', 
                 custom_data=['change','name','market_cap_USD','close','market','close'],
                 range_color = [-8, 8], # 色彩范围最大最小值
#                  hover_data= {'涨跌幅':':.2',
#                              '总市值':':.1f'}, # 鼠标悬浮显示数据的格式
                 color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                #  height = 800,
                #  width = 1600,
                 color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                )
fig.update_layout(
                  {
# 'margin' : dict(t=50, l=25, r=25, b=5),
# 'plot_bordercolor':'white',
# 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
# 'paper_bgcolor': 'white',
})
fig.update_coloraxes(showscale=False)
fig.update_traces(marker_line_width = 0.5,marker_line_color="white")
fig.update_traces(textposition='middle center', 
                  textinfo='label', 
                  textfont = dict(color='white'),
                  texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>",
                  hovertemplate= "%{label}<br>%{customdata[5]:.2f} (%{customdata[0]:.2f}%)<br>%{customdata[4]}<br>总市值=%{customdata[2]:d}亿"                  
#                   hovertemplate= "%{customdata[1]}<br>%{label}<br>(%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:d}亿"
                 ) 

import os 
from datetime import datetime
import pytz
st.text('Last updated: ' + datetime.fromtimestamp(os.path.getmtime(data_path)).astimezone(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S') +  ' (Asia/Shanghai)')

# Plot!
st.plotly_chart(fig, use_container_width=True)
