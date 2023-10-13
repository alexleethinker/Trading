from utils.config import page_config, data_dir
page_config()
import streamlit as st
import datetime
import pandas as pd
from utils.figure import treemap
import plotly.express as px

d = st.date_input("选择日期", datetime.date(2019, 7, 1))



def history_spot(date):
    store = pd.HDFStore(f'{data_dir}/history/stock/china.h5', 'r')   
    stock_list = [x.replace('/','') for x in store.keys()]     
    df = pd.DataFrame()
    for symbol in stock_list:
        try:
            dfi = store[symbol]
            dfi = dfi[dfi.index == date]
            dfi['证券代码'] = symbol
            df = pd.concat([df, dfi], ignore_index=True)
        except:
            pass
    store.close()
    return df[['证券代码','收盘','涨跌幅','成交额']]
    
# st.write(d.strftime('%Y-%m-%d %H:%M:%S'))    
df = history_spot(d.strftime('%Y-%m-%d'))
data_path = f'{data_dir}/spot/stock_spot_china_a.csv'
details = pd.read_csv(data_path)[['证券代码','证券名称','一级行业','二级行业','三级行业']]
df = df.merge(details, how = 'inner', on = '证券代码')
df = df[df['成交额'] > df['成交额'].quantile(.6) ]
fig = treemap(      df, 
                    path=[px.Constant(d.strftime('%Y-%m-%d')),'一级行业','二级行业','三级行业','证券名称'], 
                    values='成交额', 
                    color='涨跌幅', 
                    range_color = 8, 
                    custom_data= ['涨跌幅','收盘','成交额'],
                    hovertemplate = "%{label}<br>%{customdata[1]:.2f} %{customdata[0]:.2f}%<br>" + '成交额' + "=%{customdata[2]:d}亿" 
                )
st.plotly_chart(fig, use_container_width=True)