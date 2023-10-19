import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
page_config()
from utils.tables import show_dataframe

timezone = 'UTC'
data_path = '{data_dir}/spot/stock_spot_global_primary.csv'.format(data_dir=data_dir)
df = pd.read_csv(data_path,encoding = 'utf-8')


def plot_plate(plate = '欧洲'):
    values = '成交额' if traded_value_on else '总市值'
    
    if plate in ['概览','全球']:
        if traded_value_on:
            path = '{data_dir}/spot/stock_spot_global_all.csv'.format(data_dir=data_dir)
            df_copy = pd.read_csv(path,encoding = 'utf-8')
            dfi = df_copy.fillna('')
        else:
            dfi = df.fillna('')
        dfi = dfi[dfi['成交额'] > dfi['成交额'].quantile(.6) ]

        details = [] if plate == '概览' else ['一级行业','二级行业','三级行业']
        path=[px.Constant(values + "(USD)"),'地区','市场'] + details
        custom_data=['涨跌幅', values]
        range_color = 4
        hovertemplate= "%{label}<br>%{customdata[0]:.2f}%<br>" + values + "=%{customdata[2]:d}亿"  
        
        update_at(data_path, timezone)
        fig = treemap(      dfi, 
                            path=path, 
                            values=values, 
                            color='涨跌幅', 
                            range_color = range_color, 
                            custom_data=custom_data,
                            hovertemplate = hovertemplate
                        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        dfi = df[df['地区'] == plate]
        
        block = 'exchange' if plate == '欧洲' else '市场'
        
        dfi['exchange'] = dfi['exchange'].replace(dict.fromkeys(['MIL','LUXSE'],'EURONEXT'))\
                                         .replace(dict.fromkeys(['BME'],'SIX'))\
                                         .replace(dict.fromkeys(['OMXCOP','OMXHEX','OMXSTO','OMXICE','OSL'],'OMX')) 
        if plate == '欧洲':
            dfi =dfi[dfi['exchange'].isin(['EURONEXT','LSE','XETR','SIX','OMX'])]     
        
        path=[block,'一级行业','二级行业','三级行业','证券名称']
        custom_data=['涨跌幅','full_symbol','总市值','最新价','市场','成交额']
        range_color = 8
        hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.1f} (%{customdata[0]:.2f})%<br>总市值=%{customdata[2]:d}亿<br>成交额=%{customdata[5]:.2f}亿"                  
        update_at(data_path, timezone)

        market_list = dfi.groupby([block])[['总市值']].sum().sort_values('总市值',ascending=False).reset_index()[block].tolist()
        tabs = st.tabs(market_list)
        for i in range(len(market_list)):
            with tabs[i]:
                dfj = dfi[dfi[block] == market_list[i]]
                
                dfj = dfj[dfj['成交额'] > dfj['成交额'].quantile(.75) ]
                fig = treemap(dfj, 
                    path=path, 
                    values=values, 
                    color='涨跌幅', 
                    range_color = range_color, 
                    custom_data=custom_data,
                    hovertemplate = hovertemplate
                )
                st.plotly_chart(fig, use_container_width=True)
    
                show_dataframe(dfj, plate)



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
    
    
plot_plate(st.session_state.plate.split(' ')[1])


st.markdown('数据来源：TradingView（大部分市场延迟15分钟）')
