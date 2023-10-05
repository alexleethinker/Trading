import numpy as np
import math
import streamlit as st

def color_style(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: green'` for negative
    strings, red otherwise.
    """
    color = 'red' if val > 0 else 'green'
    return 'color: %s' % color

def show_dataframe(df, market = None):
    
    market_value = '流通市值' if market == '🇨🇳 A股' else '总市值'
    
    
    adj_list_100 = ['🇬🇧 英股','🇪🇺 欧股','欧洲']
    adj_list_10 =  ['南亚','东盟','中东非','拉美']
    
    # df['异动值'] = df['成交额'] * df['涨跌幅'].abs() * np.log10( (math.e - 1) * df['涨跌幅'].abs() + 1) / (np.log(df[market_value] + 1) + 1)
    df = df[~df['异动值'].isnull()]
    df['异动值'] = df['异动值'] * 100 if market in adj_list_100 else df['异动值']
    df['异动值'] = df['异动值'] * 10 if market in adj_list_10 else df['异动值']
       
    df = df[(df['涨跌幅'].abs() > 1) & (df['异动值'] > 1)].sort_values('异动值', ascending= False)\
        [['证券代码','证券名称','涨跌幅','异动值',market_value,'成交额','二级行业']].head(100)
    col = st.columns([1, 1])
    with col[0]:
        st.markdown('市场异动 (市值 > 200亿)')
        st.dataframe(df[df[market_value] > 200].head(10)\
            .style.applymap(color_style, subset=['涨跌幅'])\
            .format({'涨跌幅': "{:.2f}%"},precision=2),
            hide_index=True)
    with col[1]:
        st.markdown('市场异动 (市值 < 200亿)')
        st.dataframe(df[df[market_value] < 200].head(20)\
            .style.applymap(color_style, subset=['涨跌幅'])\
            .bar(subset=['异动值'], color='#d65f5f')\
            .format({'涨跌幅': "{:.2f}%"},precision=2),
            hide_index=True)