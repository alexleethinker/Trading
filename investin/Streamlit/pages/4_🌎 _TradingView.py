import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
page_config()

timezone = 'UTC'
data_path = '{data_dir}/spot/stock_spot_global_primary.csv'.format(data_dir=data_dir)

df = pd.read_csv(data_path,encoding = 'utf-8')
df['证券名称'] = df['证券名称'].str.replace('(UK)','').str.replace('-X','')


def plot_plate(plate = '欧洲'):

    if plate == '全球':
        dfi = df.fillna('')
        dfi = dfi[dfi['Traded_USD'] > dfi['Traded_USD'].quantile(.6) ]

        path=[px.Constant("世界(USD)"),'plate','市场','一级行业','二级行业','三级行业']
        custom_data=['change','name','market_cap_USD']
        range_color = 4
        hovertemplate= "%{label}<br>%{customdata[0]:.2f}%<br>总市值=%{customdata[2]:d}亿"    

    else:
        dfi = df[df['plate'] == plate]
        dfi = dfi[dfi['Traded_USD'] > dfi['Traded_USD'].quantile(.75) ]

        path=['plate','市场','一级行业','二级行业','三级行业','证券名称']
        custom_data=['change','name','market_cap_USD','close','市场','Traded_USD']
        range_color = 8
        hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.1f} (%{customdata[0]:.2f})%<br>总市值=%{customdata[2]:d}亿<br>成交额=%{customdata[5]:.2f}亿"                  
 
    fig = treemap(      dfi, 
                        path=path, 
                        values='market_cap_USD', 
                        color='change', 
                        range_color = range_color, 
                        custom_data=custom_data,
                        hovertemplate = hovertemplate
                    )
    return fig



update_at(data_path, timezone)

st.radio(
    "",
    key="plate",
    options=['🌎 全球','🇨🇳 中国','🇺🇸 北美','🇪🇺 欧洲','🇯🇵 亚太','🇮🇳 南亚','🇸🇬 东盟','🇸🇦 中东/非/东欧','🇧🇷 拉丁美洲'],
    horizontal=True,
    label_visibility='collapsed'
)

fig = plot_plate(st.session_state.plate.split(' ')[1])
st.plotly_chart(fig, use_container_width=True)

