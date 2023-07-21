import streamlit as st
st.set_page_config(layout= 'wide')
import pandas as pd
import plotly.express as px


BACKGROUND_COLOR = 'black'
COLOR = 'black'

def set_page_container_style(
        max_width: int = 1100, max_width_100_percent: bool = False,
        padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = 10,
        color: str = COLOR, background_color: str = BACKGROUND_COLOR,
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        st.markdown(
            f'''
            <style>
                #MainMenu {{visibility: hidden;}}
                body {{border-color: white; border-style: solid;}}
                footer {{visibility: hidden;}}
                .reportview-container .sidebar-content {{
                    padding-top: {padding_top}rem;
                }}
                .reportview-container .main .block-container {{
                    {max_width_str}
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
                .reportview-container .main {{
                    color: {color};
                    background-color: {background_color};

                }}
            </style>
            ''',
            unsafe_allow_html=True,
        )

set_page_container_style()

# hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# body {border-color: white; border-style: solid;}
# footer {visibility: hidden;}
# </style>

# # """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



data_path = './data/spot/stock_spot_global_primary.csv'
translated_industry = './data/static/translation.xlsx'

df = pd.read_csv(data_path,encoding = 'utf-8')
# trans_df = pd.read_csv(translated_industry, encoding = 'gbk')
trans_df = pd.read_excel(open(translated_industry, 'rb'),sheet_name='industry_trans')
market_df = pd.read_excel(open(translated_industry, 'rb'),sheet_name='market_trans')

df = df.merge(trans_df, on = 'industry').merge(market_df, on = 'market')
df['description'] = df['description'].str.replace('(UK)','').str.replace('-X','')


def plot_plate(plate = '欧洲'):

    if plate == '全球':
        path=[px.Constant("世界(USD)"),'plate','市场','大行业','一级行业','二级行业']
        dfi = df
        dfi = dfi[dfi['Traded_USD'] > dfi['Traded_USD'].quantile(.6) ]

        custom_data=['change','name','market_cap_USD']
        range_color = [-4, 4]
        texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>"
        hovertemplate= "%{label}<br>%{customdata[0]:.2f}%<br>总市值=%{customdata[2]:d}亿"    

    else:
        path=['plate','市场','大行业','一级行业','二级行业','description']
        dfi = df[df['plate'] == plate]
        dfi = dfi[dfi['Traded_USD'] > dfi['Traded_USD'].quantile(.75) ]

        custom_data=['change','name','market_cap_USD','close','市场','Traded_USD']
        range_color = [-8, 8]
        texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>"
        hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.1f} (%{customdata[0]:.2f})%<br>总市值=%{customdata[2]:d}亿<br>成交额=%{customdata[5]:.2f}亿"                  
 
    figi = px.treemap(dfi, 
                    path=path,  # 指定层次结构，每一个层次都应该是category型的变量
                    values='market_cap_USD', # 需要聚合的列名
                    color='change', 
                    custom_data=custom_data,
                    range_color = range_color, # 色彩范围最大最小值
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
    })
    figi.update_coloraxes(showscale=False)
    figi.update_traces(marker_line_width = 0.5,marker_line_color="white")
    figi.update_traces(textposition='middle center', 
                    textinfo='label', 
                    textfont = dict(color='white'),
                    texttemplate= texttemplate,
                    hovertemplate= hovertemplate                  
                    ) 
    return figi



import os 
from datetime import datetime
import pytz
timezone = 'UTC'
st.text('Last updated: ' + datetime.fromtimestamp(os.path.getmtime(data_path)).astimezone(tz=pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S') +  ' {timezone}'.format(timezone=timezone))

# Plot!
# st.plotly_chart(fig1, use_container_width=True)

st.radio(
    "",
    key="plate",
    options=['🌎 全球','🇺🇸 北美','🇪🇺 欧洲','🇯🇵 亚太','🇮🇳 南亚','🇸🇬 东盟','🇸🇦 中东/非/东欧','🇧🇷 拉丁美洲'],
    horizontal=True
)


# option = st.selectbox(
#     '',
#     ('🇺🇸_北美','🇪🇺_欧洲','🇯🇵_亚太','🇮🇳_南亚','🇸🇬_东盟','🇸🇦_中东/非/东欧','🇧🇷_拉丁美洲'))

st.plotly_chart(plot_plate(st.session_state.plate.split(' ')[1]), use_container_width=True, theme = 'streamlit')


# tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(['🇪🇺欧洲','🇯🇵亚太','🇮🇳南亚','🇸🇬东盟','🇸🇦中东/非/东欧','🇧🇷拉丁美洲'])
# with tab1:
#     st.plotly_chart(plot_plate('欧洲'), use_container_width=True, theme = 'streamlit')
# with tab2:
#     st.plotly_chart(plot_plate('亚太'), use_container_width=True, theme = 'streamlit')
# with tab3:
#     st.plotly_chart(plot_plate('南亚'), use_container_width=True, theme = 'streamlit')
# with tab4:
#     st.plotly_chart(plot_plate('东盟'), use_container_width=True, theme = 'streamlit')
# with tab5:
#     st.plotly_chart(plot_plate('中东/非/东欧'), use_container_width=True, theme = 'streamlit')
# with tab6:
#     st.plotly_chart(plot_plate('拉丁美洲'), use_container_width=True, theme = 'streamlit')
