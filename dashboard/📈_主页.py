import streamlit as st
st.set_page_config(layout= 'wide')
import pandas as pd
import plotly.express as px
import os 
from datetime import datetime
import pytz
import exchange_calendars as xcals

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
body {border-color: white; border-style: solid;}
footer {visibility: hidden;}
</style>

# """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


def get_treemap(data_path):
    df = pd.read_csv(data_path,encoding = 'utf-8')
    translation = './data/static/translation.xlsx'
    industry_trans_df = pd.read_excel(open(translation, 'rb'),sheet_name='industry_trans')
    market_trans_df = pd.read_excel(open(translation, 'rb'),sheet_name='market_trans')
    df = df.merge(industry_trans_df, on = 'industry').merge(market_trans_df, on = 'market')
    # df = df[df['Traded_USD'] > df['Traded_USD'].quantile(.8) ]

    fig = px.treemap(df, 
                    path=[px.Constant("成交额(USD)"),'plate','市场'],  # 指定层次结构，每一个层次都应该是category型的变量
                    values='Traded_USD', # 需要聚合的列名
                    color='change', 
                    custom_data=['change','name','Traded_USD','close','market','close'],
                    range_color = [-4, 4], # 色彩范围最大最小值
                    color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                    #  height = 800,
                    #  width = 1600,
                    color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                    )
    fig.update_layout(
        {'margin': dict(autoexpand=True,l=0,r=0,t=0,b=0)}
        )
    fig.update_coloraxes(showscale=False)
    fig.update_traces(marker_line_width = 0.5,
                      marker_line_color="white",
                      textposition='middle center', 
                      textinfo='label', 
                      textfont = dict(color='white'),
                      texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>",
                      hovertemplate= "%{label}<br>%{customdata[0]:.2f}%<br>成交额=%{customdata[2]:.1f}亿"                  
                    ) 
    return fig



def get_trading_calendars():
    exchanges = xcals.get_calendar_names(include_aliases=False)
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    today_calendars = pd.DataFrame()
    for exchange in exchanges:
        cal = xcals.get_calendar(exchange)
        df = cal.schedule.loc[today:today]
        df['exchange'] = exchange
        df['is_open'] = cal.is_trading_minute(now)
        today_calendars = pd.concat([today_calendars, df], ignore_index=True)
    continuous = today_calendars[today_calendars['break_start'].isnull()][['open','close','exchange','is_open']]
    morning = today_calendars[~today_calendars['break_start'].isnull()][['open','break_start','exchange','is_open']].rename(columns={"break_start": "close"})
    afternoon = today_calendars[~today_calendars['break_start'].isnull()][['break_end','close','exchange','is_open']].rename(columns={"break_end": "open"})
    today_calendars = pd.concat([continuous, morning, afternoon], ignore_index=True)

    exchanges_info = pd.read_csv('./data/static/exchanges.csv')
    today_calendars = today_calendars.merge(exchanges_info, how = 'left', left_on = 'exchange', right_on = 'ISO Code')
    today_calendars = today_calendars[today_calendars['Selected'].isin([1])]
    today_calendars = today_calendars.sort_values(['open','close']).reset_index(drop=True)


    color_discrete_map = {True: 'lightskyblue', False: 'gray'}
    fig = px.timeline(today_calendars, x_start="open", x_end="close", y="国家",color="is_open",
                      color_discrete_map=color_discrete_map,
                      hover_name= "国家",
                      custom_data=['open','close'],
                    )
    fig.update_yaxes(autorange="reversed",categoryorder='array', categoryarray=today_calendars['国家']) # otherwise tasks are listed from the bottom up

    fig.update_layout(
        xaxis = dict(side = 'top'),
        yaxis_title=None,
        xaxis_fixedrange = True,
        yaxis_fixedrange = True,
        dragmode=False,
        margin=dict(autoexpand=True,l=0,r=0,t=0,b=0),
        shapes=[
        dict(
        type='line',
        line=dict(color="White",width=2),
        yref='paper', y0=0, y1=1,
        xref='x', x0=now, x1=now,
        )
    ])
    fig.update_traces(hovertemplate= "%{label}",                 
                      marker_line_width = 0.5, 
                      showlegend=False
                      ) 
    return fig



data_path = './data/spot/stock_spot_global_all.csv'
timezone = 'UTC'
text = '更新时间: ' + datetime.fromtimestamp(os.path.getmtime(data_path)).astimezone(tz=pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S') +  ' ({timezone})'.format(timezone=timezone)


fig_calendar = get_trading_calendars()
fig_treemap = get_treemap(data_path)
st.plotly_chart(fig_calendar, use_container_width=True)
st.markdown(text) 
st.plotly_chart(fig_treemap, use_container_width=True)