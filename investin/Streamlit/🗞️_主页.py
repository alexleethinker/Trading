import streamlit as st
from utils.config import page_config
from utils.calendars import get_trading_calendars
page_config()



fig_calendar = get_trading_calendars()
st.plotly_chart(fig_calendar, use_container_width=True)
