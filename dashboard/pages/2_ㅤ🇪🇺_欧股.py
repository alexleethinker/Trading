import streamlit as st
st.set_page_config(layout= 'wide')
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

BACKGROUND_COLOR = 'black'
COLOR = 'black'

def set_page_container_style(
        max_width: int = 1100, max_width_100_percent: bool = True,
        padding_top: int = 0, padding_right: int = 1, padding_left: int = 1, padding_bottom: int = 1,
        color: str = COLOR, background_color: str = BACKGROUND_COLOR,
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        st.markdown(
            f'''
            <style>
                #MainMenu {{visibility: hidden;}}
                body {{border-color: white; border-style: solid;}}
                footer {{visibility: hidden;}}
                .reportview-container .sidebar-content {{
                    padding-top: {padding_top}rem;
                }}
                .reportview-container .main .block-container {{
                    {max_width_str}
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
                .reportview-container .main {{
                    color: {color};
                    background-color: {background_color};

                }}
            </style>
            ''',
            unsafe_allow_html=True,
        )

set_page_container_style()



def load_df(exchange,percentile):
    global data_path
    data_path = './data/spot/stock_spot_{exchange}.csv'.format(exchange = exchange.replace('™️','').lower())
    translated_industry = './data/static/translation.xlsx'
    df = pd.read_csv(data_path,encoding = 'utf-8')
    trans_df = pd.read_excel(open(translated_industry, 'rb'),sheet_name='industry_trans')

    if exchange == '™️EuroNext':
        market_df = pd.read_excel(open(translated_industry, 'rb'),sheet_name='market_trans')
        df = df.merge(trans_df, on = 'industry').merge(market_df, on = 'market')
        df.loc[~df['证券名称'].isnull(), 'stock_name'] = df[~df['证券名称'].isnull()]['证券名称']
        df.loc[~df['dr_name'].isnull() & df['证券名称'].isnull(), 'stock_name'] = df[~df['dr_name'].isnull() & df['证券名称'].isnull()]['dr_name'] + ' SE'
        df['stock_name'] = df['stock_name'].str.replace('�','').str.replace(' SpA','').str.replace(' NV','')
        df = df[~df['change'].isnull()]
        df['Traded_USD'] = df['Traded_USD']* 10000
        df = df[df['Traded_USD'] > df['Traded_USD'].quantile(percentile) ]

    elif exchange == '™️XETRA':
        xetr_master = './data/static/xetr_masterdata.csv'
        master_df = pd.read_csv(xetr_master,encoding = 'utf-8')
        df = df.merge(trans_df, on = 'industry').merge(master_df , on = 'isin')
        df.loc[~df['证券名称'].isnull(), 'name'] = df[~df['证券名称'].isnull()]['证券名称']
        df['turnover'] = pd.to_numeric(df['turnover'], errors="coerce")/10000
        df['marketCapitalisation'] = pd.to_numeric(df['marketCapitalisation'], errors="coerce")/100000000
        df = df[df['turnover'] > df['turnover'].quantile(percentile) ]

    timezone = 'Europe/Amsterdam'
    text = 'Last updated: ' + datetime.fromtimestamp(os.path.getmtime(data_path)).astimezone(tz=pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S') +  ' ({timezone})'.format(timezone=timezone)
    st.markdown(text)    
    return df

def plot_plate(exchange):
    

    df = load_df(exchange, .5).fillna('')
    if exchange == '™️EuroNext':
        path=[px.Constant("EuroNext-USD"),'大行业','一级行业','二级行业','stock_name']  # 指定层次结构，每一个层次都应该是category型的变量
        values='Traded_USD' # 需要聚合的列名
        color='change'
        custom_data=['change','symbol','market_cap_USD','last_price','country','Traded_USD','exchange','icb_industry','exchange_degiro','category']
        hovertemplate= "%{customdata[8]}-%{customdata[9]} | %{customdata[1]}<br>%{customdata[4]}<br>%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:.1f}亿<br>成交额=%{customdata[5]:d}万<br>%{customdata[7]}"                  

    elif exchange == '™️XETRA':                   
        path=[px.Constant("XETRA-EUR"),'大行业','一级行业','二级行业','name']  # 指定层次结构，每一个层次都应该是category型的变量
        values='turnover'
        color='changeToPrevDay'
        custom_data=['changeToPrevDay','symbol','marketCapitalisation','overview.lastPrice','xetr_industry','exchange_degiro','category','originCountry','turnover']
        hovertemplate= "%{customdata[5]}-%{customdata[6]} | %{customdata[1]}<br>%{customdata[7]}<br>%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:.1f}亿<br>成交额=%{customdata[8]:d}万<br>%{customdata[4]}"                  

    fig = px.treemap(df, 
                    path = path,  # 指定层次结构，每一个层次都应该是category型的变量
                    values = values, # 需要聚合的列名
                    color = color, 
                    custom_data = custom_data,
                    range_color = [-8, 8], # 色彩范围最大最小值
                    color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                    #  height = 800,
                    #  width = 1600,
                    color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                    )
    fig.update_layout(
                    {
                        'margin': dict(autoexpand=True,l=0,r=0,t=0,b=0),
    })
    fig.update_coloraxes(showscale=False)
    fig.update_traces(marker_line_width = 0.5,marker_line_color="white")
    fig.update_traces(textposition='middle center', 
                    textinfo='label', 
                    textfont = dict(color='white'),
                    texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>",
                    hovertemplate= hovertemplate                 
                    ) 
    return fig



import os 
from datetime import datetime
import pytz

st.radio(
    "",
    key="exchange",
    options=['™️EuroNext','™️XETRA',],
    horizontal=True,
    label_visibility='collapsed'
)





# Plot!
st.plotly_chart(plot_plate(st.session_state.exchange), use_container_width=True)



# tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["欧洲", "亚太",'拉丁美洲','东盟','中东/非/东欧','南亚'])
# with tab1:
#     st.plotly_chart(plot_plate('欧洲'), use_container_width=True, theme = 'streamlit')
# with tab2:
#     st.plotly_chart(plot_plate('亚太'), use_container_width=True, theme = 'streamlit')
# with tab3:
#     st.plotly_chart(plot_plate('拉丁美洲'), use_container_width=True, theme = 'streamlit')
# with tab4:
#     st.plotly_chart(plot_plate('东盟'), use_container_width=True, theme = 'streamlit')
# with tab5:
#     st.plotly_chart(plot_plate('中东/非/东欧'), use_container_width=True, theme = 'streamlit')
# with tab6:
#     st.plotly_chart(plot_plate('南亚'), use_container_width=True, theme = 'streamlit')

# update every 5 mins
# st_autorefresh(interval=1 * 60 * 1000, key="stock_refresh")