import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
page_config()
st.set_page_config(layout='centered')
import plotly.express as px

st.markdown('<div style="text-align: center;">千问读研报</div>', unsafe_allow_html=True)
st.markdown('该页面内容由阿里千问AI大模型自动生成，准确度请自行判断，数据来源：选定券商本周各行业研报')


timezone = 'Asia/Shanghai'
# data_path = f'{data_dir}/spot/Qwen_weekly_reports.csv'
data_path = f'{data_dir}/static/EM/Qwen_reports.csv'
update_at(data_path, timezone)

reports = pd.read_csv(data_path)
reports.columns = ['行业','研报名称','千问读研报']
reports = reports.dropna(subset=['研报名称'])
reports['千问读研报'] = reports['千问读研报'].fillna('').str.replace('###','<br>').str.replace('#','')

# st.dataframe(reports[['行业','研报名称']],hide_index=True,use_container_width=True,) 

for index, report in reports.iterrows():
    st.html(f"<br><h3><font color='lightblue'>{report['行业']}</font></h3>") 
    st.html(f"<font color='lightblue'>{report['研报名称'].replace(',','<br>')}</font>") 
    for i in report['千问读研报'].split('<br>'):
        st.markdown(i)
        # st.html(report['千问读研报']) 
# st.dataframe(reports,hide_index=True)   
# st.table(reports)  