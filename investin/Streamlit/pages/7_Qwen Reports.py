import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir, get_args
page_config()

import plotly.express as px


reports = pd.read_csv(f'{data_dir}/static/EM/Qwen_reports.csv')

reports.columns = ['行业','研报名称','千问读研报']
reports = reports.dropna(subset=['研报名称'])
reports['千问读研报'] = reports['千问读研报'].fillna('').str.replace('###','<br>').str.replace('#','')

for index, report in reports.iterrows():
    st.html(f"<br><h3><font color='lightblue'>{report['行业']}</font></h3>") 
    st.html(f"<font color='lightblue'>{report['研报名称'].replace(',','<br>')}</font>") 
    for i in report['千问读研报'].split('<br>'):
        st.markdown(i)
        # st.html(report['千问读研报']) 
# st.dataframe(reports,hide_index=True)   
# st.table(reports)  