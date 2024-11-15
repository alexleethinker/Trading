import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
page_config(layout='centered')
# st.set_page_config(layout='centered')
import plotly.express as px

st.html(f"<h3 style='text-align: center;'><font color='lightblue'>千问读研报</font></h3>") 
hint = '该页面内容由千问AI自动生成，请酌情参考。数据使用本周券商行业研报，每周日更新'
st.html(f'<p font-size: 10px">{hint}</p>')

timezone = 'Asia/Shanghai'
try:
    data_path = f'{data_dir}/spot/Qwen_weekly_reports.csv'
    reports = pd.read_csv(data_path)
except:
    data_path = f'{data_dir}/static/EM/Qwen_reports.csv'
    reports = pd.read_csv(data_path)

update_at(data_path, timezone)
reports.columns = ['行业','研报名称','千问读研报']

# reports['研报名称'] = reports['研报名称'].apply(lambda x: ','.join(x))
reports = reports[reports['研报名称']!='[]'].dropna(subset=['研报名称'])
reports['千问读研报'] = reports['千问读研报'].fillna('').str.replace('###','####')#.str.replace('#','')


for index, report in reports.iterrows():
    st.html(f"<br><h3><font color='lightblue'>{report['行业']}</font></h3>") 
    report_name = report['研报名称'].replace(',','<br>').replace('[','').replace(']','').replace("'",'')
    st.html(f"<font color='lightblue'>{report_name}</font>") 
    # for i in report['千问读研报'].split('<br>'):
    #     st.markdown(i)
    st.markdown(report['千问读研报'])