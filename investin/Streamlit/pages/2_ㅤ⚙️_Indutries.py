import streamlit as st
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir
from utils.figure import treemap
page_config()

timezone = 'UTC'
data_path = '{data_dir}/spot/stock_spot_global_primary.csv'.format(data_dir=data_dir)
df = pd.read_csv(data_path,encoding = 'utf-8')
df['market'] = df['market'].str.capitalize()
def translte_region(region):
    region = region.replace( '中国','China')\
                    .replace('北美','North America')\
                    .replace('欧洲','Europe',)\
                    .replace('亚太','APAC',)\
                    .replace('南亚','South Asia')\
                    .replace('东盟','ASEAN')\
                    .replace('中东非','MENA')\
                    .replace('拉美','Latin America')
    return region  
df['region'] = df['地区'].apply(translte_region)

with st.sidebar:
    language = st.selectbox(
        'Language',
        ('中文','English'))


def plot_plate(industry):
    
    if language == '中文':
        if industry in ['消费','金融']:
            path=[px.Constant(industry),'地区','市场']
            dfi = df[df['一级行业'].isin([industry]) & (~df['二级行业'].isin(['商业服务','经销商']))]

        elif industry in ['汽车','制药']:
            path=[px.Constant(industry),'三级行业','地区','市场','证券名称']
            dfi = df[df['二级行业'].isin([industry])]

        else:
            path=[px.Constant(industry),'地区','市场','证券名称']
            if industry in ['石油']:
                dfi = df[df['二级行业'].isin(['能源'])]
                dfi = dfi[~dfi['三级行业'].isin(['煤炭'])]  
            else:        
                dfi = df[df['三级行业'].isin([industry])]
    else:
        if industry in ['消费','金融']:
            path=[px.Constant('Industry'),'region','market']
            dfi = df[df['一级行业'].isin([industry]) & (~df['二级行业'].isin(['商业服务','经销商']))]

        elif industry in ['汽车','制药']:
            path=[px.Constant('Industry'),'industry','region','market','ticker_title']
            dfi = df[df['二级行业'].isin([industry])]

        else:
            path=[px.Constant('Industry'),'region','market','ticker_title']
            if industry in ['石油']:
                dfi = df[df['二级行业'].isin(['能源'])]
                dfi = dfi[~dfi['三级行业'].isin(['煤炭'])]  
            else:        
                dfi = df[df['三级行业'].isin([industry])]
        dfi =dfi[~dfi['ticker_title'].isnull()]


    dfi = dfi[dfi['总市值'] > dfi['总市值'].quantile(.75) ]
    update_at(data_path, timezone, language=language)
    fig = treemap(dfi, 
                    path=path,  
                    values='总市值',
                    color='涨跌幅', 
                    range_color = 8,
                    custom_data=['涨跌幅','证券代码','总市值','最新价','市场','成交额'],
                    hovertemplate= "%{label}<br>%{customdata[3]} (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:d}亿<br>成交额=%{customdata[5]:.2f}亿"                  
                    )               
    return fig



if language == '中文':
    options=['金融','消费','半导体','汽车','计算机设备','电力设备','机械加工设备','制药','石油','煤炭','钢']
else:
    options=['Finance','Consumers','Semiconductors','Motor Vehicles','Computer','Electrical Equipment','Mechanical','Pharmaceutical','Oil and Gas','Coal','Steel']

st.radio(
    "",
    key="industry",
    options=options,
    horizontal=True
)

def translate_industry(industry):
    l1 = ['金融','消费','半导体','汽车','计算机设备','电力设备','机械加工设备','制药','石油','煤炭','钢']
    l2 = ['Finance','Consumers','Semiconductors','Motor Vehicles','Computer','Electrical Equipment','Mechanical','Pharmaceutical','Oil and Gas','Coal','Steel']
    for i in range(len(l1)):
        industry = industry.replace(l2[i],l1[i])
    return industry

# Plot!
fig = plot_plate(translate_industry(st.session_state.industry))
st.plotly_chart(fig, use_container_width=True)

if language == '中文':
    st.markdown('数据来源：TradingView（大部分市场延迟15分钟）')
else:
    st.markdown('Data Source：TradingView（15mins delay for most markets）')
