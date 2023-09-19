import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
page_config()


def load_df(exchange,percentile):
    global data_path
    data_path = '{data_dir}/spot/stock_spot_{exchange}.csv'.format(data_dir=data_dir, exchange = exchange.replace('™️','').lower())
    df = pd.read_csv(data_path,encoding = 'utf-8')

    if exchange == '™️EuroNext':
        df = df[~df['change'].isnull()]
        df['Traded_USD'] = df['Traded_USD']* 10000
        df = df[df['Traded_USD'] > df['Traded_USD'].quantile(percentile) ]

    elif exchange == '™️XETRA':
        df['turnover'] = pd.to_numeric(df['turnover'], errors="coerce")/10000
        df['marketCapitalisation'] = pd.to_numeric(df['marketCapitalisation'], errors="coerce")/100000000
        df = df[df['turnover'] > df['turnover'].quantile(percentile) ]

    timezone = 'Europe/Amsterdam'
    update_at(data_path, timezone)   
    return df

def plot_plate(exchange):
    df = load_df(exchange, .5).fillna('')
    if exchange == '™️EuroNext':
        fig = treemap(df,
                      path=[px.Constant("EuroNext-USD"),'一级行业','二级行业','三级行业','证券名称'],
                      values='Traded_USD',
                      color='change',
                      range_color= 8,
                      custom_data=['change','symbol','market_cap_USD','last_price','country','Traded_USD','exchange','icb_industry','exchange_degiro','category'],
                      hovertemplate= "%{customdata[8]}-%{customdata[9]} | %{customdata[1]}<br>%{customdata[4]}<br>%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:.1f}亿<br>成交额=%{customdata[5]:d}万<br>%{customdata[7]}"                  
                      )
    elif exchange == '™️XETRA':                   
        fig = treemap(df,
                      path=[px.Constant("XETRA-EUR"),'一级行业','二级行业','三级行业','证券名称'],
                      values='turnover',
                      color='changeToPrevDay',
                      range_color= 8,
                      custom_data=['changeToPrevDay','symbol','marketCapitalisation','overview.lastPrice','xetr_industry','exchange_degiro','category','originCountry','turnover'],
                      hovertemplate= "%{customdata[5]}-%{customdata[6]} | %{customdata[1]}<br>%{customdata[7]}<br>%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:.1f}亿<br>成交额=%{customdata[8]:d}万<br>%{customdata[4]}"                  
                      )                    
    return fig



st.radio(
    "",
    key="exchange",
    options=['™️EuroNext','™️XETRA',],
    horizontal=True,
    label_visibility='collapsed'
)

# Plot!
fig = plot_plate(st.session_state.exchange)
st.plotly_chart(fig, use_container_width=True)



# update every 5 mins
# st_autorefresh(interval=1 * 60 * 1000, key="stock_refresh")