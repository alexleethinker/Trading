import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
from utils.calendars import get_trading_calendars
page_config()


def get_treemap(data_path):
    df = pd.read_csv(data_path,encoding = 'utf-8')

    fig = treemap(  df, 
                    path=[px.Constant("成交额(USD)"),'plate','市场'],
                    values='Traded_USD', 
                    color='change', 
                    range_color = 4, 
                    custom_data=['change','name','Traded_USD','close','market','close'],
                    hovertemplate= "%{label}<br>%{customdata[0]:.2f}%<br>成交额=%{customdata[2]:.1f}亿"
                    )                
    return fig




data_path = '{data_dir}/spot/stock_spot_global_all.csv'.format(data_dir=data_dir)
timezone = 'UTC'

fig_calendar = get_trading_calendars()
fig_treemap = get_treemap(data_path)
st.plotly_chart(fig_calendar, use_container_width=True)
update_at(data_path, timezone)
st.plotly_chart(fig_treemap, use_container_width=True)