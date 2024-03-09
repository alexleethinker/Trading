import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir, get_args
from utils.figure import treemap
page_config()

from utils.tables import show_dataframe


args = get_args()
language = args.language

source_text = '数据来源：' if language == '中文' else 'Data Source: '

def load_df(exchange):
    data_path = '{data_dir}/spot/stock_spot_{exchange}.csv'.format(data_dir=data_dir, exchange = exchange.replace('™️','').lower())
    df = pd.read_csv(data_path,encoding = 'utf-8')

    df = df[~df['涨跌幅'].isnull()]
    # df['成交额'] = df['成交额']* 100
    
    df = df[df['总市值'] > 2]
    
    df = df[df['成交额'] > df['成交额'].quantile(.5)]
    if exchange == '™️EuroNext':
        timezone = 'Europe/Amsterdam'

    elif exchange == '™️XETRA':
        timezone = 'Europe/Berlin'

    update_at(data_path, timezone, language=language)   
    return df

def plot_plate(exchange):
    df = load_df(exchange).fillna('')
    df = df.dropna(subset = ['成交额'])
    
    if language == '中文':
        path_list = ['一级行业','二级行业','三级行业','证券名称']
    else:
        path_list = ['sector','industry','en_name']
    
    # values = 
    if exchange == '™️EuroNext':
        fig = treemap(df,
                      path=[px.Constant("EuroNext-USD")] + path_list,
                      values='成交额' if traded_value_on else '总市值' ,
                      color='涨跌幅',
                      range_color= 8,
                      custom_data=['涨跌幅','证券代码','总市值','最新价','country','成交额','exchange','icb_industry','exchange_degiro','category'],
                      hovertemplate= "%{customdata[8]}-%{customdata[9]} | %{customdata[1]}<br>%{customdata[4]}<br>%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:.2f}亿<br>成交额=%{customdata[5]:.3f}亿<br>%{customdata[7]}"                  
                      )
    elif exchange == '™️XETRA':                   
        fig = treemap(df,
                      path=[px.Constant("XETRA-EUR")] + path_list,
                      values='成交额' if traded_value_on else '总市值',
                      color='涨跌幅',
                      range_color= 8,
                      custom_data=['涨跌幅','证券代码','总市值','最新价','xetr_industry','exchange_degiro','category','originCountry','成交额'],
                      hovertemplate= "%{customdata[5]}-%{customdata[6]} | %{customdata[1]}<br>%{customdata[7]}<br>%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:.2f}亿<br>成交额=%{customdata[8]:.3f}亿<br>%{customdata[4]}"                  
                      )  
        
    st.plotly_chart(fig, use_container_width=True)
    
    show_dataframe(df, '🇪🇺 欧股', language=language, source='euro') 



def plot_fig_euro():   
    tab1, tab2 = st.tabs(["™️EuroNext", "™️XETRA"])
    with tab1:
        plot_plate("™️EuroNext")
        st.markdown(f'{source_text}™️EuroNext')
    with tab2:
        plot_plate("™️XETRA")
        st.markdown(f'{source_text}™️XETRA（15 mins Delay）')


def plot_fig(market):
    
    source = None
    ind_list = ['一级行业','二级行业','三级行业']
    symbol_list = ['证券名称']
    
    if market == '🇨🇳 A股':
        title = 'A股-RMB'
        timezone = 'Asia/Shanghai'
        file = 'china_a'
    elif market == '🇭🇰 港股':
        title = '港股-HKD'
        timezone = 'Asia/Hong_Kong'
        file = 'hk'
    elif market == '🇺🇸 美股':
        title = '美股-USD'
        timezone = 'America/New_York'
        file = 'us'
    elif market == '🇬🇧 英股':
        title = '英股-GBP'
        timezone = 'Europe/London'
        file = 'uk'
        source = 'euro'
        if language != '中文':
            ind_list = ['sector','industry']
            symbol_list = ['en_name']
        
            
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
    
    df = df[df['总市值'] > 2]
    
    df = df[df['成交额'] > df['成交额'].quantile(.5) ]
    
    
    def plot_fig(plate= True):
        update_at(data_path, timezone, language=language)
        if plate:
            fig = treemap(df, 
                            path=[px.Constant(title)] + ind_list,
                            values=values, 
                            color='涨跌幅', 
                            range_color = 4, 
                            custom_data=['涨跌幅',values],
                            hovertemplate= "%{label}<br>涨跌幅=%{customdata[0]:.2f}%<br>"+ values +"=%{customdata[1]:d}亿"
                            )
        else:
            fig = treemap(df, 
                            path=[px.Constant(title)] + ind_list + symbol_list, 
                            values=values, 
                            color='涨跌幅', 
                            range_color = 8, 
                            custom_data=custom_data,
                            hovertemplate= hovertemplate
                            )
        return fig
    
    if language == '中文':
        tab1, tab2 = st.tabs(["板块概览", "个股详情"])
    else:
        tab1, tab2 = st.tabs(["Overview", "Details"])
        
    with tab1:
        fig_plate = plot_fig(plate = True)
        st.plotly_chart(fig_plate, use_container_width=True)
    with tab2:
        fig = plot_fig(plate= False)
        st.plotly_chart(fig, use_container_width=True)
    
    show_dataframe(df, market, language=language, source = source)
    st.markdown(f'{source_text}EastMoney')
    

def main(market):
    if market == '🇪🇺 欧股':
        plot_fig_euro()
    else:
        plot_fig(market)

col = st.columns([8, 1])

with col[0]:
    
    options = ['🇨🇳 A股','🇭🇰 港股','🇺🇸 美股','🇬🇧 英股','🇪🇺 欧股'] if language == '中文' else ['🇪🇺 Europe','🇬🇧 UK','🇺🇸 US','🇨🇳 China','🇭🇰 HongKong'] 
    st.radio(
        "",
        key="market",
        options=options,
        horizontal=True,
        label_visibility='collapsed'
    )
with col[1]:
    if language == '中文':
        traded_value_on = st.toggle('成交额')
    else: 
        traded_value_on = st.toggle('Turnover')
# Plot!

def translte_options(market):
    market = market.replace('🇨🇳 China', '🇨🇳 A股')\
                   .replace('🇭🇰 HongKong','🇭🇰 港股')\
                    .replace('🇺🇸 US', '🇺🇸 美股')\
                    .replace('🇬🇧 UK','🇬🇧 英股')\
                    .replace('🇪🇺 Europe','🇪🇺 欧股')
    return market

main(translte_options(st.session_state.market))



from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=1 * 60 * 1000, key="market_refresh")