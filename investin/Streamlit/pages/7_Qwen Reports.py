import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir, get_args
page_config()

import plotly.express as px


reports = pd.read_csv(f'{data_dir}/static/Qwen_reports.csv')


st.dataframe(reports,\
            hide_index=True)   