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



data_path = './data/spot/stock_spot_xetr.csv'
translated_industry = './data/static/translation.xlsx'
xetr_master = './data/static/xetr_masterdata.csv'

df = pd.read_csv(data_path,encoding = 'utf-8')
trans_df = pd.read_excel(open(translated_industry, 'rb'),sheet_name='industry_trans')
master_df = pd.read_csv(xetr_master,encoding = 'utf-8')
df = df.merge(trans_df, on = 'industry').merge(master_df , on = 'isin')

df.loc[~df['证券名称'].isnull(), 'name'] = df[~df['证券名称'].isnull()]['证券名称']
df['turnover'] = pd.to_numeric(df['turnover'], errors="coerce")/10000
df['marketCapitalisation'] = pd.to_numeric(df['marketCapitalisation'], errors="coerce")/100000000

def plot_plate():
    
    dfi = df.fillna("")
    dfi = dfi[dfi['turnover'] > dfi['turnover'].quantile(.5) ]

    figi = px.treemap(dfi, 
                    path=[px.Constant("XETR-EUR"),'大行业','一级行业','二级行业','name'],  # 指定层次结构，每一个层次都应该是category型的变量
    #                  path=['plate','','sector','industry',],
                    values='turnover', # 需要聚合的列名
                    color='changeToPrevDay', 
                    custom_data=['changeToPrevDay','symbol','marketCapitalisation','overview.lastPrice','xetr_industry','exchange_degiro','category','originCountry','turnover'],
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
                    hovertemplate= "%{customdata[5]}-%{customdata[6]} | %{customdata[1]}<br>%{customdata[7]}<br>%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:.1f}亿<br>成交额=%{customdata[8]:d}万<br>%{customdata[4]}"                  
    #                   hovertemplate= "%{customdata[1]}<br>%{label}<br>(%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:d}亿"
                    ) 
    return figi



import os 
from datetime import datetime
import pytz

timezone = 'Europe/Amsterdam'
st.text('Last updated: ' + datetime.fromtimestamp(os.path.getmtime(data_path)).astimezone(tz=pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S') +  ' {timezone}'.format(timezone=timezone))

# Plot!
st.plotly_chart(plot_plate(), use_container_width=True)



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
