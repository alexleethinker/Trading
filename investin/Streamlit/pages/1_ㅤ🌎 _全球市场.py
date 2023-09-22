import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
page_config()

timezone = 'UTC'
data_path = '{data_dir}/spot/stock_spot_global_primary.csv'.format(data_dir=data_dir)
df = pd.read_csv(data_path,encoding = 'utf-8')


def plot_plate(plate = '欧洲'):
    values='Traded_USD' if traded_value_on else 'market_cap_USD'
    values_show = '成交额' if traded_value_on else '总市值'
    
    if plate in ['概览','全球']:
        if traded_value_on:
            path = '{data_dir}/spot/stock_spot_global_all.csv'.format(data_dir=data_dir)
            df_copy = pd.read_csv(path,encoding = 'utf-8')
            dfi = df_copy.fillna('')
        else:
            dfi = df.fillna('')
        dfi = dfi[dfi['Traded_USD'] > dfi['Traded_USD'].quantile(.6) ]

        details = [] if plate == '概览' else ['一级行业','二级行业','三级行业']
        path=[px.Constant(values_show + "(USD)"),'plate','市场'] + details
        custom_data=['change','name', values]
        range_color = 4
        hovertemplate= "%{label}<br>%{customdata[0]:.2f}%<br>" + values_show + "=%{customdata[2]:d}亿"  

    else:
        dfi = df[df['plate'] == plate]
        dfi = dfi[dfi['Traded_USD'] > dfi['Traded_USD'].quantile(.75) ]

        path=['plate','市场','一级行业','二级行业','三级行业','证券名称']
        custom_data=['change','name','market_cap_USD','close','市场','Traded_USD']
        range_color = 8
        hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.1f} (%{customdata[0]:.2f})%<br>总市值=%{customdata[2]:d}亿<br>成交额=%{customdata[5]:.2f}亿"                  
    
    update_at(data_path, timezone)
    
    fig = treemap(      dfi, 
                        path=path, 
                        values=values, 
                        color='change', 
                        range_color = range_color, 
                        custom_data=custom_data,
                        hovertemplate = hovertemplate
                    )
    return fig




col = st.columns([9, 1])
with col[0]:
    st.radio(
        "",
        key="plate",
        options=['🌎 概览','🌎 全球','🇨🇳 中国','🇺🇸 北美','🇪🇺 欧洲','🇯🇵 亚太','🇮🇳 南亚','🇸🇬 东盟','🇸🇦 中东非','🇧🇷 拉美'],
        horizontal=True,
        label_visibility='collapsed'
    )
with col[1]:
    traded_value_on = st.toggle('成交额')
    
    
fig = plot_plate(st.session_state.plate.split(' ')[1])
st.plotly_chart(fig, use_container_width=True)

st.markdown('数据来源：TradingView（大部分市场延迟15分钟）')
