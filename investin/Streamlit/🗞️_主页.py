import streamlit as st
from utils.config import page_config
from utils.calendars import get_trading_calendars
from streamlit_autorefresh import st_autorefresh
page_config()



fig_calendar = get_trading_calendars()
st.plotly_chart(fig_calendar, use_container_width=True)

st_autorefresh(interval=1 * 60 * 1000, key="stock_refresh")