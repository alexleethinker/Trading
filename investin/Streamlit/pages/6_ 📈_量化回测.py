from utils.config import page_config
page_config()
import streamlit as st
from datetime import datetime, date
import plotly.express as px


# st.sidebar.title("Configuration")


with st.sidebar:

    market = st.selectbox(
        '选择回测市场',
        ('A股', '美股', '港股', '英股','欧股'))
    
    date_range = st.date_input(
        "回测时间范围",
        (date(datetime.today().year - 40, 1, 1), datetime.today()),
        format="YYYY/MM/DD",
        )
    
    benchmark = st.selectbox(
        '选择基准',
        ('上证指数', '沪深300'))
    
    initial_capital = st.number_input("初始资金", value = 100000)
    commission_fee = st.number_input('佣金比例', value = 0.0001, format= '%.4f' )
    
st.write('市场:', market)
st.write(date_range)





from Backtest.DataSource import HDFDataSource
from Backtest.Strategy import buy_low_sell_high_rsi
from pybroker import Strategy


strategy = Strategy(HDFDataSource(), '6/1/2021', '12/1/2021')
strategy.add_execution(buy_low_sell_high_rsi, ['600089.SH', '000520.SZ', '688521.SH'])
result = strategy.backtest()


st.write(result.orders)
st.write(result.metrics_df)
# st.write(result.portfolio)

fig = px.line(result.portfolio, x=result.portfolio.index, y="market_value", title='市值曲线')
st.plotly_chart(fig, use_container_width=True)

st.write('回测进度条')