import streamlit as st
import json
import pandas as pd
import plotly.express as px
from utils.config import page_config, update_at, data_dir, get_args
from streamlit_autorefresh import st_autorefresh

page_config()

def get_index(secid, order):

    json_path = f'{data_dir}/intraday/indices/{secid}.json'
    with open(json_path, 'r', encoding='utf-8') as data:
        data_json = json.loads(data.read())
    preClose = data_json['preClose']
    index_name = data_json['name']
    
    if data_json['trends'] != []:
        series = pd.DataFrame(data_json)['trends'].str.split(',', expand=True)
        df = series[[0,2]]
        df.columns =['time', 'ticker']
        df['ticker'] = pd.to_numeric(df["ticker"], errors="coerce")
        df['chg'] = (df['ticker'] / preClose - 1) * 100
        last_ticker = df.ticker.tail(1).values[0].round(2)
        last_chg = "{:.2%}".format(df.chg.tail(1).values[0].round(2)/100)
        df = df.reindex(list(range(0, order + 1))).reset_index(drop=True) 
    else:
        df = df.reindex(list(range(0, order + 1))).reset_index(drop=True) 
        last_ticker = preClose
        last_chg = "{:.2%}".format(0)
        
    
    return df, index_name,last_ticker, last_chg



def index_chart(df):
    y_range = int(max(abs(df.chg.min()),abs(df.chg.max()))) + 1
    line_color = 'red' if (df.dropna().chg.tail(1).values[0] > 0) else 'green'
    
    # df = df.fillna(0)
    fig = px.line(df, x=df.index, y='chg', height=90, width=200)

    # hide and lock down axes
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)

    # remove facet/subplot labels
    fig.update_layout(annotations=[], overwrite=True)

    # strip down the rest of the plot
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10,l=10,b=10,r=10),
        yaxis_range = [-y_range , y_range]
    )
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color=line_color)
    
    
    fill = 'none' if len(df) > 1000 else 'tozeroy'
    fig.update_traces(line_color=line_color, 
                      line_width=2,
                      fill = fill,
                      hovertemplate=None,
                      hoverinfo='skip')
    return fig

    # fig.show(config=dict(displayModeBar=False))
    
    
def plot_row(secid, order):
    df, index_name, last_ticker, last_chg = get_index(secid=secid, order=order)
    if df.columns.tolist() != []:
        fig = index_chart(df)
        col = st.columns([1,1])
        with col[0]:
            st.metric(label=index_name, value=last_ticker, delta=last_chg, delta_color="inverse")
        with col[1]:
            st.plotly_chart(fig, use_container_width=False)
    else:
        pass





data_path = f'{data_dir}/static/EM/Indices/indices.csv'
indices = pd.read_csv(data_path,encoding = 'utf-8')




col = st.columns([3,1,4])

with col[0]:
    indices_df = indices[indices['region'].isin(['外汇'])]
    for i, row in indices_df.iterrows():
        # st.write(type(indices_df.iloc[i]))
        plot_row(row['indices'], row['order'])

with col[2]:


    tabs= st.tabs(["中国", "美国",'亚太','欧洲'])

    # 100.UDI, 100.BDI, 100.CRB  133.USDCNH
    with tabs[0]:
        indices_df = indices[indices['region'].isin(['中国','香港'])]
        for i, row in indices_df.iterrows():
            # st.write(type(indices_df.iloc[i]))
            plot_row(row['indices'], row['order'])

    with tabs[1]:
        indices_df = indices[indices['region'].isin(['美国'])]
        for i, row in indices_df.iterrows():
            # st.write(type(indices_df.iloc[i]))
            plot_row(row['indices'], row['order'])
            
    with tabs[2]:
        indices_df = indices[indices['region'].isin(['亚太','印度'])]
        for i, row in indices_df.iterrows():
            # st.write(type(indices_df.iloc[i]))
            plot_row(row['indices'], row['order'])
    with tabs[3]:
        indices_df = indices[indices['region'].isin(['欧洲'])]
        for i, row in indices_df.iterrows():
            # st.write(type(indices_df.iloc[i]))
            plot_row(row['indices'], row['order'])
        




st_autorefresh(interval=1 * 60 * 1000, key="indices_refresh")