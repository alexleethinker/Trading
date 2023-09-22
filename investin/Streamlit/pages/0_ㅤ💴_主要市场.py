import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
page_config()


def load_df(exchange):
    data_path = '{data_dir}/spot/stock_spot_{exchange}.csv'.format(data_dir=data_dir, exchange = exchange.replace('™️','').lower())
    df = pd.read_csv(data_path,encoding = 'utf-8')

    if exchange == '™️EuroNext':
        df = df[~df['change'].isnull()]
        df['Traded_USD'] = df['Traded_USD']* 10000
        df = df[df['Traded_USD'] > df['Traded_USD'].quantile(.5)]

    elif exchange == '™️XETRA':
        df['turnover'] = pd.to_numeric(df['turnover'], errors="coerce")/10000
        df['marketCapitalisation'] = pd.to_numeric(df['marketCapitalisation'], errors="coerce")/100000000
        df = df[df['turnover'] > df['turnover'].quantile(.5) ]

    timezone = 'Europe/Amsterdam'
    update_at(data_path, timezone)   
    return df

def plot_plate(exchange):
    df = load_df(exchange).fillna('')
    if exchange == '™️EuroNext':
        fig = treemap(df,
                      path=[px.Constant("EuroNext-USD"),'一级行业','二级行业','三级行业','证券名称'],
                      values='Traded_USD' if traded_value_on else 'market_cap_USD',
                      color='change',
                      range_color= 8,
                      custom_data=['change','symbol','market_cap_USD','last_price','country','Traded_USD','exchange','icb_industry','exchange_degiro','category'],
                      hovertemplate= "%{customdata[8]}-%{customdata[9]} | %{customdata[1]}<br>%{customdata[4]}<br>%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:.1f}亿<br>成交额=%{customdata[5]:d}万<br>%{customdata[7]}"                  
                      )
    elif exchange == '™️XETRA':                   
        fig = treemap(df,
                      path=[px.Constant("XETRA-EUR"),'一级行业','二级行业','三级行业','证券名称'],
                      values='turnover' if traded_value_on else 'marketCapitalisation',
                      color='changeToPrevDay',
                      range_color= 8,
                      custom_data=['changeToPrevDay','symbol','marketCapitalisation','overview.lastPrice','xetr_industry','exchange_degiro','category','originCountry','turnover'],
                      hovertemplate= "%{customdata[5]}-%{customdata[6]} | %{customdata[1]}<br>%{customdata[7]}<br>%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:.1f}亿<br>成交额=%{customdata[8]:d}万<br>%{customdata[4]}"                  
                      )                    
    return fig


def plot_fig_euro():   
    tab1, tab2 = st.tabs(["™️EuroNext", "™️XETRA"])
    with tab1:
        fig_euronext = plot_plate("™️EuroNext")
        st.plotly_chart(fig_euronext, use_container_width=True)
        st.markdown('数据来源：™️EuroNext')
    with tab2:
        fig_extra = plot_plate("™️XETRA")
        st.plotly_chart(fig_extra, use_container_width=True)
        st.markdown('数据来源：™️XETRA（延迟15分钟）')



def plot_fig(market):
    if market == '🇨🇳 A股':
        title = 'A股-RMB'
        timezone = 'Asia/Shanghai'
        file = 'china_a'
    elif market == '🇭🇰 港股':
        title = '港股-HKD'
        timezone = 'Asia/Shanghai'
        file = 'hk'
    elif market == '🇺🇸 美股':
        title = '美股-USD'
        timezone = 'America/New_York'
        file = 'us'
    elif market == '🇬🇧 英股':
        title = '英股-GBP'
        timezone = 'Europe/London'
        file = 'uk'
        
            
    if market == '🇨🇳 A股':
        values = '成交额' if traded_value_on else '流通市值' 
        custom_data=['涨跌幅','流通市值','所属同花顺行业','投资逻辑','最新价','证券代码','主营产品','成交额']
        hovertemplate= "%{customdata[5]}<br>%{label}<br>%{customdata[4]:.2f}  (%{customdata[0]:.2f}%)<br>流通市值=%{customdata[1]:d}亿<br>成交额=%{customdata[7]:.2f}亿<br>%{customdata[2]}<br>主营产品：%{customdata[6]}<br>%{customdata[3]}<br>"
    else:
        values = '成交额' if traded_value_on else '总市值'
        custom_data=['涨跌幅','证券代码','总市值','最新价','成交额']
        hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.2f}  (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:d}亿<br>成交额=%{customdata[4]:.2f}亿"
    
    data_path = '{data_dir}/spot/stock_spot_{file}.csv'.format(data_dir=data_dir,file=file)
    df = pd.read_csv(data_path,encoding = 'utf-8')
    df['证券代码'] = df['证券代码'].astype(str)
    df = df[df['证券代码'].str[:1] != '8']
    df = df[~df['证券名称'].str.contains(' Pfd')]
    df = df[df['成交额'] > df['成交额'].quantile(.75) ]
    
    def plot_fig(plate= True):
        update_at(data_path, timezone)
        if plate:
            fig = treemap(df, 
                            path=[px.Constant(title),'一级行业','二级行业','三级行业'],
                            values=values, 
                            color='涨跌幅', 
                            range_color = 4, 
                            custom_data=['涨跌幅',values],
                            hovertemplate= "%{label}<br>涨跌幅=%{customdata[0]:.2f}%<br>"+ values +"=%{customdata[1]:d}亿"
                            )
        else:
            fig = treemap(df, 
                            path=[px.Constant(title),'一级行业','二级行业','三级行业','证券名称'], 
                            values=values, 
                            color='涨跌幅', 
                            range_color = 8, 
                            custom_data=custom_data,
                            hovertemplate= hovertemplate
                            )
        return fig
    

    tab1, tab2 = st.tabs(["板块概览", "个股详情"])
    
    with tab1:
        fig_plate = plot_fig(plate = True)
        st.plotly_chart(fig_plate, use_container_width=True)
    with tab2:
        fig = plot_fig(plate= False)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('数据来源：东方财富网')

    

def main(market):
    if market == '🇪🇺 欧股':
        plot_fig_euro()
    else:
        plot_fig(market)

col1, col2 = st.columns([9, 1])

with col1:
    st.radio(
        "",
        key="market",
        options=['🇨🇳 A股','🇭🇰 港股','🇺🇸 美股','🇬🇧 英股','🇪🇺 欧股'],
        horizontal=True,
        label_visibility='collapsed'
    )
with col2:
    traded_value_on = st.toggle('成交额')
# Plot!
main(st.session_state.market)

