import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir, get_args
from utils.figure import treemap
page_config()
from utils.tables import show_dataframe

args = get_args()
language = args.language

timezone = 'UTC'
data_path = '{data_dir}/spot/stock_spot_global_primary.csv'.format(data_dir=data_dir)
df = pd.read_csv(data_path,encoding = 'utf-8')
df['market'] = df['market'].str.capitalize()

def translte_region(region):
    region = region.replace( '中国','China')\
                    .replace('北美','North America')\
                    .replace('欧洲','Europe',)\
                    .replace('亚太','APAC',)\
                    .replace('南亚','South Asia')\
                    .replace('东盟','ASEAN')\
                    .replace('中东非','MENA')\
                    .replace('拉美','Latin America')
    return region  

df['region'] = df['地区'].apply(translte_region)



def plot_plate(plate = '欧洲'):
    values = '成交额' if traded_value_on else '总市值'
    
    if plate in ['概览','全球']:
        if traded_value_on:
            dir = '{data_dir}/spot/stock_spot_global_all.csv'.format(data_dir=data_dir)
            df_copy = pd.read_csv(dir,encoding = 'utf-8')
            dfi = df_copy.fillna('')
        else:
            dfi = df.fillna('')
        dfi = dfi[dfi['成交额'] > dfi['成交额'].quantile(.6) ]
        dfi = dfi[~dfi['证券代码'].isin(['CLIME_BTU_B'])]
        dfi['market'] = dfi['market'].str.capitalize()
        dfi['region'] = dfi['地区'].apply(translte_region)
        if language == '中文':
            details = [] if plate == '概览' else ['一级行业','二级行业','三级行业']
            path=[px.Constant(values + "(USD)"),'地区','市场'] + details
            values_show = values
        else:
            values_show = values.replace('成交额','Turnover').replace('总市值','Market Values')
            details = [] if plate == '概览' else ['sector','industry']
            path=[px.Constant(values_show + " (USD)"),'region','market'] + details
        
        custom_data=['涨跌幅', values]
        range_color = 4
        hovertemplate= "%{label}<br>%{customdata[0]:.2f}%<br>" + values_show + "=%{customdata[1]:d}亿"  
        
        update_at(data_path, timezone, language=language)
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
        
        if language == '中文':
            block = 'exchange' if plate == '欧洲' else '市场'
        else:
            block = 'exchange' if plate == '欧洲' else 'market'
        
        dfi['exchange'] = dfi['exchange'].replace(dict.fromkeys(['MIL','LUXSE'],'EURONEXT'))\
                                         .replace(dict.fromkeys(['BME'],'SIX'))\
                                         .replace(dict.fromkeys(['OMXCOP','OMXHEX','OMXSTO','OMXICE','OSL'],'OMX')) 
        if plate == '欧洲':
            dfi =dfi[dfi['exchange'].isin(['EURONEXT','LSE','XETR','SIX','OMX'])]     
        
        if language == '中文':
            path = [block,'一级行业','二级行业','三级行业','证券名称']
        else:
            path = [block,'sector','industry','ticker_title']
            dfi =dfi[~dfi['ticker_title'].isnull()]
        custom_data=['涨跌幅','full_symbol','总市值','最新价','市场','成交额']
        range_color = 8
        hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.1f} (%{customdata[0]:.2f})%<br>总市值=%{customdata[2]:d}亿<br>成交额=%{customdata[5]:.2f}亿"                  
        update_at(data_path, timezone, language=language)

        market_list = dfi.groupby([block])[['成交额']].sum().sort_values('成交额',ascending=False).reset_index()[block].tolist()
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
    
                show_dataframe(dfj, plate, language=language, source='tradingview')



col = st.columns([8, 1])
with col[0]:
    
    if language =='中文':
        options=['🌎 概览','🌎 全球','🇨🇳 中国','🇺🇸 北美','🇪🇺 欧洲','🇯🇵 亚太','🇮🇳 南亚','🇸🇬 东盟','🇸🇦 中东非','🇧🇷 拉美']
    else:
        options=['🌎 Overview','🌎 Global','🇺🇸 NorthAmerica','🇪🇺 Europe','🇨🇳 China','🇯🇵 APAC','🇮🇳 SouthAsia','🇸🇬 ASEAN','🇸🇦 MENA','🇧🇷 LatinAmerica']
    
    st.radio(
        "",
        key="plate",
        options=options,
        horizontal=True,
        label_visibility='collapsed'
    )
with col[1]:
    if language == '中文':
        traded_value_on = st.toggle('成交额')
    else: 
        traded_value_on = st.toggle('Turnover')
    
  
  
def translte_options(market):
    market = market.replace('Overview', '概览')\
                   .replace('Global','全球')\
                    .replace('China', '中国')\
                    .replace('NorthAmerica','北美')\
                    .replace('Europe','欧洲')\
                    .replace('APAC','亚太')\
                    .replace('SouthAsia','南亚')\
                    .replace('ASEAN','东盟')\
                    .replace('MENA','中东非')\
                    .replace('LatinAmerica','拉美')
    return market  
    
plot_plate(translte_options(st.session_state.plate.split(' ')[1]))

if language == '中文':
    st.markdown('数据来源：TradingView（大部分市场延迟15分钟）')
else:
    st.markdown('Data Source：TradingView（15mins delay for most markets）')
