import streamlit as st
from utils.config import page_config
from utils.calendars import get_trading_calendars
from streamlit_autorefresh import st_autorefresh
page_config()


with st.sidebar:

    language = st.selectbox(
        'Language',
        ('中文','English'))

if language == '中文':
    st.markdown("<h4 style='text-align: center;'>主要股票交易所开盘时钟(UTC)</h4>", unsafe_allow_html=True)
else:
    st.markdown("<h4 style='text-align: center;'>World Exchange Clocks(UTC)</h4>", unsafe_allow_html=True)
      
"---"    
fig_calendar = get_trading_calendars(language)
st.plotly_chart(fig_calendar, use_container_width=True)

st_autorefresh(interval=1 * 60 * 1000, key="stock_refresh")