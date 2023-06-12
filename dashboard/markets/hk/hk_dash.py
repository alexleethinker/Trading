import requests
import json
import pandas as pd
import plotly.express as px
from zhconv import convert

def translate(string):
    return convert(string, 'zh-cn')

def format_code(code):
    code = code.replace('.HK','')
    code = '{:0>5}'.format(code)
    return code




# 需要手动更新token ..............
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
house = 'https://www1.hkex.com.hk/hkexwidget/data/getequityfilter?lang=chi&token=evLtsLsBNAUVTPxtGqVeGzmJ%2fDaiJpzT84ay26sEWy8cl8dTEx3z9Mc7UDp8Cnho&sort=5&order=0&all=1&qid=1686211056954&callback=jQuery35105695767282444215_1686211008050&_=1686211008059'
res = requests.get(house, headers=headers)
hkex_df = pd.DataFrame(json.loads(res.text.replace('jQuery35105695767282444215_1686211008050(','').replace(')',''))['data']['stocklist'])
hkex_df['证券代码'] = hkex_df['ric'].apply(format_code)
hkex_df['涨跌幅'] = pd.to_numeric(hkex_df['pc'], errors="coerce")

r = requests.get('https://static03.hket.com/data-lake/p/industry/industry-data.json')
hk_df = pd.DataFrame(json.loads(r.text))
hk_df['一级行业'] = hk_df['industry'].apply(translate).str.replace('电讯','科技').str.replace('资讯科技','科技')
hk_df['二级行业'] = hk_df['business'].apply(translate)
hk_df['三级行业'] = hk_df['child-business'].apply(translate)
hk_df['证券名称'] = hk_df['name'].apply(translate)
hk_df['证券代码'] = hk_df['stock-id']
hk_df['总市值'] = hk_df['market-cap']

df = hk_df.merge(hkex_df, on = '证券代码', how = 'inner')
df = df[~df['一级行业'].isnull()]
df['总市值'] = (df['总市值']/100000000).round(1).fillna(0) 
df = df[~df['涨跌幅'].isnull()]
df = df[df['总市值'] > 0]

fig = px.treemap(df, 
                 path=['一级行业','二级行业','三级行业','证券名称'],  # 指定层次结构，每一个层次都应该是category型的变量
                 values='总市值', # 需要聚合的列名
                 color='涨跌幅', 
                 custom_data=['涨跌幅','证券代码','总市值','ls'],
                 range_color = [-10, 10], # 色彩范围最大最小值
                 hover_data= {'涨跌幅':':.2',
                             '总市值':':.1f'}, # 鼠标悬浮显示数据的格式
                 color_continuous_scale=["seagreen",'lightgrey', "indianred"],
                 height = 900,
                #  width = 1600,
                 color_continuous_midpoint=0 , # 颜色变化中间值设置为增长率=0
                )
fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
fig.update_coloraxes(showscale=False)
fig.update_traces(textposition='middle center', 
                  textinfo='label', 
                  textfont = dict(color='white'),
                  texttemplate= "%{label}<br>%{customdata[0]:.2f}%<br>",
                  hovertemplate= "%{customdata[1]}<br>%{label}<br>%{customdata[3]:.2f}  (%{customdata[0]:.2f}%)<br>总市值=%{customdata[2]:d}亿") # 显示企业名称和市值，字体24

fig.show()