from utils.config import page_config, data_dir
page_config()
import streamlit as st
import datetime
from pandas.tseries.offsets import BDay
import pandas as pd
from utils.figure import treemap
import plotly.express as px
import numpy as np
import math
import exchange_calendars as xcals


market = 'china'

col = st.columns([2,7,1])

with col[0]:
    def reset_date():
        del st.session_state['date'] 
    d = st.date_input("选择日期", datetime.date(2015, 6, 17),\
                                min_value= datetime.date(2003, 10, 14),\
                                max_value= datetime.datetime.today().date(),\
                                on_change= reset_date,\
                                label_visibility="collapsed")
    
with col[1]:
    if 'date' not in st.session_state:
        st.session_state['date'] = d
    def next_day():
        st.session_state['date'] += BDay(1)
    def previous_day():
        st.session_state['date'] -= BDay(1)
    
    sub_col = st.columns([3,2,2,5])
    with sub_col[1]:
        st.button("上一日", on_click=previous_day)
    with sub_col[2]:
        st.button("下一日", on_click=next_day)
    

with col[2]:
    traded_value_on = st.toggle('成交额')

st.markdown(f'<div align="center">{st.session_state["date"].strftime("%Y-%m-%d %A")}</div>', unsafe_allow_html=True)    


def get_date_list():
    xshg = xcals.get_calendar("XSHG")
    date_list = xshg.schedule.index.date
    date_list = [ x.strftime('%Y-%m-%d') for x in date_list ]
    return date_list

date_list = get_date_list()

if st.session_state['date'].strftime('%Y-%m-%d') in date_list:

    def history_spot(date):
        df = pd.read_feather(f'{data_dir}/history/snapshot/{market}/{date}.feather')  
        return df  
        
    df = history_spot(st.session_state['date'].strftime('%Y-%m-%d'))
    data_path = f'{data_dir}/spot/stock_spot_china_a.csv'
    details = pd.read_csv(data_path)[['证券代码','证券名称','一级行业','二级行业','三级行业']]
    df = df.merge(details, how = 'inner', on = '证券代码')
    df = df[df['成交额'] > df['成交额'].quantile(.2) ]
    df['成交额'] = (pd.to_numeric(df['成交额'], errors="coerce")/100000000).round(3).fillna(0) 
    df['总市值'] = df['成交额'] / df['换手率'] * 100
    df['异动值'] = df['成交额'] * np.maximum(df['涨跌幅'].abs(), df['振幅']) * np.log10( (math.e - 1) * df['涨跌幅'].abs() + 1) / (np.log(df['总市值'] + 1) + 1) 



    fig = treemap(      df, 
                        path=[px.Constant(st.session_state['date'].strftime('%Y-%m-%d')),'一级行业','二级行业','三级行业','证券名称'], 
                        values= '成交额' if traded_value_on else '总市值' , 
                        color='涨跌幅', 
                        range_color = 8, 
                        custom_data= ['涨跌幅','收盘','成交额','总市值'],
                        hovertemplate = "%{label}<br>%{customdata[0]:.2f}%<br>总市值=%{customdata[3]:.1f}亿<br>成交额=%{customdata[2]:.2f}亿" 
                    )
    st.plotly_chart(fig, use_container_width=True)


    from utils.tables import color_abnormal, color_style
    market_value = '总市值'
    df = df[(df['涨跌幅'].abs() > 0.5) & (df['异动值'] > 1) ].sort_values('异动值', ascending= False)\
        [['证券代码','证券名称','涨跌幅','异动值', market_value,'成交额', '二级行业']].head(100)
    col = st.columns([1, 1, 1])
    with col[0]:
        st.markdown('市场异动 (市值 > 400亿)')
        st.dataframe(df[df[market_value] > 400].head(20)\
            .style.applymap(color_style, subset=['涨跌幅'])\
            .applymap(color_abnormal, subset=['异动值'])\
            .format({'涨跌幅': "{:.2f}%"},precision=2),
            hide_index=True)
        # st.write(html_abnormal_mov, unsafe_allow_html= True)

    with col[1]:
        st.markdown('市场异动 (市值 100-400亿)')
        st.dataframe(df[df[market_value].between(100,400)].head(20)\
            .style.applymap(color_style, subset=['涨跌幅'])\
            .applymap(color_abnormal, subset=['异动值'])\
            .format({'涨跌幅': "{:.2f}%"},precision=2),
            hide_index=True)

    with col[2]:
        st.markdown('市场异动 (市值 < 100亿)')
        st.dataframe(df[df[market_value] < 100].head(20)\
            .style.applymap(color_style, subset=['涨跌幅'])\
            .applymap(color_abnormal, subset=['异动值'])\
            .format({'涨跌幅': "{:.2f}%"},precision=2),
            hide_index=True)
        
else:
    st.markdown(st.session_state['date'].strftime('%Y-%m-%d') + ' 非交易日')