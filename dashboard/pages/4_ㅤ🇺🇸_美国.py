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
translated_industry = './data/static/translation.xlsx'
# translated_name = './data/static/sg_stocks.csv'

df = pd.read_csv(data_path,encoding = 'utf-8')
# trans_df = pd.read_csv(translated_industry, encoding = 'gbk')
trans_df = pd.read_excel(open(translated_industry, 'rb'),sheet_name='industry_trans')
market_df = pd.read_excel(open(translated_industry, 'rb'),sheet_name='market_trans')
# sg_df = pd.read_csv(translated_name).fillna('')

df = df.merge(trans_df, on = 'industry').merge(market_df, on = 'market')


def plot_plate(market):
    dfi = df[df['market'] == market].fillna('')
    figi = px.treemap(dfi, 
                    path=[px.Constant("美国"),'大行业','一级行业','二级行业','证券名称'],  # 指定层次结构，每一个层次都应该是category型的变量
    #                  path=['plate','','sector','industry',],
                    values='market_cap_USD', # 需要聚合的列名
                    color='change', 
                    custom_data=['change','name','market_cap_USD','close','市场'],
                    range_color = [-8, 8], # 色彩范围最大最小值
    #                  hover_data= {'涨跌幅':':.2',
    #                              '总市值':':.1f'}, # 鼠标悬浮显示数据的格式
                    color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                    #  height = 800,
                    #  width = 1600,
                    color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                    )
    figi.update_layout(
                    {
                        'margin': dict(autoexpand=True,l=0,r=0,t=0,b=0),
    # 'margin' : dict(t=50, l=25, r=25, b=5),
    # 'plot_bordercolor':'white',
    # 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    # 'paper_bgcolor': 'white',
    })
    figi.update_coloraxes(showscale=False)
    figi.update_traces(marker_line_width = 0.5,marker_line_color="white")
    figi.update_traces(textposition='middle center', 
                    textinfo='label', 
                    textfont = dict(color='white'),
                    texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>",
                    hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.2f} (%{customdata[0]:.2f})%<br>总市值=%{customdata[2]:d}亿"                  
    #                   hovertemplate= "%{customdata[1]}<br>%{label}<br>(%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:d}亿"
                    ) 
    return figi



import os 
from datetime import datetime
import pytz
st.text('Last updated: ' + datetime.fromtimestamp(os.path.getmtime(data_path)).astimezone(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S') +  ' (Asia/Shanghai)')

# Plot!
st.plotly_chart(plot_plate('america'), use_container_width=True)



# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["欧洲", "亚太",'拉丁美洲','东盟','中东/非/东欧','南亚'])
# with tab1:
#     st.plotly_chart(plot_plate('欧洲'), use_container_width=True, theme = 'streamlit')
# with tab2:
#     st.plotly_chart(plot_plate('亚太'), use_container_width=True, theme = 'streamlit')
# with tab3:
#     st.plotly_chart(plot_plate('拉丁美洲'), use_container_width=True, theme = 'streamlit')
# with tab4:
#     st.plotly_chart(plot_plate('东盟'), use_container_width=True, theme = 'streamlit')
# with tab5:
#     st.plotly_chart(plot_plate('中东/非/东欧'), use_container_width=True, theme = 'streamlit')
# with tab6:
#     st.plotly_chart(plot_plate('南亚'), use_container_width=True, theme = 'streamlit')
